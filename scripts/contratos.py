"""Paso 2 — Une empeños con refrendos, desempeños y remates.

Uso:  python scripts/contratos.py
Escribe:
  data/processed/contratos.csv  una fila por contrato con su estado final
  data/processed/prendas.csv    una fila por prenda (empeños + estado del contrato)

Estado final de un contrato (el último movimiento manda):
  DESEMPEÑO  el cliente pagó y se llevó la prenda
  REMATE     pasó a venta (no se recuperó)
  VIGENTE    sin desempeño ni remate y la fecha de remate aún no llega
  VENCIDO    sin desempeño ni remate y ya pasó la fecha de remate (pendiente de rematar)
Si hubo remate y después desempeño, queda DESEMPEÑO con rescatado_de_remate = True.
"""
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data", "processed")


def cargar(nombre, fechas):
    return pd.read_csv(os.path.join(P, f"{nombre}.csv"), parse_dates=fechas)


def main():
    emp = cargar("empenos", ["F. Empeño", "F. Vencimiento", "F. Remate"])
    ref = cargar("refrendos", ["Fecha", "Fecha Mov."])
    des = cargar("desempenos", ["Fecha", "Fecha Mov."])
    rem = cargar("remates", ["F. Empeño", "F. Movimiento"])

    corte = max(emp["F. Empeño"].max(), ref["Fecha Mov."].max(),
                des["Fecha Mov."].max(), rem["F. Movimiento"].max())

    c = emp.groupby("Contrato").agg(
        sucursal=("Sucursal", "first"),
        cliente=("Cliente", "first"),
        usuario=("Usuario", "first"),
        prenda_pf=("Prenda", "first"),
        plan=("Plan", "first"),
        tasa=("Tasa %", "first"),
        es_compra=("Es compra", "first"),
        f_empeno=("F. Empeño", "first"),
        f_vencimiento=("F. Vencimiento", "first"),
        f_remate_programado=("F. Remate", "first"),
        n_prendas=("Contrato", "size"),
        prestamo=("Préstamo", "sum"),
        avaluo=("Avaluo", "sum"),
    )

    r = ref.groupby("Contrato").agg(
        n_refrendos=("Recibo", "size"),
        intereses_refrendo=("Intereses", "sum"),
        almacenaje_refrendo=("Almacenaje", "sum"),
        moratorios_refrendo=("Moratorios", "sum"),
        abono_capital=("Abono", "sum"),
        f_ultimo_refrendo=("Fecha Mov.", "max"),
    )
    d = des.groupby("Contrato").agg(
        f_desempeno=("Fecha Mov.", "max"),
        intereses_desempeno=("Intereses", "sum"),
        almacenaje_desempeno=("Almacenaje", "sum"),
        moratorios_desempeno=("Moratorios", "sum"),
        total_desempeno=("Total", "sum"),
    )
    m = rem.groupby("Contrato").agg(f_remate=("F. Movimiento", "max"))

    c = c.join(r).join(d).join(m)
    c["n_refrendos"] = c["n_refrendos"].fillna(0).astype(int)

    def estado(x):
        if pd.notna(x.f_desempeno):
            return "DESEMPEÑO"
        if pd.notna(x.f_remate):
            return "REMATE"
        # el refrendo mueve la fecha de remate: ~38 días desde el último refrendo
        ultimo = x.f_ultimo_refrendo if pd.notna(x.f_ultimo_refrendo) else x.f_empeno
        limite = max(x.f_remate_programado, ultimo + pd.Timedelta(days=38))
        return "VIGENTE" if limite >= corte else "VENCIDO"

    c["estado"] = c.apply(estado, axis=1)
    c["rescatado_de_remate"] = c.f_desempeno.notna() & c.f_remate.notna()
    c["refrendo_alguna_vez"] = c.n_refrendos > 0
    c["cerrado"] = c.estado.isin(["DESEMPEÑO", "REMATE"])
    fin = c.f_desempeno.fillna(c.f_remate)
    c["dias_vida"] = (fin - c.f_empeno).dt.days
    c["ingreso_total"] = c[["intereses_refrendo", "almacenaje_refrendo", "moratorios_refrendo",
                            "intereses_desempeno", "almacenaje_desempeno",
                            "moratorios_desempeno"]].fillna(0).sum(axis=1)
    c["fecha_corte"] = corte
    c.to_csv(os.path.join(P, "contratos.csv"))

    cols = ["estado", "n_refrendos", "refrendo_alguna_vez", "rescatado_de_remate",
            "cerrado", "dias_vida", "es_compra"]
    prendas = emp.drop(columns=["Es compra"]).join(c[cols], on="Contrato")
    prendas.insert(0, "prenda_id", range(1, len(prendas) + 1))
    prendas.to_csv(os.path.join(P, "prendas.csv"), index=False)

    print(f"corte de datos: {corte.date()}")
    print(c.estado.value_counts().to_string())
    print(f"contratos: {len(c)}  prendas: {len(prendas)}")


if __name__ == "__main__":
    main()
