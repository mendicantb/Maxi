# Notas: plantillas de vehículos, varios e inmuebles

Archivos (en `catalogo/plantillas/`): `vehiculos_motos`, `vehiculos_autos`, `vehiculos_bicicletas`, `vehiculos_accesorios`,
`varios_bebes_juguetes`, `varios_cascos`, `varios_navajas`, `varios_otros`, `varios_deportes`, `varios_ropa_accesorios`,
`inmuebles_casas`, `inmuebles_terrenos`, `inmuebles_sin_garantia`. Total: **115 plantillas**.
Todas llevan `solo_familia: true` salvo Victorinox, Leatherman y Transformers (existen mal capturados en otras familias).
Sin eso las regex de vehículos/navajas/cascos se llevaban prendas de herramientas, celulares y oro (se probó: 700 falsos positivos).

## Cobertura (sin compras; medida con las plantillas de estos archivos)

| Alcance | Prendas | Cubiertas | Específicas | Préstamo cubierto |
|---|---:|---:|---:|---:|
| Vehículos (MOTOCICLETA, POCHIMOVIL, AUTOMOVIL, CAMION, CAMIONETA, BICICLETAS) | 279 | 98.6% | 84.2% | 99.9% |
| Motos y motocarros (MOTOCICLETA+POCHIMOVIL+CAMION) | 127 | 98.4% | 83.5% | 77% (falta el tractor, $279k) |
| Autos y camionetas | 16 | 87.5% (2 no son autos) | 87.5% | 98% |
| Bicicletas | 140 | 97.1% | 82.1% | 97.5% |
| TRICICLO + JUGUETERIA | 61 | 95% (los 3 restantes son navaja/sandalias que cubren otros archivos) | 95% | 99% |
| CASCOS / NAVAJAS | 25 / 4 | 100% / 100% | 84% / 75% | 100% |
| Inmuebles (CASA, TERRENO, LOTE) | 19 | 100% | 100% | 100% |
| SIN GARANTÍA | 20 | 95% | 0% (genérica a propósito) | 99.5% |
| VARIOS | 665 | 44.5% (296) | 39% (261) | 49% |

El 55% de VARIOS que queda sin plantilla **no es de este alcance** (ver abajo).

## Qué hay realmente en VARIOS (780 filas; 115 son compras, 665 empeños)

Cubierto aquí (296): ~97 navajas (casi todas Victorinox, 11 Leatherman), ~49 cascos, ~29 escaleras Truper, ~20 hieleras Igloo/Coleman,
~18 hamacas, ~17 bicicletas/triciclos, ~14 ropa/sandalias/mochilas, ~13 bebés/juguetes, ~17 deportes (8 pistolas de balines/salva, caminadoras, trampolín),
4 llantas/refacciones de pochimóvil, médicos (silla de ruedas, andadera, nebulizador), 2 cajas registradoras, 1 terreno ejidal, perfumes.

**Pertenece a otras categorías (~360 prendas, 54% de VARIOS)** — no se hicieron plantillas, el motor las cruza por texto:
- Herramientas (~132): ~40 manuales de albañilería (pico, pala, barreta, marro, martillo, cuchara, llana), ~23 esmeriladoras/caladoras/lijadoras/tronzadoras/cortadoras/clavadoras/pistolas de impacto,
  ~20 compresores/bombas/generadores/fumigadoras, ~16 niveles/cintas/multímetros/extensiones, ~15 juegos de llaves/dados/pericas/desarmadores, ~13 gatos hidráulicos/diablitos/carretillas, ~5 soldadoras.
- Electrodomésticos/hogar (~135): ~33 trastes (ollas, toppers, vasos), ~26 licuadoras/batidoras/exprimidores, ~23 hornos/microondas/freidoras/sandwicheras/wafleras, ~20 aspiradoras/ventiladores/clima/planchas/máq. de coser,
  ~20 muebles (mesas, sillas, camas, roperos, lámparas), ~10 tanques de gas, ~3 básculas.
- Electrónica/audio/cómputo (~82): ~17 radios Baofeng/Steren, ~10 bocinas/micrófonos/audífonos, ~10 luces DJ/reflectores, ~7 guitarras/teclados/piano, ~12 reguladores/nobreak/inversores,
  ~20 impresora/router/disco duro/pantalla/power bank/Alexa/cámaras/Roku, ~6 consolas y controles (Xbox, PS5, Nintendo).
- Belleza/cuidado personal (~9, ver duda 4), relojes/smartwatch 3, celulares 1 (Motorola).
- No identificadas (~7): "SISAYA", "MAGERAL 1", "BREI", "TUMBA BURROS" (x2), "CARBA OLLO"/"SELLA" (x3 c/u, posible silla/cabaollo).

## Hallazgos de calidad de captura

