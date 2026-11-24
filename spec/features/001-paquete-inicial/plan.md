# Plan 001 — Paquete inicial

Escrito después de implementarlo (ver la spec). Sin código. Cada apartado dice qué RF cubre.

## Decisiones

| Decisión | Alternativa descartada y por qué | RF |
|---|---|---|
| Paquete `ogr_ui` en el repositorio `OGR-GUI`, distribución `ogr-gui` | `ogr_gui`: es el paquete de Slip2D y no podrían convivir (decisión de la propietaria) | RF-25 |
| Sin `ogr-core` en ejecución; el núcleo en el extra `[test]` | Depender del núcleo por etiqueta: pip no admite dos referencias git a la misma distribución, y cada programa tendría que fijar la nuestra (decisión de la propietaria) | RF-24, RF-25 |
| El enganche recibe `SnapShape` (vértices y segmentos por separado) y devuelve `SnapPoint` | Los `Boundary` y `Vertex` del núcleo: atan al núcleo, y con arcos cada extremo de cuerda sería un vértice al que engancharse | RF-9 |
| Las tareas reciben el progreso del programa con `install_progress(watching, phase, phase_texts)` | Importar `ogr_core.progress`: atan al núcleo; pasarlo en cada `run_task`: cada llamada lo repetiría | RF-15–RF-17 |
| El diálogo de progreso sale de `misc_dialogs.py` de Slip2D a `dialogs/progress_dialog.py`, con los textos de fase del programa | Traer `misc_dialogs.py` entero: lleva el «Acerca de» de Slip2D | RF-15, RF-16 |
| El escritor del archivo de resultados se queda en Slip2D | Traerlo: escribe el `Project` del núcleo | — |
| `Preferences(nombre, archivo)` en lugar de funciones de módulo con «OGR Slip2D» dentro | Un nombre global que cada programa cambia al arrancar: estado global, y una fuga en los tests | RF-18 |
| `ContourField` y `RangePreset` del programa; `ContourSettings.automatic` para un campo sin rango fijo | `SCALAR_FIELDS` y `for_field`: son del equilibrio límite | RF-13, RF-14 |
| `DataTipMode` en `data_tip_mode.py` | Traer `data_tips.py`: usa las etiquetas del equilibrio límite | RF-10 |
| `tr()`: el mecanismo de Slip2D y el español de estas piezas, sacado de su diccionario en `03b6c2d` | El diccionario entero (3 488 entradas, casi todas de equilibrio límite) | RF-5–RF-7 |
| `icons.register` / `unregister` para las claves de cada programa, sin tocar las de la suite | Que cada programa edite el catálogo: la misma acción acabaría con iconos distintos | RF-3, RF-4 |
| Las comprobaciones de las reglas 2 y 3 como funciones sobre una carpeta o una ventana (`ogr_ui.testing`) | Tests que cada programa copia: es la copia que diverge | RF-22, RF-23 |
| Los tests de Slip2D rehechos sin su ventana principal ni su motor | Traerlos con su ventana: necesitan el programa entero | todos |

## Módulos

Los de la tabla de `CHANGELOG_v0.1.0.md`, sección 1; ninguno importa el núcleo ni un programa.

## Interfaces

Las de la tabla «Lo que un programa hace al adoptarlo» de `docs/consumidores.md`.

## Compatibilidad

Primera versión. Respecto a Slip2D, lo que cambia para quien lo adopte está en esa misma tabla.

## Estrategia de tests

- Cada pieza sola, con un `QMainWindow` o un `QDialog` del test: sin la ventana de ningún programa.
- Los dos idiomas y los dos temas donde la pieza tiene texto o color.
- Lo que depende de la plataforma, comparado con lo que la plataforma da por defecto (el foco de la
  rueda en macOS).
- La comprobación de fugas del runner en cada archivo; la lista blanca de `tests/_runner.py`, con
  las entradas de Slip2D para estas piezas.
- Las del repositorio: licencia, capas (en el código y en `sys.modules`), versión, fuentes, nombres
  de productos, suelo de Python y acciones de la CI.

## Riesgos

- Qt distinto en cada plataforma: la CI en las tres (encontró uno en macOS).
- Que un programa adopte y diverja: la regla «se mueve, no se copia».
