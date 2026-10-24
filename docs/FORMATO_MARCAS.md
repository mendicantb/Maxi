# Diccionario de marcas y gamas (catalogo/marcas/*.yaml)

Sirve para dos cosas:
1. **Objetos genéricos por gama.** Una prenda sin historial suficiente se cotiza con el objeto genérico de su
   plantilla y gama: `Rotomartillo · gama alta`, `Licuadora · gama básica`, `Celular · gama media`.
2. **Objetos propios.** Cuando una marca+modelo (o un modelo de celular) junta **5+ empeños**, se promueve a
   objeto propio con su historial (`DeWalt DCD776`, `iPhone 15 Pro Max`). Para que el conteo sea correcto hay
   que unir las faltas de ortografía de marcas y modelos.

## Gamas

| Gama | Idea | Herramienta | Línea blanca / cocina |
|---|---|---|---|
| `alta` | profesional / premium, se presta y se vende más | DeWalt, Makita, Milwaukee, Bosch, Hilti, Stihl, Husqvarna | Samsung, LG, Whirlpool, KitchenAid |
| `media` | marca conocida de uso doméstico | Truper, Black+Decker, Ryobi, Skil, Urrea, Einhell | Mabe, Hisense, Midea, Oster, T-fal |
| `basica` | económica, china o sin marca | Pretul, Toolcraft, Hyundai, genéricas | Atvio, Mirage, Mytek, genéricas |

Usa el préstamo y la venta real (`--probar` los muestra) para confirmar: si una marca "china" se presta
como media, ponla en media.

## Formato

```yaml
sector: herramientas
categorias: [Herramienta eléctrica, Herramienta de jardín y motor]   # nombres EXACTOS de `categoria` en los YAML de plantillas
gama_por_defecto: basica          # marca no reconocida, china o vacía

marcas:                           # nombre correcto: gama + cómo la escriben
  DeWalt:
    gama: alta
    escritura: [DEWALT, DEWAL, DE WALT, DWALT, DEWALL]
  Truper:
    gama: media
    escritura: [TRUPER, TRUPPER, TRUPE]

modelos:                          # opcional: une modelos mal escritos, por marca
  Truper:
    ROTO-1/2A7: [ROTO12A7, RROTO12A7, ROTO 1/2 A7]

gama_por_objeto:                  # sólo plantillas por modelo (celulares, tablets…): id de la regla -> gama
  cel.apple.iphone-15-pro-max: alta
  cel.samsung.galaxy-a04: basica
```

- Las escrituras se comparan con la marca capturada (y si no hay, con la descripción), en MAYÚSCULAS sin
  acentos, como palabra completa. La más larga gana.
- Los modelos se comparan sin espacios ni guiones (`ROTO 1/2 A7` = `ROTO12A7`).
- Probar: `python3 scripts/marcas.py --probar catalogo/marcas/<archivo>.yaml` (sólo lee).
