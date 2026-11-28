# Plan 006 — En la entrada X,Y, la coma separa y el punto es el decimal

Sin código. Cada apartado dice qué RF cubre.

## Lo que se encontró al leer el código

- **El lector** es `ogr_ui/point_entry.py`, sin Qt (spec 004):
  - `_pair` parte los dos números por `;`, por espacios (con una coma pegada al primero) o por una
    sola coma sin espacios;
  - `_number` acepta `[.,]` como decimal;
  - el polar usa el mismo `_number`.

  Es lo único que lee. La entrada (`_CoordInput` en `widgets/status_bar.py`) solo llama a
  `read_point` y muestra el motivo.
- **Ya está escrito `x.x,x.x`**: `1.5,2.5`, `1.5, 2.5` y `@1.5,2` se aceptan hoy. Lo que cambia es
  quitar los otros separadores y la coma decimal.
- **Dos textos hablan de la coma decimal**: el motivo `WRITE_A_POINT` («Write a point as x, y (or
  x; y with decimal commas), …») y la ayuda de la entrada («Type a point and press Enter: x, y (or
  x; y with decimal commas), …»), con su español en `i18n/es.py`. La nota del módulo de
  `status_bar.py` dice «the decimal comma».
- **Tests que dicen lo contrario de la spec**. Cambian a propósito, cada uno con su porqué:
  - `tests/test_point_entry_v013.py`: `test_every_separator`, `test_one_comma_with_no_space_separates`
    (`3,4 5`), `test_the_numbers`, `test_what_010_took_gives_the_same_point`, `test_by_a_shift`
    (`@-1,5; 2,5`), `test_each_form_by_the_keyboard`, `test_the_old_signal_of_the_entry_too`
    (`12.5;3.2`), y las constantes `WRITE_A_POINT` y `HELP`;
  - `tests/test_status_bar_v010.py::test_every_separator_gives_the_same_point_to_the_bit`, que
    entrega `12.5 3.2` y `12.5;3.2`.

  Siguen igual: `test_every_character_can_be_typed` (se escribe todo, se lee al pulsar Intro), el
  texto guía y los rechazos que ya eran rechazos.

## Decisiones

| Decisión | Alternativa descartada y por qué | RF |
|---|---|---|
| `_pair` parte por comas: tiene que haber **exactamente una**, y cada lado, sin los espacios de alrededor, es un número. Sin coma, o con más de una, se rechaza con `WRITE_A_POINT` | Mantener `;` y el espacio como separadores con punto decimal: la propietaria eligió «solo la coma» | RF-1, RF-5, RF-7 |
| Cada número se lee con `ogr_ui.numbers.read_number` (spec 005: signo, cifras, un punto, exponente; sin coma, sin `nan` ni `inf`). El lector y las casillas leen así igual. El error se convierte en el `PointEntryError` del sitio (`WRITE_A_POINT` o `WRITE_A_POLAR`) | Dejar el `_NUMBER` propio sin la coma: dos expresiones de lo mismo acaban distintas, que es lo que la 005 quiso evitar | RF-2, RF-6, RF-8 |
| El polar (`@d<a`) no cambia salvo el lector de números: `@1,5<30` se rechaza con `WRITE_A_POLAR`, porque no es un polar bien escrito | Un motivo propio para la coma decimal: ver la fila siguiente | RF-4, RF-6 |
| **Un solo motivo** para todo lo que no es un punto, `WRITE_A_POINT`, con el texto nuevo: «Write a point as x, y with a decimal point (1.5, 2.5), @dx, dy or @distance<angle.» | Un motivo aparte para la coma decimal («use a point for decimals»): `1,5,2,5` no se puede distinguir de tres números mal escritos, y el motivo general ya enseña la forma con un ejemplo (D-7, que dice qué falta) | RF-5, RF-6, RF-7, RF-9 |
| La ayuda pasa a «Type a point and press Enter: x, y with a decimal point, @dx, dy from the last point, or @distance<angle in degrees.» | Dejar la ayuda y cambiar solo el motivo: diría lo contrario de lo que se acepta | RF-9 |
| Los textos viejos salen de `es.py` y entran los nuevos con su español; la nota del módulo de `status_bar.py` se corrige | — | RF-9 |
| El texto guía no cambia (`x, y · @dx, dy · @d<a`): ya escribe la coma como separador | — | RF-10 |
| La versión pasa a **0.2.0** (`0.2.0.dev0` en la rama) | 0.1.5: la regla 8 pide subir el segundo número en un cambio incompatible | — |

