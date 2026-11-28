# Spec 005 — Los números en pantalla, siempre con punto decimal

> Estado: aprobada (2026-11-28)

## Contexto y objetivo

Las casillas numéricas de `ogr_ui` (el mínimo y el máximo del diálogo de contornos y las del
diálogo de enganche) son las de Qt. Siguen la configuración regional de la **máquina**, no el idioma
del programa. En una máquina configurada para España muestran coma y leen «2.5» como 25: un rango o
una tolerancia diez veces mayor, sin aviso. El resto de números que escribe `ogr_ui` (la leyenda, la
barra de estado, el tamaño del intervalo, los ejes del gráfico XY) salen con punto, pero ningún test
lo fija, y cada programa los escribe a su manera.

Lo pide la sesión de OGR FEM2D por escrito el 2026-11-28, en la T37 de su spec 006
(`FEM2D/Promts_desarrollo/2026_11_28_peticion_ogr_gui_coma_decimal.md`). Pide una forma común de
escribir y leer un número de pantalla, usada en la leyenda continua, la barra de estado, el diálogo
de contornos y los ejes del gráfico XY. La evidencia es suya: con la configuración de España, una
casilla de Qt toma «2.5» como 25.

El escrito pedía la coma en español, por la D12 de su spec 006. **La propietaria decide otra cosa
(2026-11-28)**:

- el separador decimal que se muestra es **siempre el punto**, en inglés y en español, sea cual sea
  la configuración de la máquina;
- en una casilla, el separador decimal que se escribe es **solo el punto**: la tecla de la coma no
  escribe nada. Nunca se acepta un separador de miles (aprobación de la spec, 2026-11-28: en un
  principio se aceptaban el punto y la coma);
- entran **todos** los números que `ogr_ui` muestra o lee en pantalla, no solo los cuatro del
  escrito. También las etiquetas de la leyenda por bandas, el tamaño del intervalo y las casillas
  del diálogo de enganche.

## Usuarios / actores

- OGR FEM2D, que deja de escribir sus números y su casilla a su manera y usa las comunes.
- OGR Slip2D y OGR Data, cuando adopten el paquete.
- El ingeniero que escribe un rango o una tolerancia, en una máquina con cualquier configuración
  regional.

## Historias de usuario

- H1: Como ingeniero con la máquina en español quiero que «2.5» en una casilla sea 2,5 y no 25,
  para no fijar sin saberlo un rango diez veces mayor.
- H2: Como ingeniero quiero que si pulso la coma en vez del punto no se escriba nada, para que la
  casilla nunca tenga un número que no se lee como se ve.
- H3: Como ingeniero quiero ver los números de la leyenda, la barra, los diálogos y los gráficos
  escritos igual, para compararlos sin pensar.
- H4: Como programa de la suite quiero una sola forma de escribir un número y una sola casilla, para
  que mis números digan lo mismo que los de `ogr_ui`.

## Requisitos funcionales (EARS)

Lo que se muestra:

- **RF-1** (ubicuo): EL SISTEMA escribirá todo número que muestra una pieza de `ogr_ui` con el
  punto como separador decimal y sin separador de miles, en inglés y en español y con cualquier
  configuración regional de la máquina.
- **RF-2** (ubicuo): EL SISTEMA cumplirá RF-1 en cada uno de estos sitios: las cifras de la leyenda
  continua, las etiquetas de la leyenda por bandas (con su «+» en la última), las coordenadas de la
  barra de estado, el mínimo, el máximo y el tamaño del intervalo del diálogo de contornos, las
  casillas del diálogo de enganche y los ejes del gráfico XY.
- **RF-3** (no deseado): SI un programa ha pedido a matplotlib que use la configuración regional al
  escribir los ejes, ENTONCES EL SISTEMA escribirá igualmente con punto los ejes del gráfico XY.
- **RF-4** (ubicuo): EL SISTEMA dará a los programas una forma común de escribir un número para la
  pantalla, con los decimales o la notación científica que pidan, que cumpla RF-1.

Lo que se escribe en una casilla:

- **RF-5** (ubicuo): EL SISTEMA dará a los programas una casilla numérica común, la misma que usan
  los diálogos de contornos y de enganche.
- **RF-6** (ubicuo): EL SISTEMA aceptará en la casilla un signo delante, cifras, **un** punto
  decimal y un exponente (`-1.5e3`), en inglés y en español y con cualquier configuración de la
  máquina.
- **RF-7** (no deseado): SI se pulsa la coma en la casilla, ENTONCES EL SISTEMA no escribirá nada y
  la casilla conservará lo que tenía, en inglés y en español y con cualquier configuración de la
  máquina.
- **RF-8** (ubicuo): EL SISTEMA leerá el punto siempre como separador decimal: «1.000» es 1, nunca
  mil.
- **RF-9** (no deseado): SI se intenta escribir en la casilla un segundo punto (`1.2.3`) o un
  carácter que no sea de un número, ENTONCES EL SISTEMA no lo dejará entrar y la casilla conservará
  lo que tenía.
- **RF-10** (no deseado): SI lo escrito queda fuera del rango de la casilla o sin terminar (`-`,
  `1e`) al salir de ella, ENTONCES EL SISTEMA hará lo que hace hoy una casilla de Qt: volverá al
  último valor válido.

Compatibilidad:

- **RF-11** (ubicuo): EL SISTEMA devolverá desde los diálogos de contornos y de enganche los mismos
  valores que hoy para lo que hoy se escribe con punto, y cada control conservará su test de la
  regla 7.
- **RF-12** (ubicuo): EL SISTEMA no cambiará la configuración regional por defecto de la aplicación
  ni la de matplotlib: lo de RF-1 lo hace cada pieza para sí misma.

