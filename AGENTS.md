# OGR GUI

Las piezas de interfaz que comparten los programas de la suite: los temas claro y oscuro, los
iconos, `tr()` y su diccionario, el motor de enganche, la barra de estado, la leyenda de color, los
contornos, las tareas en segundo plano, las preferencias guardadas y las guardas que mantienen
usable una ventana de Qt (tamaño de los diálogos, anchura de los botones, la rueda del ratón, el
recolector de basura). Y las comprobaciones de las reglas 2 y 3 de la suite, para que cada programa
las llame sobre su paquete y su ventana.

**Tres nombres**: el repositorio es `samuelsl27/OGR-GUI`, la distribución `ogr-gui` y el paquete
de importación **`ogr_ui`**. No es `ogr_gui` a propósito: así se llama el paquete de interfaz de
OGR Slip2D, y los dos tienen que poder vivir en un mismo entorno (decisión de la propietaria del
2026-11-24).

Autor y titular del copyright: Samuel Sáez López (UPCT). Licencia AGPL-3.0-or-later.

> Este archivo es el **contrato de trabajo** con cualquier agente de IA. Se consulta antes de cada
> acción. Deriva de los `AGENTS.md` de OGR-Core y de OGR FEM2D; el código sale de OGR Slip2D.

> **Estado (2026-11-24, v0.1.0):** las piezas son las de OGR Slip2D en su commit `03b6c2d`
> (v0.1.486), copiadas sin tocarlo (decisión D1 (ii) de la spec 006 de OGR FEM2D y su ADR-0005).
> Qué cambió al sacarlas y por qué: `docs/changelog/CHANGELOG_v0.1.0.md`. Quién fija qué versión:
> [`docs/consumidores.md`](docs/consumidores.md). **El código de `ogr_ui` solo se cambia en este
> repositorio.**

---

## Stack

- **Lenguaje**: Python 3.11+, con anotaciones de tipo donde aclaren.
- **Interfaz**: PySide6 (Qt 6), qtawesome (los iconos de Font Awesome 6 Free) y Matplotlib (el
  gráfico XY). Nada más en tiempo de ejecución.
- **Sin `ogr_core`**: el paquete no importa el núcleo (decisión de la propietaria del 2026-11-24).
  Cada programa fija su propia etiqueta del núcleo, y pip no admite dos referencias git distintas a
  la misma distribución: si `ogr-gui` dependiera de `ogr-core`, todos los programas tendrían que
  fijar la etiqueta que fijara este. Las dos piezas que en Slip2D leían el núcleo reciben lo que
  necesitan por una interfaz pequeña (`SnapShape` en el enganche; `install_progress` en las
  tareas).
- **Tests**: el runner de la suite (`ogr_core.testing.runner`) a través de `tests/_runner.py`. El
  núcleo entra **solo** para eso, por el extra `[test]` de `pyproject.toml`, fijado a una etiqueta,
  y el runner se niega si el instalado no es ese. Aporta un `pytest` simulado; **no** hay pytest
  real.

## Comandos

Todo con el intérprete del `.venv` del repositorio (`.venv\Scripts\python` en Windows).

```bash
QT_QPA_PLATFORM=offscreen .venv/Scripts/python tests/_runner.py            # toda la suite (lo que corre la CI)
QT_QPA_PLATFORM=offscreen .venv/Scripts/python tests/_runner.py --jobs 4   # en cuatro procesos
QT_QPA_PLATFORM=offscreen .venv/Scripts/python tests/_runner.py snap       # archivos que contengan eso
QT_QPA_PLATFORM=offscreen .venv/Scripts/python tests/_runner.py -k legend  # tests con ese nombre
```

`QT_QPA_PLATFORM=offscreen` es **obligatorio**: los tests construyen widgets reales que no llegan
a la pantalla. La suite entera de una versión es la primera orden, sin filtrar; una corrida
filtrada lo dice (`FILTERED RUN`) y no vale para publicar.

Instalación para desarrollo, una vez:

```bash
py -3.14 -m venv .venv                                  # Windows; en otro sistema, python3 -m venv .venv
.venv/Scripts/python -m pip install -e ".[test]"        # el paquete, y ogr-core de su etiqueta para los tests
```

