# Plan 005 — Los números en pantalla, siempre con punto decimal

Sin código. Cada apartado dice qué RF cubre.

## Lo que se encontró al leer el código

- **Lo que se escribe ya sale con punto**, porque se escribe con el formato de Python (`f"{v:.3f}"`),
  que no mira la configuración regional. Son cuatro sitios, cada uno con su propia copia de la
  regla:
  - `ColourScaleLegend.format_value` (`widgets/legend.py`), las cifras de la leyenda continua;
  - `ContourSettings.format_value` y `band_label` (`contours.py`), las etiquetas por bandas y el
    «Interval size:» del diálogo de contornos;
  - `OgrStatusBar.update_coords` (`widgets/status_bar.py`), `X: +1.250   Y: …`.

  Ningún test lo fija con una configuración regional española. Los tests de hoy (`"0.500"`,
  `"6.000+"`) corren con la de la máquina de la CI.
- **Lo que falla son las casillas.** Las siete de `snap_dialog.py` (que salen de `_spin`) y
  `sp_min` y `sp_max` de `contour_options_dialog.py` son `QDoubleSpinBox` con la configuración por
  defecto de la aplicación. Esa configuración es la de la máquina: con la de España muestran
  `2,5000` y leen «2.5» como 25. Además, una casilla de Qt con la configuración C o inglesa acepta
  la coma como separador de miles («1,000» da 1000), y eso RF-7 lo prohíbe.
- **Los ejes del gráfico XY** (`xy_chart.py`) usan el `ScalarFormatter` de matplotlib. Por defecto
  escribe con punto, pero sigue `axes.formatter.use_locale` si un programa lo enciende (RF-3).
- **El runner ya vigila la configuración regional por defecto de Qt** (`qt.locale` en
  `ogr_core.testing.leaks`), y la de Python (`locale`). Un test que la cambie tiene que devolverla.
- **`DecimalBox` de FEM2D** (`ogr_fem2d/gui/dialogs/fields.py`) ya resuelve la parte de Qt: usa la
  configuración C, quita el separador de miles y valida con su propia expresión. Se toma su forma,
  no su código, porque acepta la coma y depende de `units.shown`.

## Decisiones

| Decisión | Alternativa descartada y por qué | RF |
|---|---|---|
| Un módulo nuevo sin Qt, `ogr_ui/numbers.py`, con **`format_number(valor, decimales, científica, con_signo)`** y **`read_number(texto)`**. Escribir es el formato de Python (`f`, `e`, con `+` si se pide). Leer acepta un signo, cifras, un punto y un exponente, y nada más: ni coma, ni espacios dentro, ni `nan` ni `inf` | Dejar cada sitio con su f-string: ya sale con punto, pero cuatro copias de la regla son cómo acaban diciendo cosas distintas, y el programa no tendría la suya (RF-4) | RF-1, RF-4, RF-6, RF-8 |
| `ColourScaleLegend.format_value`, `ContourSettings.format_value` (y con él `band_label` y el tamaño del intervalo) y `update_coords` escriben con `format_number`. El resultado es el mismo carácter a carácter | Cambiar el formato de alguno al pasar (más decimales, sin `+`): no lo pide la spec, y RF-11 pide lo mismo que hoy | RF-1, RF-2, RF-11 |
| Una casilla nueva, **`NumberBox`**, en `ogr_ui/widgets/number_box.py`, hija de `QDoubleSpinBox`. Tiene su propia configuración regional, la C sin separador de miles y que lo rechaza, puesta al crearla. Escribe el valor con `format_number(valor, decimals())` y lo lee con `read_number`. Su validación es la expresión de RF-6, aplicada al texto sin el prefijo y el sufijo, y deja pasar el texto especial del mínimo | Cambiar la configuración por defecto de la aplicación a la C: arreglaría todas las casillas de golpe, también las del programa, pero RF-12 lo prohíbe. Cambiaría fechas y todo lo demás, y el runner lo vería como fuga. Ponerle a cada casilla de Qt `setLocale(C)` sin más: Qt seguiría aceptando la coma como separador de miles | RF-5–RF-9, RF-12 |
| La coma y un segundo punto devuelven `Invalid` en la validación. Qt no los deja entrar, ni tecleados ni pegados, y la casilla conserva lo que tenía. Lo que está a medio escribir (`-`, `1e`, `.`) devuelve `Intermediate`. Fuera de rango, también `Intermediate`, y Qt vuelve al último valor válido al salir, como hoy | Cambiar la coma por un punto al teclearla: la propietaria lo descarta (la coma no escribe nada). Un mensaje al rechazarla: la spec no lo pide, y la casilla que no escribe es la respuesta | RF-7, RF-9, RF-10 |
| Los diálogos de contornos (`sp_min`, `sp_max`) y de enganche (`_spin`) usan `NumberBox` con los mismos decimales, rangos, pasos y sufijos que hoy | Dejar las casillas del enganche para otra spec: la propietaria las incluyó (alcance (a)) | RF-2, RF-5, RF-11 |
| Los ejes del gráfico XY: tras dibujar, a cada eje con `ScalarFormatter` se le apaga el uso de la configuración regional, solo en esos ejes. Los formateadores logarítmicos no la usan y no se tocan | Cambiar `rcParams` o usar `rc_context` al crear la figura: tocaría lo global de matplotlib (RF-12, regla 5), y el formateador lee el valor al dibujar, no al crear | RF-2, RF-3, RF-12 |
| `NumberBox`, `format_number` y `read_number` se exportan para los programas desde `ogr_ui.widgets` y `ogr_ui.numbers` | Dejarlos privados: el escrito de FEM2D pide justo esto para quitar su `DecimalBox` y `units.shown` | RF-4, RF-5 |

