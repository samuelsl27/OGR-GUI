# Plan 004 — La entrada X,Y con relativos, polares y coma decimal

Sin código. Cada apartado dice qué RF cubre.

## Lo que se encontró al leer el código

- **La entrada** (`ogr_ui/widgets/status_bar.py`, `_CoordInput`) es un `QLineEdit` con un validador
  de expresión regular (solo `-?d(.d)? sep -?d(.d)?`) y un `_submit` que parte el texto y emite
  `coords_submitted(x, y)`. La barra (`OgrStatusBar`) la expone como `coord_input` y reenvía la
  señal como `manual_coords_submitted`. El validador impide escribir `@`, `<` y la letra `e` de un
  exponente: por eso FEM2D lo quita.
- **Lo que se rechaza hoy no se dice**: `_submit` vuelve sin nada si no hay dos números (D-7, «nunca
  silenciosas», no se cumple).
- **El lector de FEM2D** (`ogr_fem2d/gui/canvas/tools.py`, `parse_point`, `_pair`, `_NUMBER`) ya
  hace lo que piden RF-1–RF-9 y no depende de Qt. Sus reglas son las de la spec; sus mensajes, en
  inglés para `tr()`. Se toman sus reglas, no su código: es de FEM2D y nombra «vertex».
- **Dos tests de la 0.1.0 dicen lo contrario de la spec**, y cambian a propósito:
  - `test_a_letter_is_refused_and_one_number_gives_nothing` espera que `x` no se pueda escribir y
    que la entrada quede vacía. Con RF-15 y RF-10, `x` se escribe, se rechaza al pulsar Intro y se
    queda.
  - `test_its_texts_are_translated` busca la ayuda de Slip2D, que se va (RF-13).
- **El texto guía** `x, y` está en `EXCEPTIONS` de `tests/test_i18n_v010.py` como notación. Pasa a
  ser `x, y · @dx, dy · @d<a`, con la misma razón.
- **El ancho**: la entrada mide como mucho 130 px, y el texto guía nuevo no cabe. Si crece, la barra
  deja menos sitio a los mensajes (`message_room`, que un test de la 0.1.0 pide mayor de 200 px a
  1366 px de ancho).

## Decisiones

| Decisión | Alternativa descartada y por qué | RF |
|---|---|---|
| El lector es una función sin Qt en un módulo nuevo, `ogr_ui/point_entry.py`: `read_point(texto, referencia)` devuelve `(x, y)` o lanza `PointEntryError` con el mensaje en inglés, la clave de `tr()` | Leer dentro del `QLineEdit`: no se probaría sin un widget, y un programa no podría usarlo en otro campo (la tabla de coordenadas de FEM2D) | RF-1–RF-9 |
| Las reglas de RF-1 y RF-2, por este orden: con `;`, se parte por `;`; si no, por espacios, y una coma pegada al final del primer trozo es parte del separador; si queda un solo trozo con una sola coma, se parte por la coma. Cada trozo tiene que ser un número entero (signo, dígitos con punto o coma decimal, exponente) | Adivinar por el número de comas o por el idioma activo: `1,5,2,5` tendría dos lecturas, y lo que se acepta dependería del idioma (casos límite) | RF-1, RF-2, RF-7 |
| Un número que da no finito al leerse (`1e999`) se rechaza con el mensaje de RF-7; `nan` e `inf` ya no son números para la regla | Aceptarlos: el programa recibiría un punto que no puede dibujar | RF-9 |
| El polar, con el coseno y el seno del ángulo en radianes, y cada uno a cero exacto si su valor absoluto es menor que 1e-15 | Sin el redondeo: `@1<90` daría x + 6e-17, que no engancha con el punto de al lado | RF-4 |
| La referencia la da el programa con `OgrStatusBar.set_point_reference(punto o None)`, que la pasa a la entrada; una referencia no finita se rechaza con `ValueError` al darla | Que la entrada pida la referencia al programa con una señal en cada Intro: obliga a responder en el mismo ciclo y no se puede probar sin él | RF-5, RF-8 |
| Tres mensajes de rechazo, cortos y con la notación: el de cómo se escribe un punto, el de un polar mal escrito, y el de un relativo sin referencia | Uno solo para todo: `@1<` no diría qué le falta (D-7) | RF-7, RF-8, RF-9 |
| La entrada emite `point_refused(texto traducido)`, y la barra lo muestra con `showMessage` sin tiempo (lo sustituye el mensaje siguiente) | Un tiempo fijo: el motivo desaparecería mientras se corrige; un diálogo: no se abre un modal por un número mal escrito (D-8) | RF-7, RF-8, D-5 |
| Sin validador: se escribe cualquier carácter y la entrada solo lee al pulsar Intro | Un validador más ancho: rechazaría `@1<` a medio escribir, o dejaría pasar lo ambiguo; de las dos formas, sin decir por qué | RF-15 |
| La entrada se ensancha lo justo para el texto guía entero con su fuente y sus márgenes, medido con las métricas de la fuente, no con un número fijo de píxeles | Un ancho fijo mayor: depende de la fuente de cada plataforma | RF-14 |
| La ayuda general, una frase por `tr()`, con su español; el programa la cambia con `setToolTip` como cualquier widget | Un argumento nuevo para la ayuda: ya se puede, y no hace falta otra interfaz | RF-13 |
| Se conservan `coords_submitted(float, float)` y `manual_coords_submitted(float, float)` | Una señal nueva con el punto: rompería a quien ya escucha la de siempre | RF-16 |

