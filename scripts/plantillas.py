"""Paso 3 — Clasifica cada prenda en una plantilla y calcula métricas.

Uso:  python scripts/plantillas.py [--sin-historial]
Lee:  data/processed/prendas.csv  +  catalogo/plantillas/*.yaml
Escribe:
  data/processed/prendas_clasificadas.csv   prenda -> categoría / plantilla / variante / atributos
  reportes/categorias.csv                   métricas por categoría
  reportes/plantillas.csv                   métricas por plantilla
  reportes/variantes.csv                    métricas por variante
  reportes/pendientes.csv                   lo que no cayó en ninguna plantilla, agrupado
  reportes/cobertura.md                     resumen legible
  reportes/historial/cobertura.csv          una fila por corrida (para ver el avance)
  catalogo/catalogo.json                    catálogo completo + métricas (para cargar a MAXI-POS)

Formato de catálogo: ver docs/FORMATO_PLANTILLAS.md
"""
import glob
import json
import os
import re
import sys
import unicodedata
from datetime import datetime

import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data", "processed")
CAT_DIR = os.path.join(ROOT, "catalogo", "plantillas")
REP = os.path.join(ROOT, "reportes")

SERIE_RE = re.compile(r"NO\.?\s*SERIE\s*:?.*$", re.IGNORECASE)
VACIOS = {"", "SN", "S N", "X", "XX", "XXX", "NAN", "NONE", "SIN", "SIN GARANTIA", "0", "00", "000"}


def norm(s):
    """Mayúsculas, sin acentos, sólo letras/números/espacios. Ñ se conserva como N."""
    if not isinstance(s, str):
        return ""
    s = unicodedata.normalize("NFKD", s.upper())
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^A-Z0-9\.\/]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def campo(s):
    n = norm(s)
    return "" if n in VACIOS else n


def texto_prenda(row):
    desc = SERIE_RE.sub("", row.get("Descripcion") or "")
    partes = [norm(desc)]
    marca, modelo = campo(row.get("Marca")), campo(row.get("Modelo"))
    if marca:
        partes.append(f"MARCA {marca}")
    if modelo:
        partes.append(f"MODELO {modelo}")
    return " | ".join(partes)


# ---------------------------------------------------------------- catálogo

def cargar_catalogo(archivos=None):
    categorias = []
    for path in archivos or sorted(glob.glob(os.path.join(CAT_DIR, "*.yaml"))):
        with open(path, encoding="utf-8") as f:
            cat = yaml.safe_load(f)
        if not cat:
            continue
        cat["_archivo"] = os.path.basename(path)
        comunes = cat.get("atributos", {}) or {}
        for p in cat.get("plantillas", []) or []:
            p["_match"] = [re.compile(r, re.IGNORECASE) for r in p.get("match", [])]
            p["_excluir"] = [re.compile(r, re.IGNORECASE)
                             for r in (p.get("excluir", []) or []) + (cat.get("excluir", []) or [])]
            attrs = dict(comunes)
            attrs.update(p.get("atributos", {}) or {})
            p["_attrs"] = {k: dict(v, _re=re.compile(v["regex"], re.IGNORECASE))
                           for k, v in attrs.items() if v and v.get("regex")}
        categorias.append(cat)
    return categorias


def extraer_atributos(plantilla, texto):
    out = {}
    for nombre, a in plantilla["_attrs"].items():
        m = a["_re"].search(texto)
        if not m:
            continue
        val = (m.group(1) if m.groups() and m.group(1) else m.group(0)).strip().upper()
        val = (a.get("mapa") or {}).get(val, val)
        if a.get("formato"):
            val = a["formato"].format(val)
        out[nombre] = val
    return out


def variante(plantilla, attrs):
    claves = [k for k, a in plantilla["_attrs"].items() if a.get("crea_variante")]
    if not claves:
        return "Base"
    return " · ".join(f"{attrs.get(k, '?')}" for k in claves)


