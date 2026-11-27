# Spec 004 — La entrada X,Y con relativos, polares y coma decimal

> Estado: hecha (2026-11-27, v0.1.3)

## Contexto y objetivo

La entrada «Enter X,Y:» («Introducir X,Y:») de la barra de estado solo acepta un punto absoluto con
punto decimal: `12.5, 3.2`, `12.5 3.2` o `12.5;3.2`. Un programa que dibuja contornos necesita
además el punto relativo al anterior (`@dx, dy`), el polar desde él (`@distancia<ángulo`) y la coma
decimal del español. Si no, el ingeniero calcula a mano cada vértice. Hoy OGR FEM2D rodea la
entrada: le quita su validador y su respuesta a Intro, conecta su propio lector
(`ogr_fem2d/gui/canvas/tools.py`, `parse_point`, con sus tests) y le cambia la ayuda y el texto guía.
Esta spec trae ese comportamiento a la pieza para que ningún programa la rodee.

Lo pide la sesión de OGR FEM2D por escrito el 2026-11-25: es la tercera parte del escrito que dio
las specs 002 y 003 (`FEM2D/Promts_desarrollo/2026_11_24_peticion_ogr_gui_rango_entero.md`). Da sus
reglas, que son las de su spec 006 (D10 y D12). Decisiones de la propietaria (2026-11-27):

- el programa le da a la entrada el punto de referencia del relativo, y la entrada entrega siempre
  un punto absoluto;
- lo que no se puede leer se queda en la entrada y se dice por qué;
- entran también las dos cosas de la pieza que no cumplen las reglas: la ayuda es de Slip2D
  (regla 10) y el texto guía es solo `x, y`.

## Usuarios / actores

- OGR FEM2D, que dibuja contornos con puntos escritos y deja de rodear la entrada.
- OGR Slip2D y OGR Data, cuando adopten el paquete.
- El ingeniero que escribe un vértice en la barra de estado en vez de pulsar en el lienzo.

## Historias de usuario

- H1: Como ingeniero quiero escribir el vértice siguiente como desplazamiento o como distancia y
  ángulo desde el anterior, para no calcular sus coordenadas a mano.
- H2: Como ingeniero que trabaja con coma decimal quiero escribir `1,5; 2,5`, para no cambiar de
  costumbre al dibujar.
- H3: Como ingeniero quiero que lo que escribo mal se quede en la entrada con el motivo a la vista,
  para corregirlo sin volver a escribirlo.
- H4: Como programa de la suite quiero recibir siempre un punto absoluto, para no leer el texto yo
  mismo.

## Requisitos funcionales (EARS)

Lo que se acepta:

- **RF-1** (evento): CUANDO se pulse Intro con un punto absoluto escrito, EL SISTEMA entregará al
  programa ese punto (x, y). Se escribe con uno de estos separadores entre los dos números:
  - punto y coma (`1,5; 2,5`, `1.5;2.5`);
  - espacios, con o sin una coma justo antes (`1,5 2,5`, `1.5, 2.5`);
  - una sola coma sin espacios, y entonces el decimal es el punto (`1.5,2.5`, `3,4`).
- **RF-2** (ubicuo): EL SISTEMA aceptará en cada número el punto o la coma como separador decimal,
  un signo delante y un exponente (`-1,5e3`).
- **RF-3** (evento): CUANDO se pulse Intro con `@dx, dy` (los dos números con las reglas de RF-1) y
  haya un punto de referencia, EL SISTEMA entregará el punto de referencia más (dx, dy).
- **RF-4** (evento): CUANDO se pulse Intro con `@d<a` y haya un punto de referencia, EL SISTEMA
  entregará el punto a distancia d del de referencia, en la dirección del ángulo a. El ángulo va en
  grados, medido desde +x en sentido antihorario.
- **RF-5** (ubicuo): EL SISTEMA permitirá al programa dar el punto de referencia del relativo, o
  decir que no hay ninguno, en cualquier momento. Por defecto no hay ninguno.
