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
| OGR FEM2D | `samuelsl27/OGR-FEM2D` | `v0.2.0` | 2026-11-28 (`7f44ad4`; antes, la `v0.1.3` desde el 2026-11-27, `41a6c5d`, y la `v0.1.0` desde el 2026-11-24, `c49831d`) | `python tests/_runner.py` |

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
| Entrada X,Y | solo absolutos con punto decimal; la ayuda habla de la polilínea de Slip2D | desde la 0.1.3, relativos (`@dx, dy`) y polares (`@d<a`), desde el punto que el programa da con `set_point_reference`; lo que no se puede leer se queda con su motivo en la barra. Desde la 0.2.0, `x.x,x.x`: solo la coma separa y el decimal es el punto |
| Números en pantalla | f-strings y `QDoubleSpinBox` con la configuración de la máquina | desde la 0.1.4, siempre con punto: `ogr_ui.numbers.format_number` para escribir y `ogr_ui.widgets.NumberBox` para las casillas, en las que la coma no se escribe |
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
| Spec 002: el percentil del ajuste, por campo | OGR FEM2D | Hecha en la 0.1.1; adoptada por FEM2D con la `v0.1.3` (`41a6c5d`) |
| Spec 003: el español de los mensajes del núcleo | OGR FEM2D (y Slip2D al adoptar) | Hecha en la 0.1.2; adoptada por FEM2D con la `v0.1.3` (`41a6c5d`) |
| Spec 004: la entrada X,Y con relativos, polares y coma decimal | OGR FEM2D | Hecha en la 0.1.3; adoptada por FEM2D con la `v0.1.3` (`41a6c5d`) |
| Spec 005: los números en pantalla, siempre con punto decimal | OGR FEM2D (y OGR Data al adoptar) | Hecha en la 0.1.4; adoptada por FEM2D con la `v0.2.0` (`7f44ad4`) |
| Spec 006: en la entrada X,Y, la coma separa y el punto es el decimal | OGR FEM2D (y Slip2D y OGR Data al adoptar) | Hecha en la 0.2.0, **incompatible**; adoptada por FEM2D con la `v0.2.0` (`7f44ad4`), avisado antes de la etiqueta |

## Pendiente de OGR Slip2D, para cuando lo adopte

Cambios de Slip2D en piezas con gemela aquí que **no** piden código en `ogr_ui`, sino una forma de
escribirlos al adoptarlo. Se anotan al recibirlos; se tachan cuando Slip2D fije una versión.

- **Slip2D 0.1.500 (`99b66f6`, D438), `ContourSettings.for_reported(caption)`.** La escala de
  partida del campo del factor cuando la corrida informa de un Ky o de un desplazamiento de
  Newmark. Es de dominio y no entra aquí: con `ogr_ui` 0.1.3 es un `ContourField` por magnitud,
  que el programa da al diálogo según lo que informe la corrida
  (comprobado el 2026-11-27 con `defaults()` y `fit_to(values, field.fit_percentile)`):
  - Ky: `start=ContourSettings(palette="Viridis", intervals=8, auto_range=True, decimals=4)`,
    con el `fit_percentile` de 0,98 por defecto. Oscuro en el valor bajo;
  - Newmark: lo mismo con `decimals=3, reverse=True` y `fit_percentile=1.0`. Oscuro en el valor
    alto, y el extremo no se recorta;

  (Corregido con la 0.2.0: era «Hot to cold», rojo en el extremo crítico, hasta Slip2D 0.1.506.)
  - factor: el `ContourField` del factor de siempre (0–6 en 24 bandas).

  La marca de la leyenda (`ColourScaleLegend.configure(mark=...)`) no cambia: recibe el Ky o el
  desplazamiento de la crítica en lugar del factor.