## Módulos

Dentro de `ogr_ui`, sin importar el núcleo ni ningún programa:

- `ogr_ui/numbers.py`: nuevo, sin Qt, con `format_number` y `read_number`.
- `ogr_ui/widgets/number_box.py`: nuevo, con `NumberBox`. `ogr_ui/widgets/__init__.py` lo exporta.
- `ogr_ui/widgets/legend.py`, `ogr_ui/contours.py`, `ogr_ui/widgets/status_bar.py`: escriben con
  `format_number`.
- `ogr_ui/dialogs/contour_options_dialog.py` y `ogr_ui/dialogs/snap_dialog.py`: `NumberBox` en vez
  de `QDoubleSpinBox`.
- `ogr_ui/xy_chart.py`: los ejes sin la configuración regional.
- `ogr_ui/i18n/es.py`: **ningún texto nuevo**. La casilla no dice nada, y lo que se escribe son
  números.
- `tests/test_numbers_v014.py`: nuevo.
- `docs/changelog/PENDIENTE_v0.1.4.md` (renombrado a `CHANGELOG_v0.1.4.md` en el commit de la
  versión), `docs/consumidores.md` y `roadmap.md`. La versión pasa a `0.1.4.dev0`.
- La respuesta a FEM2D, en `GUI/notas/2026_11_28_respuesta_a_fem2d_punto_decimal.md`, como la del
  2026-11-24.

## Interfaces

```text
from ogr_ui.numbers import format_number, read_number
from ogr_ui.widgets import NumberBox

format_number(2.5, 3)                    -> "2.500"       (también con la máquina en español)
format_number(1250.0, 2, scientific=True)-> "1.25e+03"
format_number(1.25, 3, signed=True)      -> "+1.250"
read_number("2.5")                       -> 2.5
read_number("1.000")                     -> 1.0
read_number("2,5")                       -> ValueError

box = NumberBox()                        # una QDoubleSpinBox: setRange, setDecimals, setSuffix…
box.setDecimals(3); box.setSuffix(" m")
# teclear «2,5»   -> la coma no entra: queda «25 m»
# teclear «2.5»   -> 2.5, se ve «2.500 m»
```

Desde FEM2D, cuando su spec lo cambie: `units.number(v, spec)` puede pasar a `format_number`, y
`Number.box` pasa a ser un `NumberBox` en vez de un `DecimalBox`.

## Compatibilidad

