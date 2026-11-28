# Spec 006 — En la entrada X,Y, la coma separa y el punto es el decimal

> Estado: hecha (2026-11-28, v0.2.0)

## Contexto y objetivo

La entrada «Enter X,Y:» («Introducir X,Y:») de la barra de estado acepta hoy la coma como decimal
(spec 004): `1,5; 2,5` y `1,5 2,5` dan (1.5, 2.5). También acepta como separador de coordenadas el
punto y coma y el espacio. La spec 005 dejó el punto como único separador decimal en el resto de
`ogr_ui`, y en sus casillas la coma no se escribe. La entrada X,Y quedó fuera de esa spec, y es el
último sitio de `ogr_ui` donde una coma puede ser un decimal.

La propietaria fija el criterio el 2026-11-28: **en la entrada X,Y, la coma separa las dos
coordenadas y el punto es el separador decimal** (`x.x,x.x`). Es lo que pide la D12 de la spec 006
de OGR FEM2D, modificada el mismo día («una coma en un número se rechaza, porque se presta a
confusión y a errores»). El `CHANGELOG_v0.0.15.md` de FEM2D (commit `3ec4fc8`) espera que se
corrija aquí. Decisiones de la propietaria (2026-11-28):

- **solo la coma** separa las coordenadas: el espacio solo y el punto y coma dejan de separar;
- es un cambio incompatible y sube a la **0.2.0**. El aviso de margen de la regla 8 es el escrito a
  FEM2D, el único programa que fija `ogr-gui`, que sigue en la 0.1.4 hasta que suba a propósito. No
  hay versión intermedia.

## Usuarios / actores

- OGR FEM2D, que dibuja contornos con puntos escritos y ya no acepta la coma decimal en lo suyo.
- OGR Slip2D y OGR Data, cuando adopten el paquete.
- El ingeniero que escribe un vértice en la barra de estado.

## Historias de usuario

- H1: Como ingeniero quiero escribir un punto siempre de la misma forma, `x.x,x.x`, para que la coma
  no signifique dos cosas según lo que haya alrededor.
- H2: Como ingeniero que escribe por costumbre `1,5; 2,5`, quiero que se rechace con un motivo que
  diga cómo se escribe, para no dibujar un punto que no quería.
- H3: Como programa de la suite quiero que la entrada lea los números igual que las casillas
  (spec 005), para que en ningún sitio una coma sea un decimal.

## Requisitos funcionales (EARS)

Lo que se acepta:

- **RF-1** (evento): CUANDO se pulse Intro con dos números separados por **una coma**, con o sin
  espacios alrededor de la coma (`1.5,2.5`, `1.5, 2.5`, `1.5 ,2.5`), EL SISTEMA entregará al
  programa el punto (x, y).
- **RF-2** (ubicuo): EL SISTEMA aceptará en cada número el punto como único separador decimal, un
  signo delante y un exponente (`-1.5e3`, `.5`, `5.`).
- **RF-3** (evento): CUANDO se pulse Intro con `@dx,dy` (los dos números con las reglas de RF-1 y
  RF-2) y haya un punto de referencia, EL SISTEMA entregará el punto de referencia más (dx, dy).
- **RF-4** (evento): CUANDO se pulse Intro con `@d<a` (d y a con las reglas de RF-2) y haya un punto
  de referencia, EL SISTEMA entregará el punto a distancia d en la dirección a, como en la spec 004.

Lo que se rechaza:

- **RF-5** (no deseado): SI lo escrito separa los números con un espacio solo (`1.5 2.5`) o con un
  punto y coma (`1.5; 2.5`), ENTONCES EL SISTEMA no entregará ningún punto y dirá en la barra de
  estado cómo se escribe un punto.
- **RF-6** (no deseado): SI un número lleva una coma decimal (`1,5; 2,5`, `1,5 2,5`, `1,5,2,5`,
  `@1,5<30`), ENTONCES EL SISTEMA no entregará ningún punto y dirá en la barra de estado cómo se
  escribe un punto.
- **RF-7** (no deseado): SI lo escrito tiene más o menos de una coma entre dos números (`1.5`,
  `1.5,2.5,3.5`, `1.5,,2.5`, `,2.5`, `1.5,`), ENTONCES EL SISTEMA no entregará ningún punto y dirá
  en la barra de estado cómo se escribe un punto.
- **RF-8** (ubicuo): EL SISTEMA seguirá rechazando, con los mismos motivos y comportamiento que en
  la spec 004, un relativo o un polar sin punto de referencia (RF-8 de la 004), un número no finito
  (RF-9 de la 004) y lo que no es un punto. Lo rechazado se queda en la entrada (RF-10 de la 004).

Lo que se ve:

- **RF-9** (ubicuo): EL SISTEMA dirá, en el motivo de rechazo y en la ayuda de la entrada, en inglés
  y en español, que las coordenadas se separan con una coma y los decimales con un punto, sin
  mencionar la coma decimal.
