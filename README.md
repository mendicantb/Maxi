# Maxi — datos y análisis

Repositorio de datos de MAXI Empeños para análisis estructurado. Primer proyecto: sacar del historial de
PRENDA FLEX el **catálogo de plantillas de MAXI-POS** (Categoría › Familia › Variante), con métricas por
plantilla para que la evaluadora y el cliente sepan qué pasa con cada tipo de artículo:
cuánto se presta, qué % desempeña, refrenda o se remata, a cuánto se vende y en cuántos días sale.

> **Repo privado.** `data/raw/CLIENTES.xls` tiene CURP, INE, teléfonos y domicilios, y algunas descripciones
> originales traen contraseñas de equipos (en `data/processed/` ya van tapadas con `***`).

## Estado actual (corte 4-oct-2026, sucursal Candelaria)

- 10,589 prendas en 9,303 contratos (mar-2024 → oct-2026); 4,651 ventas de vitrina; 1,666 apartados.
- **33 categorías · 644 plantillas** cubren el **99%** de las prendas (95% en plantilla específica, no genérica).
- Resumen legible: [`reportes/cobertura.md`](reportes/cobertura.md).
- Modelo Plantilla › Objeto › Variante: [`docs/MODELO_PLANTILLAS.md`](docs/MODELO_PLANTILLAS.md) y
  `reportes/maxi_pos_plantillas.xlsx` (228 plantillas, 3,116 objetos, sin joyería).

## Estructura

```
data/raw/            exportes de PRENDA FLEX tal cual (.xls)
data/processed/      CSV limpios + contratos, prendas, ventas, prendas_clasificadas
catalogo/plantillas/ reglas de cada categoría (YAML) — aquí se edita el catálogo
catalogo/catalogo.json   catálogo + métricas (todas las reglas)
catalogo/maxi_pos.json   modelo MAXI-POS: Plantilla › Objeto › Variante (ver docs/MODELO_PLANTILLAS.md)
reportes/            métricas por categoría / plantilla / variante, pendientes, historial de cobertura
docs/                PLAN.md, FORMATO_PLANTILLAS.md, notas_<categoría>.md (decisiones y dudas)
scripts/             pipeline
```

## Cómo correrlo

```bash
pip install -r requirements.txt
bash scripts/correr_todo.sh          # ingest → contratos → ventas → plantillas → exportar
python3 scripts/plantillas.py --probar catalogo/plantillas/celulares.yaml   # probar una categoría sin escribir nada
```

Para actualizar: reemplaza los `.xls` en `data/raw/` con los exportes nuevos (mismos nombres) y corre el pipeline.
Cada corrida agrega una fila a `reportes/historial/cobertura.csv`.

## Archivos de PRENDA FLEX que usa

| Archivo | Qué es |
|---|---|
| `EMPENOS_2024-2026.xls` | una fila por prenda empeñada (familia, descripción, marca, modelo, préstamo, avalúo, plan) |
| `REFRENDOS_2024-2026.xls` | pagos de refrendo por contrato |
| `DESEMPENOS_2024-2026.xls` | desempeños por contrato |
| `REMATES_2024-2026.xls` | prendas que pasaron a venta (con pesos en joyería) |
| `VENTAS_VITRINA_2024-2026.xls` | todas las ventas (incluye apartados liquidados) |
| `VENTAS_APARTADOS_2024-2026.xls` | apartados con estatus (liquidado / remate / vigente) |
| `APARTADOS_LIQUIDADOS…`, `APARTADOS_REMATADOS…` | detalle de apartados (respaldo) |
| `CLIENTES.xls` | padrón de clientes |

Liga ventas ↔ empeños: el código de la prenda en ventas es `4001` + contrato (6 dígitos) + sufijo.

## Definiciones

- **Estado del contrato**: DESEMPEÑO, REMATE, VIGENTE o VENCIDO (manda el último movimiento; ver `scripts/contratos.py`).
- **% desempeña / refrenda / remate**: sobre prendas empeñadas, sin compras directas.
- **DROP (cerrados)**: % rematado entre contratos ya cerrados (desempeño o remate).
- **Venta / préstamo**: precio de venta final ÷ préstamo (mediana).
- **Días en vitrina**: de la fecha de remate a la venta (mediana). **Salida**: A ≤30 días, B ≤90, C >90.
