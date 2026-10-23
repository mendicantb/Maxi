# Notas: plantillas de electrónica

Archivos: `catalogo/plantillas/electronica_{pantallas,audio,computo,videojuegos,musica}.yaml` (59 plantillas).

| Archivo | Prendas | Cubiertas | Específicas | Préstamo cubierto |
|---|---|---|---|---|
| pantallas (PANTALLAS, MONITOR, PROYECTORES, DVD´S) | 377 | 99.7% | 93.6% | 100% |
| audio (bocinas, AUDIO, AUDICULARES, MINI COPONENTE, ESTEREO DE AUTO) | 540 | 99.4% | 99.3% | 99.8% |
| computo (LAPTOP, COMPUTO, IMPRESORA, ROUTER, REGULADORES) | 166 | 99.4% | 99.4% | 99.7% |
| videojuegos | 33 | 100% | 100% | 100% |
| musica (ART. MUSICALES, INSTRUMENTOS, BAJO ELECTRICO, GUITARRA) | 36 | 100% | 100% | 100% |

## Hallazgos / dudas
1. Las familias de bocinas (PORTATILES / DE PISO / AMPLIFICADAS) están mezcladas (JBL Flip en "amplificadas", bicicletas en "amplificadas"). Se clasificó por el artículo, no por la familia: JBL (Flip/Charge/Partybox/otras), Sony, Alexa/Echo, barra de sonido, "de piso/amplificada" (Kaiser, HKPRO, LG Xboom, micrófono, tripié, luces) y "portátil genérica". La frontera portátil vs piso es heurística (palabras GRANDE/PISO/TRIPIE/MICROFONO/marcas Kaiser).
2. La familia ROUTER de PRENDA FLEX son fresadoras de carpintería (Makita, DeWalt, Bosch), no routers de red. Se creó `elec.router.carpinteria`; probablemente deban pasar a Herramientas. También hay un rotomartillo en REGULADORES, bicicletas en bocinas y una plancha en PANTALLAS (quedan sin plantilla o como otra_familia).
3. Pantallas: la diferencia Smart vs no Smart casi no se captura (evaluadoras escriben "pantalla ... con control"). Hay 164 Smart y 166 "LED/LCD" por palabras clave; el LED/LCD en realidad es "sin dato". Se podría fusionar en una sola plantilla "Pantalla TV" con variante por pulgadas. Pulgadas se saca del texto o del modelo (HKP43R03, 32A4KV); ~20 pantallas quedan con variante "?" por no traer medida.
4. Laptops: procesador/RAM/disco casi nunca se captura de forma consistente (y a veces "477 GB", "930 GB"), por eso la variante es solo por marca (HP, Lenovo, Acer, Asus, Dell, MacBook, Chromebook, Gamer, Otras) y el procesador es atributo descriptivo (`crea_variante: false`). Sugerencia: pedir en el POS campos RAM/almacenamiento/procesador al capturar.
5. Duplicación intencional: mezcladora/DJ existe en audio (familia AUDIO) y en música (ART. MUSICALES) con ids distintos; no hay choque porque cada familia busca primero en su categoría. Consolas: variante solo en Xbox One (S/X) y Series (S/X); PS4/PS5/Switch sin variante (versión Slim/Pro/OLED rara vez se anota). Muchas bocinas y audífonos son marcas chinas sin modelo, por eso las plantillas por marca se agrupan en "portátil Bluetooth (otras marcas)".
