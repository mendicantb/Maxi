# Notas: plantillas de herramientas

Archivos (categorías) en `catalogo/plantillas/`:

| Archivo | Categoría | Plantillas | Qué cubre |
|---|---|---:|---|
| `herramientas_electricas.yaml` | Herramienta eléctrica | 19 | demoledor, rotomartillo, taladros, atornillador/impacto, esmeriladoras, rectificadora, sierras (circular, caladora, ingletadora, tronzadora), cepillo, lijadora, router, pistola de calor, soldadora |
| `herramientas_jardin_motor.yaml` | Herramienta de jardín y motor | 14 | motosierra, desbrozadoras (gasolina / eléctrica), sopladora, aspersora, motobomba, bailarina, generador, hidrolavadora, compresor, bombas, motor eléctrico, vibrador |
| `herramientas_manuales.yaml` | Herramienta manual y de obra | 17 | gato, carretilla, escalera, báscula, nivel, dados/matracas, llaves, pinzas/cizallas, desarmadores, martillos, palas/picos, albañilería, serrucho, especializada |
| `herramientas_varias.yaml` | Herramienta varia (sin identificar) | 4 | genéricas (`generica: true`, `solo_familia: true`): eléctrica, sierra, motor, manual |

Las genéricas van en un archivo propio, que ordena al final, y no al final de cada archivo. Las familias PRENDA FLEX
mezcladas (HERRAMIENTA LIGERA, ALBAÑILERIA, MANUALES, MECANICO, INDUSTRIAL) están listadas en los 4 archivos.
El motor busca por familia en orden alfabético de archivo, así que una genérica dentro de `electricas` le quitaría
prendas a las plantillas específicas de `jardin_motor` y `manuales`.

## Cobertura (todo el alcance junto, 2,149 prendas)

- Cubiertas 99.2%, específicas 98.2%, préstamo cubierto 99.3%.
- Sin plantilla: 17 prendas, que son celulares, relojes, licuadoras y cuchillos capturados en familias de herramienta.
  Les tocan las plantillas de otros agentes por el paso "otra_familia".
- `--probar` por archivo da cifras bajas porque cada archivo cubre sólo una parte de las familias mezcladas.
  Hay que correr la prueba con los 4 archivos juntos.

## Variantes (crea_variante: true)

- `gama` (Alta / Media / Básica), por marca con sus faltas de ortografía. Aplica en eléctricas y jardín/motor.
  - Alta: DeWalt, Makita, Bosch, Milwaukee, Hilti, Stihl, Husqvarna, Kärcher, Lincoln, Ridgid, Honda.
  - Media: Truper, Urrea, Black+Decker, Skil, Ryobi, Koblenz, Stanley, Craftsman, Total, Ingco, Husky, Kinro, Oakland.
  - Básica: Pretul, genéricas y toda marca no listada, incluida la prenda sin marca.
- `alimentacion` (Con batería / Eléctrico con cable) en rotomartillo y esmeriladora angular.
- `tipo` (Inversora / Convencional) en soldadora.
- Litros en compresor.
- Tonelaje en gato.

## Hallazgos y dudas

1. Las familias están muy desordenadas. Hay rotomartillos en TALADRO y HERRAMIENTA LIGERA, esmeriladoras y rectificadoras en PULIDOR y RECTIFICADORA,
   motosierras en DESBROZADORA, y celulares, relojes y licuadoras en CEPILLO DE MANO, CALADORAS, LIJADORAS y TALADRO INALAMBRICO.
2. RECTIFICADORA y PULIDOR casi siempre son esmeriladoras angulares. Las mandé a "Esmeriladora angular 4 1/2" por modelo (GWS, DWE4xx, G650, 6130…).
   "Rectificadora / minipulidora recta" quedó sólo para lo que no tiene ese indicio. Faltan "Esmeriladora 7"-9"" y "Esmeril de banco" con volumen propio.
3. La marca llega vacía o "SN" en muchas prendas, y con faltas: STHIL, DEWAL, TRUPPER, BOSH. La gama se calcula con las faltas conocidas.
   Si la marca no se reconoce, la gama queda en "Básica" y no en un valor desconocido. Esto puede subestimar equipos buenos con marca mal escrita.
4. Tonelaje del gato y litros del compresor: cuando falta el dato queda "N/D". Conviene que la evaluadora lo capture.
   El gato no distingue botella, patín y tijera como variante, sólo como atributo `tipo`.
5. Los lotes de herramientas ("2 marros, un martillo, un nivel…") se detectan con 3 o más nombres de herramienta en la descripción.
   Caen en "Maletín / lote de herramientas varias", pero no se pueden cotizar por pieza.
6. PIN *** en las descripciones es la palabra PINZA censurada. Se trata como pinzas / alicates.
7. Criterio de plantillas manuales: no se separó Pretul de Truper dentro de plantillas manuales (martillos, llaves…), sólo `gama` no variante.
8. Desbrozadora a gasolina: la cilindrada (cc) casi nunca se captura, por eso es atributo y no variante.
   La marca (Stihl FS vs Kinro/Husky) ya se refleja en la gama.
9. Efecto secundario: al explorar corrí una vez `python3 scripts/plantillas.py --help`. El script ignora argumentos desconocidos y sí escribió
   `reportes/*`, `data/processed/prendas_clasificadas.csv`, `catalogo/catalogo.json` y una fila en `reportes/historial/cobertura.csv`
   (con sólo celulares.yaml, ~0.7% de cobertura). Se regeneran al correr `python3 scripts/plantillas.py`.
   La fila del historial es la única que conviene borrar a mano.