- **RF-6** (ubicuo): EL SISTEMA aceptará espacios al principio, al final y alrededor de `@`, `<` y
  `;`.

Lo que se rechaza:

- **RF-7** (no deseado): SI lo escrito es ambiguo (`1,5,2,5`, `1,5,2.5`) o no es un punto (`abc`,
  tres números, un número solo), ENTONCES EL SISTEMA no entregará ningún punto. Dirá en la barra de
  estado cómo se escribe un punto.
- **RF-8** (no deseado): SI se escribe un relativo o un polar y no hay punto de referencia,
  ENTONCES EL SISTEMA no entregará ningún punto. Dirá en la barra de estado que un relativo
  necesita un primer punto, escrito como x, y.
- **RF-9** (no deseado): SI un número no es finito (`nan`, `inf`, un exponente que desborda),
  ENTONCES EL SISTEMA lo rechazará como en RF-7.
- **RF-10** (no deseado): SI se rechaza lo escrito, ENTONCES EL SISTEMA lo dejará en la entrada tal
  como estaba, para corregirlo.
- **RF-11** (evento): CUANDO se entregue un punto, EL SISTEMA vaciará la entrada, como hoy.
- **RF-12** (evento): CUANDO se pulse Intro con la entrada vacía, EL SISTEMA no hará nada, como hoy.

Lo que se ve:

- **RF-13** (ubicuo): EL SISTEMA dará a la entrada una ayuda general, en inglés y en español, con
  las tres formas que se pueden escribir, sin nombrar ningún programa ni ninguna herramienta. El
  programa podrá dar la suya.
- **RF-14** (ubicuo): EL SISTEMA mostrará en la entrada vacía el texto guía `x, y · @dx, dy · @d<a`,
  entero.
- **RF-15** (ubicuo): EL SISTEMA no impedirá escribir ningún carácter en la entrada: lo que no vale
  se rechaza al pulsar Intro (RF-7), con su motivo.

Compatibilidad:

- **RF-16** (ubicuo): EL SISTEMA seguirá entregando el punto por la misma señal que hoy, con los dos
  números, y lo que hoy se acepta dará el mismo punto.

## Requisitos no funcionales

- Inglés y español: los mensajes de rechazo y la ayuda, con su traducción (regla 2). El texto guía
  es notación y no se traduce.
- Capas: sin el núcleo ni ningún programa (regla 10). La entrada no sabe qué se dibuja; el punto
  de referencia y las unidades son del programa.
- Las tres plataformas de la CI.

## Diseño

- **D-7, entradas tolerantes, nunca silenciosas**: se acepta lo que no es ambiguo (coma o punto
  decimal, espacios, `;`). Lo ambiguo se rechaza con un mensaje que dice cómo escribirlo, y nada se
  adivina.
- **D-5 y D-14**: el motivo del rechazo, a la vista en la barra de estado, y el texto, en la
  entrada para corregirlo; nada se borra sin que la persona lo decida.
- **D-6**: los mensajes son cortos, en presente y con la notación del oficio (`@dx, dy`, `@d<a`,
  grados).
- **Regla 10**: la ayuda de hoy («While drawing a boundary… in-progress polyline») es de Slip2D.

Lista de comprobación (se marca al validar):

**Toda pieza**
- [x] No importa el núcleo ni ningún programa; el punto de referencia llega del programa.
- [x] Sus textos pasan por `tr()` y tienen su español en `i18n/es.py`; el texto guía, como
      notación, en la lista de excepciones con su porqué.
- [x] Probada sin pantalla, sin `exec()` y sin dejar estado (regla 5).

**Entrada**
- [x] Acepta lo no ambiguo y rechaza lo ambiguo con un mensaje que dice qué falta (D-7).
- [x] El texto guía se lee entero, en los dos idiomas y en los dos temas.