def buscar(plantillas, texto):
    for p in plantillas:
        if any(r.search(texto) for r in p["_match"]) and not any(r.search(texto) for r in p["_excluir"]):
            return p
    return None


def clasificar(prendas, categorias):
    por_familia = {}
    todas = []
    for cat in categorias:
        for p in cat.get("plantillas", []) or []:
            p["_cat"] = cat
            todas.append(p)
            for fam in cat.get("familias_prendaflex", []) or []:
                por_familia.setdefault(fam, []).append(p)

    filas = []
    for row in prendas.to_dict("records"):
        texto = texto_prenda(row)
        fam = row.get("Familia")
        p = buscar(por_familia.get(fam, []), texto)
        tipo = "familia"
        if p is None:
            p = buscar([x for x in todas if not x.get("solo_familia")], texto)
            tipo = "otra_familia"
        if p is None:
            filas.append(dict(prenda_id=row["prenda_id"], texto=texto, match="ninguno"))
            continue
        attrs = extraer_atributos(p, texto)
        filas.append(dict(
            prenda_id=row["prenda_id"], texto=texto, match=tipo,
            categoria=p["_cat"]["categoria"], plantilla_id=p["id"], plantilla=p["nombre"],
            generica=bool(p.get("generica")), variante=variante(p, attrs),
            atributos=json.dumps(attrs, ensure_ascii=False)))
    return prendas.merge(pd.DataFrame(filas), on="prenda_id", how="left")


# ---------------------------------------------------------------- métricas

def metricas(g):
    g = g[g.es_compra != True]  # noqa: E712  las compras no son empeños
    if g.empty:
        return pd.Series(dtype=float)
    cerr = g[g.cerrado == True]  # noqa: E712
    return pd.Series({
        "prendas": len(g),
        "contratos": g.Contrato.nunique(),
        "prestamo_total": g["Préstamo"].sum(),
        "prestamo_prom": g["Préstamo"].mean(),
        "prestamo_p25": g["Préstamo"].quantile(.25),
        "prestamo_mediana": g["Préstamo"].median(),
        "prestamo_p75": g["Préstamo"].quantile(.75),
        "avaluo_prom": g["Avaluo"].mean(),
        "ltv": g["Préstamo"].sum() / g["Avaluo"].sum() if g["Avaluo"].sum() else None,
        "pct_desempeno": (g.estado == "DESEMPEÑO").mean(),
        "pct_remate": (g.estado == "REMATE").mean(),
        "pct_vigente": g.estado.isin(["VIGENTE", "VENCIDO"]).mean(),
        "pct_refrenda": g.refrendo_alguna_vez.mean(),
        "refrendos_prom": g.n_refrendos.mean(),
        "drop_cerrados": (cerr.estado == "REMATE").mean() if len(cerr) else None,
        "drop_valor_cerrados": (cerr.loc[cerr.estado == "REMATE", "Préstamo"].sum()
                                / cerr["Préstamo"].sum()) if len(cerr) and cerr["Préstamo"].sum() else None,
        "dias_vida_prom": g.dias_vida.mean(),
    })


def tabla(df, claves):
    t = df.groupby(claves, dropna=False).apply(metricas, include_groups=False)
    if isinstance(t, pd.Series):
        t = t.unstack()
    return t.reset_index().sort_values("prendas", ascending=False)


def pendientes(df):
    sin = df[df.match == "ninguno"].copy()
    # agrupa por familia PF + marca + primeras 2 palabras de la descripción
    sin["marca_n"] = sin.Marca.map(campo)
    sin["inicio"] = sin.texto.str.split(" | ", regex=False).str[0].str.split().str[:2].str.join(" ")
    g = sin.groupby(["Familia", "marca_n", "inicio"]).agg(
        prendas=("prenda_id", "size"), prestamo_total=("Préstamo", "sum"),
        ejemplo=("Descripcion", "first")).reset_index()
    return g.sort_values(["prendas", "prestamo_total"], ascending=False)


