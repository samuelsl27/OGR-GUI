# Tareas 003 — El español de los mensajes del núcleo

En orden de dependencia. Cada tarea ≤ 30 min, tests primero, y se marca `[x]` al terminarla con la
suite entera en verde. Una tarea cada vez.

- [x] **T1** El extra `[test]` a `ogr-core` v0.2.12 en `pyproject.toml`, esa etiqueta instalada en
  el `.venv`, y la mención de la etiqueta en `spec/constitution/tech-stack.md` si la hay — RF-1, RF-5
  - Hecho cuando: `ogr_core.__version__` del `.venv` es 0.2.12 y la suite entera de la 0.1.1 pasa
    con él, sin filtrar.
- [x] **T2** Los tests de `tests/test_core_messages_v012.py`, primero y en rojo: el descubrimiento
  de los catálogos (los 20 de la v0.2.12), cada plantilla inglesa y singular traducida con su
  catálogo y su código en el mensaje del fallo, los campos como multiconjunto (con un caso malo que
  el comparador rechaza), las plantillas sin palabras, `render` con `translate=tr` en español, y una
  plantilla inventada que sale en inglés — RF-1, RF-2, RF-4, RF-5, RF-6, RF-7
  - Hecho cuando: el archivo corre, falla solo por las traducciones que faltan, y los casos del
    comparador y de RF-6 y RF-7 pasan ya.
- [x] **T3** `ogr_ui/i18n/core_es.py` generado una vez desde el diccionario de Slip2D en `67faf4f`
  con un guion del scratchpad (fuera del repositorio), y la copia congelada
  `tests/data/slip2d_core_es_67faf4f.json`; `tr()` y `package_translations("es")` con `ES` y
  `CORE_ES`; la nota del módulo; `test_package_translations_is_a_copy` al día — RF-2, RF-3
  - Hecho cuando: el test de RF-3 (cada entrada de la copia congelada, igual en `CORE_ES`) pasa,
    `core_es.py` no importa nada y `test_i18n_v010` y `test_layering_v010` en verde.
- [x] **T4** Las traducciones que Slip2D no tiene, escritas con su terminología, y la revisión de
  RF-8 (la búsqueda de términos de equilibrio límite y la lectura a mano de cada candidata); las
  cuatro de RF-9 con los campos de su plantilla; las idénticas a `IDENTICAL` con su porqué — RF-1,
  RF-4, RF-5, RF-8, RF-9
  - Hecho cuando: `tests/test_core_messages_v012.py` entero en verde, la lista de RF-8 escrita en
    el test y en el borrador del changelog, y la suite entera en verde.
  - Nota: al generar `core_es.py` salieron las cuatro de RF-9 (`{name!r}` escrito `«{name}»`);
    la propietaria decidió (2026-11-27) conservar los campos de la plantilla, y la spec ganó
    RF-9 antes del código. RF-8 no tiene ninguna. T3 y T4 se hicieron con un solo guion de
    generación (el del scratchpad), que toma las de Slip2D y las nuevas a la vez.
- [x] **T5** Documentación: `docs/changelog/PENDIENTE_v0.1.2.md` (qué se encontró, las entradas
  nuevas para que la propietaria las lea, las de RF-8 con la de Slip2D al lado, y qué tiene o puede
  hacer cada programa), `docs/consumidores.md` y `roadmap.md` — RF-1–RF-9
  - Hecho cuando: los tres archivos dicen lo mismo que el plan, y la suite entera en verde.
  - Nota: la versión pasa a `0.1.2.dev0` en esta rama (la 0.1.1 está en `main`).
- [x] **T6** Validación final — RF-1–RF-9
  - Hecho cuando: cada RF tiene su test en verde en la tabla «Validación» de la spec, la lista de
    diseño de la spec está marcada, la suite entera pasa sin filtrar y sin fugas en serie y con
    `--jobs 4`, y la CI de la PR en verde en Linux, Windows y macOS.