1. **VARIOS es 54% otras categorías** (herramientas, hogar, audio). Además las familias propias existen (HERRAMIENTA LIGERA, LICUADORA, BOCINAS…), así que la evaluadora usa VARIOS por pereza o duda.
2. **Cascos y navajas**: la familia CASCOS tiene 28 y NAVAJAS 4, pero hay ~49 cascos y ~97 navajas en VARIOS (y 3 Victorinox en HERRAMIENTA LIGERA, 1 en TRICICLO). TRICICLO también trae sandalias y navaja.
3. **COLECCIONABLES** son 6 celulares Motorola Moto G05 + 1 Moto G22 + una caja de dinero (no hay coleccionables reales). **AUTOS** = una bocina XDOBO. **SIN GARANTÍA** trae una soldadora Husky. **NIVELES** trae hamacas (mezclas con niveles de albañil).
4. **Motos**: el modelo casi no se captura; 39 de 125 son "Italika + año" o "Italika 150" y 64 no traen año (variante "?"). FT1780 se tomó como FT180 (typo). "D125" y "125Z/150Z/200Z" son modelos Italika; "Piaggio 2023/2024" (18 pochimóviles) tiene préstamos de $1,000 a $45,000: seguramente hay Ape de pasaje y de carga mezclados y falta capturar modelo.
   En POCHIMOVIL entran Italika AT110/GS150/150 que son motos, no motocarros.
5. **Autos**: sólo 16 prendas y casi nunca dicen modelo ("VOLKSWAGEN 2015", "DOG 2012" = Dodge, "NISSAN 2002 NATS01"); hay una plantilla por marca y el año crea la variante. Hay 2 tractores Massey Ferguson MF-2625 ($129k-$150k, los préstamos más altos del grupo) en la familia CAMION.
6. **Inmuebles**: el texto no dice casa/terreno/lote (Marca y Modelo vienen vacíos). Solo la familia PF lo distingue, por eso hay un archivo por familia (el motor prueba primero las plantillas de la familia). 27 de 39 registros tienen "0", "SN" o "SIN GARANTIA" en superficie/construcción. Hay terrenos con 3 recámaras y casas con construcción = superficie (1639.48/1639.48), datos inconsistentes.
7. **Compras**: 115 de las 780 prendas de VARIOS son compras (es_compra); la mayor parte de las hamacas y el volumen de algunos artículos viene de ahí.

## Dudas / decisiones para revisar

1. Muebles, trastes, lámparas y ropero se dejaron al agente de hogar (ya existen hogar_muebles/hogar_cocina); quedan sin plantilla en el motor completo ropero, taza de baño, frutero, lámparas, topers/cubiertos, etc.
2. Instrumentos musicales (guitarra/teclado/piano; familias ART. MUSICALES, GUITARRA, INSTRUMENTOS MUSICALES) y radios se asumen de electrónica/audio.
3. Pistolas de balines/salva/postas (8 prendas, plantilla `dep.pistola-balines`): confirmar con Dirección/legal que se aceptan; el checklist pide confirmar que NO sea arma de fuego.
4. Belleza/cuidado personal: lo cubre hogar_belleza (planchas de cabello, rasuradoras). Perfumes sí los hice yo (varios_ropa_accesorios); verificar que no choquen con hogar_belleza.
5. Escaleras (Truper, ~35) y hieleras (~20) se hicieron aquí, pero podrían solaparse con herramientas/hogar (las familias ESCALERAS y NEVERAS existen). Si otro agente las cubre, borrar `varios.escalera.*` y `varios.hielera` o dejarlos con prioridad por orden de archivo.
6. `NEVERAS` ambiguas: "NEVERA IGLOO/COLEMAN" es hielera; "7 PIES NEVERA" es refrigerador. La plantilla de hielera excluye "PIES/REFRIGERADOR".
7. Variante "con casita" del triciclo infantil: sólo 28 de 55 dicen casita/lona; el resto queda variante "?".
8. Marcas: se cubrió ITALICA/ITALKA/ITALIKA, VICTORINO/VICTRINO/VOICTOPRINOX, BICLETA/BOICICLETA/BIBLETA, TRICILO/TRCICLO/TRICICLIO, TRANSFORMERS, CAMINADRA; faltan modelos que aún no aparecen en el histórico (Honda, Bajaj, TVS…, tienen plantilla pero 0 o 1 prenda).

## Cómo probar

`python3 scripts/plantillas.py --probar catalogo/plantillas/<archivo>.yaml` solo prueba contra las familias PF del archivo. Los varios_* incluyen VARIOS
en sus familias, así que su cobertura individual sale diluida (poca de VARIOS es de ese archivo): usar el corte por familia de la tabla de arriba.

## Resultado con TODAS las categorías cargadas (motor completo, sin escribir reportes)

- 33 archivos / 644 plantillas. VARIOS: **85.6%** cubierto (665 empeños); ~95 prendas siguen sin plantilla (diablitos, radios Baofeng/Steren, cámaras, reflectores/luces DJ, extensiones, cintas de topografía, generadores "GENERARDOR", licuadoras con typo, lámparas, teléfono de casa, power bank, panel solar, topers).
- Mis familias: 98-100% cubiertas; ninguna plantilla mía atrapa prendas de otras familias (excepto los 3 Victorinox de HERRAMIENTA LIGERA, a propósito).
- Las únicas prendas de mis familias que caen en plantillas ajenas son las que no son mías: bocina XDOBO (AUTOS) y Kaiser (BICICLETAS) -> Audio; 7 Motorola (COLECCIONABLES) -> Celulares.
- **Falsos positivos de otros agentes sobre VARIOS (revisar):** `oro.juego` se llevó 8 "JUEGO DE ... VASOS/JARRAS/TAZAS", `oro.cadena` un polipasto "con cadena gruesa",
  `oro.dije` una máquina de corte de cabello, `oro.reloj` un reloj inteligente (debería ir a Relojes). La joyería debería exigir ORO/PLATA/KILATES o marcar `solo_familia: true`.
