# Notas: plantillas de CELULARES y TABLETS

Archivos: `catalogo/plantillas/celulares.yaml` (274 plantillas, 19 genéricas) y `catalogo/plantillas/tablets.yaml` (23 plantillas, 4 genéricas).
Prueba: `python3 scripts/plantillas.py --probar catalogo/plantillas/<archivo>.yaml` (excluye compras, `es_compra`).

## Cobertura final

| Archivo | Prendas | Cubiertas | En plantilla específica | Préstamo cubierto |
|---|---|---|---|---|
| celulares.yaml | 2,501 | 99.6% | 93.5% | 99.8% |
| tablets.yaml | 99 | 97.0% | 79.8% | 99.2% |

Lo que queda sin plantilla:
- Celulares (11 prendas): 2 tablets Huawei AGR-W09 capturadas como celular (el motor las manda a `tablets.yaml` en la segunda pasada, `otra_familia`), y basura capturada como celular (bicicleta, triciclo, plancha, reloj smart, "Naomicase", "X Tigi F18A", "Power SM").
- Tablets (3 prendas): 2 taladros DeWalt DWD024 capturados como tablet y 1 prenda "COLOR GRIS L.P20KG SERIE15222" sin marca ni modelo. Se corrigen en la captura, no con plantilla.

## Cómo está armado (para la evaluadora y para quien mantenga el YAML)

1. **Orden**: primero todas las específicas (por marca), luego todas las genéricas. El archivo se ordena así a propósito: una genérica de una marca no debe ganarle a una específica de otra (pasó con Honor y los códigos `...-LX3`, que Huawei también usa).
2. **Guardia de marca** `^(?=.*MARCA)`: los tokens cortos (A14, A54, G24, E13, Y01, C55, X6...) son ambiguos entre marcas (Samsung A54 / Oppo A54 / ZTE Blade A54; Redmi A3 / Samsung A3...). Cada token corto sólo cuenta si en el texto aparece la marca (con sus faltas de ortografía: `SAMNSUNG`, `SANSUNG`, `MOTORLA`, `MNOTOROLA`, `XIAMOI`, `XIOMI`, `APPO`, `APPPO`, `BALDE`/`BLANDE`/`BLDE` para Blade, etc.). Los códigos largos y únicos (`SM-A145M`, `XT2423`, `CPH2577`, `23100RN82L`) no llevan guardia.
3. **Números sin pegarse**: todos los tokens llevan `(?<![A-Z0-9])` antes y `(?![A-Z0-9])` o `(?![0-9])` después, así "A14" no gana a "A145M" ni a números de serie. Las variantes con sufijo (A03s, A04s, A05s, A10s, A10e, A52s, Moto G04s, Redmi A3x, E22i...) van ANTES del modelo base.
4. **Tablets en celulares**: `excluir` de la categoría Celulares (`TABLET`, `IPAD`, `MATEPAD`, `GALAXY TAB`) para que caigan a `tablets.yaml`.
5. **Genéricas**: todas llevan `solo_familia: true` para que no "chupen" prendas de otras categorías en la segunda pasada (ej. "CEL" en un accesorio). Las específicas NO son `solo_familia`, así se detectan celulares capturados en otra familia (ver hallazgos).
6. **Atributos** (nivel categoría): `capacidad` (`formato: '{}GB'`, **crea variante**), `ram` (`'{}GB RAM'`, sólo descriptivo), `color` (sólo descriptivo, normalizado NEGRA->NEGRO...).
7. **Checklist / fotos / molde** se definen una vez en `defaults:` con anclas YAML (`&chk_android`, `*chk_android`...). El parser las expande, el motor no se entera. Si el cargador de MAXI-POS no usa un parser YAML estándar (que expanda anclas) hay que expandirlas al importar. `defaults:` es una clave extra que el motor ignora.

## Decisiones de agrupación (qué es "un artículo que se cotiza igual")

- Se agrupó por **modelo comercial**, no por código de hardware, salvo que el código distinga precio claramente.
- **Merges** deliberados (si se ve que el precio se separa, partir la plantilla):
  - Galaxy A04 + A04e (A045M / A042M); A01 + A01 Core; A14 4G (A145M) + 5G (A146M); A15 4G (A155M) + 5G (A156M); A16 4G/5G; A22 4G (A225F) + 5G (A226B); A13 4G/5G; A17 4G/5G.
  - Moto E22 + E22i; E32 + E32s; E7 Power + E7i Power; Redmi 13 (4G) agrupado aparte de 13C.
  - Honor X7a/b/c juntos; X5b con X5; X6b con X6b Plus; X6a con X6a Plus.
  - Oppo A6x/A60 juntos (2 prendas, "A6X" no está claro).
  - Huawei Y7 2018/2019 juntos; Poco M4 con M4 Pro.
