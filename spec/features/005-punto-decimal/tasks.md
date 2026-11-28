# Tareas 005 — Los números en pantalla, siempre con punto decimal

En orden de dependencia. Cada tarea ≤ 30 min, tests primero, y se marca `[x]` al terminarla con la
suite entera en verde. Una tarea cada vez.

- [x] **T1** Escribir y leer sin Qt: `ogr_ui/numbers.py` (`format_number`, `read_number`). Tests
  primero en `tests/test_numbers_v014.py`:
  - `format_number` con decimales, científica y signo, en inglés y en español: siempre punto, sin
    miles (`1000000.00`);
  - `read_number` acepta `2.5`, `.5`, `5.`, `-0`, `1.5e3`, `1.5E-3`, y `1.000` da 1;
  - `read_number` rechaza `2,5`, `1.2.3`, `1 000`, `abc`, `nan`, `inf` y `1e999` con `ValueError`.

  Cubre RF-1, RF-4, RF-6 y RF-8.
  - Hecho cuando: esas clases están en verde, `numbers.py` no importa Qt ni el núcleo, y la suite
    entera está en verde.
- [x] **T2** La casilla común, `ogr_ui/widgets/number_box.py` (`NumberBox`), exportada desde
  `ogr_ui.widgets`. Tests primero, con `QTest.keyClicks` y con la configuración de Qt en España y
  en inglés (creada después de ponerla y devuelta en un `finally`):
  - `2.5` da 2.5 y se ve `2.500` al salir;
  - `2,5` deja `25`, `1.2.3` deja `1.23` y una letra no entra;
  - pegar `2,5` o `1.234,56` no cambia nada;
  - fuera de rango y a medio escribir (`-`, `1e`), al salir vuelve al último valor;
  - con sufijo, con texto especial y con notación científica;
  - el texto y el valor coinciden al redondear (`0.12345` con 4 decimales);
  - `QLocale()` queda como estaba.

  Cubre RF-5 a RF-10 y RF-12.
  - Hecho cuando: esas clases están en verde y la suite entera está en verde, sin fugas.
- [x] **T3** Las piezas que escriben números pasan a `format_number`: `ColourScaleLegend.format_value`,
  `ContourSettings.format_value` (y con él `band_label` y el tamaño del intervalo) y
  `OgrStatusBar.update_coords`. Tests primero:
  - la salida de la 0.1.3, escrita a mano en el test, carácter a carácter, con `-0` incluido (si
    discrepa, se avisa antes de cambiar nada, regla 6);
  - cada sitio, con la configuración de Qt en España y en los dos idiomas.

  Cubre RF-1, RF-2 y RF-11.
  - Hecho cuando: esas clases, `test_legend_v010`, `test_contours_v010` y `test_status_bar_v010`
    están en verde sin tocarlos, y la suite entera está en verde.
- [x] **T4** Los diálogos con `NumberBox`: `sp_min` y `sp_max` del de contornos y `_spin` del de
  enganche, con los mismos decimales, rangos, pasos y sufijos. Tests primero:
  - con la configuración de Qt en España, cada casilla muestra punto y teclear `2.5` da 2.5 en lo
    que devuelve el diálogo;
  - la coma no entra.

  Cubre RF-2, RF-5 y RF-11.
  - Hecho cuando: esas clases, `test_contours_v010`, `test_snap_dialog_v010` (con sus tests de la
    regla 7) y `test_dialog_guards_v010` están en verde sin tocarlos, y la suite entera está en
    verde.
- [x] **T5** Los ejes del gráfico XY sin la configuración regional. Tests primero:
  - dentro de `matplotlib.rc_context` con `axes.formatter.use_locale` encendido, los
    `ScalarFormatter` de los dos ejes dicen que no la usan, y las etiquetas dibujadas llevan punto;
  - la escala logarítmica sigue dibujándose;
  - `rcParams` queda como estaba.

  Cubre RF-2, RF-3 y RF-12.
  - Hecho cuando: esas clases y `test_xy_chart_files_v010` están en verde, y la suite entera está
    en verde, sin fugas.
- [x] **T6** Documentación de la versión, todos los RF:
  - la versión a `0.1.4.dev0` en `pyproject.toml` y `ogr_ui/__init__.py`;
  - `docs/changelog/PENDIENTE_v0.1.4.md`, renombrado a `CHANGELOG_v0.1.4.md` en el commit de la
    versión: qué se encontró (las casillas que leían «2.5» como 25, la coma como separador de miles
    en inglés), la tecla decimal del teclado numérico y qué tiene que cambiar FEM2D;
  - `docs/consumidores.md` y `roadmap.md`;
  - la respuesta a FEM2D en `GUI/notas/2026_11_28_respuesta_a_fem2d_punto_decimal.md`.
  - Hecho cuando: los archivos dicen lo mismo que la spec y el plan, `test_version_v010` está en
    verde, y la suite entera está en verde.
- [x] **T7** Validación final, RF-1 a RF-12.
  - Hecho cuando:
    - cada RF tiene su test en verde en la tabla «Validación» de la spec;
    - la lista de diseño está marcada, con capturas sin pantalla de los dos diálogos y de la
      leyenda en inglés y en español y en los dos temas;
    - la suite entera pasa sin filtrar y sin fugas, en serie y con `--jobs 4`;
    - la suite de FEM2D pasa contra este árbol;
    - la CI de la PR está en verde en Linux, Windows y macOS.

Todos los RF de la spec (RF-1 a RF-12) están en alguna tarea.