## Requisitos no funcionales

- Inglés y español: el mismo número se escribe igual en los dos (es lo que se prueba). Si hay algún
  texto nuevo, pasa por `tr()` con su español (regla 2).
- Independiente de la máquina: los tests fijan una configuración regional de España y otra inglesa y
  la devuelven al terminar (regla 5).
- Capas: sin el núcleo ni ningún programa (regla 10).
- Las tres plataformas de la CI.

## Diseño

- **D-7, entradas tolerantes, nunca silenciosas**: la casilla no deja entrar lo que no puede leer
  como se ve. La coma no entra (decisión de la propietaria), y tampoco un segundo punto ni una letra:
  lo que queda escrito es siempre el número que se usa. D-7 pone la coma entre lo que se acepta, pero
  como ejemplo de la entrada X,Y, que no cambia (spec 004).
- **D-6, la notación del oficio**: una sola notación de los números en toda la suite, la misma que
  la tabla CSV y que los informes numéricos.
- **D-12, leyendas que dicen la verdad**: las etiquetas de la leyenda y los números del diálogo que
  fija su rango se escriben igual.
- **D-1, lo conocido primero**: la casilla se comporta como una de Qt (flechas, rueda con la guarda
  de siempre, rango), salvo en lo que lee.

Lista de comprobación (se marca al validar):

**Toda pieza**
- [ ] No importa el núcleo ni ningún programa.
- [ ] Sus textos, si los hay, pasan por `tr()` y tienen su español en `i18n/es.py`.
- [ ] Probada sin pantalla, sin `exec()` y sin dejar estado (regla 5), también la configuración
      regional.

**Entrada**
- [ ] La coma, un segundo punto y una letra no entran (RF-7, RF-9); lo escrito es lo que se lee.

**Leyenda y diálogo de contornos**
- [ ] Las etiquetas de la leyenda y los números del diálogo se escriben igual (D-12).

**Y siempre**
- [ ] Ninguno de los patrones de «Lo que no se hace».

No aplica: colores, iconos, acciones de menú, proceso largo.

## Qué cambia para los programas

**Compatible** (sube el tercer número: 0.1.4). Lo que hoy sale con punto sigue saliendo igual. Lo
que hoy se escribe con punto en una casilla da el mismo valor (RF-11). Lo que cambia es que una
casilla de `ogr_ui` en una máquina con configuración de España deja de leer «2.5» como 25, y que la
coma no se escribe en ella (en esa máquina, hoy era el separador decimal).

- **OGR FEM2D**:
  - **Primero su spec**: la D12 de su spec 006 dice «coma en español». Con la decisión de la
    propietaria pasa a «punto siempre; en una casilla, la coma no se escribe». La cambia su sesión, no esta.
  - `units.shown`, `units.number` y `units.pair` dejan de poner la coma, y `pair` vuelve a `x, y`.
    Puede cambiarlas por la forma común (RF-4).
  - `DecimalBox` puede cambiarse por la casilla común (RF-5). Es distinta: no deja escribir la coma,
    y `DecimalBox` la acepta.
  - Deja de rodear con `units.shown` las etiquetas por bandas que pasa a la leyenda.
- **OGR Data**: su spec 025 dice «separador decimal por idioma». Cuando adopte el paquete, chocará
  con esta decisión. Lo decide su sesión con la propietaria.
- **OGR Slip2D**, cuando adopte el paquete: nada. Ya escribe con punto, y sus casillas de Qt pasan a
  ser la común.

## Casos límite

- `2.5` da 2.5. Al teclear `2,5`, la coma no entra y queda `25`: es lo que se ve (RF-7).
- `1.000` da 1 (RF-8).
- `.5` y `5.`: números válidos (0.5 y 5).
- `-0`: vale, y se muestra como lo muestra hoy la casilla de Qt.
- `1.5e3` y `1.5E-3`: valen. La casilla con notación científica lo muestra como `1.500e+03`.
- Una casilla con prefijo o sufijo (una unidad, `" m"`): lo que se lee es el número, sin la unidad.
- Una casilla con texto especial para su mínimo («ninguno»): sigue funcionando como en Qt.
- Pegar `2,5` o `1.234,56`: no entra, como al teclearlo (RF-7, RF-9); la casilla conserva lo que
  tenía.
- Un número muy grande en la leyenda: `1000000.00`, sin separador de miles (RF-1).
- El idioma cambia y el programa se reinicia (es lo que hacen hoy los programas): no hay cambio en
  caliente que probar.

## Fuera de alcance

- La tabla CSV y todo archivo que lea un programa: ya se escriben con punto, y no son pantalla.
- Las casillas y los textos de cada programa que no usan las piezas de `ogr_ui`: los cambia cada
  programa (arriba).
- Un separador decimal por idioma o configurable: la propietaria lo descarta.
- Los números dentro de un texto traducido (`tr("… %s …")`): el número que se mete ya va escrito
  con RF-4.
- La entrada X,Y de la barra de estado: la spec 004 ya la cubre y sigue aceptando la coma decimal
  (`1,5; 2,5`). No cambia aquí; si se quiere que tampoco la acepte, es un cambio de la spec 004.

## Criterios de finalización

- Todos los RF con su test en verde y la suite entera en verde en las tres plataformas de la CI.
- La lista de diseño marcada.
- El changelog de la versión dice qué se encontró (las casillas que leían «2.5» como 25 en una
  máquina española) y qué tiene que cambiar FEM2D.
- Un escrito para la sesión de OGR FEM2D con su respuesta: la decisión de la propietaria y lo que
  le toca cambiar.
- `docs/consumidores.md` y `roadmap.md` al día.

## Dudas abiertas

- Ninguna.
