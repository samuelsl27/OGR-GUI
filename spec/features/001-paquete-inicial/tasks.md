# Tareas 001 — Paquete inicial

Escritas después de hacerlas (ver la spec), en el orden en que se hicieron.

- [x] **T1** Repositorio y esqueleto: licencia, CLA, `AGENTS.md`, `pyproject.toml`, runner, CI, `.gitignore` — RF-25
  - Hecho cuando: `tests/_runner.py` arranca con `shared: ogr_core 0.2.8 … installed`.
- [x] **T2** Copiar las piezas de Slip2D `03b6c2d` con `ogr_gui` → `ogr_ui` — RF-1–RF-3, RF-11, RF-12, RF-19–RF-21
  - Hecho cuando: los 30 módulos importan sin pantalla.
- [x] **T3** Cortar el enganche del núcleo (`SnapShape`, `SnapPoint`) — RF-9
  - Hecho cuando: `test_snap_engine_v010` en verde, arcos por cuerdas incluidos.
- [x] **T4** Cortar las tareas del núcleo y del programa (`install_progress`, `progress_dialog`) — RF-15–RF-17
  - Hecho cuando: `test_background_tasks_v010` en verde.
- [x] **T5** `Preferences`, `DataTipMode`, contornos con `ContourField` y `RangePreset`, título vacío de la leyenda — RF-10, RF-13, RF-18
  - Hecho cuando: `test_preferences_v010`, `test_snap_dialog_v010`, `test_contours_v010` y `test_legend_v010` en verde.
- [x] **T6** `tr()` y el español de las piezas; `register`/`unregister` de iconos — RF-3–RF-8
  - Hecho cuando: `test_i18n_v010`, `test_qt_catalog_v010` y `test_themes_icons_v010` en verde.
- [x] **T7** `ogr_ui.testing`: censo de textos y comprobaciones de menús — RF-22, RF-23
  - Hecho cuando: `test_text_census_v010` y `test_menus_v010` en verde.
- [x] **T8** Tests del repositorio: capas, versión, licencia, fuentes, nombres, Python, CI — RF-24, RF-25
  - Hecho cuando: los siete archivos en verde.
- [x] **T9** Arreglos encontrados al trasladar los tests: *Restore Defaults* de contornos, `unregister` de claves de la suite — RF-4, RF-14
  - Hecho cuando: `TestRestoreDefaultsIsTheFieldsStart` y `TestASuiteKeyCannotBeRemoved` en verde.
- [x] **T10** CI en las tres plataformas; el test del foco de la rueda, con lo que da cada plataforma; macOS con un solo Python — RF-19
  - Hecho cuando: la run 45436738545 en verde.
- [x] **T11** Validación final y etiqueta — todos los RF
  - Hecho cuando: 421 casos en verde en serie y con `--jobs 4`, sin fugas; `v0.1.0` etiquetada e instalable desde la etiqueta; changelog escrito.
