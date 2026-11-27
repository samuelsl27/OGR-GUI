# Tareas 004 — La entrada X,Y con relativos, polares y coma decimal

En orden de dependencia. Cada tarea ≤ 30 min, tests primero, y se marca `[x]` al terminarla con la
suite entera en verde. Una tarea cada vez.

- [x] **T1** El lector sin Qt, `ogr_ui/point_entry.py` (`read_point`, `PointEntryError`). Tests
  primero en `tests/test_point_entry_v013.py`: cada forma absoluta de RF-1 y los números de RF-2;
  el relativo y el polar con identidades escritas a mano (`@2<60` desde (1, 1) da (2, 1 + √3);
  `@1<90` y `@1<180` exactos; distancia negativa; 405°); espacios de RF-6; lo que se rechaza con
  su mensaje (RF-7, RF-8, RF-9); lo de la 0.1.0, al bit (RF-16) — RF-1–RF-4, RF-6–RF-9, RF-16
  - Hecho cuando: esas clases en verde, `point_entry.py` no importa Qt ni el núcleo, y la suite
    entera en verde.
- [x] **T2** La entrada y la barra: sin validador, con `read_point`, la referencia
  (`OgrStatusBar.set_point_reference`), `point_refused` y el motivo en la barra, el texto que se
  queda o se vacía; los dos tests de la 0.1.0 que cambian a propósito. Tests primero, con la barra
  en un `QMainWindow` del test y el teclado de `QTest` — RF-5, RF-7, RF-8, RF-10, RF-11, RF-12,
  RF-15, RF-16
  - Hecho cuando: esas clases y `test_status_bar_v010` en verde, y la suite entera en verde.
- [x] **T3** Lo que se ve: la ayuda general, el texto guía nuevo y el ancho de la entrada medido
  con su fuente; los cuatro textos con su español en `ogr_ui/i18n/es.py`, la ayuda de Slip2D
  fuera, `EXCEPTIONS` al día, y la nota del módulo. Tests primero: la ayuda en los dos idiomas sin
  palabras de un programa; el texto guía entero, en los dos temas; más de 200 px para los mensajes
  a 1366 px — RF-13, RF-14
  - Hecho cuando: esas clases, `test_i18n_v010` y `test_text_census_v010` en verde, y la suite
    entera en verde.
- [x] **T4** Documentación de la versión: la versión a `0.1.3.dev0`,
  `docs/changelog/PENDIENTE_v0.1.3.md` (qué se encontró, los dos tests que cambiaron, y qué puede
  quitar FEM2D), `docs/consumidores.md` y `roadmap.md` — RF-1–RF-16
  - Hecho cuando: los archivos dicen lo mismo que el plan, y la suite entera en verde.
- [x] **T5** Validación final — RF-1–RF-16
  - Hecho cuando: cada RF tiene su test en verde en la tabla «Validación» de la spec, la lista de
    diseño está marcada con capturas en inglés y español y en los dos temas, la suite entera pasa
    sin filtrar y sin fugas en serie y con `--jobs 4`, la suite de FEM2D contra este árbol, y la CI
    de la PR en verde en Linux, Windows y macOS.
