# Plantilla › Objeto › Variante — cómo queda MAXI

## Los 4 niveles

| Nivel | Qué es | Ejemplo celular | Ejemplo moto | Ejemplo general |
|---|---|---|---|---|
| **Categoría** | Agrupa para navegar y reportar | Electrónica | Vehículos | Hogar - Línea blanca |
| **Plantilla** | El *formulario*: qué campos se capturan, checklist, fotos, molde de descripción | **Celulares** | **Motos** | **Lavadora** |
| **Objeto** | El artículo concreto que se busca y se cotiza | **iPhone 15**, iPhone 16, Galaxy A14 | **Italika FT150**, Italika DM150 | **Mabe LMDX3123**, Mirage LMS013M |
| **Variante** | La combinación que cambia el precio | iPhone 15 · 128 GB | FT150 · 2021 | (casi nunca: el modelo ya fija los kilos) |

- **Celulares es una plantilla**, no un objeto: define que todo celular lleva marca, modelo, capacidad, color,
  IMEI, checklist (enciende, cuenta cerrada…) y fotos.
- **iPhone 15 y iPhone 16 son objetos distintos** que usan la misma plantilla. Cada uno tiene su historial.
- **Variante = sólo lo que mueve el precio.** En celulares: capacidad (128/256 GB). El **color es un atributo
  descriptivo**: se captura y sale en la descripción, pero no crea otro precio. Si mañana el negro se vende más
  caro que el rosa, se cambia a `crea_variante: true` y listo.
- Regla de precio (mockup): un objeto o variante con **5+ empeños propios** sugiere con su historial; con menos,
  usa la regla de la plantilla.

## Dos tipos de plantilla

1. **Plantilla por modelo** — la marca y el modelo comercial importan mucho para el precio.
   Celulares, Tablets, Motos, Autos y camionetas, Videojuegos, Relojes.
   El catálogo ya trae los objetos limpios (nombres comerciales, sinónimos, códigos de modelo).
2. **Plantilla por tipo de artículo** — el tipo pesa más que el modelo exacto.
   Lavadora, Licuadora, Rotomartillo, Tanque de gas, Ventilador, Bocina… (todo lo "general").
   Los objetos se **proponen** a partir de la marca y modelo que capturó la evaluadora
   (`Truper ROTO12A7`, `Mabe LMDX3123PBADO`). Vienen con faltas de captura (`ROTO12A7` / `RROTO12A7`):
   hay que depurarlos antes de cargarlos.

## Cuánto hay (corte 4-oct-2026, sin joyería)

- **228 plantillas**: 6 por modelo + 222 de artículo general, en 31 categorías.
- **3,116 objetos** propuestos; **352 con 5+ empeños** (ya pueden sugerir precio con historial).
  El resto es cola larga de 1–4 empeños: se cotizan con la regla de su plantilla.
- **3,307 variantes**.

| Plantilla | Objetos | Con historial (5+) | Empeños |
|---|---:|---:|---:|
| Celulares | 253 | 139 | 2,504 |
| Motos | 31 | 10 | 125 |
| Tablets | 21 | 9 | 96 |
| Relojes | 17 | 11 | 146 |
| Esmeriladora angular 4 ½ | 117 | 16 | 286 |
| Rotomartillo | 112 | 8 | 223 |
| Desbrozadora a gasolina | 61 | 10 | 174 |
| Lavadora | 53 | 6 | 141 |

## Plantilla Motos

- **Campos**: marca, modelo (objeto), **año (crea variante)**, cilindrada, color, placas, NIV, núm. de motor, km, llaves.
- **Checklist**: factura, tarjeta de circulación, placas, NIV coincide, REPUVE, sin adeudos, arranca, llaves,
  luces, llantas y frenos, carrocería, tablero.
- **Fotos**: lados, frente, trasera, tablero, NIV, motor, placa, tarjeta, factura.
- **Objetos con más historial**: Piaggio Ape (pochimóvil) 18 · Italika ZW150 9 · Italika FT150 8 ·
  Italika D125 7 · Italika AT125 6 · Italika Serie Z 5 · Dinamo 5 · Veloci 5.
- **Hueco**: 64 de 125 motos no traen año y 19 dicen sólo "Italika", así que las variantes por año casi no
  tienen datos todavía. En MAXI-POS el año y el modelo deben ser obligatorios.
- Historial: desempeña 78 %, se remata 12 %, venta mediana $14,750 (≈1.4× el préstamo), 86 días en vitrina.

## Dónde está todo

- `reportes/maxi_pos_plantillas.xlsx` — hojas **Plantillas** (campos, checklist, fotos), **Objetos** y
  **Variantes**, cada una con préstamo, % desempeña / refrenda / remate, venta y días en vitrina.
- `catalogo/maxi_pos.json` — lo mismo para cargar a MAXI-POS.
- Las reglas viven en `catalogo/plantillas/*.yaml`; `scripts/exportar_maxi.py` arma el modelo.

## Decisiones tomadas

- Joyería (oro y plata) no usa objetos (se cotiza por peso y kilataje): queda fuera de este export.
- Se aceptan pistolas de balines / salva (plantilla en Deportes y recreación).
- Salida: A ≤30 días en vitrina, B ≤90, C >90.