- **RF-10** (ubicuo): EL SISTEMA mantendrá el texto guía `x, y · @dx, dy · @d<a`.

Compatibilidad:

- **RF-11** (ubicuo): EL SISTEMA seguirá entregando el punto por la misma señal que hoy, y lo que se
  escribe con punto decimal y coma de separador dará el mismo punto que en la 0.1.4.

## Requisitos no funcionales

- Inglés y español: los textos que cambian, con su traducción (regla 2).
- Capas: sin el núcleo ni ningún programa (regla 10).
- Las tres plataformas de la CI.

## Diseño

- **D-7, entradas tolerantes, nunca silenciosas**: se acepta lo que no es ambiguo y se rechaza lo
  demás con un motivo que dice cómo escribirlo. La coma ya no se acepta como decimal: la
  propietaria decide que una coma que puede ser dos cosas se presta a confusión. **D-7 se enmienda**
  (ver abajo), como D-12 con la spec 002.
- **D-6**: los mensajes son cortos, en presente y con la notación del oficio (`x, y`, `@dx, dy`,
  `@d<a`).
- **D-14**: lo rechazado se queda en la entrada para corregirlo.

**Enmienda de D-7** (`spec/constitution/referencias-de-diseno.md`), con la aprobación de esta spec.
Hoy dice: «Se acepta lo que no es ambiguo (espacios, coma o punto decimal, `12.5, 3.2` o `12.5 3.2`
en la entrada X,Y de la barra de estado)». Pasa a decir que el separador decimal es siempre el punto
(spec 005) y que en la entrada X,Y la coma separa las coordenadas (`12.5, 3.2`). Lleva la nota
«Enmendado el 2026-11-28 con la spec 006».

Lista de comprobación (se marca al validar):

**Toda pieza**
- [x] No importa el núcleo ni ningún programa.
- [x] Sus textos pasan por `tr()` y tienen su español en `i18n/es.py`; no queda ningún texto que
      hable de la coma decimal.
- [x] Probada sin pantalla, sin `exec()` y sin dejar estado (regla 5).

**Entrada**
- [x] Acepta lo no ambiguo (`x.x,x.x`) y rechaza lo demás con un motivo que dice cómo escribirlo.
- [x] El texto guía se lee entero, en los dos idiomas y en los dos temas.

**Texto**
- [x] Corto, en presente, sin claves internas ni signos de exclamación.

**Y siempre**
- [x] Ninguno de los patrones de «Lo que no se hace».

No aplica: colores, iconos, diálogos, acciones de menú, proceso largo.

## Qué cambia para los programas

**Incompatible**: sube el segundo número, a la **0.2.0**. Lo que deja de leerse:

- la coma decimal: `1,5; 2,5`, `1,5 2,5`, `1,5, 2,5`, `@1,5<30`;
- el espacio solo y el punto y coma como separadores: `12.5 3.2` y `12.5;3.2`. Se aceptaban desde
  la 0.1.0, y RF-16 de la spec 004 los mantenía.

Lo que no cambia: `1.5,2.5`, `1.5, 2.5`, `3,4`, `@dx,dy` con punto decimal y `@d<a`, por la misma
señal.

- **OGR FEM2D**: el aviso de margen es el escrito que recibe antes de que se etiquete la 0.2.0.
  Al subir la fijación:
  - sus tests de `read_point` (el contrato de la v0.1.3, que aceptan la coma) cambian a este
    criterio;
  - su ayuda, si da la suya, deja de hablar de la coma decimal y del punto y coma.
- **OGR Slip2D y OGR Data**, cuando adopten el paquete: la entrada lee solo `x.x,x.x`.

## Casos límite

- `3,4`: el punto (3, 4), como hoy.
- `1.5 , 2.5` y `  1.5,2.5  `: valen (espacios alrededor de la coma y al principio y al final).
- `-1.5,-2.5` y `1e3,2E-3`: valen.
- `1.5,2.5,3.5`: tres números, se rechaza (RF-7).
- `1,5,2,5`: se rechaza (RF-6), como hoy, con el mismo motivo.
- `1.5;2.5`, `1.5 2.5`: se rechazan (RF-5), aunque no sean ambiguos: la propietaria quiere una sola
  forma.
- `@ 1.5 , 2`: espacios después de `@` y alrededor de la coma, valen.
- `@1.5<30` vale. `@1,5<30` se rechaza (RF-6).
- La entrada vacía: Intro no hace nada, como hoy.
- Un `1,5` escrito pensando en «uno y medio» da el punto (1, 5), sin aviso. Es lo que dice el
  criterio: la coma separa. Es la única lectura posible y no es ambigua.

## Fuera de alcance

- Las casillas numéricas y lo que se escribe en pantalla: ya los cubre la spec 005.
- Pasar el punto a las unidades del modelo y el enganche sobre un punto escrito: son del programa.
- Expresiones, unidades escritas, historial de puntos, coordenadas absolutas frente a relativas con
  otro prefijo (lo mismo que en la spec 004).