## Módulos

Dentro de `ogr_ui`, sin importar el núcleo ni ningún programa:

- `ogr_ui/point_entry.py`: `_pair` y `_number` con el criterio nuevo, `WRITE_A_POINT` nuevo, la nota
  del módulo; importa `ogr_ui.numbers`, que no tiene Qt.
- `ogr_ui/widgets/status_bar.py`: la ayuda y la nota del módulo.
- `ogr_ui/i18n/es.py`: dos textos que salen y dos que entran (abajo).
- `tests/test_coordinate_comma_v020.py`: nuevo, con los RF de esta spec.
- `tests/test_point_entry_v013.py` y `tests/test_status_bar_v010.py`: los tests de arriba, cambiados
  a propósito.
- `docs/changelog/PENDIENTE_v0.2.0.md`, `docs/consumidores.md`, `roadmap.md`; la versión.
- El escrito a FEM2D, `GUI/notas/2026_11_28_aviso_a_fem2d_coma_separa_coordenadas.md`, antes de
  etiquetar.

Textos, con su español:

| Inglés (la clave) | Español |
|---|---|
| Write a point as x, y with a decimal point (1.5, 2.5), @dx, dy or @distance<angle. | Escribe un punto como x, y con punto decimal (1.5, 2.5), @dx, dy o @distancia<ángulo. |
| Type a point and press Enter: x, y with a decimal point, @dx, dy from the last point, or @distance<angle in degrees. | Escribe un punto y pulsa Intro: x, y con punto decimal, @dx, dy desde el último punto, o @distancia<ángulo en grados. |

## Interfaces

Ninguna nueva: `read_point(texto, referencia)`, `PointEntryError`,
`OgrStatusBar.set_point_reference` y `manual_coords_submitted` siguen con la misma firma.

```text
read_point("1.5,2.5")       -> (1.5, 2.5)
read_point(" 1.5 , 2.5 ")   -> (1.5, 2.5)
read_point("3,4")           -> (3.0, 4.0)
read_point("@1.5,2", (1,1)) -> (2.5, 3.0)
read_point("1,5; 2,5")      -> PointEntryError("Write a point as x, y with a decimal point (1.5, 2.5), …")
read_point("1.5 2.5")       -> PointEntryError(el mismo)
read_point("@1,5<30", ref)  -> PointEntryError("Write a polar point as @distance<angle, …")
```

## Compatibilidad

**Incompatible: 0.2.0.** Un programa en la 0.1.x no cambia nada hasta que suba su fijación.

- Sigue igual: `x.x,x.x` con o sin espacios, `3,4`, `@dx,dy` con punto decimal, `@d<a`, la señal, la
  referencia, el texto guía y lo rechazado que se queda.
- Deja de leerse: la coma decimal, el espacio solo y el punto y coma.
- `read_point` lanza `PointEntryError` en esos casos, en vez de devolver el punto. FEM2D lo usa en
  sus tests, que cambian.

## Estrategia de tests

- **El lector solo**, en `tests/test_coordinate_comma_v020.py`:
  - cada forma de RF-1, RF-2 y RF-3;
  - cada rechazo de RF-5, RF-6 y RF-7, con su motivo;
  - el polar con punto, y `@1,5<30` rechazado;
  - lo que la 0.1.4 aceptaba con punto y coma de separador, al bit (RF-11).
- **La entrada en una barra de una ventana del test**, con el teclado de `QTest`:
  - `1.5,2.5` + Intro da el punto y vacía la entrada;
  - `1,5; 2,5` + Intro deja el texto y el motivo nuevo en la barra, en inglés y en español.
- **Los textos**: el motivo y la ayuda, en los dos idiomas, sin «decimal comma» ni «coma decimal»
  (RF-9). `test_i18n_v010` y `test_text_census_v010` en verde.
- **Estado restaurado**: el idioma y las ventanas, como en la spec 004 (regla 5).
- **Plataformas**: nada depende de ellas; la CI de las tres.

## Riesgos

- **Un `1,5` pensado como «uno y medio» da (1, 5) sin aviso.** Es lo que dice la spec (casos
  límite): la coma solo puede separar. No hay forma de distinguirlo sin adivinar.
- **Los tests de FEM2D contra este árbol fallarán** en sus casos de `read_point` con coma decimal.
  Se esperan y se listan en la validación. No se cambia FEM2D desde aquí.
