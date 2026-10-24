# Notas: gamas de Celulares y Tablets

Archivo: `catalogo/marcas/celulares.yaml` (gama de las 297 reglas de `celulares.yaml` y `tablets.yaml`).

## Criterio
- **alta**: iPhone 12+, Galaxy S/Note, A5x (A52-A56), Moto Edge, Xiaomi 11T, Huawei P, Red Magic, Galaxy Tab S/OnePlus Pad.
- **media**: Galaxy A11-A4x, Moto G2x-G8x y G9, Redmi 9T/10/12/13/15, Redmi Note, Poco M/X, Oppo Reno y A57-A80, Vivo V Lite, Honor X8/X9, Huawei Nova, Axon, iPhone 11/X, Tab A8/A9, Lenovo M10/M11.
- **básica**: Galaxy A0x/A10/A20s/J, Moto E/G0x/G1x/G24, Redmi A/C/9, Poco C, ZTE Blade, Oppo A1x-A5x, Vivo Y, Honor X5-X7, Realme, Huawei Y, iPhone 6/7/8/SE, Lanix, Alcatel, genéricas chinas.
- Las marcas con modelo sin identificar toman la gama típica de la marca (bloque `marcas`).

## Resultado (datos: prendas_clasificadas.csv)
| Gama | Reglas | Empeños | Préstamo mediano | Venta mediana |
|---|---:|---:|---:|---:|
| alta | 50 | 107 | 2,000 | 3,750 |
| media | 104 | 831 | 1,200 | 1,850 |
| básica | 143 | 1,710 | 900 | 1,500 |

Monótono basica < media < alta. 145 de 274 reglas por modelo tienen 5+ empeños (objeto propio): 8 alta, 53 media, 84 básica. Las otras 129 más las 23 genéricas caen al objeto "Celular/Tablet · gama X".

## Dudas
- Los datos traen pocos iPhone (la mayoría de reglas Apple, S y Note sin empeños): la gama alta sale de precio de mercado, no de historial.
- Moto G24/G14/G05 se prestan igual que un E13 (~1,000): se dejaron básica; Moto G2x-G8x media aunque el préstamo es parecido.
- iPhone 11 y X/XR/XS quedaron en media (préstamo 2,500 y venta 4,350), no alta.
- Redmi Note 13/14 Pro y Reno 13 podrían subir a alta; con 1-5 empeños no hay evidencia.
- Genéricas Motorola/Xiaomi/Samsung mezclan gamas; se fijaron Samsung media, Motorola y Xiaomi básica.
