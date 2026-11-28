# Tareas 006 — En la entrada X,Y, la coma separa y el punto es el decimal

En orden de dependencia. Cada tarea ≤ 30 min, tests primero, y se marca `[x]` al terminarla con la
suite entera en verde. Una tarea cada vez.

- [x] **T1** El lector con el criterio nuevo, en `ogr_ui/point_entry.py`: exactamente una coma entre
  los dos números, cada número con `read_number`, y el polar con el mismo lector. Tests primero, en
  `tests/test_coordinate_comma_v020.py`:
  - cada forma de RF-1 y RF-2, y el relativo `@dx,dy` (RF-3);
  - el polar con punto, y `@1,5<30` rechazado (RF-4, RF-6);
  - los rechazos de RF-5 (`1.5 2.5`, `1.5; 2.5`), RF-6 (`1,5; 2,5`, `1,5 2,5`, `1,5,2,5`) y RF-7
    (`1.5`, `1.5,2.5,3.5`, `1.5,,2.5`, `,2.5`, `1.5,`), con su motivo;
  - lo que se rechazaba sigue rechazado (RF-8);
  - lo que la 0.1.4 aceptaba con punto y coma de separador, al bit (RF-11).

  Los tests de `tests/test_point_entry_v013.py` que dicen lo contrario cambian a propósito, cada uno
  con su porqué, y también `test_status_bar_v010::test_every_separator_gives_the_same_point_to_the_bit`,
  que el lector nuevo rompe (pasado aquí desde T2 para dejar la suite en verde). Cubre RF-1–RF-8 y RF-11.
  - Hecho cuando: esas clases y `test_point_entry_v013` están en verde, `point_entry.py` no importa
    Qt ni el núcleo, y la suite entera está en verde.
- [x] **T2** Lo que se ve y la entrada en la barra:
  - el motivo `WRITE_A_POINT` y la ayuda nuevos, con su español en `i18n/es.py`, y los viejos
    fuera;
  - la nota del módulo de `status_bar.py`.

  Tests primero, con la barra en un `QMainWindow` del test y el teclado de `QTest`:
  - `1.5,2.5` + Intro entrega el punto y vacía la entrada;
  - `1,5; 2,5` + Intro deja el texto y el motivo nuevo, en inglés y en español;
  - ni el motivo ni la ayuda hablan de la coma decimal;
  - el texto guía no cambia.

  Cubre RF-5, RF-6, RF-8, RF-9, RF-10 y RF-11.
  - Hecho cuando: esas clases, `test_point_entry_v013`, `test_status_bar_v010`, `test_i18n_v010` y
    `test_text_census_v010` están en verde, y la suite entera está en verde.
- [x] **T3** Documentación de la versión, RF-1–RF-11:
  - la versión a `0.2.0.dev0`;
  - `docs/changelog/PENDIENTE_v0.2.0.md`, renombrado a `CHANGELOG_v0.2.0.md` en el commit de la
    versión: qué se encontró, qué deja de leerse, los tests que cambiaron y qué tiene que cambiar
    FEM2D;
  - `docs/consumidores.md` y `roadmap.md`;
  - el aviso a FEM2D en `GUI/notas/2026_11_28_aviso_a_fem2d_coma_separa_coordenadas.md`.
  - Hecho cuando: los archivos dicen lo mismo que la spec y el plan, `test_version_v010` está en
    verde, y la suite entera está en verde.
- [x] **T4** Validación final, RF-1–RF-11.
  - Hecho cuando:
    - cada RF tiene su test en verde en la tabla «Validación» de la spec;
    - la lista de diseño está marcada, con capturas de la barra a 1366 px en inglés y en español y
      en los dos temas, con un rechazo a la vista;
    - la suite entera pasa sin filtrar y sin fugas, en serie y con `--jobs 4`;
    - la suite de FEM2D se ha corrido contra este árbol, con sus fallos esperados en la coma decimal
      listados;
    - la CI de la PR está en verde en Linux, Windows y macOS.

Todos los RF de la spec (RF-1–RF-11) están en alguna tarea.
