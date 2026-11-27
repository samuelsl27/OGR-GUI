# Spec 002 — El percentil del ajuste, por campo

> Estado: hecha (2026-11-27, v0.1.1)

## Contexto y objetivo

`ContourOptionsDialog` ajusta el rango a los resultados con el máximo al percentil 98: en OGR
Slip2D, una superficie con un factor de seguridad de 40 aplastaría en una banda todas las demás. En
OGR FEM2D el rango de un campo de tensiones tiene que ser el entero: el pico en la pared de un
túnel es justo lo que se busca, y al percentil 98 desaparecería de la leyenda. FEM2D calcula su
propio rango así, del mínimo al máximo (`ogr_fem2d/results/drawing.py`, `value_range`), y mientras
tanto usa el diálogo con sus rangos de un clic y sin «Fit to results» (su spec 006, plan, «Parte
D»). Esta spec deja que cada campo diga qué parte de los valores cubre su máximo, para que el
ajuste del diálogo sea el del programa y FEM2D pueda ofrecerlo.

Lo pide la sesión de OGR FEM2D por escrito el 2026-11-24
(`FEM2D/Promts_desarrollo/2026_11_24_peticion_ogr_gui_rango_entero.md`), con su evidencia y el
test que lo demostraría. Decisiones de la propietaria (2026-11-25): tres specs para las tres cosas
del escrito (esta, el español de los mensajes de `ogr_core.api` y la entrada X,Y); el percentil, **por
campo** y no por diálogo; y D-12 enmendado (abajo, «Diseño»).

## Usuarios / actores

- OGR FEM2D, que quiere el rango entero en sus campos y «Fit to results» en su diálogo.
- OGR Slip2D, cuando lo adopte, que sigue con el percentil 98 sin decir nada.
- El ingeniero que abre «Contour Options» («Opciones de contornos») y pulsa «Fit to results»
  («Ajustar a los resultados») o deja marcada «Automatic range from the results».

## Historias de usuario

- H1: Como programa de la suite quiero decir, campo a campo, si el ajuste recorta los valores
  extremos, para que el rango automático sea el que mi cálculo necesita.
- H2: Como ingeniero que mira tensiones quiero que el ajuste incluya el pico, para verlo en la
  leyenda y en el dibujo.
- H3: Como ingeniero quiero que la ayuda de la casilla diga lo que hace el campo que tengo elegido,
  para no creer que se recortan valores que no se recortan, ni al revés.

## Requisitos funcionales (EARS)

- **RF-1** (ubicuo): EL SISTEMA permitirá al programa dar a cada campo que se puede contornear un
  percentil del ajuste, un número mayor que 0 y no mayor que 1.
- **RF-2** (ubicuo): EL SISTEMA usará 0,98 como percentil del ajuste de un campo al que el programa
  no le dé uno.
- **RF-3** (evento): CUANDO se pulse «Fit to results», EL SISTEMA pondrá como mínimo el menor valor
  finito y como máximo el valor del percentil del ajuste del campo elegido.
- **RF-4** (estado): MIENTRAS esté marcada «Automatic range from the results», EL SISTEMA mostrará
  el mínimo y el máximo con el percentil del ajuste del campo elegido.
- **RF-5** (evento): CUANDO se pulse «Restore Defaults» o se cambie de campo y el campo empiece con
  el rango automático, EL SISTEMA ajustará el rango con el percentil de ese campo.
- **RF-6** (ubicuo): EL SISTEMA dará como máximo del ajuste el mayor valor finito cuando el
  percentil del campo sea 1.
- **RF-7** (estado): MIENTRAS el campo elegido tenga un percentil menor que 1, la ayuda de «Automatic
  range from the results» dirá que el máximo usa un percentil para que un valor extremo no aplaste
  los demás; MIENTRAS sea 1, dirá que el rango va del menor valor al mayor.
- **RF-8** (evento): CUANDO se cambie de campo en el diálogo, EL SISTEMA cambiará la ayuda de la
  casilla a la del campo nuevo.
- **RF-9** (no deseado): SI el programa da a un campo un percentil que no es un número, es menor o
  igual que 0 o es mayor que 1, ENTONCES EL SISTEMA lo rechazará al declarar el campo con un error
  que nombra el campo y dice el intervalo admitido.
- **RF-10** (ubicuo): EL SISTEMA dará, a un programa que no da percentiles, los mismos rangos que la
  versión 0.1.0 con los mismos valores.

## Requisitos no funcionales

- Las tres plataformas de la CI (Linux, Windows, macOS).
- Inglés y español: los textos nuevos de la ayuda, con su traducción en `ogr_ui/i18n/es.py`
  (regla 2).
- Capas: sin el núcleo ni ningún programa (regla 10; el percentil llega del programa).

## Diseño

- **D-12, enmendado** (decisión de la propietaria del 2026-11-25): «el rango automático es el del
  campo: recorta los extremos con el percentil que el programa le da (0,98 si no da ninguno) o los
  incluye todos». Esta spec es su aplicación; el texto de D-12 en
  `spec/constitution/referencias-de-diseno.md` ya lo dice.
- **D-6**: la ayuda dice lo que hace el campo elegido, en presente y en pocas palabras (RF-7).
- **D-4**: el porqué de un ajuste que recorta sigue a la vista, en la ayuda de la casilla, sin
  añadir un control.

Lista de comprobación (se marca al validar):

**Toda pieza**
- [x] No importa el núcleo ni ningún programa; el percentil llega como argumento.
- [x] Sus textos pasan por `tr()` y tienen su español en `i18n/es.py`; ningún texto queda fuera del
      censo.
- [x] Probada sin pantalla, sin `exec()` y sin dejar estado (regla 5).

