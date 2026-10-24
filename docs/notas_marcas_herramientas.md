# Notas: marcas de herramientas (catalogo/marcas/herramientas.yaml)

Alcance: Herramienta eléctrica, de jardín y motor, manual y de obra, varia. 2,237 prendas (sin compras).

## Resultado de `--probar`
- Marca reconocida: **76.7%** del total. Las prendas sin marca real (vacía, SN, X, XX, VARIAS, SM, GENERICA, SIN MARCA) son
  **13.5%**; sobre las que sí traen marca capturada se reconoce el **88.2%**.
- Lo no reconocido son palabras que no son marca (MARRO, PLANCHUELA, BRUSHLESS, PRENSA, NUEVO LEON) y marcas sueltas de 1-2 empeños.
- 94 marcas: 14 alta, 26 media, 54 básica. Prendas por gama: alta 548, media 777, básica 912.
- Objetos propios (plantilla+marca+modelo con 5+ empeños): **58** (492 empeños). Con 3+ son 146.

## Préstamo mediano por gama (plantillas grandes)
| Plantilla | alta | media | básica | ¿sube? |
|---|---:|---:|---:|---|
| Rotomartillo | 1000 | 400 | 350 | sí (media y básica casi iguales) |
| Esmeriladora 4 1/2 | 600 | 300 | 300 | alta sí; media = básica |
| Taladro con cable | 400 | 300 | 250 | sí |
| Desbrozadora a gasolina | 2250 | 1500 | 1000 | sí |
| Motosierra | 2000 | 1400 | 900 | sí (n pequeño en media/básica: 16 y 18) |
| Sierra circular | 1500 | 725 | 400 | sí |
| Soldadora | 1150 | 1000 | 800 | sí, pero alta sólo tiene 4 casos y media 5 |
No sube bien: Caladora (alta 475, básica 400, media 350) y Esmeriladora media vs básica (Truper y Pretul se prestan igual, 300).

## Criterios de gama (con datos)
- Alta: DeWalt, Makita, Milwaukee, Bosch, Hilti, Metabo, Stihl, Husqvarna, Dolmar, Honda, Yamaha, Lincoln, Miller, Ridgid.
  Préstamo relativo a la mediana de su plantilla: DeWalt 1.8x, Milwaukee 1.9x, Bosch 1.6x, Makita 1.4x.
- Media: Truper, Black+Decker, Ryobi, Skil, Stanley, Urrea, Surtek, Craftsman, Koblenz, Karcher, Kinro, etc.
- Básica: Pretul, Toolcraft, Hyundai, Ingco, Husky, Oakland, Columbia, Burcat y la larga cola china.

## Dudas / decisiones a validar
1. **Husky** (HKM5220, HKD5200, 52CC) es una línea de gasolina barata; se presta ~1000-1200, como Pretul/Columbia. La puse básica, pero
   sus cajas de dados y llaves (Husky de Home Depot) se prestan más (400-1800). Una sola marca no puede ser las dos cosas.
2. **Kinro** media: préstamo 1500-2000 en desbrozadora/motosierra (venta ~2600), por encima de Columbia/Takashi. Si el dueño la ve china, bajar a básica.
3. **Teeno, Shawty, Duralast, Koblenz** se prestan por encima de su gama (1.2x-1.8x, pocos casos). Duralast y Koblenz en media; Teeno y Shawty se quedan básica.
4. **Karcher** media (préstamo 600 en hidrolavadora, menor que Koblenz 900). Podría ser alta si se espera lo que dice el doc para premium.
5. Modelos sin número real que cuentan como objeto propio: Pretul "ESMA 4 1" (10 empeños), Truper "4 1/2" (5), Stihl "291" y "351" en desbrozadora
   (¿FS291? ¿MS291?), Weg "MONOFASICO 2 1/2". Conviene excluirlos como modelo en el exportador.
6. No unidos por duda: Truper ERGO 4580 vs ESMA 4580N/4580PN (probable misma línea), DeWalt DW508 vs DW508S, Stihl FS55 vs FS55R,
   Husky 52PLUS (desbrozadora) vs HKM52 PLUS (motosierra), Truper ROTO12 sin sufijo.
7. DeWalt DCD776 aparece en Rotomartillo y en Taladro inalámbrico (es taladro): error de plantilla, no de marca.
8. "BOSCH STIHL", "TRUPER TRUPPER PRETUL" y similares (marca cruda doble) toman la marca de la escritura más larga; son casos raros.
