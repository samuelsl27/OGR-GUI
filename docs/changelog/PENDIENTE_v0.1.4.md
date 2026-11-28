# OGR GUI 0.1.4 — sin publicar

Un cambio compatible, la [spec 005](../../spec/features/005-punto-decimal/spec.md), que pidió OGR
FEM2D el 2026-11-28 en la T37 de su spec 006: una sola forma de escribir y leer los números en
pantalla. El escrito pedía la coma en español. **La propietaria decidió otra cosa** (2026-11-28):

- se muestra **siempre el punto**, en inglés y en español y con cualquier configuración de la
  máquina;
- en una casilla, **la coma no escribe nada**.

## 1. Qué cambia

| Pieza | 0.1.3 | 0.1.4 |
|---|---|---|
| `ogr_ui/numbers.py` | — | nuevo, sin Qt: `format_number(valor, decimales, scientific, signed)` y `read_number(texto)`, que acepta un signo, cifras, un punto y un exponente, y rechaza la coma, un segundo punto, `nan` e `inf` con `ValueError` |
| `ogr_ui.widgets.NumberBox` | — | nueva: una `QDoubleSpinBox` que muestra y acepta el punto, y solo el punto, en cualquier máquina; la coma, un segundo punto o una letra no entran, tecleados ni pegados |
| Las casillas de los diálogos de contornos (`sp_min`, `sp_max`) y de enganche (las siete de `_spin`) | `QDoubleSpinBox` con la configuración de la máquina | `NumberBox`, con los mismos decimales, rangos, pasos y sufijos |
| La leyenda, las bandas, el tamaño del intervalo y la barra de estado | un f-string cada una | `format_number`; el mismo texto carácter a carácter |
| Los ejes del gráfico XY | seguían `axes.formatter.use_locale` si un programa lo encendía | con punto siempre, solo en esos ejes; `rcParams` no se toca |
| `i18n/es.py` | 75 entradas | las mismas: no hay textos nuevos |

## 2. Qué se encontró

- **Las casillas leían «2.5» como 25 en una máquina española.** Una `QDoubleSpinBox` sigue la
  configuración regional por defecto de la aplicación, que es la de la máquina, no el idioma del
  programa. Con la de España muestra `2,500` y toma el punto como separador de miles: un rango o una
  tolerancia diez veces mayor, sin aviso. Lo vio FEM2D en su T37. Queda como evidencia en
  `TestTheEvidence`.
- **Con una configuración inglesa o la C, la coma era separador de miles**: «1,000» daba 1000.
  También se va.
- **Lo demás ya salía con punto**: el formato de Python no mira la configuración regional. Pero
  eran cuatro copias de la regla y ningún test lo fijaba con una configuración española.
- **El mínimo del espaciado de la rejilla es 0, no 1e-6** (regla 6, **no se cambia aquí**). El
  diálogo de enganche pide `lo=1e-6` con 4 decimales, y Qt redondea el mínimo a los decimales de la
  casilla: se puede escribir un espaciado 0. Pasaba igual en la 0.1.3 y en Slip2D. El test de esta
  versión lo fija tal como está, y va a «Pendiente de decidir» de la hoja de ruta.
- **Lo que está a medio escribir vuelve al último valor escrito, no al de antes de escribir.** Una
  casilla de Qt sigue al teclado: con «1e», el último valor válido es 1, y con «50» en una casilla
  de 0 a 10, es 5. Es lo que hace Qt y lo que dice RF-10. El test lo dice así.
- **La tecla decimal del teclado numérico** (riesgo del plan, sin probar): en algunas
  distribuciones de teclado, Windows la manda como coma, y entonces no escribe nada. No se puede
  probar sin un teclado físico. Si molesta, que esa tecla escriba punto sería un cambio de la spec.

## 3. Tests

`tests/test_numbers_v014.py`, 35 casos:

- **Escribir y leer**: los decimales, la notación científica y el signo en los dos idiomas; lo que
  se lee y lo que se rechaza; lo que escribían los f-strings de la 0.1.3, igual.
- **La casilla**, tecleada con la configuración de Qt en España y en inglés:
  - `2.5` da 2.5 y `1.000` da 1;
  - la coma no entra, en los dos idiomas, ni tampoco un segundo punto ni una letra;
  - pegar `2,5`, `1.234,56` o `1,000.5` no cambia nada;
  - lo que está a medio escribir o fuera de rango vuelve al último valor;
  - el sufijo, el texto especial del mínimo, la notación científica, el redondeo y las flechas;
  - la configuración por defecto de Qt queda como estaba.
- **Las piezas**: la leyenda, las bandas y la barra, con el texto de la 0.1.3 escrito a mano.
- **Los diálogos**: cada casilla es una `NumberBox` con lo que tenía, y lo que se teclea con punto
  es lo que devuelven.
- **El gráfico**: con `axes.formatter.use_locale` encendido y la configuración numérica española en
  Python, los ejes escriben con punto; la escala logarítmica sigue, y `rcParams` queda igual.

Los tests de la 0.1.0 de los dos diálogos (los de la regla 7 incluidos), de la leyenda, de los
contornos y de la barra, **sin tocar**.

## 4. Qué tiene que hacer un programa

Nada, si escribe con punto: los diálogos devuelven lo mismo y las piezas escriben lo mismo. Cambia,
a propósito, lo que se puede teclear en las casillas de `ogr_ui`: en una máquina española, la coma
ya no escribe nada (antes era el decimal) y «2.5» es 2.5 (antes era 25).

- **OGR FEM2D** ya cambió lo suyo en `3ec4fc8` (su D12 modificada, `units.number` con punto,
  `DecimalBox` sin coma). Al subir la fijación:
  - `DecimalBox` puede pasar a `NumberBox`, que lee lo mismo; si se queda, no pasa nada;
  - no hace falta nada para las piezas de `ogr_ui`: ya escriben con punto;
  - **su entrada X,Y sigue aceptando `1,5; 2,5`** (spec 004, sin cambios). Su changelog espera que
    se quite aquí: no entra en esta versión, y lo decide la propietaria.
- **OGR Data**: su spec 025 dice «separador decimal por idioma». Chocará con esta decisión cuando
  adopte el paquete: lo decide su sesión con la propietaria.
- **OGR Slip2D**, cuando adopte el paquete: nada; ya escribe con punto.
