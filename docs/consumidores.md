# Quién usa OGR GUI

Qué programas de la suite usan este paquete, qué versión fija cada uno, qué cambios están en curso
y para quién, y cómo se pide y se adopta un cambio. Las reglas están en
[`AGENTS.md`](../AGENTS.md); esto es el estado.

Es la tabla equivalente a la de `docs/consumidores.md` de OGR-Core, aquí y no allí: `ogr-gui` no
depende del núcleo (decisión de la propietaria del 2026-11-24), así que no es un consumidor suyo
más que para su runner de tests, que entra por el extra `[test]`.

## Programas

| Programa | Repositorio | `ogr-gui` que fija | Desde | Suite entera |
|---|---|---|---|---|
| OGR FEM2D | `samuelsl27/OGR-FEM2D` | `v0.1.0` | 2026-11-24 (su spec 006, T19, `c49831d`) | `python tests/_runner.py` |

- **La verdad es el `pyproject.toml` de cada programa**
  (`ogr-gui @ git+https://github.com/samuelsl27/OGR-GUI@vX.Y.Z`). Esta tabla la repite para que se
  vea quién se queda atrás, y se corrige aquí cuando un programa sube su fijación.
- **OGR Slip2D y OGR Data** no lo usan: llevan sus propias copias de estas piezas (Slip2D, el
  original; OGR Data, una copia a mano de los temas, de `tr()` y del patrón de operaciones en
  `ogr_data/gui/`). Lo adoptan cuando sus sesiones lo decidan; nada de esto les obliga. Cuando uno
  lo fije, entra en la tabla.
- **«Suite entera»** es el comando que el `AGENTS.md` del programa da para publicar, con el Python
  de su `.venv` y desde su carpeta.

## Lo que un programa hace al adoptarlo

Lo que en OGR Slip2D estaba atado al programa o al núcleo y aquí se recibe:

| Pieza | En Slip2D | Aquí |
|---|---|---|
| Enganche | `resolve(cursor, boundaries)`, con los `Boundary` y `Vertex` del núcleo | `resolve(cursor, shapes)`, con `SnapShape` (`SnapShape.polyline(puntos, cerrado)`) y `SnapPoint` |
| Tareas | el progreso y las fases de `ogr_core.progress` | `install_progress(watching, phase, phase_texts)` una vez, al arrancar |
| Diálogo de progreso | `ogr_gui/dialogs/misc_dialogs.py`, con la fase `OPTIMIZE` | `ogr_ui.dialogs.progress_dialog`, con los textos de fase del programa |
| Preferencias | funciones de módulo con `"OGR Slip2D"` dentro | `Preferences("Nombre del programa", "nombre-de-archivo")` |
| Contornos | `SCALAR_FIELDS`, `available_fields`, `ContourSettings.for_field` (el 0–6 del factor de seguridad) | `ContourField` y `RangePreset`, que da el programa al diálogo; desde la 0.1.1, `ContourField.fit_percentile` (0,98 por defecto; 1 para el rango entero), que el programa pasa también a `fit_to` cuando ajusta el rango al dibujar |
| Leyenda | título por defecto «Factor of safety» | título vacío: lo pone el programa |
| Modo de los *data tips* | `ogr_gui.data_tips.DataTipMode` | `ogr_ui.data_tip_mode.DataTipMode` (los *data tips* siguen en el programa) |
| Entrada X,Y | solo absolutos con punto decimal; la ayuda habla de la polilínea de Slip2D | desde la 0.1.3, relativos (`@dx, dy`), polares (`@d<a`) y coma decimal, desde el punto que el programa da con `set_point_reference`; lo que no se puede leer se queda con su motivo en la barra |
| Iconos | solo el catálogo | `register()` para las claves propias; una clave de la suite no se redefine |
| `tr()` | el diccionario entero del programa | el mecanismo y el español de estas piezas; desde la 0.1.2, también el de las plantillas de los mensajes con código del núcleo, que el programa ya no lleva; el programa añade el suyo con `add_translations()`, que devuelve las claves que cambió |
| Reglas 2 y 3 | tests del programa | `ogr_ui.testing.texts` y `ogr_ui.testing.menus`, llamados por los tests del programa |

Lo que el runner del programa añade a su lista blanca de fugas por estas piezas: las mismas
entradas que tiene `tests/_runner.py` de este repositorio (la caché de iconos, la guarda de la
rueda, el suelo de los botones, la paleta original, el recolector, `backend_fallback` de
Matplotlib), con `ogr_ui` en lugar de `ogr_gui`.

## Cambios en curso

| Cambio | Para quién | Estado |
|---|---|---|
| Spec 002: el percentil del ajuste, por campo | OGR FEM2D | Hecha en la 0.1.1; FEM2D la adopta cuando suba su fijación (`CHANGELOG_v0.1.1.md`, sección 4) |
| Spec 003: el español de los mensajes del núcleo | OGR FEM2D (y Slip2D al adoptar) | Hecha en la 0.1.2; FEM2D la adopta cuando suba su fijación (`CHANGELOG_v0.1.2.md`, sección 5) |
| Spec 004: la entrada X,Y con relativos, polares y coma decimal | OGR FEM2D | Validada en la PR #3 (`PENDIENTE_v0.1.3.md`); por fusionar y etiquetar |

## Cómo pide un programa un cambio

El código de `ogr_ui` solo se cambia en este repositorio. La sesión de un programa que necesita
algo **no lo edita ni lo copia**: lo pide por escrito, con lo que encontró y la evidencia, y lo
lleva la propietaria a la sesión de OGR-GUI. El cambio va en una rama corta con su PR; antes de
etiquetar, la suite entera de este repositorio y la de cada programa de la tabla contra el árbol
que se etiqueta.

## Cómo sube un programa la versión que fija

En un commit suyo y a propósito; nunca fija una rama.

1. `pyproject.toml`: `ogr-gui @ git+https://github.com/samuelsl27/OGR-GUI@vX.Y.Z`.
2. Su entorno, que no se entera solo:

   ```bash
   .venv/Scripts/python -m pip install --no-deps --force-reinstall "ogr-gui @ git+https://github.com/samuelsl27/OGR-GUI@vX.Y.Z"
   ```

3. Lo que el changelog de esa versión le pida.
4. Su suite entera.
5. La fila de la tabla de arriba, que se corrige en este repositorio.