# ---------------------------------------------------------------- salida

def pct(x):
    return "—" if pd.isna(x) else f"{x*100:.0f}%"


def dinero(x):
    return "—" if pd.isna(x) else f"${x:,.0f}"


def escribir_reportes(df, categorias, guardar_historial=True):
    os.makedirs(os.path.join(REP, "historial"), exist_ok=True)
    df.to_csv(os.path.join(P, "prendas_clasificadas.csv"), index=False)

    emp = df[df.es_compra != True]  # noqa: E712
    cats = tabla(df.assign(categoria=df.categoria.fillna("(sin plantilla)")), ["categoria"])
    plts = tabla(df[df.plantilla_id.notna()], ["categoria", "plantilla_id", "plantilla", "generica"])
    vars_ = tabla(df[df.plantilla_id.notna()], ["categoria", "plantilla_id", "plantilla", "variante"])
    pend = pendientes(df)
    cats.to_csv(os.path.join(REP, "categorias.csv"), index=False)
    plts.to_csv(os.path.join(REP, "plantillas.csv"), index=False)
    vars_.to_csv(os.path.join(REP, "variantes.csv"), index=False)
    pend.to_csv(os.path.join(REP, "pendientes.csv"), index=False)

    cubierto = emp.plantilla_id.notna()
    especifico = cubierto & (emp.generica != True)  # noqa: E712
    resumen = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "categorias": len(categorias),
        "plantillas": sum(len(c.get("plantillas") or []) for c in categorias),
        "prendas": len(emp),
        "pct_prendas_cubiertas": round(cubierto.mean(), 4),
        "pct_prendas_especificas": round(especifico.mean(), 4),
        "pct_prestamo_cubierto": round(emp.loc[cubierto, "Préstamo"].sum() / emp["Préstamo"].sum(), 4),
        "pct_fuera_de_familia": round((emp.match == "otra_familia").mean(), 4),
    }
    hist = os.path.join(REP, "historial", "cobertura.csv")
    if guardar_historial:
        pd.DataFrame([resumen]).to_csv(hist, mode="a", index=False, header=not os.path.exists(hist))

    # catálogo para MAXI-POS: definición + métricas
    m_p = plts.set_index("plantilla_id")
    m_v = vars_.groupby("plantilla_id")
    salida = []
    for cat in categorias:
        c_out = {k: v for k, v in cat.items() if not k.startswith("_") and k != "plantillas"}
        c_out["plantillas"] = []
        for p in cat.get("plantillas") or []:
            p_out = {k: v for k, v in p.items() if not k.startswith("_")}
            if p["id"] in m_p.index:
                p_out["metricas"] = json.loads(m_p.loc[[p["id"]]].iloc[0].drop(
                    ["categoria", "plantilla", "generica"]).to_json())
                p_out["variantes"] = json.loads(m_v.get_group(p["id"]).drop(
                    columns=["categoria", "plantilla_id", "plantilla"]).to_json(orient="records")) \
                    if p["id"] in m_v.groups else []
            c_out["plantillas"].append(p_out)
        salida.append(c_out)
    with open(os.path.join(ROOT, "catalogo", "catalogo.json"), "w", encoding="utf-8") as f:
        json.dump({"generado": resumen["fecha"], "resumen": resumen, "categorias": salida},
                  f, ensure_ascii=False, indent=1, default=str)

    # resumen legible
    L = [f"# Cobertura de plantillas — {resumen['fecha']}", "",
         f"- Categorías: **{resumen['categorias']}** · Plantillas: **{resumen['plantillas']}**",
         f"- Prendas (sin compras): **{resumen['prendas']:,}**",
         f"- Cubiertas por alguna plantilla: **{pct(resumen['pct_prendas_cubiertas'])}** "
         f"(específicas: {pct(resumen['pct_prendas_especificas'])}, el resto cae en una genérica)",
         f"- Préstamo cubierto: **{pct(resumen['pct_prestamo_cubierto'])}**",
         f"- Clasificadas fuera de su familia PRENDA FLEX: {pct(resumen['pct_fuera_de_familia'])} (revisar)",
         "", "## Por categoría", "",
         "| Categoría | Prendas | Préstamo prom. | Desempeña | Remate | Refrenda ≥1 | DROP (cerrados) |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    for _, r in cats.iterrows():
        L.append(f"| {r.categoria} | {int(r.prendas):,} | {dinero(r.prestamo_prom)} | {pct(r.pct_desempeno)} | "
                 f"{pct(r.pct_remate)} | {pct(r.pct_refrenda)} | {pct(r.drop_cerrados)} |")
    L += ["", "## Top 40 plantillas", "",
          "| Categoría | Plantilla | Prendas | Préstamo mediana | Desempeña | Remate | Refrenda ≥1 |",
          "|---|---|---:|---:|---:|---:|---:|"]
    for _, r in plts.head(40).iterrows():
        L.append(f"| {r.categoria} | {r.plantilla} | {int(r.prendas):,} | {dinero(r.prestamo_mediana)} | "
                 f"{pct(r.pct_desempeno)} | {pct(r.pct_remate)} | {pct(r.pct_refrenda)} |")
    L += ["", "## Top 30 pendientes (sin plantilla)", "", "| Familia PF | Marca | Inicio | Prendas | Ejemplo |",
          "|---|---|---|---:|---|"]
    for _, r in pend.head(30).iterrows():
        ej = str(r.ejemplo)[:70].replace("|", "/")
        L.append(f"| {r.Familia} | {r.marca_n} | {r.inicio} | {r.prendas} | {ej} |")
    with open(os.path.join(REP, "cobertura.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    return resumen


def probar(path, prendas):
    """Prueba UN archivo contra sus familias PRENDA FLEX, sin escribir nada."""
    cats = cargar_catalogo([path])
    familias = {f for c in cats for f in c.get("familias_prendaflex") or []}
    sub = prendas[prendas.Familia.isin(familias)]
    sub = sub[sub.es_compra != True]  # noqa: E712
    df = clasificar(sub, cats)
    ok = df.plantilla_id.notna()
    esp = ok & (df.generica != True)  # noqa: E712
    print(f"familias PF: {sorted(familias)}")
    print(f"prendas: {len(df)}  cubiertas: {ok.mean():.1%}  especificas: {esp.mean():.1%}  "
          f"prestamo cubierto: {df.loc[ok, 'Préstamo'].sum() / df['Préstamo'].sum():.1%}")
    print("\n-- por familia PF --")
    print(df.assign(ok=ok, esp=esp).groupby("Familia")[["ok", "esp"]].agg(["size", "mean"]).round(2).to_string())
    print("\n-- plantillas (prendas) --")
    print(df.groupby(["plantilla_id"]).size().sort_values(ascending=False).to_string())
    print("\n-- variantes top 40 --")
    print(df.groupby(["plantilla_id", "variante"]).size().sort_values(ascending=False).head(40).to_string())
    print("\n-- 60 ejemplos SIN plantilla --")
    for t in df.loc[~ok, "texto"].sample(min(60, (~ok).sum()), random_state=0):
        print("  ", t[:160])
    print("\n-- 30 ejemplos en GENÉRICA --")
    gen = df[ok & ~esp]
    for t in gen["texto"].sample(min(30, len(gen)), random_state=0):
        print("  ", t[:160])


def main():
    prendas = pd.read_csv(os.path.join(P, "prendas.csv"))
    if "--probar" in sys.argv:
        probar(sys.argv[sys.argv.index("--probar") + 1], prendas)
        return
    categorias = cargar_catalogo()
    df = clasificar(prendas, categorias)
    resumen = escribir_reportes(df, categorias, guardar_historial="--sin-historial" not in sys.argv)
    for k, v in resumen.items():
        print(f"{k:26s} {v}")


if __name__ == "__main__":
    main()
