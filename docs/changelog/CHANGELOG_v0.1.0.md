# OGR GUI 0.1.0 — 2026-11-24

La primera versión: las piezas de interfaz que comparten los programas de la suite, sacadas de
OGR Slip2D v0.1.486 (commit `03b6c2d`) sin tocar ese programa. La pidió OGR FEM2D (spec 006,
decisión D1 (ii), y su ADR-0005, aprobados por la propietaria el 2026-11-24) para sus partes C y D.

## 1. Qué entra

| Pieza | De Slip2D (`ogr_gui/…`) | Aquí (`ogr_ui/…`) |
|---|---|---|
| Temas claro y oscuro, `ROLE_COLORS`, `theme_color`, `apply_theme` | `themes/__init__.py` | igual |
| ~90 claves de iconos sobre Font Awesome 6 | `resources/icons.py` | igual, más `register`/`unregister` |
| Leyenda de color, `ToggleLabel`, `StatusIndicators` | `widgets/legend.py` | igual; título por defecto vacío |
| Paletas, niveles, rango | `contours.py` | sin los campos de equilibrio límite; `ContourField`, `RangePreset` |
| Enganche SNAP / ORTHO / OSNAP | `canvas/snap_engine.py` | sobre `SnapShape` y `SnapPoint`, sin el núcleo |
| Diálogo de enganche | `dialogs/snap_dialog.py` | igual; `DataTipMode` en `data_tip_mode.py` |
| Barra de estado | `widgets/status_bar.py` | igual |
| Motivo de una entrada deshabilitada | `disabled_reasons.py` | igual |
| Tareas en un hilo, cancelables | `background.py` | sin el núcleo: `install_progress` |
| Diálogo de progreso | `dialogs/misc_dialogs.py` (dos clases) | `dialogs/progress_dialog.py`; los textos de fase, del programa |
| Preferencias guardadas | `user_prefs.py` | `Preferences(programa, archivo)` |
| Diálogo de preferencias | `dialogs/preferences_dialog.py` | igual |
| Tamaño de los diálogos, suelo de los botones, rueda | `dialog_size.py`, `button_floor.py`, `wheel_guard.py` | igual |
| Gráfico XY, recolector, carpetas, catálogo de Qt | `xy_chart.py`, `gc_guard.py`, `file_folders.py`, `qt_catalog.py` | igual |
| Opciones de contornos | `dialogs/contour_options_dialog.py` | los campos y los rangos de un clic, del programa |
| `tr()` y compañía | `i18n/__init__.py`, sus últimas 40 líneas | el mecanismo, más `remove_language_listener` y `package_translations`; `add_translations` devuelve las claves que cambió |
| El español de estas piezas | 71 entradas de las 3 488 de Slip2D, las mismas palabras | `i18n/es.py` |
| Comprobaciones de la regla 2 | `tests/test_gui_spanish_v1318.py`, `test_i18n_coverage_v141.py` | `testing/texts.py`: funciones sobre la carpeta de un paquete |
| Comprobaciones de la regla 3 | `tests/test_menu_reachability_v142.py`, `test_disabled_reasons_v1294.py` | `testing/menus.py`: funciones sobre una ventana |

Unas 4 800 líneas de código, con las comprobaciones de `testing/`. No entra `data_tips.py` (importa `labels.py`, de equilibrio límite),
ni la ventana, el lienzo o la interpretación de Slip2D.

## 2. Qué se encontró al sacarlas

- **El nombre `ogr_gui` choca.** Es el paquete de interfaz de Slip2D: con el mismo nombre, Slip2D no
  podría instalar este paquete sin renombrar antes el suyo. Decisión de la propietaria
  (2026-11-24): el repositorio y la distribución se quedan `OGR-GUI` / `ogr-gui`, como dicen el
  ADR-0005 y la spec 006 de FEM2D; el paquete se importa como **`ogr_ui`**.
- **Depender de `ogr-core` fijado habría atado a todos los programas a una sola etiqueta.** pip no
  admite dos referencias git distintas a la misma distribución: FEM2D fija `v0.2.7`, el núcleo va
  por `v0.2.8`, y con `ogr-gui` pidiendo una, el programa no se instala si fija otra. Además OGR
  Data no usa el núcleo. Decisión de la propietaria (2026-11-24): **`ogr_ui` no importa el
  núcleo**; `ogr-core` entra solo por el extra `[test]`, para el runner de la suite. Por eso no
  hay fila en `docs/consumidores.md` de OGR-Core, y la tabla de quién fija qué está aquí.