**Texto**
- [x] Corto, en presente, sin claves internas ni signos de exclamación.

**Y siempre**
- [x] Ninguno de los patrones de «Lo que no se hace».

No aplica: colores, iconos, diálogos, acciones de menú, proceso largo.

## Qué cambia para los programas

**Compatible** (sube el tercer número). Lo que hoy se acepta da el mismo punto por la misma señal
(RF-16). Un programa que no da un punto de referencia no recibe nunca un relativo: se rechaza con su
motivo (RF-8).

- **OGR FEM2D**:
  - puede dejar de quitar el validador y la respuesta a Intro, y de conectar su lector;
  - da el punto de referencia (el último vértice, o el centro de un círculo) cada vez que cambia;
  - recibe el punto absoluto por la señal de siempre;
  - su ayuda y su texto guía pueden irse, o quedarse si dicen algo de más;
  - los puntos van en las unidades que se muestran; pasarlos a las del modelo sigue siendo suyo.
- **OGR Slip2D**, cuando adopte el paquete: la ayuda deja de hablar de su polilínea. Puede dar la
  suya.

## Casos límite

- `3,4` y `1,5`: una sola coma sin espacios separa los dos números. Son los puntos (3, 4) y (1, 5),
  no el número 1,5 solo, como hoy. `3,4 5` son dos números, 3,4 y 5.
- `1,5, 2,5`: la coma pegada al primer número y seguida de espacio es el separador. Son 1,5 y 2,5.
- `-0`, `+1`, `.5`, `5.`: números válidos.
- `@0<90` y `@1<0`: distancia cero o ángulo cero son válidos. Un seno o un coseno que es casi cero
  da exactamente cero (`@1<90` es (x, y + 1), no (x + 6e-17, y + 1)).
- `@-1<45`: una distancia negativa es un punto en la dirección opuesta, como en el lector de FEM2D.
- Un ángulo de más de 360 o negativo: vale, se toma como es.
- `@ 1; 2`: espacios después de `@`, aceptados (RF-6).
- Un punto de referencia que el programa quita (`ninguno`) después de darlo: un relativo se rechaza
  desde ese momento.
- Dos Intros seguidos con lo mismo rechazado: el mismo motivo, sin más.
- Lo que se escribe en otro idioma activo: los números y los separadores se leen igual en inglés y
  en español; solo cambia el idioma del mensaje.

## Fuera de alcance

- Pasar el punto a las unidades del modelo: es del programa.
- El enganche (SNAP, ORTHO, OSNAP) sobre un punto escrito: el programa decide si aplica.
- Un punto relativo a algo que no sea el punto de referencia que da el programa (`#x, y` absoluto
  frente a relativo por defecto, coordenadas cilíndricas).
- Expresiones (`1+2`, `sqrt(2)`) y unidades escritas (`2 m`).
- Un historial de puntos escritos (flecha arriba).
- La tabla de coordenadas de FEM2D (`CoordinatesDialog`): es suya.

## Criterios de finalización

- Todos los RF con su test en verde y la suite entera en verde en las tres plataformas de la CI.
- La lista de diseño marcada.
- El changelog de la versión dice qué se encontró y qué puede quitar FEM2D.
- `docs/consumidores.md` y `roadmap.md` al día.

## Dudas abiertas

- Ninguna.

## Validación

2026-11-27, en la rama `dev/004-entrada-xy`, commit `bdf7add`. Suite entera sin filtrar: **497 casos,
497 en verde, sin fugas**, en serie y con `--jobs 4` (Windows). Los tests son de
`tests/test_point_entry_v013.py` salvo donde se dice.

