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
from plantillas import campo, metricas  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data", "processed")

POR_MODELO = {"Celulares", "Tablets", "Motos", "Autos y camionetas", "Videojuegos", "Relojes"}
EXCLUIR = {"Joyería de oro", "Joyería de plata"}
MIN_HISTORIAL = 5  # regla del mockup: con 5+ operaciones propias manda el historial

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

    # objetos: por modelo = la regla del YAML; generales = marca + modelo capturados
    df["marca_obj"] = df.apply(marca_de, axis=1)
    gen = ~por_modelo
    df.loc[gen, "marca_obj"] = df[gen].groupby("plantilla_id")["marca_obj"].transform(unificar_marcas)
    modelo = df.Modelo.map(campo).str.replace(r"[^A-Z0-9]", "", regex=True)
    modelo = modelo.where((modelo.str.len() >= 2) & (modelo != df.marca_obj.str.upper().str.replace(" ", "")), "")
    df["objeto"] = df.plantilla.where(por_modelo, "")
    df.loc[gen, "objeto"] = [
        (f"{m} {mo}" if m and mo else f"{m} (modelo sin anotar)" if m else "Sin marca")
        for m, mo in zip(df.loc[gen, "marca_obj"], modelo[gen])]
    df.loc[por_modelo, "marca_obj"] = [defs.get(i, {}).get("p", {}).get("marca") or m
                                       for i, m in zip(df.loc[por_modelo, "plantilla_id"],
                                                       df.loc[por_modelo, "marca_obj"])]
    # "FT150" -> "Italika FT150" (si el nombre no trae ya la marca)
    df.loc[por_modelo, "objeto"] = [
        o if not m or o.upper().startswith(m.upper()) or "(" in o and m.upper() in o.upper() else f"{m} {o}"
        for o, m in zip(df.loc[por_modelo, "objeto"], df.loc[por_modelo, "marca_obj"])]

    m_pl = tabla_metricas(df, ["categoria", "plantilla_maxi_id", "plantilla_maxi"])
    m_ob = tabla_metricas(df, ["categoria", "plantilla_maxi_id", "plantilla_maxi", "objeto", "plantilla_id"])
    m_va = tabla_metricas(df, ["categoria", "plantilla_maxi_id", "plantilla_maxi", "objeto", "variante"])
    for t in (m_ob, m_va):
        t["precio_por"] = t.prendas.map(lambda n: "historial" if n >= MIN_HISTORIAL else "regla de la plantilla")
    m_ob["marca"] = m_ob.objeto.map(df.groupby("objeto").marca_obj.first())

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
                "objeto": o.objeto, "marca": o.marca,
                "sinonimos": defs[o.plantilla_id]["p"].get("sinonimos") if cat in POR_MODELO else None,
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
        "Objetos": len(s["objetos"]),
        "Objetos con historial (5+)": sum(o["precio_por"] == "historial" for o in s["objetos"]),
        "Checklist": texto_lista(s["checklist"]), "Fotos": texto_lista(s["fotos"]),
        **{k: s["historial"][k] for k in CAMPOS_METRICA}} for s in salida]).sort_values("prendas", ascending=False)
    cols = ["categoria", "plantilla_maxi", "objeto", "marca", "precio_por"] + CAMPOS_METRICA
    hoja_ob = m_ob[cols].sort_values(["categoria", "plantilla_maxi", "prendas"], ascending=[True, True, False])
    hoja_va = m_va[["categoria", "plantilla_maxi", "objeto", "variante", "precio_por"] + CAMPOS_METRICA] \
        .sort_values(["categoria", "plantilla_maxi", "objeto", "prendas"], ascending=[True, True, True, False])
    ren = {"categoria": "Categoría", "plantilla_maxi": "Plantilla", "objeto": "Objeto", "marca": "Marca",
           "variante": "Variante", "precio_por": "Precio sugerido por", "prendas": "Empeños",
           "prestamo_p25": "Préstamo p25", "prestamo_mediana": "Préstamo mediana", "prestamo_p75": "Préstamo p75",
           "pct_desempeno": "% desempeña", "pct_refrenda": "% refrenda ≥1", "pct_remate": "% remate",
           "drop_cerrados": "DROP cerrados", "vendidas": "Vendidas", "venta_p25": "Venta p25",
           "venta_mediana": "Venta mediana", "venta_p75": "Venta p75", "venta_sobre_prestamo": "Venta ÷ préstamo",
           "dias_vitrina_mediana": "Días en vitrina", "salida": "Salida"}
    xlsx = os.path.join(ROOT, "reportes", "maxi_pos_plantillas.xlsx")
    with pd.ExcelWriter(xlsx) as w:
        for nombre, t in [("Plantillas", hoja_pl), ("Objetos", hoja_ob), ("Variantes", hoja_va)]:
            t.rename(columns=ren).to_excel(w, sheet_name=nombre, index=False)
    print(f"plantillas: {len(salida)}  objetos: {len(m_ob)}  "
          f"con historial (5+): {(m_ob.precio_por == 'historial').sum()}  variantes: {len(m_va)}")


if __name__ == "__main__":
    main()