- **Lo que tocaba el núcleo o el programa, y cómo se cortó** (`tests/test_layering_v010.py` lo
  mantiene cortado, en el código y en `sys.modules`):
  - el enganche leía `b.polyline.vertices` y `b.polyline.closed` de los `Boundary` del núcleo y
    devolvía sus `Vertex`. Ahora recibe `SnapShape`, con los vértices y los segmentos por separado,
    para que un contorno con arcos dé sus cuerdas sin que cada extremo de cuerda sea un vértice al
    que engancharse (lo pedía FEM2D). `SnapShape.polyline` hace lo que el motor hacía con un
    `Boundary`. La reexportación de `nice_step` (de `ogr_core.numbers`) no viene;
  - las tareas leían `ogr_core.progress` (los puntos de control y la fase) y escribían el archivo
    de resultados del `Project` con `save_results`. Lo primero lo entrega el programa una vez con
    `install_progress`; lo segundo (`ResultsWriter`, `write_results_file`) se queda en Slip2D;
  - el diálogo de progreso estaba junto al «Acerca de» de Slip2D y nombraba su fase `OPTIMIZE`
    («Optimizing the critical surface…»): ahora cada programa da sus textos de fase;
  - el diálogo de enganche importaba `DataTipMode` de `data_tips.py`, que no puede venir;
  - las preferencias llevaban `"OGR Slip2D"` y `ogr-slip2d.ini` dentro;
  - los contornos llevaban los campos de equilibrio límite y el 0–6 del factor de seguridad, y la
    leyenda el título «Factor of safety».
- **El comentario de los iconos decía «compatible with GPL-3.0» y «OFL»**: la suite es AGPL-3.0, y
  los iconos de Font Awesome Free son CC BY 4.0 (las fuentes, SIL OFL 1.1). `THIRD_PARTY.md` lleva
  la atribución que pide CC BY, y un test lo comprueba.
- **Encontrado al trasladar los tests y arreglado aquí** (las tres son de este paquete, no de
  Slip2D):
  - *Restore Defaults* del diálogo de contornos escribía FILLED y «sin invertir» como constantes y
    dejaba la notación científica como estaba. En Slip2D era lo mismo que el inicio de sus campos;
    con `ContourField.start` no lo es. Ahora vuelve al inicio del campo, control a control;
  - `icons.unregister` quitaba también claves de la suite; ahora las rechaza, como `register`;
  - una línea de `testing/texts.py` había perdido su continuación al escribirse (era válida, pero
    una sola línea de 90 columnas).
- **Encontrado y NO arreglado** (regla 6: se reporta antes; las cuatro están igual en Slip2D):
  - **`SnapSettings.ortho_snap_angle_deg` no hace nada** (regla 7). El diálogo de enganche lo
    ofrece («Orthogonal window», con una ayuda que promete bloquear el eje dentro de ese ángulo),
    y el motor no lo lee: ORTHO bloquea siempre al eje más cercano. Arreglarlo cambia el
    comportamiento del enganche, o quitar el control cambia el diálogo: decisión de la propietaria;
  - en el diálogo de contornos, *Fit to results* queda habilitado al pasar entre dos campos
    automáticos aunque los valores no son de ese campo (no hace nada al pulsarlo);
  - `qt_catalog.switch_qt_translator` quita el traductor anterior y no lo borra: queda uno muerto,
    hijo de la aplicación, por cada cambio de idioma;
  - `hold_wrapped_height` fija la altura que pide una nota a la anchura mínima de la ventana, que
    con una nota larga y una anchura mínima pequeña puede pasar de la pantalla. Los diálogos reales
    caben; es un límite del diseño.

## 3. Tests

421 casos en 22 archivos, en verde en Windows (Python 3.14, PySide6 6.12.0), en serie y con
`--jobs 4`, sin fugas (`shared: ogr_core 0.2.8 … installed`). Unos 400 son los de Slip2D sobre
estas piezas, rehechos sin su ventana principal ni su motor (cada archivo dice de cuáles salen y
qué se quedó fuera, y por qué); el resto, de las interfaces nuevas (`SnapShape`, `ContourField`,
`RangePreset`, `install_progress`, `Preferences`, `register`) y del repositorio: licencia, capas,
versión, fuentes, nombres de productos, suelo de Python y acciones de la CI. La CI corre la suite
en Linux, Windows y macOS con Python 3.11, 3.12 y 3.13. Su primera corrida en macOS falló un
test, el mismo en las tres versiones: pedía que la guarda de la rueda dejara cada desplegable en
`StrongFocus`, y en macOS un desplegable no editable nace con `TabFocus` (Qt no le da el foco con
la rueda en esa plataforma), que la guarda no toca porque no hace falta. El test pide ahora lo que
la guarda promete: que la rueda no dé el foco a ninguna caja, y que solo cambie la que lo tenía.

La suite de OGR Slip2D no se ha tocado ni corrido: ningún archivo suyo ha cambiado por esta
versión (sus piezas son las de `03b6c2d`, comprobado con `git diff`, y las 71 traducciones son
las de su diccionario en ese commit).

## 4. Qué tiene que hacer un programa para usarla

Fijar `ogr-gui @ git+https://github.com/samuelsl27/OGR-GUI@v0.1.0` y lo que dice la tabla de
`docs/consumidores.md` («Lo que un programa hace al adoptarlo»). Para OGR FEM2D, que la pidió:

- el paquete se importa como **`ogr_ui`**, no `ogr_gui`;
- no trae `ogr-core`: el programa sigue fijando el suyo, el que quiera;
- su `tests/_runner.py` añade a su lista blanca las entradas de estas piezas que tiene el
  `tests/_runner.py` de este repositorio;
- su ADR-0005, su `tech-stack.md`, su `AGENTS.md` y su spec 006 dicen que `ogr-gui` depende de
  `ogr-core` por etiqueta y que el programa fija «por él, la de `ogr-core` que pida `ogr-gui`»:
  ya no es así, y lo corrige su sesión.
