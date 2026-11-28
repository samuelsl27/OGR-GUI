# Spec 005 — Los números en pantalla, siempre con punto decimal

> Estado: hecha (2026-11-28, v0.1.4)

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
- [x] No importa el núcleo ni ningún programa.
- [x] Sus textos, si los hay, pasan por `tr()` y tienen su español en `i18n/es.py`.
- [x] Probada sin pantalla, sin `exec()` y sin dejar estado (regla 5), también la configuración
      regional.

**Entrada**
- [x] La coma, un segundo punto y una letra no entran (RF-7, RF-9); lo escrito es lo que se lee.

**Leyenda y diálogo de contornos**
- [x] Las etiquetas de la leyenda y los números del diálogo se escriben igual (D-12).

**Y siempre**
- [x] Ninguno de los patrones de «Lo que no se hace».

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

## Validación

2026-11-28, en la rama `dev/005-punto-decimal`, commit `4b5f71e`. Suite entera sin filtrar: **532
casos, 532 en verde, sin fugas**, en serie y con `--jobs 4` (Windows). Los tests son de
`tests/test_numbers_v014.py`.

| RF | Test que lo cubre | Resultado |
|---|---|---|
| RF-1 | `TestWritingANumber.test_a_point_and_no_thousands_in_both_languages`; `TestWhatThePiecesWrite` (sus tres casos, con la máquina en España y en inglés y los dos idiomas) | verde |
| RF-2 | `TestWhatThePiecesWrite.test_the_continuous_legend`, `test_the_bands_and_the_interval`, `test_the_status_bar`; `TestTheDialogsTakeAPoint.test_the_contour_dialog`, `test_the_snap_dialog`; `TestTheChartWritesAPoint.test_with_the_locale_asked_for` | verde |
| RF-3 | `TestTheChartWritesAPoint.test_with_the_locale_asked_for` (con `use_locale` encendido y la configuración numérica española en Python, que pinta comas sin el arreglo) y `test_a_log_scale_is_still_drawn` | verde |
| RF-4 | `TestWritingANumber` (sus cinco casos); `TestTheNumbersHaveNoQt`; `TestWhatThePiecesWrite.test_they_write_with_the_one_function` | verde |
| RF-5 | `TestTheNumberBox.test_it_is_a_qt_double_spin_box`; `TestTheDialogsTakeAPoint` (cada casilla es una `NumberBox`) | verde |
| RF-6 | `TestReadingANumber.test_what_is_read`; `TestTheNumberBox.test_a_point_is_read_and_shown`, `test_a_second_point_and_a_letter_do_not_go_in` (`-1.5e3`), `test_in_scientific_notation` | verde |
| RF-7 | `TestTheNumberBox.test_a_comma_writes_nothing` (dos máquinas, dos idiomas), `test_a_paste_with_a_comma_changes_nothing`, `test_with_a_suffix`; `TestTheDialogsTakeAPoint` | verde |
| RF-8 | `TestReadingANumber.test_one_point_is_always_the_decimal_mark`; `TestTheNumberBox.test_one_point_is_always_the_decimal_mark` | verde |
| RF-9 | `TestReadingANumber.test_what_is_refused`; `TestTheNumberBox.test_a_second_point_and_a_letter_do_not_go_in`, `test_a_paste_with_a_comma_changes_nothing` (`1.234,56`, `1,000.5`) | verde |
| RF-10 | `TestTheNumberBox.test_out_of_range_or_half_written_goes_back` | verde |
| RF-11 | `TestWritingANumber.test_what_the_pieces_wrote_in_013`; `TestWhatThePiecesWrite` (el texto de la 0.1.3, a mano); `TestTheDialogsTakeAPoint.test_the_boxes_keep_what_they_had`; `test_contours_v010`, `test_snap_dialog_v010` (con los de la regla 7), `test_legend_v010` y `test_status_bar_v010`, sin tocar | verde |
| RF-12 | `TestTheNumberBox.test_the_default_locale_is_left_as_it_was`; `TestTheChartWritesAPoint.test_matplotlib_is_left_as_it_was`; el vigilante de fugas del runner (`qt.locale`, `locale`, `rcParams`) | verde |

Lista de diseño: marcada arriba, mirando la pieza. Capturas sin pantalla
(`QT_QPA_FONTDIR=C:/Windows/Fonts`) con la configuración de Qt en España, en inglés y en español y en
los dos temas: el diálogo de contornos, el de enganche y la leyenda (continua y por bandas). Todos
los números llevan punto («1.0000», «12.0 px», «3.00», «6.000+»). En el máximo del diálogo de
contornos, tecleado «2,5», queda «25»: la coma no entró. Ningún principio falla.

CI de la [PR #7](https://github.com/samuelsl27/OGR-GUI/pull/7), commit `4b5f71e`: en verde en Linux y
Windows (Python 3.11, 3.12 y 3.13), en macOS (3.12) y la licencia.

La suite entera de OGR FEM2D (`3ec4fc8`) contra este árbol, con `--jobs 4`: 857 casos, 856 en
verde. Falla `test_the_installed_one`, como tiene que fallar contra otro árbol (fija la v0.1.3).

Lo que se encontró al validar:

- **FEM2D ya hizo su parte** en `3ec4fc8`, antes de esta validación. «Qué cambia para los
  programas» pedía cambiar primero su D12, y eso ya está hecho. Lo que le queda está en el changelog
  y en la respuesta escrita.
- **Su changelog espera que la entrada X,Y deje de aceptar la coma.** Esta spec lo deja fuera
  («Fuera de alcance»), y sería un cambio de la spec 004. Lo decide la propietaria.
- **El mínimo del espaciado de la rejilla es 0, no 1e-6** (Qt lo redondea a los 4 decimales de la
  casilla). Ya pasaba antes, no se cambia aquí y va a la hoja de ruta.