- Una versión de margen que avise y siga aceptando lo de hoy: la propietaria la descarta.

## Criterios de finalización

- Todos los RF con su test en verde y la suite entera en verde en las tres plataformas de la CI.
- La lista de diseño marcada y D-7 enmendado.
- El changelog de la 0.2.0 dice qué se encontró, qué deja de leerse y qué tiene que cambiar FEM2D.
- El escrito a FEM2D, antes de la etiqueta.
- `docs/consumidores.md` y `roadmap.md` al día.

## Dudas abiertas

- Ninguna.

## Validación

2026-11-28, en la rama `dev/006-coma-separa-coordenadas`. Suite entera sin filtrar: **549 casos,
549 en verde, sin fugas**, en serie y con `--jobs 4` (Windows). Los tests son de
`tests/test_coordinate_comma_v020.py` salvo donde se dice.

| RF | Test que lo cubre | Resultado |
|---|---|---|
| RF-1 | `TestWhatIsRead.test_one_comma_with_or_without_spaces`; `TestTheEntryInTheBar.test_a_point_with_a_comma_is_handed_over` | verde |
| RF-2 | `TestWhatIsRead.test_the_numbers`; `TestTheReaderReadsNumbersAsTheBoxesDo` | verde |
| RF-3 | `TestWhatIsRead.test_a_relative_point` | verde |
| RF-4 | `TestWhatIsRead.test_a_polar_point`; `test_point_entry_v013::TestARelativePoint.test_polar_identities` y `test_polar_forms` | verde |
| RF-5 | `TestWhatIsRefused.test_a_lone_space_or_a_semicolon`; `TestTheEntryInTheBar.test_a_decimal_comma_stays_with_its_reason` | verde |
| RF-6 | `TestWhatIsRefused.test_a_decimal_comma`; `TestTheEntryInTheBar.test_a_decimal_comma_stays_with_its_reason` | verde |
| RF-7 | `TestWhatIsRefused.test_more_or_fewer_than_one_comma` | verde |
| RF-8 | `TestWhatIsRefused.test_what_was_refused_still_is`; `test_point_entry_v013::TestWhatIsRefused` y `TestARefusalSaysWhyAndKeepsTheText` | verde |
| RF-9 | `TestWhatIsSaid.test_the_reason_and_the_help`, `test_their_spanish`, `test_no_word_of_a_decimal_comma`; `test_status_bar_v010::test_its_texts_are_translated` | verde |
| RF-10 | `TestWhatIsSaid.test_the_placeholder_is_the_same`; `test_point_entry_v013::TestWhatTheEntryShows.test_the_whole_placeholder_in_both_themes` | verde |
| RF-11 | `TestWhat014TookWithAPoint.test_the_same_point_to_the_bit`; `test_point_entry_v013::TestTheEntryHandsOverAnAbsolutePoint.test_the_old_signal_of_the_entry_too`; `test_status_bar_v010::test_every_separator_gives_the_same_point_to_the_bit` | verde |

Lista de diseño: marcada arriba, mirando la pieza. Capturas sin pantalla
(`QT_QPA_FONTDIR=C:/Windows/Fonts`) de la barra a 1366 px, en inglés y en español y en los dos temas.
Con la entrada vacía, el texto guía se lee entero. Con `1,5; 2,5` e Intro, el texto se queda en la
entrada y la barra dice «Write a point as x, y with a decimal point (1.5, 2.5), …» / «Escribe un
punto como x, y con punto decimal (1.5, 2.5), …», entero. Ningún principio falla.

CI de la [PR #8](https://github.com/samuelsl27/OGR-GUI/pull/8): en verde en Linux y Windows (Python
3.11, 3.12 y 3.13), en macOS (3.12) y la licencia.

La suite entera de OGR FEM2D (`000ee03`) contra este árbol, con `--jobs 4`: 857 casos, 852 en
verde. Los cinco que fallan son los esperados:

- `test_gui_tools_v0014::TestTypedPoints::test_what_each_form_means`, que fija la coma decimal y el
  espacio de la v0.1.3;
- `test_gui_tools_v0014::TestTheWindowsTools::test_typed_points_table_circle_and_arc` (`"0; 20"`) y
  `test_gui_case006_v0014::TestCase006ByTheWindow::test_the_model_is_the_cases` (`"1; 0"`): escriben
  un punto con punto y coma;
- `test_gui_interpret_v0015::TestTheDefaultPalette::test_its_lightness_grows_with_the_value`, que
  usa `ContourSettings.automatic` como ejemplo de paleta divergente. Lo rompe la gemela de Viridis,
  que pidió la propietaria con T1, no esta spec;
- `test_the_installed_one`, que fija la v0.1.3.

Los cuatro primeros están en el aviso a FEM2D y en el changelog, con lo que cambia cada uno.