## Estructura

| Ruta | Contenido |
|---|---|
| `ogr_ui/themes/` | Las hojas de estilo clara y oscura, `ROLE_COLORS`, `theme_color(role)`, `apply_theme()` |
| `ogr_ui/resources/icons.py` | ~90 claves semánticas sobre Font Awesome 6; `register()` para las de cada programa |
| `ogr_ui/i18n/` | `tr()` y su mecanismo; `es.py`, el español de los textos de este paquete y nada más |
| `ogr_ui/canvas/snap_engine.py` | SNAP, ORTHO y OSNAP, con tolerancias en píxeles, sobre `SnapShape` |
| `ogr_ui/widgets/` | La barra de estado con sus palancas y la entrada X,Y; la leyenda de color |
| `ogr_ui/contours.py` | Paletas, niveles y rango, sin Qt; `ContourField` y `RangePreset` los da cada programa |
| `ogr_ui/dialogs/` | Enganche, contornos, preferencias y progreso |
| `ogr_ui/background.py` | Tareas en un hilo, cancelables |
| `ogr_ui/user_prefs.py` | `Preferences(programa, archivo)`: idioma y tema guardados |
| `ogr_ui/disabled_reasons.py` | El motivo de una entrada deshabilitada, en la barra de estado |
| `ogr_ui/dialog_size.py`, `button_floor.py`, `wheel_guard.py`, `gc_guard.py` | Las guardas |
| `ogr_ui/xy_chart.py`, `file_folders.py`, `qt_catalog.py` | Gráfico XY no modal; la carpeta de cada diálogo; el catálogo de Qt |
| `ogr_ui/testing/` | Las comprobaciones de las reglas 2 (`texts`) y 3 (`menus`) para los tests de cada programa |
| `tests/` | Un archivo por pieza |
| `docs/` | Changelog y `consumidores.md` |

## Capas

`ogr_ui` **no importa el núcleo ni ningún programa**: ni `ogr_core`, ni `ogr_slip2d`, `ogr_gui`,
`ogr_api`, `ogr_cli`, `ogr_mcp`, ni `ogr_fem2d`, ni `ogr_data`, ni `mcp`. Lo comprueba
`tests/test_layering_v010.py`, que lee el código y mira `sys.modules` en tiempo de ejecución.

Lo que es de un programa se queda en el programa: la ventana principal, el lienzo, la
interpretación, los campos que se pueden contornear, las etiquetas de los objetos. Aquí entra una
pieza cuando dos programas la necesitan iguales, y **se mueve**, no se copia: copiarla es cómo
acaban diciendo cosas distintas.

## Un paquete y varios programas

Las mismas reglas que el núcleo (`AGENTS.md` de OGR-Core, «Un núcleo y varios programas»):

- **El código de `ogr_ui` solo se cambia aquí.** La sesión de un programa que necesita algo lo
  pide por escrito, con lo que encontró y la evidencia; no lo edita, no lo copia y no lo rodea. Y
  desde aquí no se edita un programa: lo que un programa tiene que cambiar se le da escrito.
- **Cada programa fija una etiqueta `vX.Y.Z` y la sube a propósito**, en un commit suyo
  (`ogr-gui @ git+https://github.com/samuelsl27/OGR-GUI@vX.Y.Z`). Nunca una rama.
- **Un solo `main`**, siempre publicable. Cada cambio, en una rama corta `dev/…` con su PR; la CI
  corre la suite en Linux, Windows y macOS. La rama se borra al fusionarse, en GitHub y en local;
  una sin fusionar, solo con el OK de la propietaria, y antes se archiva en `archivo/<nombre>` si
  lleva algo que `main` no tiene.
- **Antes de etiquetar**, la suite entera de este repositorio y la de cada programa de
  `docs/consumidores.md` que vaya a fijar la versión, contra el árbol que se etiqueta (con ese
  árbol por delante en el `PYTHONPATH`). Suites de programas distintos pueden correr a la vez en
  este PC; dos del mismo, no.
