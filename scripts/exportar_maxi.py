"""Paso 5 — Exporta el catálogo en el modelo de MAXI-POS: Plantilla › Objeto › Variante.

Uso:  python scripts/exportar_maxi.py
Lee:  data/processed/prendas_clasificadas.csv + catalogo/plantillas/*.yaml
Escribe:
  catalogo/maxi_pos.json               plantillas con sus campos, objetos y variantes + historial
  reportes/maxi_pos_plantillas.xlsx    lo mismo en Excel (hojas Plantillas / Objetos / Variantes)

Modelo (ver docs/MODELO_PLANTILLAS.md):
  Plantilla = el formulario: qué campos se capturan, checklist y fotos (Celulares, Motos, Lavadora).
  Objeto    = el artículo concreto que se busca y se cotiza (iPhone 15, Italika FT150, Mabe 16 kg).
  Variante  = la combinación de atributos que cambia el precio (128 GB, año 2021).

- En las categorías "por modelo" (celulares, motos…) la plantilla es la categoría y cada regla del
  YAML es un objeto.
- En artículos generales cada regla del YAML es una plantilla (tipo de artículo) y los objetos se
  proponen con la marca y el modelo que capturó la evaluadora.
- Joyería (oro y plata) no se exporta: se cotiza por peso y kilataje, no con objetos.
"""
import difflib
import glob
import json
import os
import sys

import pandas as pd
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marcas import cargar as cargar_marcas, gama_objeto, resolver  # noqa: E402
from plantillas import campo, metricas  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data", "processed")

POR_MODELO = {"Celulares", "Tablets", "Motos", "Autos y camionetas", "Videojuegos", "Relojes"}
EXCLUIR = {"Joyería de oro", "Joyería de plata"}
MIN_HISTORIAL = 5  # regla del mockup: con 5+ operaciones propias manda el historial
MIN_OBJETO = 5     # empeños para que una marca+modelo sea objeto propio; si no, va al genérico por gama
GAMA_TXT = {"alta": "gama alta", "media": "gama media", "basica": "gama básica"}

CAMPOS_METRICA = ["prendas", "prestamo_p25", "prestamo_mediana", "prestamo_p75", "pct_desempeno",
                  "pct_refrenda", "pct_remate", "drop_cerrados", "vendidas", "venta_p25",
                  "venta_mediana", "venta_p75", "venta_sobre_prestamo", "dias_vitrina_mediana", "salida"]


def leer_yaml():
    defs = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "catalogo", "plantillas", "*.yaml"))):
        cat = yaml.safe_load(open(path, encoding="utf-8"))
        for p in cat.get("plantillas") or []:
            attrs = dict(cat.get("atributos") or {})
            attrs.update(p.get("atributos") or {})
            defs[p["id"]] = dict(cat=cat, p=p, attrs=attrs)
    return defs


def campos(attrs, por_modelo):
    out = [{"campo": "marca", "tipo": "lista", "crea_variante": False}]
    if por_modelo:
        out.append({"campo": "modelo", "tipo": "objeto", "crea_variante": False})
    else:
        out.append({"campo": "modelo", "tipo": "texto", "crea_variante": False})
    for k, a in attrs.items():
        if not a or k.startswith("marca") or k.startswith("modelo"):
            continue
        out.append({"campo": k, "tipo": "lista", "crea_variante": bool(a.get("crea_variante")),
                    "valores": sorted({str(v) for v in (a.get("mapa") or {}).values()}) or None})
    return out


def marca_de(row):
    try:
        attrs = json.loads(row.atributos) if isinstance(row.atributos, str) else {}
    except ValueError:
        attrs = {}
    for k, v in attrs.items():
        if k.startswith("marca") and v:
            return str(v).title()
    m = campo(row.Marca)
    return m.title() if m else ""


def unificar_marcas(serie):
    """Junta faltas de ortografía con la marca más frecuente parecida (SAMNSUNG -> Samsung)."""
    conteo = serie[serie != ""].value_counts()
    canon = {}
    for m in conteo.index:  # de más a menos frecuente
        cerca = difflib.get_close_matches(m, list(canon.values()) or [m], n=1, cutoff=0.8)
        canon[m] = cerca[0] if cerca and cerca[0] != m and conteo[cerca[0]] >= conteo[m] else m
    return serie.map(lambda m: canon.get(m, m))


def texto_lista(xs):
    """Checklist/fotos pueden venir como texto o como {item: …, obligatorio: …}."""
    out = []
    for x in xs or []:
        if isinstance(x, dict):
            nombre = x.get("item") or x.get("nombre") or next(iter(x.values()))
            out.append(f"{nombre}{' (opcional)' if x.get('obligatorio') is False else ''}")
        else:
            out.append(str(x))
    return " · ".join(out)


def tabla_metricas(df, claves):
    t = df.groupby(claves, dropna=False).apply(metricas, include_groups=False)
    if isinstance(t, pd.Series):
        t = t.unstack()
    return t.reset_index()