- **Slip2D 0.1.502 (`344d9ce`), `ContourSettings.fit_percentile_for(caption)`.** Arregla en Slip2D
  lo que esta sesión le avisó de su diálogo de contornos en la 0.1.500, confirmado allí en vivo
  (Newmark de su D437 en la 0.1.501: la ventana dibujaba 0–31,083 cm y el diálogo proponía
  0–17,862 al abrir, en la casilla y en *Fit*; *Restore Defaults* daba el 0–6 en 24 bandas, también
  con Ky). Ahora el diálogo recibe la magnitud de la corrida y usa su escala (`for_reported`) y su
  percentil (1,0 para Newmark, 0,98 para el resto) en los cuatro caminos; la ventana usa la misma
  regla. No pide nada aquí: en `ogr_ui` es el `fit_percentile` y el `start` del `ContourField` de
  cada magnitud (spec 002, 0.1.1), y `fit_percentile_for` desaparece al adoptarlo. El tercer
  punto del aviso, 24 intervalos al tocar la casilla del rango automático, **no se reprodujo**:
  esa línea es del botón «0 a 6», que en una corrida sísmica pasa a deshabilitarse; la lectura de
  esta sesión estaba equivocada.
- **Slip2D 0.1.503 (`fa73de8`, D442), el conmutador *Critical Probabilistic Surface* de
  Interpretar.** Su changelog dejaba la gemela aquí «sin comprobar»; comprobado el 2026-11-27,
  **no la hay**. Lo que toca es de Slip2D: `interpret_window.py`, `canvas/canvas_view.py`
  (`PROBABILISTIC_SURFACE_COLOUR`, `#f77f00`), `probabilistic.py` (`user_defined`) y dos textos
  de su `i18n`. En `ogr_ui` no hay ventana de Interpretar ni lienzo, ninguna clave de
  `ROLE_COLORS` es un color de superficie, y los dos textos no son del núcleo, así que no van a
  `core_es.py`. Lo único compartido que usa el camino es `disabled_reasons.gate`, idéntica en los
  dos repositorios y sin cambios: desmarcar una entrada que se queda gris lo hace Slip2D por su
  cuenta (`refresh_statistics_gates`), no `gate`.
- **Slip2D 0.1.506 (`c4c46df`), Viridis en todo campo que no es el factor de seguridad.** La
  propuesta D5 de OGR FEM2D, con el alcance que eligió la propietaria el 2026-11-28: los campos
  hidráulicos, el Ky y el Newmark empiezan en Viridis (`FIELD_PALETTE`), de luminosidad creciente,
  oscuros en el extremo crítico. El factor sigue en Rainbow de 24 bandas, 0–6. **Tiene gemela
  aquí**: `ContourSettings.automatic(field)`, la partida de un `ContourField` sin `start`, decía
  «Hot to cold». Desde la 0.2.0 usa `FIELD_PALETTE = "Viridis"`, como Slip2D, con un test que
  calcula la L* de CIE 1976 de cada parada. FEM2D da su propio `start` a cada campo, así que no le
  cambia nada que no elija él.
- **Slip2D 0.1.497–0.1.501, `i18n`.** Las entradas nuevas son de catálogos del motor de Slip2D
  (`method.newmark_record_missing`, `method.seismic_static_unstable*`, `stat.sens_no_range`), dos
  *tooltips* del lienzo y la nota de la página Seismic. Ninguna es de `ogr_core`, así que nada va
  a `ogr_ui/i18n/core_es.py`: se quedan en el diccionario de Slip2D, que las añade con
  `add_translations()`. Tampoco iría allí la fila «Critical surface» del informe si OGR-Core la
  saca: es un `T("...")` del informe, no un mensaje con código.
- **El censo de términos retirados de Slip2D** (`\bFoS\b` sobre los valores en castellano) tomó el
  campo `{fos:.4f}` por el término. Aquí no hay censo de términos; los que miran letras en un
  texto quitan antes los campos (`ogr_ui.testing.texts._letters` y `wordless` de
  `tests/test_core_messages_v012.py`). Si se añade uno, que haga lo mismo.

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