- **`docs/consumidores.md` al día**: qué fija cada programa y qué cambios están en curso.

## Las siete reglas de la suite

Son las de OGR Slip2D. Cada una existe porque su ausencia causó un problema real.

1. **El trabajo numérico se valida contra algo EXTERNO**: un caso publicado, una solución cerrada o
   una identidad analítica. Aquí casi no hay números; los colores medidos de una paleta y la
   conversión de píxeles a unidades del modelo cuentan.
2. **Todo texto visible pasa por `tr()`** y tiene su traducción española en `ogr_ui/i18n/es.py`. Lo
   comprueba `tests/test_i18n_v010.py` con `ogr_ui.testing.texts`, lo mismo que cada programa
   llama sobre el suyo. Un texto que un programa pasa a una pieza (el título de la leyenda, la
   etiqueta de un campo, el texto de una fase) lo traduce el programa.
3. **Toda acción debe ser alcanzable desde un menú.** Aquí no hay ventana principal: la cumple cada
   programa, con `ogr_ui.testing.menus` sobre su barra de menús real.
4. **Cada archivo lleva su cabecera de licencia** (SPDX AGPL-3.0-or-later y copyright).
5. **Los tests no filtran estado**: el idioma, el tema, la hoja de estilo, la paleta, lo global de
   un módulo. Lo comprueba el runner archivo a archivo (`✗ [LEAK]`); a la lista blanca de
   `tests/_runner.py` solo va lo que no es del test, con su porqué.
6. **Las anomalías se reportan ANTES de corregirlas**, con la evidencia.
7. **Ningún ajuste puede no hacer nada**: todo control de un diálogo lleva el test que demuestra
   que cambia lo que el diálogo devuelve.

## Reglas propias

8. **Versiones**: serie propia desde 0.1.0. El número va en `pyproject.toml` y en
   `ogr_ui/__init__.py`, y un test falla si discrepan. Es `X.Y.Z` en el commit que se etiqueta y
   `X.Y.Z.dev0` entre dos etiquetas. Cada versión publicada lleva su etiqueta y su changelog.
   Mientras la serie sea 0.x, un cambio incompatible sube el segundo número y se avisa con al
   menos una versión de margen; uno compatible, el tercero.
9. **Un cambio que obliga a cambiar un programa** se anota en el changelog con lo que ese programa
   tiene que cambiar.
10. **Una pieza no sabe de qué programa es.** Ni un texto, ni una clave, ni un nombre de archivo de
    un programa en el código de `ogr_ui`: lo que cambia de un programa a otro se recibe como
    argumento (el nombre en `QSettings`, los campos de un contorno, el texto de una fase).
11. **Los iconos llevan su atribución.** Los de Font Awesome Free son CC BY 4.0: `THIRD_PARTY.md`
    lo dice, y un test lo comprueba.

---

## Flujo de trabajo

- **Antes de una tarea no trivial, propón un plan y espera el OK de la propietaria.**
- **Una tarea a la vez.** Al terminar, di qué cambiaste y qué probaste.
- **Si no estás seguro al 80 %, pregunta. No inventes.**
- Cada versión con su changelog en `docs/changelog/`, registrando **qué se encontró**, no solo qué
  se escribió.

## No hagas

- **No instales dependencias sin preguntar**, y comprueba su licencia (compatible con AGPL-3.0).
- **No uses `pytest` directamente**: el runner aporta uno simulado.
- **No abras diálogos modales en código que un test vaya a ejecutar**: `exec()` y `QMessageBox`
  bloquean sin pantalla.
- **No cambies `LICENSE`, `CLA.md` ni las cabeceras SPDX** sin pedirlo.
- **No añadas telemetría ni llamadas de red** que no se hayan pedido.
- **No importes `ogr_core`** ni ningún programa desde `ogr_ui`.

## Documentación de referencia

La documentación de programas comerciales sirve para entender **qué** hace una función y **cómo**
se comporta. **El código no puede contener ninguna referencia a esos productos ni a sus marcas**, ni
copiar su texto (`tests/test_no_vendor_names_v010.py`).

---

© 2026 Samuel Sáez López — UPCT — AGPL-3.0-or-later
