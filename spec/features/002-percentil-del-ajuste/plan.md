# Plan 002 — El percentil del ajuste, por campo

Sin código. Cada apartado dice qué RF cubre.

## Lo que se encontró al leer el código

- El ajuste ya admite un percentil (`ContourSettings.fit_to(values, percentile=0.98)`); lo que falta
  es que el diálogo lo reciba. El diálogo lo llama en tres sitios, siempre con el 0,98 por defecto:
  la casilla de rango automático, «Fit to results» y «Restore Defaults» (que también corre al
  cambiar de campo).
- **El dibujo no lo hace el diálogo.** Con el rango automático marcado, el programa vuelve a
  ajustar el rango él mismo al dibujar: Slip2D, en `interpret_window.py`, con
  `self.contours.fit_to(values)`. Si el programa no pasa el mismo percentil, el diálogo enseñaría un
  máximo y el dibujo usaría otro, que es lo que D-12 prohíbe. La spec no lo dice porque es del
  programa; este plan lo resuelve dándole al programa el percentil en el mismo objeto que ya le da
  al diálogo (abajo, «Interfaces»), y el changelog se lo dice (regla 9).
- La ayuda de la casilla se pone una vez, al construir el diálogo, y no cambia al cambiar de campo.

## Decisiones

| Decisión | Alternativa descartada y por qué | RF |
|---|---|---|
| El percentil es un atributo nuevo de `ContourField`, `fit_percentile`, con 0,98 por defecto | Un argumento del diálogo: la propietaria lo quiso por campo. Guardarlo en `ContourSettings`: es la declaración del programa, no un ajuste de la persona; entraría en `to_dict()`, se guardaría en los proyectos y podría desdecir lo que el programa declara | RF-1, RF-2 |
| El diálogo pasa a `fit_to` el `fit_percentile` del campo elegido en los tres sitios | Una función de ajuste propia del programa: fuera de alcance de la spec | RF-3–RF-6 |
| `fit_to` no cambia: con percentil 1 su índice ya es el último valor | Una rama aparte para «sin recorte»: duplicaría el tratamiento de no finitos y de rango plano, que tiene que ser el mismo con cualquier percentil (casos límite) | RF-6 |
| La validación va en la construcción de `ContourField` (`__post_init__`) y lanza `ValueError` con la clave del campo y «(0, 1]» | Validar en el diálogo o en `fit_to`: el error llegaría tarde, al abrir el diálogo o al dibujar, lejos de quien lo declaró | RF-9 |
| Se rechazan también los booleanos (`True` es 1 en Python) y lo que no es `int` ni `float` | Aceptar cualquier cosa que compare: `True` pasaría por 1 y un texto fallaría con un error de tipo que no nombra el campo | RF-9 |
| La ayuda de la casilla tiene dos textos literales, cada uno por `tr()`, y se elige con el percentil del campo elegido al construir y al cambiar de campo | Un texto con el percentil dentro («usa el percentil 98»): una plantilla más que traducir, y el número no le dice nada a quien lee lo que pasa | RF-7, RF-8 |
| Solo el percentil 1 exacto da el texto «del menor al mayor» | Decidirlo por los valores (si el recorte cambia algo): la ayuda dependería de los datos y cambiaría con cada cálculo | RF-7 |
| Un campo que el diálogo no conoce (ajustes sin lista de campos) es `ContourField(clave, clave)`, como hoy, y por eso usa 0,98 | — | RF-2, RF-10 |

## Módulos

Dentro de `ogr_ui`, sin importar el núcleo ni ningún programa:

- `ogr_ui/contours.py` — `ContourField.fit_percentile` y su validación; la nota del módulo, que hoy
  dice que el rango automático siempre usa un percentil.
- `ogr_ui/dialogs/contour_options_dialog.py` — el percentil del campo elegido en los tres ajustes;
  la ayuda de la casilla, al construir y al cambiar de campo; la nota del módulo.
- `ogr_ui/i18n/es.py` — un texto nuevo (abajo).
- `ogr_ui/__init__.py` y `pyproject.toml` — 0.1.1 (al etiquetar; entre tanto, 0.1.1.dev0, que ya
  es).
- `docs/changelog/CHANGELOG_v0.1.1.md` — nuevo; `docs/consumidores.md` — la fila de contornos de
  «Lo que un programa hace al adoptarlo» y «Cambios en curso».

Texto nuevo, con su español:

| Inglés (la clave) | Español |
|---|---|
| Left on, the range follows the data as results change, from the smallest value to the largest. | Activado, el rango sigue a los datos según cambian los resultados, del menor valor al mayor. |

El texto de hoy («…The upper bound uses a percentile so a single extreme value cannot squash
everything else into one band.») se queda igual para los campos que recortan.

## Interfaces

El programa declara el percentil donde ya declara el campo, y lo usa al dibujar:

