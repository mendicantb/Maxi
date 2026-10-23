# Plan de trabajo — Plantillas MAXI-POS desde el historial

Objetivo final: cargar a MAXI-POS un catálogo de plantillas (Categoría › Familia › Variante) donde cada
plantilla trae su historial: cuánto se presta, qué % desempeña / refrenda / se remata, y — cuando haya
datos de ventas — a cuánto se vende y en cuántos días sale.

## Fase 1 — Descubrir plantillas (hecho en esta corrida)

| Paso | Qué | Resultado |
|---|---|---|
| 1 | Convertir exportes PRENDA FLEX a CSV limpio | `scripts/ingest.py` → `data/processed/` |
| 2 | Estado final de cada contrato | `scripts/contratos.py` → `contratos.csv`, `prendas.csv` |
| 3 | Reglas de plantilla por categoría (YAML) | `catalogo/plantillas/*.yaml` |
| 4 | Clasificar cada prenda + métricas | `scripts/plantillas.py` → `reportes/` y `catalogo/catalogo.json` |

## Fase 2 — Cerrar huecos (ciclo semanal, P3)

Cada semana:
1. Exportar de PRENDA FLEX los 4 reportes (empeños, refrendos, desempeños, remates) a `data/raw/`.
2. `bash scripts/correr_todo.sh`
3. Revisar `reportes/pendientes.csv` (lo que no cayó en plantilla) → crear plantilla o agregar sinónimo.
4. Revisar prendas `otra_familia` (capturadas en la familia PF equivocada) → retroalimentar a evaluadoras.
5. `reportes/historial/cobertura.csv` registra el avance de cobertura en cada corrida.

Responsable sugerido: Valuador Senior (llave "catálogo"), respaldo: Líder de sucursal (P6).

## Fase 3 — Precio de venta y salida (hecho)

`scripts/ventas.py` liga VENTAS_VITRINA y VENTAS_APARTADOS con la prenda empeñada por el código
`4001` + contrato. Cada plantilla y variante trae: vendidas, venta p25/mediana/p75, venta ÷ préstamo,
margen, días en vitrina y Salida A/B/C, y % de apartados perdidos.

Pendiente: la mercancía nueva (códigos 8053, 8003, 5003, 0013, 8253 ≈ 1,750 ventas) no viene de empeño
y todavía no se clasifica en plantillas; es la base para el análisis de retail.

## Fase 4 — Cargar a MAXI-POS

`catalogo/catalogo.json` ya tiene la forma de la plantilla del mockup:
familia, marca, sinónimos, atributos que crean variante vs. describen, checklist, fotos, molde de
descripción, y por variante: operaciones, préstamo (p25/mediana/p75), % desempeña, % refrenda,
% remate, DROP. Regla del mockup: con 5+ operaciones propias el sugerido toma el historial; si no, la regla.

## Lo que la gente verá (ejemplo)

> **Celulares** · 2,500 empeños · préstamo mediano $X · 6 de cada 10 desempeñan, 4 refrendan al menos
> una vez, 3 se rematan.

Las cifras reales están en `reportes/cobertura.md` y `reportes/plantillas.csv`.