## Módulos

Dentro de `ogr_ui`, sin importar el núcleo ni ningún programa:

- `ogr_ui/point_entry.py` — nuevo, sin Qt: `read_point`, `PointEntryError`, y los textos de sus
  mensajes.
- `ogr_ui/widgets/status_bar.py` — `_CoordInput` sin validador, con `read_point`, la referencia,
  `point_refused`, la ayuda nueva, el texto guía y su ancho; `OgrStatusBar.set_point_reference` y el
  mensaje del rechazo; la nota del módulo, que hoy habla de «a boundary drawing».
- `ogr_ui/i18n/es.py` — cuatro textos nuevos (abajo); sale la ayuda de Slip2D.
- `tests/test_point_entry_v013.py` — nuevo.
- `tests/test_status_bar_v010.py` — los dos tests de la 0.1.0 que cambian.
- `tests/test_i18n_v010.py` — `EXCEPTIONS`, con el texto guía nuevo.
- `docs/changelog/PENDIENTE_v0.1.3.md`, `docs/consumidores.md`, `roadmap.md`; la versión a
  `0.1.3.dev0`.

Textos nuevos, con su español:

| Inglés (la clave) | Español |
|---|---|
| Write a point as x, y (or x; y with decimal commas), @dx, dy or @distance<angle. | Escribe un punto como x, y (o x; y con coma decimal), @dx, dy o @distancia<ángulo. |
| Write a polar point as @distance<angle, with the angle in degrees. | Escribe un punto polar como @distancia<ángulo, con el ángulo en grados. |
| A relative point needs a first point: give it as x, y. | Un punto relativo necesita un primer punto: escríbelo como x, y. |
| Type a point and press Enter: x, y (or x; y with decimal commas), @dx, dy from the last point, or @distance<angle in degrees. | Escribe un punto y pulsa Intro: x, y (o x; y con coma decimal), @dx, dy desde el último punto, o @distancia<ángulo en grados. |

## Interfaces

```text
bar = OgrStatusBar(window)
bar.manual_coords_submitted.connect(on_point)       # como hoy: siempre un punto absoluto

bar.set_point_reference((10.0, 5.0))               # el último vértice, en las unidades mostradas
# «@2, 0» + Intro      -> on_point(12.0, 5.0)
# «@2<90» + Intro      -> on_point(10.0, 7.0)
# «1,5; 2,5» + Intro   -> on_point(1.5, 2.5)
# «1,5,2,5» + Intro    -> ningún punto; la barra dice «Write a point as x, y (…)»; el texto se queda

bar.set_point_reference(None)                      # sin referencia: «@…» se rechaza con su motivo

from ogr_ui.point_entry import read_point, PointEntryError   # el lector, para otro campo
read_point("@3<0", (1.0, 1.0))                     # (4.0, 1.0)
```