```text
STRESS = ContourField("sigma_1", "Major principal stress", fit_percentile=1.0)
FOS    = ContourField("fos", "Factor of safety")              # 0,98

ContourOptionsDialog(settings, fields=[STRESS, FOS], values=..., presets=...)

# al dibujar con el rango automático, el mismo percentil que el diálogo:
settings.fit_to(values, percentile=FIELDS[settings.field].fit_percentile)

ContourField("x", "X", fit_percentile=0)    # ValueError: el campo 'x' ... (0, 1]
```

## Compatibilidad

**Compatible** (0.1.1). `ContourField` gana un argumento con nombre y valor por defecto, y
`fit_to` no cambia. Un programa que fija la 0.1.0 y sube a la 0.1.1 sin tocar nada obtiene los
mismos rangos y la misma ayuda (RF-10). Lo que puede cambiar un programa, y el changelog lo dice:
dar `fit_percentile` a sus campos y pasar ese mismo percentil a `fit_to` al dibujar. FEM2D, además,
puede volver a ofrecer «Fit to results».

## Estrategia de tests

Un archivo nuevo, `tests/test_fit_percentile_v011.py`, con la pieza sola (un diálogo del test, sin
ventana de ningún programa):

- **La regla 1, una identidad**: con los valores 0, 1, …, 99 el índice del percentil 0,98 es
  `round(0,98 · 99) = 97`, y el del 1, el 99; con un pico (cien valores entre 1 y 2 y un 50), 0,98
  no llega al pico y 1 da 50 (el test que pide FEM2D). Los números esperados se escriben a mano, no
  se calculan con la función que se prueba.
- **RF-1, RF-2, RF-9**: el defecto es 0,98; 1 y 0,5 se aceptan; 0, −0,1, 1,01, NaN, ±∞, `"0.9"`,
  `None` y `True` se rechazan con `ValueError`, y el mensaje lleva la clave del campo y «(0, 1]».
- **RF-3, regla 7**: un diálogo con dos campos sobre los mismos valores con pico; «Fit to results»
  da máximos distintos con 0,98 y con 1, y lo que devuelve el diálogo al aceptar (`settings.vmax`)
  es ese máximo.
- **RF-4**: con la casilla marcada, el máximo mostrado es el del percentil del campo.
- **RF-5**: «Restore Defaults» y el cambio a un campo que empieza en automático ajustan con el
  percentil de ese campo (dos campos con percentiles distintos, ida y vuelta).
- **RF-6**: con 1, el máximo es el mayor valor finito aunque haya NaN e ∞ entre ellos.
- **RF-7, RF-8**: la ayuda de la casilla, en inglés y en español, es la de recorte con 0,98 y con
  0,9999, y la de «del menor al mayor» con 1; cambia al cambiar de campo, en los dos sentidos.
- **RF-10**: un diálogo sin percentiles da, con unos valores fijos, el mínimo y el máximo que se
  escriben a mano con la regla de la 0.1.0, y su ayuda es el texto de la 0.1.0.
- **Casos límite**: pico negativo (el mínimo es el menor valor con 0,98 y con 1); un solo valor y
  todos iguales (el mismo rango abierto con los dos percentiles).
- **Tamaño**: el diálogo, en español y con cada campo elegido, cabe en 1366×728 (su `sizeHint`); la
  ayuda es un *tooltip* y no lo cambia, pero se comprueba.
- **Idiomas y temas**: la ayuda en los dos idiomas (arriba); el tema no entra (la pieza no pone
  colores nuevos), así que no se prueba en los dos.
- **Plataformas**: nada depende de ella; la CI en las tres.
- **Regla 5**: el idioma se restaura en cada test que lo cambia; el runner lo vigila.
- Las de siempre siguen en verde: el censo de textos (`test_text_census_v010.py`, que encuentra el
  texto nuevo y su español) y los de contornos de la 0.1.0 sin tocar.

## Diseño

- **D-12 (enmendado)**: el rango automático del diálogo es el del campo, y el programa tiene el
  mismo percentil para dibujar; los dos dicen lo mismo si el programa lo pasa (riesgo abajo).
- **D-6**: la ayuda dice lo que hace el campo elegido, en presente; un texto nuevo de una frase.
- **D-4**: no se añade ningún control.

## Riesgos

- **Que un programa dé el percentil al diálogo y no al dibujar**: el diálogo enseñaría el rango
  entero y el dibujo el recortado. `ogr_ui` no lo puede comprobar (el dibujo es del programa); lo
  dice el changelog en «Qué tiene que cambiar cada programa», con la línea de ejemplo de arriba, y
  se le pide a FEM2D un test suyo que compare los dos.
- **Que la ayuda no cambie en algún camino de cambio de campo**: todos pasan por el mismo
  manejador de cambio de campo; el test lo recorre en los dos sentidos.
