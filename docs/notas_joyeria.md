# Notas de plantillas: joyería (oro, plata) y relojes

Archivos: `catalogo/plantillas/joyeria_oro.yaml`, `joyeria_plata.yaml`, `relojes.yaml`.
Los dos de joyería se generaron con la misma estructura (mismas plantillas (oro suma "Reloj de oro"), mismo orden); sólo cambian atributos de metal y genérica.

## Cobertura (prueba con `scripts/plantillas.py --probar`)
| Archivo | Plantillas | Cubiertas | Específicas | Préstamo cubierto |
|---|---|---|---|---|
| joyeria_oro | 16 | 99.7% | 99.0% | 99.0% |
| joyeria_plata | 15 | 99.8% | 99.5% | 99.9% |
| relojes | 17 | 100% | 73.1% | 100% |

(Base: prendas sin `es_compra`: oro 960, plata 880, relojes 130.)
Lo que queda sin plantilla en oro/plata no es joyería: "SIN GARANTIA ...", "COMPLEMENTO DE CONTRA 4299 Y 4298" (ajustes de contrato capturados como prenda; ahí está el préstamo no cubierto del oro).

## Regla de pieza principal (orden de evaluación)
1. **Juego / Conjunto** si dice JUEGO/CONJUNTO.
2. **Lote de varias piezas** si aparecen 2 o más TIPOS distintos entre: anillo, aretes (broquel/arracada/argolla cuentan como uno), pulso/esclava/brazalete, cadena, collar/gargantilla; o palabras "VARIAS/VARIADO/SET". Dije NO cuenta como tipo: "CADENA CON DIJE" es Cadena. Un lote se cotiza por peso total y conteo, no por pieza.
3. Argollas de matrimonio (ARGOLLA + MATRIMONIO/BODA, ALIANZA), Monedas, Lingote/chatarra, Reloj de oro (sólo oro).
4. Pieza única por palabra: Anillo > Broqueles > Aretes/Arracadas > Argollas (aretes de aro) > Esclava > Pulso/Pulsera > Gargantilla/Collar > Cadena > Dije.
5. **El portador manda**: si hay cadena/pulso y dije, la plantilla es la cadena/pulso (el dije es descriptivo). Dije sólo si no hay portador. "PULSO DE PLACA", "PULSO TIPO ROLEX" son Pulso.
6. Genérica: contiene ORO/K/10K (oro) o PLATA/925 (plata) sin tipo de pieza.
La pieza no se decide por la primera mencionada sino por la jerarquía de arriba (más estable con las faltas de ortografía); en la práctica coincide casi siempre.
Atributos: kilataje (oro) y ley 925/950/999 (plata) son `crea_variante: true`; tejido, peso_g, piedra, color_oro/color_plata y condición son descriptivos.

## Decisiones
- "ARGOLLAS" sin más es **aretes de aro** (en esta casa casi todas lo son); sólo es "Argollas de matrimonio" con MATRIMONIO/BODA/ALIANZA. "COMPROMISO" va a Anillo.
- Esclava es plantilla propia (pocos casos) y no se mezcla con Pulso, aunque en el lote cuenta como pulso.
- Relojes: plantillas por marca con volumen (Rolex 18, Fossil 11, Casio 6, Rado 6, Invicta 5, Orient 5, Huawei 5, Michael Kors 4, Tag Heuer 2); smartwatch genérico, Apple Watch y Samsung incluidos aunque con poco volumen. Rolex NO se separa en original/réplica: sólo existe el atributo descriptivo `autenticidad` si la evaluadora escribió REPLICA/CLON/ORIGINAL. "Orient clon" va en la plantilla Orient.
- Hay variante "?" (sin kilataje) en ~40-50% de oro: la evaluadora no siempre lo anota; el POS debe pedirlo.

## Tejidos encontrados (descripciones)
ESLABON (con variantes ESLABOM/ESLAVON, el más común, >320 menciones oro+plata), CUADRO, TORZAL/TORSAL, CARTIER, FIGARO, BISMARCK, CUBANA/CUBANO, BARBADA, CLEOPATRA, ROLO, LAZO, SINGAPUR, VENECIANA, CLABES, ESCALERITAS, GUCCI, COCODRILO, ENTRELAZADO, TRENZADO, BOLITAS, PLACA, LISO, ESPIRAL, ROSARIO (plata). Colores de oro: TRES OROS, DOS OROS, ORO ROSA/ROJO, BICOLOR.

## Pesos típicos (gramos netos, remates.csv, mediana [P25-P75])
Oro: anillo 1.9 [1.3-2.9], aretes 1.1 [0.45-2.5], argollas 1.9 [1.5-2.6], cadena 3.7 [2.3-8.6], pulso 4.9 [3.3-10.6], dije 1.1 [0.6-1.9].
Plata: anillo 11 [6.5-28], aretes 7.7 [3.5-13], argollas 4.0 [3.8-7.2], cadena 15 [10-26], pulso 8.2 [5.1-17], dije 10.9 [7-12].
(Clasificación aproximada por palabra en la descripción del remate; sólo piezas con P. Neto > 0.)

## Dudas
1. Complementos de contrato y "SIN GARANTIA" caen en familia ORO: ¿se filtran por proceso o se crea plantilla "Ajuste/complemento"?
2. Lote en plata es 19% de las prendas (171 de 880): ¿cotizar por peso total con una sola variante o exigir desglose por pieza?
3. Kilataje faltante: ¿obligatorio en el POS?
4. Oro: "RELOJ DE 14K" (8 piezas) tiene su plantilla; ¿se separa reloj de bolsillo?
5. Réplica/original de Rolex y Rado no se puede inferir de la descripción.
