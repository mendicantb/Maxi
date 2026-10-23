"""Paso 1 — Convierte los .xls de PRENDA FLEX en CSV limpios.

Uso:  python scripts/ingest.py
Lee:  data/raw/*.xls
Escribe: data/processed/{empenos,refrendos,desempenos,remates,clientes}.csv

- Montos "12,000.00" -> 12000.0
- Fechas "23/abr/2024" -> 2024-04-23
- Quita la fila de totales que PRENDA FLEX agrega al final
- Enmascara contraseñas/PIN escritas en la descripción
"""
import os
import re
import sys

import pandas as pd
import xlrd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
OUT = os.path.join(ROOT, "data", "processed")

ARCHIVOS = {
    "empenos": "EMPENOS_2024-2026.xls",
    "refrendos": "REFRENDOS_2024-2026.xls",
    "desempenos": "DESEMPENOS_2024-2026.xls",
    "remates": "REMATES_2024-2026.xls",
    "clientes": "CLIENTES.xls",
}

MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
         "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}

MONTOS = {"Préstamo", "Avaluo", "Intereses", "Almacenaje", "Moratorios", "Iva",
          "Total", "Abono", "Gtos. Venta", "P. Total", "P. Piedra", "P. Neto"}

PASSWORD_RE = re.compile(
    r"(CONTRASE[ÑN]A|CONTRA|PASSWORD|PASS|PIN|PATR[OÓ]N|CLAVE)\s*[:=]?\s*[\w\-\.]+",
    re.IGNORECASE)


def leer_xls(path):
    # Los archivos son BIFF antiguos sin CODEPAGE; cp1252 respeta Ñ y acentos
    book = xlrd.open_workbook(path, encoding_override="cp1252",
                              logfile=open(os.devnull, "w"))
    sh = book.sheet_by_index(0)
    rows = [sh.row_values(r) for r in range(sh.nrows)]
    df = pd.DataFrame(rows[1:], columns=[str(c).strip() for c in rows[0]])
    return df.replace({"": None})


def fecha(s):
    if not isinstance(s, str):
        return pd.NaT
    m = re.match(r"(\d{1,2})/([a-zA-Z]{3})/(\d{4})", s.strip())
    if not m or m.group(2).lower() not in MESES:
        return pd.NaT
    return pd.Timestamp(int(m.group(3)), MESES[m.group(2).lower()], int(m.group(1)))


def monto(s):
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return None
    try:
        return float(str(s).replace(",", "").replace("$", "").strip())
    except ValueError:
        return None


def limpiar(nombre, df):
    if "Sucursal" in df.columns:
        df = df[df["Sucursal"].notna()]  # fila de totales
    for c in df.columns:
        if c in MONTOS:
            df[c] = df[c].map(monto)
        elif c.startswith("F.") or c in ("Fecha", "Fecha Mov."):
            df[c] = df[c].map(fecha)
    if "Contrato" in df.columns:
        df["Contrato"] = pd.to_numeric(df["Contrato"], errors="coerce").astype("Int64")
    if "Descripcion" in df.columns:
        df["Descripcion"] = df["Descripcion"].fillna("").str.replace(
            PASSWORD_RE, r"\1 ***", regex=True)
    if nombre == "empenos":
        # "TASA GEN 4 SEM-4.06000" -> plan + tasa numérica
        partes = df["Tasa"].fillna("").str.rsplit("-", n=1, expand=True)
        df["Plan"] = partes[0].str.strip()
        df["Tasa %"] = pd.to_numeric(partes[1], errors="coerce")
        df["Es compra"] = df["Plan"].str.startswith("COMPRA")
    return df


def main():
    os.makedirs(OUT, exist_ok=True)
    for nombre, archivo in ARCHIVOS.items():
        path = os.path.join(RAW, archivo)
        if not os.path.exists(path):
            print(f"falta {path}", file=sys.stderr)
            continue
        df = limpiar(nombre, leer_xls(path))
        df.to_csv(os.path.join(OUT, f"{nombre}.csv"), index=False)
        print(f"{nombre:12s} {len(df):6d} filas")


if __name__ == "__main__":
    main()
