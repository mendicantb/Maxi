"""Paso 3 — Liga las ventas de vitrina y los apartados con la prenda empeñada.

Uso:  python scripts/ventas.py
Lee:  data/processed/{ventas_vitrina,ventas_apartados,prendas,contratos}.csv
Escribe:
  data/processed/ventas.csv           cada venta con su contrato / prenda_id (si es de empeño)
  data/processed/prendas_ventas.csv   una fila por prenda vendida: precio final, días a la venta, etc.

Cómo se liga:
- El código de la prenda en ventas es "4001" + contrato (6 dígitos) + sufijo. Sólo los códigos 4001
  son prendas de empeño/compra; 8053, 8003, 5003, 0013, 8253… son mercancía nueva y no se ligan.
- Dentro del contrato se elige la prenda cuya descripción (sin "NO. SERIE") coincide; si no, la única
  o la primera prenda sin venta.
- VENTAS_VITRINA ya incluye los apartados liquidados (mismo día y cliente), así que es la fuente
  de venta. VENTAS_APARTADOS sólo se usa para saber si la prenda se apartó y si el apartado se perdió.
- Si una prenda se vendió dos veces (devolución y reventa) cuenta la última venta.
"""
import os
import re

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data", "processed")


def clave(s):
    s = re.sub(r"NO\.?\s*SERIE\s*:?.*$", "", str(s or ""), flags=re.IGNORECASE)
    return re.sub(r"[^A-Z0-9]+", " ", s.upper()).strip()


def main():
    ven = pd.read_csv(os.path.join(P, "ventas_vitrina.csv"), parse_dates=["Fecha"], dtype={"Codigo": str})
    apa = pd.read_csv(os.path.join(P, "ventas_apartados.csv"), parse_dates=["Fecha", "F. Movimiento"],
                      dtype={"Codigo": str})
    prendas = pd.read_csv(os.path.join(P, "prendas.csv"))
    contratos = pd.read_csv(os.path.join(P, "contratos.csv"), parse_dates=["f_remate", "f_empeno"])

    prendas["k"] = prendas.Descripcion.map(clave)
    por_contrato = {c: g for c, g in prendas.groupby("Contrato")}

    def ligar(df):
        ids = []
        usados = set()
        for row in df.itertuples():
            g = por_contrato.get(row.Contrato) if pd.notna(row.Contrato) else None
            if g is None:
                ids.append(None)
                continue
            k = clave(row.Descripcion)
            hit = g[g.k == k]
            if hit.empty:
                libres = g[~g.prenda_id.isin(usados)]
                hit = libres if not libres.empty else g
            pid = int(hit.prenda_id.iloc[0])
            usados.add(pid)
            ids.append(pid)
        return pd.Series(ids, index=df.index, dtype="Int64")

    ven = ven.sort_values("Fecha")
    ven["prenda_id"] = ligar(ven)
    apa["prenda_id"] = ligar(apa)
    ven["origen"] = ven["Codigo"].fillna("").str[:4].map(
        lambda x: "empeño" if x == "4001" else "mercancía")
    ven.to_csv(os.path.join(P, "ventas.csv"), index=False)

    v = ven[ven.prenda_id.notna()].groupby("prenda_id").agg(
        f_venta=("Fecha", "last"), p_venta=("P. Venta", "last"), precio_lista=("Precio", "last"),
        descuento=("Descuento", "last"), costo=("Costo", "last"), n_ventas=("Fecha", "size"))
    a = apa[apa.prenda_id.notna()].groupby("prenda_id").agg(
        n_apartados=("Estatus", "size"),
        apartado_perdido=("Estatus", lambda s: (s == "Remate").any()),
        f_primer_apartado=("Fecha", "min"))
    pv = v.join(a, how="outer")
    base = prendas.set_index("prenda_id")[["Contrato", "Préstamo"]].join(
        contratos.set_index("Contrato")[["f_remate", "f_empeno"]], on="Contrato")
    pv = pv.join(base)
    # entra a vitrina el día del remate (las compras, el día de la compra)
    entrada = pv.f_remate.fillna(pv.f_empeno)
    pv["dias_a_venta"] = (pv.f_venta - entrada).dt.days.clip(lower=0)
    pv["vendida"] = pv.f_venta.notna()
    pv["multiplicador"] = (pv.p_venta / pv["Préstamo"]).where(pv["Préstamo"] > 0)
    pv["margen"] = ((pv.p_venta - pv.costo) / pv.p_venta).where(pv.p_venta > 0)
    pv.drop(columns=["Contrato", "Préstamo", "f_remate", "f_empeno"]).to_csv(
        os.path.join(P, "prendas_ventas.csv"))

    e = ven.origen == "empeño"
    print(f"ventas vitrina: {len(ven)}  de empeño: {e.sum()}  ligadas a prenda: {ven.prenda_id.notna().sum()}")
    print(f"prendas vendidas: {pv.vendida.sum()}  apartadas: {pv.n_apartados.notna().sum()}  "
          f"días a venta (mediana): {pv.dias_a_venta.median():.0f}")


if __name__ == "__main__":
    main()
