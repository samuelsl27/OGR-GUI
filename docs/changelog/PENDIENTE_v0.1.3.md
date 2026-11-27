# OGR GUI 0.1.3 — (sin fecha: se pone al etiquetar)

Un cambio compatible, la [spec 004](../../spec/features/004-entrada-xy/spec.md), que pidió OGR
FEM2D el 2026-11-25: la entrada X,Y de la barra de estado lee relativos, polares y la coma decimal,
y dice por qué rechaza lo que no puede leer.

## 1. Qué cambia

| Pieza | 0.1.2 | 0.1.3 |
|---|---|---|
| `ogr_ui/point_entry.py` | — | nuevo, sin Qt: `read_point(texto, referencia)` da el punto absoluto o lanza `PointEntryError` con el motivo (la clave inglesa de `tr()`); `as_reference` comprueba un punto de referencia |
| Lo que lee la entrada | `x, y`, `x y`, `x;y`, con punto decimal | además la coma decimal (`1,5; 2,5`, `1,5 2,5`), el signo y el exponente, `@dx, dy` y `@distancia<ángulo` (grados desde +x, en sentido antihorario) |
| La referencia del relativo | — | `OgrStatusBar.set_point_reference(punto o None)`; sin ella, un relativo se rechaza con su motivo |
| Lo que no se puede leer | se descartaba sin decir nada, y la entrada quedaba vacía | se queda en la entrada; la barra dice por qué (`point_refused`) hasta el mensaje siguiente, en inglés o en español |
| El validador | no dejaba escribir `@`, `<` ni la `e` de un exponente | no hay: se lee al pulsar Intro |
| La ayuda | «While drawing a boundary… in-progress polyline» (de Slip2D) | una general, con las tres formas, que no nombra nada de un programa |
| El texto guía | `x, y` | `x, y · @dx, dy · @d<a`, entero: la entrada mide lo que necesita con su fuente (antes, 130 px como mucho) |
| Las señales | `coords_submitted`, `manual_coords_submitted` | las mismas, con el punto absoluto |
| `i18n/es.py` | 72 entradas | 75: tres motivos y la ayuda nueva; sale la ayuda de Slip2D |

## 2. Qué se encontró

- **Lo que se rechazaba no se decía**: `_submit` volvía sin nada si no había dos números, y D-7
  («nunca silenciosas») no se cumplía.
- **El lector de FEM2D** (`ogr_fem2d/gui/canvas/tools.py`, `parse_point`) ya hacía lo que pide la
  spec y no dependía de Qt. Se tomaron sus reglas, no su código, que es de FEM2D y habla de
  «vertex». Se añadió que un número que no es finito al leerlo (`1e999`) se rechaza.
- **La ayuda era de Slip2D** (regla 10), y FEM2D la sustituía por la suya.
- **Sin fuentes, el ancho engaña.** Sin pantalla y sin `QT_QPA_FONTDIR`, cada letra es una caja
  ancha: la entrada mide 258 px en lugar de unos 80, y a 1366 px la barra deja 186 px a los mensajes
  con un tema puesto (292 sin tema); con las fuentes de Windows, 818 sin tema. Por eso el test no compara ese
  hueco con un número de píxeles cuando hay tema: comprueba que la entrada no pasa de lo que
  necesita su texto guía. El test de la 0.1.0 (más de 200 px sin tema) sigue igual y en verde.
- **Dos tests de la 0.1.0 cambian a propósito**, con su porqué en el test:
  - `test_a_letter_is_refused_and_one_number_gives_nothing`: una letra ya se escribe; al pulsar
    Intro se rechaza, se queda y la barra dice por qué.
  - `test_its_texts_are_translated`: la ayuda es la nueva.

## 3. Tests

`tests/test_point_entry_v013.py`, 30 casos:

- **El lector**: cada forma absoluta; los números (coma, signo, exponente, `.5`, `5.`); el relativo y
  el polar como identidades escritas a mano (`@2<60` desde (1, 1) da (2, 1 + √3); `@1<90`, `@1<180`,
  `@1<270` exactos; distancia negativa; 405°; −90°); lo que se rechaza, con su motivo; lo que la 0.1.0
  aceptaba, al bit.
- **La entrada**, con el teclado en una barra de una ventana del test: cada forma, la señal de
  siempre, la referencia dada, cambiada y quitada, los rechazos en inglés y en español, y la entrada
  vacía.
- **Lo que se ve**: la ayuda en los dos idiomas, el texto guía entero en los dos temas, y el sitio
  de los mensajes.

`test_i18n_v010.py`: `EXCEPTIONS` tiene el texto guía nuevo, como notación.

## 4. Qué tiene que hacer un programa

Nada, si no escribe relativos: lo que la 0.1.0 aceptaba da el mismo punto por la misma señal.
Puede notar que la entrada es más ancha, que deja escribir cualquier carácter, y que lo rechazado
se queda con su motivo en la barra en lugar de borrarse.

- **OGR FEM2D**:
  - puede quitar su rodeo de la entrada (`_typed_points` y `_typed` de su ventana: el validador, el
    `returnPressed.disconnect()` y su texto guía);
  - da el punto de referencia con `statusBar().set_point_reference(...)` cada vez que cambia (el
    último vértice, o el centro de un círculo), en las unidades mostradas;
  - recibe el punto absoluto por `manual_coords_submitted`, y lo pasa a las unidades del modelo
    como hoy;
  - puede usar `ogr_ui.point_entry.read_point` en su tabla de coordenadas, o seguir con su lector.

  Si no cambia nada, su rodeo sigue funcionando: quita un validador que ya no hay y desconecta la
  respuesta a Intro de la entrada, la nueva incluida.
- **OGR Slip2D**, cuando adopte el paquete: la ayuda deja de hablar de su polilínea; puede dar la
  suya con `setToolTip`.