## Compatibilidad

**Compatible** (0.1.3). Lo que la 0.1.0 aceptaba da el mismo punto por la misma señal (RF-16). Lo
que cambia para un programa que fija la 0.1.2:

- la entrada deja escribir cualquier carácter y dice por qué rechaza;
- su ayuda es otra, y la entrada es más ancha;
- sin `set_point_reference`, un relativo se rechaza con su motivo.

FEM2D puede quitar su rodeo (`_typed_points` y `_typed` de su ventana) y su lector, o conservar su
lector para la tabla de coordenadas. Si conserva el rodeo, sigue funcionando: quita un validador que
ya no está y desconecta la respuesta a Intro. Eso último lo comprueba su suite contra este árbol
antes de etiquetar.

## Estrategia de tests

`tests/test_point_entry_v013.py`:

- **El lector solo, la regla 1 con identidades escritas a mano**: cada forma de RF-1 da (1,5, 2,5) o
  el punto que dice el caso límite; `@2<60` desde (1, 1) da (2, 1 + √3) con √3 escrito; `@1<90` da
  exactamente (x, y + 1), y `@1<180` exactamente (x − 1, y); `@-1<45` y un ángulo de 405.
- **RF-7–RF-9**: `1,5,2,5`, `1,5,2.5`, `abc`, un número solo, tres números, `@1<`, `@<2`, `1e999`,
  `nan`, `inf`. Cada uno lanza con el mensaje que le toca, y el mensaje es una clave con su español.
- **RF-16**: lo que la 0.1.0 aceptaba (`12.5, 3.2`, `12.5 3.2`, `12.5;3.2`, `-1.25, -2.5`) da lo
  mismo, al bit.
- **La entrada en una barra de un `QMainWindow` del test**: Intro con cada forma emite el punto y
  vacía (RF-11); un rechazo no emite, deja el texto y la barra dice el motivo, en inglés y en
  español (RF-7, RF-8, RF-10); vacía no hace nada (RF-12); la referencia dada, cambiada y quitada
  (RF-5); `@`, `<` y `e` se escriben con el teclado (`QTest.keyClicks`) (RF-15).
- **RF-13, RF-14**: la ayuda, en los dos idiomas, sin «boundary», «polyline» ni «vertex»; el texto
  guía cabe entero (su ancho con la fuente de la entrada, más los márgenes, no pasa del de la
  entrada); a 1366 px la barra sigue dejando más de 200 px a los mensajes.
- **Los dos temas**: la entrada no pone colores; se comprueba el ancho en los dos.
- **Plataformas**: el ancho depende de la fuente, y por eso se mide y no se fija; la CI en las tres.
- **Regla 5**: el idioma y la referencia se restauran; la barra es del test y se borra.
- **Las de siempre**: el censo de textos (los cuatro nuevos, con su español), `test_layering_v010`
  (`point_entry.py` no importa Qt ni el núcleo).

## Diseño

- **D-7**: lo no ambiguo se acepta y lo ambiguo se rechaza con el mensaje que dice cómo escribirlo.
- **D-5, D-14**: el motivo, en la barra hasta el mensaje siguiente; el texto, en la entrada.
- **D-6**: cuatro frases cortas, en presente, con la notación (`@dx, dy`, `@d<a`).

## Riesgos

- **Que FEM2D rompa al subir**: su `returnPressed.disconnect()` desconecta también lo nuevo, y su
  lector sigue funcionando. Se comprueba con su suite contra este árbol; el changelog le dice qué
  puede quitar.
- **Que la entrada más ancha le quite sitio a los mensajes** a 1366 px: el test de la 0.1.0 lo
  vigila, y uno nuevo lo mide con el texto guía.
- **Que un programa espere que el texto rechazado se borre**, como antes: lo dice el changelog.