**Diálogo**
- [x] Cabe en 1366×728 en español, con el catálogo de Qt, en los dos temas (la ayuda nueva no cambia
      el tamaño, pero se comprueba).
- [x] Cada control mueve lo que el diálogo devuelve (regla 7): «Fit to results» con 0,98 y con 1 da
      máximos distintos sobre unos mismos valores con un pico.
- [x] «Restaurar» vuelve a los valores de partida, con el percentil del campo.

**Texto**
- [x] Corto, en presente, sin claves internas ni signos de exclamación.

**Y siempre**
- [x] Ninguno de los patrones de «Lo que no se hace».

No aplica: colores, iconos, acciones de menú, proceso largo (la pieza no los toca).

## Qué cambia para los programas

**Compatible**: sube el tercer número (0.1.1). Un programa que no da percentiles no cambia nada
(RF-10); OGR Slip2D, cuando lo adopte, tampoco. OGR FEM2D da percentil 1 a sus campos y puede
volver a ofrecer «Fit to results» (su spec 006, «Parte D»). El changelog de la versión lo dice
(regla 9).

## Casos límite

- Valores con un pico (el test que pide FEM2D): con 0,98 el máximo es el del percentil; con 1, el
  pico (RF-3, RF-6).
- Pico negativo (una compresión): el mínimo es siempre el menor valor, con cualquier percentil, así
  que no se recorta por abajo.
- Valores no finitos (NaN, ±∞): no cuentan, con cualquier percentil, como hoy.
- Un solo valor, o todos iguales: el rango se abre como hoy (el mínimo y un máximo un poco por
  encima), con cualquier percentil.
- Pocos valores: el percentil elige uno de los valores, no interpola, como hoy.
- Sin valores, o valores de otro campo: «Fit to results» sigue deshabilitado, como hoy; el percentil
  no cambia eso.
- Percentil 1 exacto frente a 0,9999…: solo el 1 dice «del menor valor al mayor» en la ayuda; un
  percentil menor que 1 dice que recorta aunque con pocos valores dé el máximo.

## Fuera de alcance

- Una función de ajuste propia del programa (la otra opción del escrito de FEM2D): con el percentil
  basta para lo que pide, y no se añade otra interfaz.
- Recortar por abajo (un percentil del mínimo).
- Un control en el diálogo para que el ingeniero elija el percentil.
- Que «Fit to results» se deshabilite con su porqué (`roadmap.md`, «Pendiente de decidir»): es otra
  candidata.
- El español de los mensajes de `ogr_core.api` y la entrada X,Y con relativos y polares: specs
  003 y 004.

## Criterios de finalización

- Todos los RF con su test en verde y la suite entera en verde en las tres plataformas de la CI.
- La lista de diseño marcada.
- El changelog de la 0.1.1 dice qué se encontró y qué puede cambiar FEM2D.
- `docs/consumidores.md` y `roadmap.md` al día.

## Dudas abiertas

- Ninguna.

## Validación

2026-11-27, en la rama `dev/002-percentil-del-ajuste`. Suite entera sin filtrar: **447 casos, 447
en verde, sin fugas**, en serie y con `--jobs 4` (Windows, `ogr_core 0.2.8` del extra `[test]`).
Todos los tests son de `tests/test_fit_percentile_v011.py` salvo donde se dice.

| RF | Test que lo cubre | Resultado |
|---|---|---|
| RF-1 | `TestTheFieldDeclaresItsPercentile.test_a_program_gives_its_own` | verde |
| RF-2 | `TestTheFieldDeclaresItsPercentile.test_the_default_is_the_98th_percentile`; `TestNoPercentileIsVersion010.test_settings_with_no_field_list` | verde |
| RF-3 | `TestTheDialogFitsWithTheFieldsPercentile.test_fit_to_results_and_what_the_dialog_returns` (también la regla 7: lo que devuelve al aceptar) | verde |
| RF-4 | `TestTheDialogFitsWithTheFieldsPercentile.test_the_automatic_range_shows_the_fields_fit` | verde |
| RF-5 | `TestTheDialogFitsWithTheFieldsPercentile.test_restore_defaults_fits_with_the_fields_percentile` y `test_there_and_back_between_fields` | verde |
| RF-6 | `TestTheFitWithAPercentile` (sus cinco casos: el índice, el pico, el pico negativo, los no finitos, el rango plano) | verde |
| RF-7 | `TestTheHelpSaysWhatTheFieldDoes.test_in_english_and_in_spanish` (0,98, 0,9999 y 1) | verde |
| RF-8 | `TestTheHelpSaysWhatTheFieldDoes.test_it_follows_a_change_of_field_both_ways` | verde |
| RF-9 | `TestTheFieldDeclaresItsPercentile.test_a_wrong_percentile_is_refused_naming_the_field` | verde |
| RF-10 | `TestNoPercentileIsVersion010.test_the_ranges_of_010`; `TestTheHelpSaysWhatTheFieldDoes.test_no_percentile_is_the_help_of_010`; `tests/test_contours_v010.py`, sin tocar | verde |

Lista de diseño: marcada arriba, mirando la pieza. Capturas sin pantalla
(`QT_QPA_FONTDIR=C:/Windows/Fonts`) del diálogo abierto en un campo con percentil 1 sobre los
valores con pico, en inglés y en español y en los dos temas: el máximo es 50, el pico; el diálogo
mide 334×577 en los cuatro casos, dentro de 1366×728; la ayuda es la de «del menor valor al mayor»
en los dos idiomas. Ningún principio falla.

CI de la [PR #1](https://github.com/samuelsl27/OGR-GUI/pull/1), commit `29c207e`: en verde en Linux y Windows (Python 3.11, 3.12 y 3.13) y en macOS (3.12), y la licencia, en las dos corridas (push y PR).
