# Notas: marcas de vehículos y varios (catalogo/marcas/vehiculos_varios.yaml)

Cobertura: Motos, Autos y camionetas, Bicicletas, Relojes, Navajas, Cascos, Bebés y juguetes, Varios, Deportes y
recreación, Ropa/calzado/accesorios, Accesorios para vehículos (806 prendas sin compras).

## Resultado de `--probar`
- Marca reconocida: 77 % global; 89 % de las prendas que sí traen marca capturada.
- Sin marca capturada (SN, X, XX, vacía): 16 %. Otro ~7 % trae una descripción en el campo marca
  ("HAMACAS", "TRICICLO", "BICI CHICA GRIS", "CASCO"): no son marcas y no se inventaron.
- Por categoría: Motos 100 %, Autos 100 %, Relojes 87 %, Navajas 84 %, Bicicletas 72 %, Cascos 70 %,
  Bebés y juguetes 65 %, Varios 63 %, Deportes 44 %, Ropa 12 %, Accesorios vehículos 0 %.
- Varios, Ropa, Deportes y Accesorios quedan bajos porque son artículos sin marca (hamacas, sandalias, llantas
  de pochimóvil, pistolas de balines); la meta de 80 % sólo aplica a las categorías de marca.
- 142 marcas: 22 alta, 44 media, 76 básica.

## Gamas (confirmadas con préstamo mediano)
| Categoría | alta | media | básica |
|---|---|---|---|
| Motos | $4,250 (2 prendas) | $7,000 | $6,000 |
| Bicicletas | n/a | $650 | $400 |
| Relojes | $3,000 | $700 | $150 |
| Navajas | $775 | $80 (2) | $275 |

- Motos: Italika FT/DM/ZW/D/Serie Z = media; AT/ST/DT/GS/150cc/genérica = básica; Yamaha FZ, Honda, Kawasaki = alta.
  Vento, Dinamo, Veloci, Tribu = básica; Kiwo = media (préstamo $12,000 en 4 casos, ver dudas).
- Relojes: Rolex, Tag Heuer, Rado, Apple Watch = alta; Fossil, Michael Kors, Invicta, Huawei, Samsung = media;
  Casio y Orient (clones) = básica porque se prestan ~$100.
- Todas las reglas de Motos, Autos y Relojes tienen `gama_por_objeto`.

## Modelos unidos
Italika (ZW150, FT150/FT150GTS, D125/D1252025, 125Z, AT110LT, DT125LT…), Yamaha Enticer 125, Kiwo KY200,
Mercurio Kaiser/Kaizer y Montaña, Victorinox (VICTORINO, VICTORIO → sin modelo), Rolex Oyster Perpetual.
Los años capturados como "modelo" (2023, 2024…) se mandan a "" porque el año ya crea la variante.
Piaggio con año como modelo se unifica en APE.

## Objetos propios (5+ empeños marca+modelo): 10
Piaggio Ape 18, Leatherman Surge 10, Italika ZW150 9, FT150 8, Rolex CL5 8, Italika D125 7, AT125 6,
Rado 01780 6, Mercurio Kaiser 5, Orient LHL469617SA7A 5. Además 27 marcas con 5+ empeños (objeto de marca).

## Pendientes
- Italika "150", "2025" y similares: 19 motos sin modelo; el POS debe exigir modelo.
- Navajas: 6 "NAVAJA COLOR ROJA" sin marca; probablemente Victorinox pero no se asumió.
- Hay artículos fuera de categoría (mesa, ollas, freidora, radios) capturados como bicicleta o reloj.