def main():
    df = pd.read_csv(os.path.join(P, "prendas_clasificadas.csv"), low_memory=False)
    df = df[df.plantilla_id.notna() & ~df.categoria.isin(EXCLUIR)].copy()
    defs = leer_yaml()

    por_modelo = df.categoria.isin(POR_MODELO)
    df["plantilla_maxi"] = df.plantilla.where(~por_modelo, df.categoria)
    df["plantilla_maxi_id"] = df.plantilla_id.where(~por_modelo, df.categoria.str.lower().str.replace(" ", "-"))

    # marca, gama y modelo limpios (catalogo/marcas/*.yaml)
    cfg_marcas = cargar_marcas()
    res = [resolver(r, cfg_marcas.get(r["categoria"])) for r in df.to_dict("records")]
    df["marca_obj"], df["gama"], df["modelo_obj"], df["marca_ok"] = zip(*res)
    df["marca_res"] = df.marca_obj
    fija = [gama_objeto(i, cfg_marcas.get(c)) for i, c in zip(df.plantilla_id, df.categoria)]
    df["gama"] = [f or g for f, g in zip(fija, df.gama)]

    # candidato a objeto propio: modelo de celular/moto (regla no genérica) o marca + modelo capturados
    marca_regla = df.plantilla_id.map(lambda i: defs.get(i, {}).get("p", {}).get("marca"))
    generica = df.plantilla_id.map(lambda i: bool(defs.get(i, {}).get("p", {}).get("generica")))
    cand = pd.Series(None, index=df.index, dtype=object)
    pm = por_modelo & ~generica
    cand[pm] = [o if not m or o.upper().startswith(str(m).upper()) else f"{m} {o}"
                for o, m in zip(df.loc[pm, "plantilla"], marca_regla[pm])]
    gen = ~por_modelo & df.marca_ok & (df.modelo_obj != "")
    cand[gen] = df.loc[gen, "marca_obj"] + " " + df.loc[gen, "modelo_obj"]
    df["candidato"] = cand
    n = df[df.es_compra != True].groupby(["plantilla_maxi_id", "candidato"]).size()  # noqa: E712
    propio = [pd.notna(c) and n.get((p, c), 0) >= MIN_OBJETO for p, c in zip(df.plantilla_maxi_id, df.candidato)]
    df["tipo_objeto"] = ["propio" if x else "genérico por gama" for x in propio]
    df["objeto"] = [c if x else f"{pl} · {GAMA_TXT.get(g, 'gama básica')}"
                    for c, x, pl, g in zip(df.candidato, propio, df.plantilla_maxi, df.gama)]
    df.loc[[not x for x in propio], "marca_obj"] = None

    m_pl = tabla_metricas(df, ["categoria", "plantilla_maxi_id", "plantilla_maxi"])
    m_ob = tabla_metricas(df, ["categoria", "plantilla_maxi_id", "plantilla_maxi", "objeto", "tipo_objeto", "gama"])
    m_va = tabla_metricas(df, ["categoria", "plantilla_maxi_id", "plantilla_maxi", "objeto", "variante"])
    for t in (m_ob, m_va):
        t["precio_por"] = t.prendas.map(lambda n: "historial" if n >= MIN_HISTORIAL else "regla de la plantilla")
    m_ob["marca"] = m_ob.objeto.map(df.groupby("objeto").marca_obj.first())
    m_ob["plantilla_id"] = m_ob.objeto.map(df.groupby("objeto").plantilla_id.first())
    # en los genéricos: qué marcas caen ahí
    marcas_gen = (df[(df.tipo_objeto != "propio") & (df.marca_res != "")].groupby("objeto").marca_res
                  .agg(lambda x: ", ".join(x.value_counts().head(6).index)))
    m_ob["marcas_incluidas"] = m_ob.objeto.map(marcas_gen)
    # por promover: marca+modelo con 2-4 empeños (llegan a objeto propio al juntar 5)
    pend = n[(n >= 2) & (n < MIN_OBJETO)].reset_index(name="empeños")
    pend["plantilla"] = pend.plantilla_maxi_id.map(df.groupby("plantilla_maxi_id").plantilla_maxi.first())

    salida = []
    for (cat, pid, nombre), _ in df.groupby(["categoria", "plantilla_maxi_id", "plantilla_maxi"]):
        ids = df.loc[df.plantilla_maxi_id == pid, "plantilla_id"].unique()
        d0 = defs[ids[0]]
        attrs = dict(d0["cat"].get("atributos") or {}) if cat in POR_MODELO else d0["attrs"]
        fila = m_pl[m_pl.plantilla_maxi_id == pid].iloc[0]
        objs = m_ob[m_ob.plantilla_maxi_id == pid].sort_values("prendas", ascending=False)
        salida.append({
            "id": pid, "plantilla": nombre, "categoria": cat,
            "campos": campos(attrs, cat in POR_MODELO),
            "checklist": d0["p"].get("checklist"), "fotos": d0["p"].get("fotos"),
            "molde_descripcion": d0["p"].get("molde_descripcion"),
            "historial": {k: fila.get(k) for k in CAMPOS_METRICA},
            "objetos": [{
                "objeto": o.objeto, "tipo": o.tipo_objeto, "gama": o.gama, "marca": o.marca,
                "marcas_incluidas": o.marcas_incluidas if isinstance(o.marcas_incluidas, str) else None,
                "sinonimos": defs[o.plantilla_id]["p"].get("sinonimos")
                if cat in POR_MODELO and o.tipo_objeto == "propio" else None,
                "precio_por": o.precio_por,
                "historial": {k: o.get(k) for k in CAMPOS_METRICA},
                "variantes": [{"variante": v.variante, "precio_por": v.precio_por,
                               "historial": {k: v.get(k) for k in CAMPOS_METRICA}}
                              for _, v in m_va[(m_va.plantilla_maxi_id == pid) & (m_va.objeto == o.objeto)]
                              .sort_values("prendas", ascending=False).iterrows()],
            } for _, o in objs.iterrows()],
        })

    with open(os.path.join(ROOT, "catalogo", "maxi_pos.json"), "w", encoding="utf-8") as f:
        json.dump({"modelo": "Plantilla > Objeto > Variante", "plantillas": salida}, f,
                  ensure_ascii=False, indent=1, default=lambda x: None if pd.isna(x) else str(x))

    # Excel para revisar a mano
    hoja_pl = pd.DataFrame([{
        "Categoría": s["categoria"], "Plantilla": s["plantilla"],
        "Campos que crean variante": ", ".join(c["campo"] for c in s["campos"] if c["crea_variante"]) or "—",
        "Campos descriptivos": ", ".join(c["campo"] for c in s["campos"] if not c["crea_variante"]),
        "Objetos propios": sum(o["tipo"] == "propio" for o in s["objetos"]),
        "Genéricos por gama": sum(o["tipo"] != "propio" for o in s["objetos"]),
        "Objetos con historial (5+)": sum(o["precio_por"] == "historial" for o in s["objetos"]),
        "Checklist": texto_lista(s["checklist"]), "Fotos": texto_lista(s["fotos"]),
        **{k: s["historial"][k] for k in CAMPOS_METRICA}} for s in salida]).sort_values("prendas", ascending=False)
    cols = ["categoria", "plantilla_maxi", "objeto", "tipo_objeto", "gama", "marca", "marcas_incluidas",
            "precio_por"] + CAMPOS_METRICA
    hoja_ob = m_ob[cols].sort_values(["categoria", "plantilla_maxi", "tipo_objeto", "prendas"],
                                     ascending=[True, True, True, False])
    hoja_pp = pend[["plantilla", "candidato", "empeños"]].sort_values(["plantilla", "empeños"],
                                                                     ascending=[True, False])
    hoja_va = m_va[["categoria", "plantilla_maxi", "objeto", "variante", "precio_por"] + CAMPOS_METRICA] \
        .sort_values(["categoria", "plantilla_maxi", "objeto", "prendas"], ascending=[True, True, True, False])
    ren = {"categoria": "Categoría", "plantilla_maxi": "Plantilla", "objeto": "Objeto", "marca": "Marca",
           "variante": "Variante", "precio_por": "Precio sugerido por", "tipo_objeto": "Tipo de objeto",
           "gama": "Gama", "marcas_incluidas": "Marcas que caen aquí", "candidato": "Marca + modelo", "prendas": "Empeños",
           "prestamo_p25": "Préstamo p25", "prestamo_mediana": "Préstamo mediana", "prestamo_p75": "Préstamo p75",
           "pct_desempeno": "% desempeña", "pct_refrenda": "% refrenda ≥1", "pct_remate": "% remate",
           "drop_cerrados": "DROP cerrados", "vendidas": "Vendidas", "venta_p25": "Venta p25",
           "venta_mediana": "Venta mediana", "venta_p75": "Venta p75", "venta_sobre_prestamo": "Venta ÷ préstamo",
           "dias_vitrina_mediana": "Días en vitrina", "salida": "Salida"}
    xlsx = os.path.join(ROOT, "reportes", "maxi_pos_plantillas.xlsx")
    with pd.ExcelWriter(xlsx) as w:
        for nombre, t in [("Plantillas", hoja_pl), ("Objetos", hoja_ob), ("Variantes", hoja_va),
                          ("Por promover", hoja_pp)]:
            t.rename(columns=ren).to_excel(w, sheet_name=nombre, index=False)
    prop = m_ob.tipo_objeto == "propio"
    print(f"plantillas: {len(salida)}  objetos propios: {prop.sum()}  genéricos por gama: {(~prop).sum()}  "
          f"variantes: {len(m_va)}  por promover (2-4 empeños): {len(pend)}")
    emp = df[df.es_compra != True]  # noqa: E712
    print(f"empeños en objeto propio: {(emp.tipo_objeto == 'propio').mean():.0%}  "
          f"marca reconocida: {emp.marca_ok.mean():.0%}")


if __name__ == "__main__":
    main()
