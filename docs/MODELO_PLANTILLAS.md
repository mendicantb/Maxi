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
- **Objeto propio vs genérico por gama.** Un artículo es **objeto propio** (`iPhone 15 Pro Max`,
  `Truper ROTO-1/2A7`, `DeWalt DCD776`) sólo cuando junta **5+ empeños** con marca reconocida y modelo.
  Mientras no, cae en el **objeto genérico de su plantilla y gama**: `Rotomartillo · gama alta`,
  `Celulares · gama media`, `Lavadora · gama básica`. Así la evaluadora siempre tiene historial con qué cotizar,
  aunque sea una marca china o un modelo que nunca ha visto. Cuando un modelo llega a 5 empeños, se promueve.
- La **gama** sale de la marca (`catalogo/marcas/*.yaml`, formato en `docs/FORMATO_MARCAS.md`):
  alta = profesional / premium (DeWalt, Makita, Milwaukee, Stihl, Apple, LG…), media = marca conocida
  doméstica (Truper, Black+Decker, Mirage…), básica = económica, china o sin marca. En celulares, tablets y
  motos la gama va por modelo (iPhone 15 Pro = alta, Moto G24 = básica).

## Dos tipos de plantilla

1. **Plantilla por modelo** — la marca y el modelo comercial importan mucho para el precio.
   Celulares, Tablets, Motos, Autos y camionetas, Videojuegos, Relojes.
   El catálogo ya trae los objetos limpios (nombres comerciales, sinónimos, códigos de modelo).
2. **Plantilla por tipo de artículo** — el tipo pesa más que el modelo exacto.
   Lavadora, Licuadora, Rotomartillo, Tanque de gas, Ventilador, Bocina… (todo lo "general").
   Los objetos propios salen de marca + modelo capturados, ya unificados (`ROTO12A7` = `RROTO12A7` =
   `ROTO-1/2A7`).

## Cuánto hay (corte 4-oct-2026, sin joyería)

- **228 plantillas**: 6 por modelo + 222 de artículo general, en 31 categorías.
- **274 objetos propios** (5+ empeños) que juntan el **42 %** de los empeños.
- **408 objetos genéricos por gama** para el resto. Marca reconocida en el **84 %** de las prendas.
- **977 variantes**. **486 candidatos por promover** (2–4 empeños, hoja *Por promover*).

La gama sí separa el préstamo (mediana):

| Genérico | Alta | Media | Básica |
|---|---:|---:|---:|
| Celulares | $2,100 | $1,000 | $800 |
| Rotomartillo | $800 | $350 | $350 |
| Desbrozadora a gasolina | $2,200 | $1,500 | $1,000 |
| Lavadora | $1,800 | $1,500 | $1,500 |

Donde no separa (esmeriladora: Truper y Pretul se prestan igual) la gama sólo informa; el precio lo da el historial.

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

- `reportes/maxi_pos_plantillas.xlsx` — hojas **Plantillas** (campos, checklist, fotos), **Objetos**
  (propios y genéricos por gama, con las marcas que caen en cada genérico), **Variantes** y **Por promover**, cada una con préstamo, % desempeña / refrenda / remate, venta y días en vitrina.
- `catalogo/maxi_pos.json` — lo mismo para cargar a MAXI-POS.
- Las reglas viven en `catalogo/plantillas/*.yaml` y las marcas/gamas en `catalogo/marcas/*.yaml`; `scripts/exportar_maxi.py` arma el modelo.

## Decisiones tomadas

- Joyería (oro y plata) no usa objetos (se cotiza por peso y kilataje): queda fuera de este export.
- Se aceptan pistolas de balines / salva (plantilla en Deportes y recreación).
- Salida: A ≤30 días en vitrina, B ≤90, C >90.