- **Separados** a propósito: A03 / A03s / A03 Core, A05 / A05s, A10 / A10s / A10e, A52 / A52s, G04 / G04s, Redmi A3 / A3x, Redmi 9A / 9C / 9T.
- iPhone: se crearon 11 a 17 (base, Pro, Pro Max, Plus, mini, 16e) aunque varios tienen 0 prendas hoy, porque son los de mayor préstamo (iPhone 15 Pro Max = $53k de préstamo con 6 prendas). Los Galaxy S20 a S25 también (S24 FE tiene 3).
- Plantillas que se descartaron por 0 prendas y bajo valor: Galaxy A31, A51, A71, Moto G Power, Vivo Y20.

## Códigos de modelo mapeados y confianza

Alta = el código aparece en los datos junto al nombre comercial escrito por la evaluadora, o lo conozco con seguridad.

| Código | Modelo | Confianza |
|---|---|---|
| SM-A145M / A146M | Galaxy A14 (4G / 5G) | Alta |
| SM-A045M, A042M, A047M | A04, A04e, A04s | Alta |
| SM-A055M, A057M/F | A05, A05s | Alta |
| SM-A065M, A075M | A06, A07 | Alta |
| SM-A035M, A037M, A032M | A03, A03s, A03 Core | Alta |
| SM-A155M/A156M, A165M/A166M, A175F/A176B | A15, A16, A17 | Alta |
| SM-A115M, A125/A127M, A135M, A225/A226, A235M, A245M, A256E, A325M, A346M, A356E, A366E, A525M, A528B, A546E | A11, A12, A13, A22, A23, A24, A25, A32, A34, A35, A36, A52, A52s, A54 | Alta |
| SM-A013M, A022M/G, A105M, A102U, A107M, A207M | A01 Core, A02, A10, A10e, A10s, A20s | Alta (A102U = A10e es de EE.UU., aparece en los datos como "A10E") |
| SM-S721B | S24 FE | Alta |
| SM-G532M | Galaxy J2 Prime | Media |
| SM-J410G, J250M, J810M | J4 (Core), J2 Pro, J8 | Media |
| SM-X200, X205 / X110 / X210 | Tab A8 / Tab A9 / Tab A9+ | Alta (X210 = A9+ aunque la evaluadora escriba "A9") |
| SM-T290, SM-X620 | Tab A 8.0 (2019), Tab S10 FE | Media / Media |
| XT2423 | Moto G24 | Alta |
| XT2231 / XT2233 / XT2235 | G22 / G42 / G32 | Alta |
| XT2341, XT2333, XT2335, XT2343, XT2347, XT2255, XT2237, XT2433, XT2521, XT2523 | G14, G23, G53, G54, G84, G72, G73, G35, G15, G05 | Alta |
| XT2345 | Moto E13 | Alta |
| XT2155, XT2159, XT2239, XT2229 | E20, E40, E22/E22i, E32s | Alta |
| XT2128, XT2133, XT2091, XT2055, XT2113 | G20, G60, G9 Power, G8 Power Lite, One 5G Ace | Alta |
| XT2535 | Moto G06 | Media (6 prendas con sólo el código; G06 con nombre aparece 12 veces) |
| XT2421 | G04 / G04s / E14 (¡ambiguo!) | Ver dudas. Ya hay nombre comercial en casi todas |
| XT2081 | Moto E7 Plus | Media |
| XT2097 | E7 Power / E7i Power | Media |
| XT2213 | Moto G 5G (2022) | Media |
| XT2245, XT2307, XT2503, XT2139, XT2413 | Edge 30 Neo, Edge 40 Neo, Edge 60 Fusion, Edge 20 Lite, G Play 2024 | Media |
| CPH2579, CPH2565, CPH2577, CPH2669, CPH2185, CPH2269, CPH2477, CPH2083, CPH2387 | Oppo A38, A78, A58, A40, A15, A16, A17, A12, A57 | Alta (los 6 primeros vistos con el nombre en los datos); A16/A12/A57 Media-Alta |
| CPH2363, CPH2365, CPH2205, CPH2599, CPH2699, CPH2531, CPH2557 | Reno 7, Reno 6, Reno 5 Lite, Reno 11, Reno 13/13F, Reno 10, A79 | Media-Alta |
| RMX3834 | Realme Note 50 | Media (26 prendas, sin nombre en los datos; mi memoria dice Note 50) |
| RMX3830, RMX3890, RMX3939, RMX3933, RMX3930 | Realme C51, C67, C63, Note 60, C61 | Alta (aparecen con nombre en los datos) |
| V2332, V2333, V2118, V2430, V2434, V2247, V2441, V2419, V2314, V2242 | Vivo Y03, Y18, Y01, Y04, Y29, Y36, V50 Lite, V40 Lite, V30 Lite, V25e | Alta / V2419 Media |
| V2028 | Vivo Y1s / Y1 (por confirmar) | Baja |
| 23100RN82L, 2409BRN2CL, 2312CRNCCL, 25028RN03L, 24044RN32L, 2212ARNC4L, 23053RN02L, 24049RN28L | Redmi 13C, 14C, A3, A5, A3x, 12C, 12, 13 | Alta |
| 23129RA5FL, 23117RA68G, 24117RN76L, 24116RACCG, 2303ERA42L, 23028RA60L, 2201117TL, M2101K7BL | Redmi Note 13, 13 Pro, 14, 14 Pro, 12S, 12, 11, 10S | Alta |
| 21061119AL, 220333QNY, 23026RN54G, M2006C3LG/LC, M2004J19G, 25062RN2DL, 25078RA3EL | Redmi 10, 10C, A2, 9A, 9C, 15, 15C | Media (9A/9C se mezclan en M2006C3x / M2004J19x) |
| 2410FPCC5G, 2310FPCA4G, 2207117BPG, 22071219CG, 2201117PG, 22041219PG, 23122PCD1G, 2312FPCAG | Poco C75, C65, M5s, M5, M4 Pro, M4, X6, M6 Pro | Alta / Media |
| Z2350, Z2356, Z2466, Z2450, Z2473, Z2467, A7030, A7050, A7040, 7060, 9046, ZTE 8050 | Axon 60 Lite, Axon 60, Blade A35e, A55, A56, V70, A71, V41, A54, V50 Smart, V40 Pro, Axon 50 Lite | Alta; A7040 y 8050 Media |
| WDY-LX3, JDY-LX3, VNE-LX3, VNA-LX3, WOD-LX3, NIC-LX3, NLA-LX3, GFY-LX3, ALT-LX3, RKY-LX3, CLK/CKL-LX3, CRT-LX3, LLY-LX3, ANY-LX3 | Honor X6a, X6b, X6, X5, X5 Plus, X6c, X5c, 9A, X7c, X7a, X7b, X8a, X8b, X9 | Alta/Media (tomados de lo que escribe la evaluadora junto al código) |
| JLN-LX3, MAO-LX9, ABR-LX9, FRL-L23, JKM-LX3, MAR-LX3A, DRA-LX3, DUB-LX3 | Huawei Nova 9 SE, Nova 11, P50, Y9a, Y8s, P30, Y5, Y7 | Alta/Media |
| A2403, A2111/A2221, A2631, A2641/A2484, A2893, A3092, A3286, A3408, A1778 | iPhone 12, 11, 13, 13 Pro Max, 14 Pro Max, 15, 16, 16e, 7 | Alta (A1778 Media) |
| MGJC3LZ/A, MLNG3E/A, MLMQ3LL/A, NLF53LL/A | iPhone 12, 13, 13, 13 Pro Max (números de parte) | Media: se quitaron los de iPhone 16 (MTMJ3...), ver dudas |
| AGR/AGRK/AGS-W09, KOB2-W09 | Huawei MatePad T10 / T10s, T8 | Media |
| TB328FU, TB330FU, 8505F, TB310/311FU, TB331FC | Lenovo Tab M10 3ra gen, M11, M8 HD, M9, Xiaoxin Pad 2024 | Alta / M9 Media |

