# Tareas 002 — El percentil del ajuste, por campo

En orden de dependencia. Cada tarea ≤ 30 min, tests primero, y se marca `[x]` al terminarla con la
suite entera en verde. Una tarea cada vez.

- [x] **T1** `ContourField.fit_percentile` con 0,98 por defecto y su validación al construir;
  la nota de `contours.py` al día. Tests primero en `tests/test_fit_percentile_v011.py`
  (`TestTheFieldDeclaresItsPercentile`), y la identidad de la regla 1 sobre `fit_to`: 0…99 da 97
  con 0,98 y 99 con 1; el pico (cien valores entre 1 y 2 y un 50) no llega con 0,98 y da 50 con 1;
  pico negativo, NaN e ∞, un solo valor y todos iguales — RF-1, RF-2, RF-6, RF-9
  - Hecho cuando: `TestTheFieldDeclaresItsPercentile` y `TestTheFitWithAPercentile` en verde, con
    0, −0,1, 1,01, NaN, ±∞, `"0.9"`, `None` y `True` rechazados con la clave del campo y «(0, 1]»
    en el mensaje, y la suite entera en verde.
- [x] **T2** El diálogo ajusta con el percentil del campo elegido en «Fit to results», la casilla
  de rango automático y «Restore Defaults» (y el cambio de campo). Tests primero
  (`TestTheDialogFitsWithTheFieldsPercentile`): dos campos (0,98 y 1) sobre los mismos valores con
  pico; lo que devuelve el diálogo al aceptar (regla 7); ida y vuelta entre campos; un diálogo sin
  percentiles con los números de la 0.1.0 escritos a mano — RF-3, RF-4, RF-5, RF-10
  - Hecho cuando: esa clase en verde, `test_contours_v010.py` sin tocar y en verde, y la suite
    entera en verde.
- [x] **T3** La ayuda de la casilla según el percentil del campo elegido, al construir y al cambiar
  de campo; el texto nuevo y su español en `ogr_ui/i18n/es.py`; la nota del diálogo al día. Tests
  primero (`TestTheHelpSaysWhatTheFieldDoes`): en inglés y en español, con 0,98, 0,9999 y 1, en los
  dos sentidos del cambio de campo; un diálogo sin percentiles da el texto de la 0.1.0; el diálogo
  en español cabe en 1366×728 con cada campo — RF-7, RF-8, RF-10
  - Hecho cuando: esa clase, `test_text_census_v010` y `test_i18n_v010` en verde, y la suite entera
    en verde.
- [x] **T4** Documentación de la versión: `docs/changelog/CHANGELOG_v0.1.1.md` (qué se encontró,
  incluido que el programa ajusta el rango al dibujar, y qué puede cambiar cada programa, con la
  línea de ejemplo); la fila de contornos de «Lo que un programa hace al adoptarlo» y «Cambios en
  curso» de `docs/consumidores.md`; `roadmap.md` — RF-1–RF-10
  - Hecho cuando: los tres archivos dicen lo mismo que el plan, y la suite entera en verde.
  - Nota: el changelog va en `docs/changelog/PENDIENTE_v0.1.1.md` y se renombra a
    `CHANGELOG_v0.1.1.md` al etiquetar: `test_version_v010` no admite el changelog de la 0.1.1
    mientras la versión sea `0.1.1.dev0`.
- [x] **T5** Validación final — RF-1–RF-10
  - Hecho cuando: cada RF tiene su test en verde en la tabla «Validación» de la spec, la lista de
    diseño de la spec está marcada, la suite entera pasa sin filtrar y sin fugas en serie y con
    `--jobs 4`, la CI de la PR en verde en Linux, Windows y macOS, y la spec en «hecha». La
    etiqueta `v0.1.1` (el número sin `.dev0`, la suite de FEM2D contra este árbol, regla
    «Antes de etiquetar») es un paso aparte con el OK de la propietaria.