| RF | Test que lo cubre | Resultado |
|---|---|---|
| RF-1 | `TestAnAbsolutePoint.test_every_separator`, `test_one_comma_with_no_space_separates`; `TestTheEntryHandsOverAnAbsolutePoint.test_each_form_by_the_keyboard` | verde |
| RF-2 | `TestAnAbsolutePoint.test_the_numbers` | verde |
| RF-3 | `TestARelativePoint.test_by_a_shift` | verde |
| RF-4 | `TestARelativePoint.test_polar_identities` y `test_polar_forms` (identidades escritas a mano, regla 1) | verde |
| RF-5 | `TestTheEntryHandsOverAnAbsolutePoint.test_the_reference_given_changed_and_taken_away` y `test_a_reference_that_is_not_a_point_is_refused_where_it_is_given`; `TestWhatIsRefused.test_a_reference_that_is_not_a_point` | verde |
| RF-6 | `TestAnAbsolutePoint.test_spaces_around`; `TestARelativePoint.test_by_a_shift` y `test_polar_forms` | verde |
| RF-7 | `TestWhatIsRefused.test_what_is_ambiguous_or_not_a_point`, `test_a_polar_point_written_wrong`; `TestARefusalSaysWhyAndKeepsTheText.test_in_english_and_in_spanish` | verde |
| RF-8 | `TestWhatIsRefused.test_a_relative_point_with_no_reference`; `TestARefusalSaysWhyAndKeepsTheText.test_in_english_and_in_spanish` | verde |
| RF-9 | `TestWhatIsRefused.test_what_is_not_finite` | verde |
| RF-10 | `TestARefusalSaysWhyAndKeepsTheText` (sus tres casos); `tests/test_status_bar_v010.py::test_a_letter_is_refused_and_one_number_gives_nothing`, cambiado a propósito | verde |
| RF-11 | `TestTheEntryHandsOverAnAbsolutePoint.test_each_form_by_the_keyboard` | verde |
| RF-12 | `TestTheEntryHandsOverAnAbsolutePoint.test_an_empty_entry_does_nothing` | verde |
| RF-13 | `TestWhatTheEntryShows.test_a_general_help_in_both_languages` y `test_a_program_gives_its_own`; `tests/test_status_bar_v010.py::test_its_texts_are_translated` | verde |
| RF-14 | `TestWhatTheEntryShows.test_the_whole_placeholder_in_both_themes` y `test_the_messages_keep_their_room_at_1366` | verde |
| RF-15 | `TestTheEntryHandsOverAnAbsolutePoint.test_every_character_can_be_typed` | verde |
| RF-16 | `TestAnAbsolutePoint.test_what_010_took_gives_the_same_point`; `TestTheEntryHandsOverAnAbsolutePoint.test_the_old_signal_of_the_entry_too`; `tests/test_status_bar_v010.py::test_every_separator_gives_the_same_point_to_the_bit`, sin tocar | verde |

Lista de diseño: marcada arriba, mirando la pieza. Capturas sin pantalla
(`QT_QPA_FONTDIR=C:/Windows/Fonts`) de la barra a 1366 px, en inglés y en español y en los dos temas:
el texto guía se lee entero con la entrada vacía (90 px); con `1,5,2,5` e Intro, el texto se queda
en la entrada y la barra dice «Write a point as x, y (…)» / «Escribe un punto como x, y (…)», con
734 px o más para los mensajes. Ningún principio falla.

CI de la [PR #3](https://github.com/samuelsl27/OGR-GUI/pull/3), commit `bdf7add`: en verde en Linux y
Windows (Python 3.11, 3.12 y 3.13) y en macOS (3.12), y la licencia.

La suite entera de OGR FEM2D contra este árbol (con `--jobs 4`): 829 casos, 827 en verde. Falla
`test_the_installed_one`, como tiene que fallar contra otro árbol. El otro,
`test_gui_bridge_v0015.py::TestTheDoor::test_a_wrong_token_and_turning_it_off` (con una fuga de un
archivo del puente), pasa solo, con este árbol y sin él: es del puente de FEM2D bajo carga, no de la
entrada. Su rodeo de la entrada sigue funcionando sin cambios.