## Dudas y hallazgos importantes

1. **La capacidad casi nunca viene en el texto (83% de los celulares)**. `capacidad` crea variante, así que la mayoría queda como variante `?` (sólo 17% tiene "128GB", "64 GB"...). En la captura nueva conviene obligar a elegir capacidad (checklist) para los modelos con más de una (Galaxy A15/A16/A35, Redmi Note, iPhone, Moto G54...). También cuesta saber la variante de iPhone: sin GB el préstamo varía mucho (iPhone 11: $500 a $3,755).
2. **Moto XT2421 es ambiguo**: la evaluadora lo escribió en Moto G04, G04s y E14 con el mismo código. Se resolvió por el nombre ("MOTO G04S", "E14"); el código solo cae en `cel.motorola.xt2421` ("Moto G04 / E14"). Revisar con la evaluadora qué se vende realmente.
3. **Vivo "Y1" (12 prendas, préstamo ~$1,000) NO es Y01 (~$1,460)**. Creé `cel.vivo.y1s` ("Vivo Y1s / Y1, por confirmar") que también absorbe el código V2028 (6 prendas, ~$1,030). Mi hipótesis es Vivo Y1s, baja confianza.
4. **Realme RMX3834 = 26 prendas** y no trae nombre; la mapeé a Note 50 (Media). Si no es, renombrar la plantilla (el id `cel.realme.note-50` no se usa en ningún otro lado todavía).
5. **Contradicción en iPhone**: "MARCA IPHONE 16 | MTMJ3VC/A" y "MARCA IPHONE 15 | MTMJ3E/A" comparten prefijo de número de parte; se quitaron esos códigos y se confía en el nombre. Otra prenda dice "IPHONE 13 MAX" en descripción y "IPHONE12 PRO" en modelo (cae en 12 Pro).
6. **Otros sin mapear** (quedan en genérica de la marca): Moto XT2429 (3 prendas), XT2167, XT2221; Xiaomi "MODELO 9" (7 prendas, ¿Redmi 9?), "Magic 5" bajo marca XIAMO (3, ¿Honor Magic5?), 25078PC3EG, 220233L2G; Realme RMX5313/RMX5303; Oppo CPH2859, PEMM00; Samsung SM 780G, "A37", "4525M" (¿A525M?), "Note 20 Ultra"; Apple A2211; Honor CMA-LX3; Huawei ART-TL28.
7. **Oppo C55 con marca REALME** (1 prenda): la descripción dice OPPO y el modelo C55; cae en `cel.oppo.c71` ("Oppo C71 / C55"). Hay un C55 de Realme también (4 prendas, plantilla propia); revisar.
8. **Celulares capturados en otra familia**: al correr las plantillas contra las demás familias aparecen 16 prendas (Redmi A3, Moto G22/G54/G05, iPhone 13...) que son celulares en otra familia de PRENDA FLEX; salen como `otra_familia` en el reporte. También datos sucios: una lijadora Truper con modelo "REDMI NOTE 12S" y una pantalla JVC con modelo "GALAXY A05S" (la evaluadora copió el modelo del renglón anterior).
9. **Ruido de captura**: la descripción a veces dice otra marca que el campo Marca (ej. "CARGADOR SAMSUNG" en un Xiaomi; "MARCA SAMSUNG" en un Moto G04). Como la guardia de marca revisa todo el texto, el Samsung genérico ya no se come estos casos porque las específicas van primero. Se auditó que cada prenda en plantilla específica tenga la marca esperada: 0 discrepancias reales (4 casos de marca mal escrita en el campo Marca).
10. **Spread de precio dentro de una misma plantilla** (candidatas a separar si el negocio lo pide): Oppo A58 (p10 $450 / p90 $2,372), iPhone 11, Moto G04s, Vivo Y01, Oppo A78. Probablemente es capacidad o estado, no modelo.

