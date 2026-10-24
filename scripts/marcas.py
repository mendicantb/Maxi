"""Diccionario de marcas: nombre correcto, gama (alta / media / basica) y modelos unificados.

Lo usa scripts/exportar_maxi.py para decidir el objeto de cada prenda:
  - objeto propio si la marca+modelo (o el modelo de celular) junta suficientes empeños
  - si no, el objeto genérico de su plantilla y gama: "Rotomartillo · gama alta"

Archivos: catalogo/marcas/*.yaml (formato en docs/FORMATO_MARCAS.md)

Prueba de un archivo (sólo lee):
  python3 scripts/marcas.py --probar catalogo/marcas/herramientas.yaml
"""
import glob
import json
import os
import re
import sys

import pandas as pd
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plantillas import campo, norm  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMAS = ("alta", "media", "basica")


def solo_alnum(s):
    return re.sub(r"[^A-Z0-9]", "", norm(s))


def cargar(archivos=None):
    """Devuelve {categoria: sector} con regex de marcas ya compiladas."""
    por_cat = {}
    for path in archivos or sorted(glob.glob(os.path.join(ROOT, "catalogo", "marcas", "*.yaml"))):
        cfg = yaml.safe_load(open(path, encoding="utf-8")) or {}
        cfg["_archivo"] = os.path.basename(path)
        reglas = []
        for nombre, m in (cfg.get("marcas") or {}).items():
            m = m or {}
            escrituras = {norm(nombre)} | {norm(e) for e in m.get("escritura") or []}
            for e in escrituras:
                if e:
                    reglas.append((len(e), re.compile(rf"\b{re.escape(e)}\b"), nombre, m.get("gama", "media")))
        cfg["_reglas"] = [r[1:] for r in sorted(reglas, key=lambda r: -r[0])]  # escritura más larga primero
        modelos = {}
        for marca, mods in (cfg.get("modelos") or {}).items():
            for canon, variantes in (mods or {}).items():
                for v in [canon] + list(variantes or []):
                    modelos[(marca, solo_alnum(v))] = canon
        cfg["_modelos"] = modelos
        for cat in cfg.get("categorias") or []:
            por_cat[cat] = cfg
    return por_cat


def marca_cruda(row):
    try:
        attrs = json.loads(row["atributos"]) if isinstance(row.get("atributos"), str) else {}
    except ValueError:
        attrs = {}
    partes = [str(v) for k, v in attrs.items() if k.startswith("marca") and v]
    partes.append(campo(row.get("Marca")))
    return norm(" ".join(p for p in partes if p))


def resolver(row, cfg):
    """-> (marca, gama, modelo, reconocida)"""
    texto_marca = marca_cruda(row)
    modelo = solo_alnum(campo(row.get("Modelo")))
    marca, gama, ok = "", (cfg or {}).get("gama_por_defecto", "basica"), False
    if cfg:
        for fuente in (texto_marca, row.get("texto") or ""):
            for rx, nombre, g in cfg["_reglas"]:
                if rx.search(fuente):
                    marca, gama, ok = nombre, g, True
                    break
            if ok:
                break
        if ok:
            modelo = cfg["_modelos"].get((marca, modelo), modelo)
    if not ok:
        marca = texto_marca.title()
    if solo_alnum(marca) and modelo == solo_alnum(marca):
        modelo = ""
    return marca, gama, (modelo if len(modelo) >= 2 else ""), ok


def gama_objeto(plantilla_id, cfg):
    """Para plantillas por modelo (celulares): gama fija por id de regla."""
    return ((cfg or {}).get("gama_por_objeto") or {}).get(plantilla_id)


def probar(path):
    cfgs = cargar([path])
    cats = set(cfgs)
    df = pd.read_csv(os.path.join(ROOT, "data", "processed", "prendas_clasificadas.csv"), low_memory=False)
    df = df[df.categoria.isin(cats) & (df.es_compra != True)]  # noqa: E712
    res = [resolver(r, cfgs[r["categoria"]]) for r in df.to_dict("records")]
    df["marca_n"], df["gama"], df["modelo_n"], df["ok"] = zip(*res)
    print(f"categorías: {sorted(cats)}")
    print(f"prendas: {len(df)}  marca reconocida: {df.ok.mean():.1%}")
    print("\n-- gama --")
    print(df.gama.value_counts(normalize=True).round(3).to_string())
    print("\n-- préstamo mediano por gama y plantilla (top 25 plantillas) --")
    top = df.plantilla.value_counts().head(25).index
    print(df[df.plantilla.isin(top)].pivot_table(index="plantilla", columns="gama", values="Préstamo",
                                                  aggfunc="median").round(0).to_string())
    print("\n-- 50 marcas crudas NO reconocidas (más frecuentes) --")
    sin = df[~df.ok].assign(cruda=df.loc[~df.ok, "Marca"].map(campo))
    print(sin.cruda.replace("", "(vacía)").value_counts().head(50).to_string())
    print("\n-- marca+modelo con 3+ empeños (candidatos a objeto propio) --")
    g = df[df.modelo_n != ""].groupby(["plantilla", "marca_n", "modelo_n"]).size()
    print(g[g >= 3].sort_values(ascending=False).head(60).to_string())
    if cfgs and any(c.get("gama_por_objeto") for c in cfgs.values()):
        sin_gama = df[[gama_objeto(i, cfgs[c]) is None for i, c in zip(df.plantilla_id, df.categoria)]]
        print(f"\n-- reglas sin gama_por_objeto: {sin_gama.plantilla_id.nunique()} "
              f"({len(sin_gama)} prendas) --")
        print(sin_gama.plantilla_id.value_counts().head(40).to_string())


if __name__ == "__main__":
    if "--probar" in sys.argv:
        probar(sys.argv[sys.argv.index("--probar") + 1])