**Compatible: 0.1.4.**

- Lo que se escribe es lo mismo carácter a carácter. `format_value` y `band_label` siguen ahí con
  la misma firma.
- `sp_min`, `sp_max` y las casillas del enganche siguen siendo `QDoubleSpinBox` (`NumberBox` es una
  hija). Dan el mismo `value()` para lo que se escribe con punto, y sus tests de la regla 7 no
  cambian.
- Cambia, a propósito, lo que se puede teclear en esas casillas. En una máquina española, la coma
  ya no escribe nada (antes era el decimal) y «2.5» es 2.5 (antes era 25). En una inglesa, la coma
  ya no es separador de miles.
- Un programa que encienda `axes.formatter.use_locale` lo sigue teniendo en sus gráficos, pero no
  en el de `ogr_ui`.

## Estrategia de tests

- **La pieza sola, sin ventana de ningún programa**, en `tests/test_numbers_v014.py`:
  - `format_number` y `read_number` con la tabla de los casos límite de la spec;
  - `NumberBox` tecleado con `QTest.keyClicks`: `2.5` da 2.5, `2,5` deja `25`, `1.000` da 1,
    `1.2.3` deja `1.23`, una letra no entra, y pegar `2,5` o `1.234,56` no cambia nada;
  - fuera de rango y a medio escribir, al salir vuelve al último valor;
  - con sufijo, con texto especial y con notación científica.
- **La configuración de la máquina**: cada test de RF-1, RF-2 y RF-6 corre dos veces, con la
  configuración por defecto de Qt puesta en España y en inglés. La casilla se crea después de
  ponerla, porque toma la configuración al crearse, y se devuelve la anterior en un `finally`. La de
  Python no se toca: el formato de Python no la usa, y el runner lo vigila igual.
- **Cada sitio de RF-2**, en los dos idiomas (`set_language`, restaurado):
  - la leyenda continua y la por bandas;
  - la barra de estado;
  - el diálogo de contornos (el mínimo, el máximo y el tamaño del intervalo) y el de enganche;
  - los ejes del gráfico, leídos de las etiquetas que dibuja matplotlib.
- **RF-3**: el gráfico XY dentro de `matplotlib.rc_context` con `axes.formatter.use_locale`
  encendido. Sus formateadores dicen que no usan la configuración regional, y `rcParams` queda como
  estaba (lo vigila la regla 5).
- **RF-11**: los tests de hoy de los diálogos de contornos y de enganche (`test_contours_v010.py` y
  `test_snap_dialog_v010.py`, con los de la regla 7) **sin tocar**, más uno que compara
  `format_value`, `band_label` y `update_coords` con la salida de la 0.1.3, escrita a mano en el test.
- **RF-12**: tras crear casillas, una leyenda y un gráfico, `QLocale()` y
  `axes.formatter.use_locale` son los de antes.
- **Temas**: no cambia ningún color. Las capturas sin pantalla de los dos diálogos, en los dos
  temas, son para la lista de diseño.
- **Plataformas**: los teclados no entran en los tests (`keyClicks` manda caracteres), así que lo
  que dependa de la plataforma es solo la configuración C de Qt. Va a la CI de las tres.

## Riesgos

- **La tecla decimal del teclado numérico.** En algunas distribuciones de teclado, Windows la manda
  como coma. Con la decisión de la propietaria, entonces no escribiría nada. No se puede probar sin
  un teclado físico. Se anota en el changelog y en la respuesta a FEM2D. Si molesta, hacer que esa
  tecla escriba punto es un cambio de la spec.
- **El redondeo de Qt.** `QDoubleSpinBox` redondea el valor a `decimals()` con su propia función, y
  `textFromValue` tiene que coincidir con ella o el texto y el valor discrepan. El test compara los
  dos en los casos de redondeo a la mitad (`0.12345` con 4 decimales).
- **`-0`**: el formato de Python da `-0.000` y el de Qt `-0.000` o `0.000` según la versión. Se fija
  el de hoy en el test de RF-11, y si discrepa se avisa antes de cambiarlo (regla 6).