## Observaciones del motor (`scripts/plantillas.py`, no se modificó)

- `extraer_atributos`: la `variante` usa `?` cuando falta un atributo con `crea_variante`; no hay valor por omisión. Sería útil un `default:` por atributo o mostrar "Sin capacidad".
- `texto_prenda` descarta Marca/Modelo "SN", "X", "SIN", pero no "SM" (aparece como MODELO SM en una prenda), ni valores de relleno como "CELULARES" o un IMEI de 15 dígitos en Marca.
- `norm` conserva `.` y `/`, por eso "9T.128" y "SM A055M/DS" necesitan lookaheads cuidadosos (`(?![A-Z0-9])` y no `\b` solamente).
- `buscar` devuelve la primera plantilla de la lista; entre varias categorías el orden depende del orden alfabético de archivos (`sorted(glob)`) y de cómo `clasificar` arma `por_familia`. Una genérica "sin solo_familia" de otro agente podría ganar sobre una específica mía sólo en la segunda pasada, no en la primera.
- `--probar` calcula `pct_prestamo_cubierto` sobre `Préstamo` y excluye compras (`es_compra`), por eso 2,501 y no 2,548.
- Las tres claves nuevas que usé (`defaults:` con anclas, `formato:` en atributos, `solo_familia:`) las aceptó el motor sin cambios (`formato` y `solo_familia` ya existían en el código; `defaults` se ignora).
