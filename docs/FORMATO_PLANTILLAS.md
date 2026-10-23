# Formato de plantillas (catalogo/plantillas/*.yaml)

Un archivo YAML por **categoría**. Estructura MAXI-POS: **Categoría › Familia (plantilla) › Variante**.

```yaml
categoria: Celulares                 # nombre visible
familias_prendaflex: [CELULARES]     # familias de PRENDA FLEX que se revisan primero contra esta categoría
excluir: []                          # regex que descartan cualquier plantilla de la categoría

atributos:                           # atributos comunes a todas las plantillas de la categoría
  color:
    regex: '\b(NEGRO|NEGRA|BLANCO|BLANCA|AZUL|ROJO|ROJA|GRIS|VERDE|MORADO|ROSA|DORADO|PLATA)\b'
    mapa: {NEGRA: NEGRO, BLANCA: BLANCO, ROJA: ROJO}   # normaliza valores
    crea_variante: false             # sólo describe
  capacidad:
    regex: '\b(32|64|128|256|512)\s*GB\b'
    mapa: {'64': 64GB, '128': 128GB}
    crea_variante: true              # cambia el precio -> crea variante

plantillas:                          # se evalúan EN ORDEN: la primera que hace match gana
  - id: cel.apple.iphone-14-pro-max  # único, minúsculas: <cat>.<marca>.<modelo>
    nombre: iPhone 14 Pro Max        # la "Familia" en MAXI-POS
    marca: Apple
    match:                           # regex sobre el texto normalizado (ver abajo); basta una
      - 'IPHONE\s*14\s*PRO\s*MAX'
      - '\bA2893\b'                  # número de modelo Apple
    excluir: ['FUNDA SOLA']          # opcional
    sinonimos: [iphone 14 pro max, 14 pro max]   # palabras que la encuentran en la búsqueda
    atributos: {}                    # atributos propios (se suman a los comunes)
    checklist: [Enciende, Pantalla sin estrellar, Face ID, Cuenta iCloud cerrada]
    fotos: [Frente encendido, Reverso, Pantalla Acerca de / IMEI]
    molde_descripcion: '{marca} {nombre} {capacidad} {color}'

  - id: cel.apple.generico
    nombre: iPhone (modelo sin identificar)
    marca: Apple
    generica: true                   # cuenta como cobertura parcial
    match: ['\bIPHONE\b', 'MARCA APPLE']
```

## Texto contra el que se hace match

Para cada prenda se arma: `DESCRIPCION (sin "NO. SERIE: …") | MARCA <marca> | MODELO <modelo>`,
en MAYÚSCULAS, sin acentos, sólo letras, números, `.` y `/`. Marca/modelo vacíos (`SN`, `X`, `XXX`) se omiten.
Ejemplo: `IPHONE 14 PRO MAX MORADO CON FUNDA COLOR ROJA | MARCA APPLE | MODELO IPHONE 14 PRO MAX A2893`

Las regex son de Python, insensibles a mayúsculas. Usa `\b` para no pegarle a números de serie.

## Orden de búsqueda

1. Plantillas de las categorías cuyo `familias_prendaflex` incluye la familia de la prenda.
2. Si no hubo match: todas las demás plantillas (salvo las marcadas `solo_familia: true`).
   Estas quedan como `otra_familia` en el reporte para revisar (la evaluadora la capturó en otra familia).
3. Sin match: va a `reportes/pendientes.csv` = **plantillas por crear**.

## Reglas para escribir plantillas

- Específicas primero, genéricas al final (`generica: true`).
- Una plantilla = un artículo que se cotiza igual (iPhone 13, Rotomartillo Bosch GBH 2-26, Cadena de oro).
- Atributo `crea_variante: true` sólo si mueve el préstamo (capacidad, año, kilataje, con/sin batería).
- Tolerar faltas de ortografía comunes en el regex (`SA?M?N?SUNG`, `MOTOR?OLA`, `XIA?O?MI`).
- Corre `python scripts/plantillas.py --sin-historial` para ver el efecto; revisa `reportes/pendientes.csv`.
