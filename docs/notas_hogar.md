# Notas catalogo Hogar (plantillas hogar_*.yaml)

Archivos: `catalogo/plantillas/hogar_{belleza,clima,cocina,linea_blanca,muebles,ropa_limpieza}.yaml` (72 plantillas).

## Cobertura (alcance propio: 1,105 prendas de las familias PRENDA FLEX de hogar, sin duplicados de otros agentes)
- Cubiertas 99.9 %, especificas 99.5 %, prestamo cubierto 99.98 %.
- Por categoria (prendas / % especificas): Cocina 545 / 99.8, Linea blanca 186 / 98.9, Clima 221 / 99.1, Ropa y limpieza 69 / 100, Belleza 66 / 100, Muebles 17 / 100.
- Cada archivo lista TODAS las familias de hogar en `familias_prendaflex` a proposito: ELECTRODOMESTICOS y ELECTRODOMESTICOS PEQUENOS mezclan de todo, y asi las plantillas de hogar se prueban antes que las genericas de otras categorias (que robaban prendas, p. ej. una aspiradora Koblenz caia en `elec.regulador.voltaje`).
  Consecuencia: `--probar` sobre UN archivo mide las 1,019+ prendas contra solo esas plantillas y sale bajo (5-50 %); medir con todos los hogar_*.yaml juntos.

## Prendas capturadas en familias de hogar que NO son de hogar (para otros agentes)
Pulidora Truper (REFRIGERADOR), bascula Truper, desbrozadora Sthil y "arpiradora adaptado" Sthil (ELECTRODOMESTICOS / CONGELADOT¿R), esmeril Makita, aspersora Husqvarna (ASPIRADORAS), laptop HP (LAVADORAS), pantalla Roku HKPRO (PLANCHAS DE VAPOR), patin electrico (VENTILADORES), minicomponente LG (TANQUE DE GAS), guitarra (MUEBLES), extension Truper. Hoy las atrapan plantillas de otros agentes por `otra_familia` (algunas mal: bascula -> `herr.sierra.circular`, extension -> `navaja.marca-conocida`, laptop/pantalla/patin -> `elec.audio.generica`).
La familia `CONGELADOT¿R` (2 prendas) es en realidad la desbrozadora Sthil FS-120; no se incluyo en hogar.

## Decisiones
- Variantes (`crea_variante: true`): lavadora = kilos + tipo (doble tina / automatica); refrigerador y congelador = pies cubicos; tanque de gas = kg; estufa = no. de quemadores; minisplit = toneladas/BTU; olla de presion = litros; maquina de coser = tipo (overlock...); aspiradora = tipo.
- Ventilador: chico (10-12", ~$150) y estandar de pedestal/piso (~$500) son plantillas distintas porque el prestamo es 3x; ademas techo, torre, caja y mini/recargable.
- Estufa: de piso con horno (Mabe, Acros...), de mesa / parrilla de gas (Foset, Super Flama...), empotrable, de lena, parrilla electrica, induccion. La estufa de piso 4-6 quemadores vale 800-2,000 y la de mesa 100-500.
- Plancha de cabello vs plancha de vapor: se separan por palabras (CABELLO, ALACIADORA, marcas Conair/Revlon...) con `excluir`.
- Licuadora Ninja y batidora de pedestal (KitchenAid, Hamilton) separadas de la licuadora/batidora de mano normal por precio.

## Hallazgos / dudas
1. Capacidad de lavadora: ~25 % de las descripciones no trae kilos y ~85 % no dice el tipo. Los Mirage LMS013M/016M, Mabe LMDX y HKPRO THK-SM son doble tina aunque la evaluadora no lo escriba (el modelo dice los kilos: LMS013M = 13 kg; ya se extrae del modelo LMS/LMD/WSA/THK-SM). Conviene que el POS pida kilos y tipo al capturar.
2. "LAVADORA SECADORA" (Mabe LMDX1123, Winia) en realidad suele ser doble tina con centrifuga, no lavasecadora; se mapea a Doble tina.
3. Tanque de gas: 25 % sin capacidad ("TANQUE DE GAS COLOR GRIS"); typos como "120K" (= 20K) o "TANQUE DE 30 CILINDROS". Prestamo 200-1,000 depende del kg, asi que vale la pena exigir kg.
4. Refrigerador: casi nadie anota pies cubicos (solo ~25 %); el modelo Mabe RMA/RMS/RMP trae el tamano pero no se decodifica. Prestamo va de $1,500 a $6,000.
5. Datos atipicos: cafetera industrial Sanson $7,652 y maquina de hielo Sanson $3,142 (equipo de negocio, no hogar); mesa plegable "WHITE" $1,250 vs $300-500 normal; ventilador Kingsman $900 (fuera de rango).
6. `ELECTRODOMESTICOS` concentra 184 prendas de 20+ tipos distintos; recomiendo que el POS nuevo sustituya esas familias por la categoria de plantilla.
