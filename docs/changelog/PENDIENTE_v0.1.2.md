# OGR GUI 0.1.2 — (sin fecha: se pone al etiquetar)

Un cambio compatible, la [spec 003](../../spec/features/003-espanol-del-nucleo/spec.md), que pidió
OGR FEM2D el 2026-11-25 para los mensajes de `ogr_core.api` y que la propietaria extendió a todos
los catálogos del núcleo: el español de los mensajes con código de `ogr_core`, en `ogr_ui`.

## 1. Qué cambia

| Pieza | 0.1.1 | 0.1.2 |
|---|---|---|
| `ogr_ui/i18n/core_es.py` | — | nuevo: `CORE_ES`, 335 entradas, una por plantilla con palabras de los 20 catálogos de `ogr_core` v0.2.12, por catálogo y con el código en un comentario. No importa nada |
| `tr()` en español | los textos de las piezas | además las plantillas del núcleo, desde que se importa `ogr_ui.i18n`, sin que el programa haga nada |
| `package_translations("es")` | `ES` (72 entradas) | `ES` y `CORE_ES` (407); ninguna clave está en las dos |
| El extra `[test]` | `ogr-core` v0.2.8 | v0.2.12 (decisión de la propietaria) |
| Versión entre etiquetas | — | `0.1.2.dev0` |

## 2. Qué se encontró

- **Los catálogos** (`ogr_core` v0.2.12): 20 diccionarios de `MessageSpec` y 346 códigos, que dan
  345 plantillas distintas. Diez no tienen palabras (`{first}; {second}`, `{type}: {text}`,
  `{name} #{n}`…) y no llevan entrada (RF-6). **Ninguna plantilla del núcleo tiene hoy forma
  singular** (`one`): las tienen los mensajes de Slip2D, no los del núcleo. El test la comprobaría
  igual, y lo demuestra con un catálogo hecho en el test.
- **Dos módulos del núcleo no se importan** sin una dependencia opcional suya
  (`ogr_core.statistics.probabilistic` y `ogr_core.statistics.sensitivity`); el test comprueba que
  no definen ningún catálogo, para que saltarlos no esconda ninguno.
- **El español de OGR Slip2D** (`ogr_gui/i18n/__init__.py`, commit `67faf4f`, v0.1.492, sobre el
  núcleo v0.2.12) tiene 237 de las plantillas: todas las de los 17 catálogos que traduce y las 5 de
  `REPORTED_NOTES`. Faltaban las 70 con palabras de `ogr_core.api` y las 28 de `REFINE_MESSAGES`
  (el mallador de FEM2D): las 98 se han escrito en esta versión (abajo, sección 4).
- **RF-8, ninguna.** Se buscaron en las 237 de Slip2D las palabras de equilibrio límite («dovela»,
  «talud», «superficie de deslizamiento» o «de rotura», «factor de seguridad», «FS», «método»,
  «rotura», «deslizamiento») sin su palabra inglesa en la plantilla, y se leyeron a mano las 41
  entradas que tienen alguna de esas o «búsqueda», «círculo» o «equilibrio». En todas la palabra está también en el inglés («slices», «Slope
  Limits», «the sliding of the surface», «analysis method»…): son plantillas de equilibrio límite,
  no generales.
- **RF-9: cuatro de Slip2D no conservan los campos de su plantilla.** La plantilla dice `{name!r}`
  (el valor sale entre comillas rectas, `'Arcilla'`) y Slip2D escribe `«{name}»`. Aquí llevan las
  palabras de Slip2D con los campos de la plantilla (decisión de la propietaria del 2026-11-27, al
  encontrarlo; la spec ganó RF-9):

| Código | Slip2D (`67faf4f`) | `ogr_ui` 0.1.2 |
|---|---|---|
| `import.water_dropped` | «{name}» usaba una superficie de agua del otro proyecto; asígnale una de este modelo. | {name!r} usaba una superficie de agua del otro proyecto; asígnale una de este modelo. |
| `import.anisotropic_dropped` | «{name}» ha perdido su superficie anisótropa, que era del otro proyecto. | {name!r} ha perdido su superficie anisótropa, que era del otro proyecto. |
| `import.link_renamed` | «{name}»: {who} toma ahora la resistencia de «{here}», el material de ese nombre en este modelo. | {name!r}: {who} toma ahora la resistencia de {here!r}, el material de ese nombre en este modelo. |
| `import.link_dropped` | «{name}»: {who} enlazaba un material que este modelo no puede enlazar; conserva la resistencia que tenía, sin enlace. | {name!r}: {who} enlazaba un material que este modelo no puede enlazar; conserva la resistencia que tenía, sin enlace. |

- **Dos se traducen por sí mismas** y van a `IDENTICAL` de `tests/test_i18n_v010.py` con su porqué:
  `api.error` («error») y `api.bridge.listing.item` («pid {pid} ({title})»).
- **Los valores no se traducen aquí.** Varias plantillas de `ogr_core.api` llevan como valor el
  nombre de una operación o una ruta de menú (`{new_op}`, `{tool}`, `{menu}`, `{program}`). Si el
  programa pasa un menú en inglés, la frase sale en español con el menú en inglés: el valor es del
  programa.

## 3. Tests

`tests/test_core_messages_v012.py`, 20 casos: los 20 catálogos de la v0.2.12, encontrados
recorriendo el núcleo; cada plantilla con su traducción, y una que falta, nombrada con su catálogo y
su código (también la forma singular, con un catálogo hecho en el test); ninguna entrada que no sea
una plantilla del núcleo; `tr()` y `render(..., translate=tr)` en español sin nada más
(«El modelo p1 está ocupado con una lectura (3 s).»); las palabras de Slip2D, contra una copia
congelada de sus 237 entradas (`tests/data/slip2d_core_es_67faf4f.json`), salvo las de RF-9, que
están en este changelog; los campos de cada traducción (nombre, conversión y formato, como
multiconjunto, con traducciones malas que el comparador rechaza); las plantillas sin palabras; una
plantilla de un núcleo más nuevo, que sale en inglés. `test_i18n_v010.py`:
`test_package_translations_is_a_copy` pasa a esperar `ES` y `CORE_ES`, e `IDENTICAL` tiene las dos
de arriba.

## 4. Las 98 entradas nuevas, para leerlas

Escritas en esta versión con la terminología de las de Slip2D («Los que hay», «tiene que ser»,
«puente para agentes», «en marcha», «tarea»). Las demás son las de Slip2D, tal como estaban.

| Código | Inglés | Español |
|---|---|---|
| `api.did_you_mean.one` | Did you mean '{name}'? | ¿Querías decir «{name}»? |
| `api.did_you_mean.many` | Did you mean {names} or '{last}'? | ¿Querías decir {names} o «{last}»? |
| `api.unknown` | Unknown {kind} {word!r}. | {kind} desconocido: {word!r}. |
| `api.known` | Known: {names}. | Los que hay: {names}. |
| `api.known.more` | Known: {names} (+{more} more). | Los que hay: {names} (y {more} más). |
| `api.field.empty_path` | An empty {root} path. | Una ruta de {root} vacía. |
| `api.field.empty_path.hint` | Use 'section.field', e.g. '{example}'. | Usa «sección.campo», por ejemplo «{example}». |
| `api.field.empty_path.hint.plain` | Use 'section.field'. | Usa «sección.campo». |
| `api.field.too_deep` | '{walked}' is a value, not a section; '{path}' goes too deep. | «{walked}» es un valor, no una sección; «{path}» baja demasiado. |
| `api.field.retired` | '{path}' is not a {root} any more. | «{path}» ya no es un {root}. |
| `api.field.unknown` | '{name}' is not a field of {where}. | «{name}» no es un campo de {where}. |
| `api.field.listing` | Fields of {where}: {names}. | Campos de {where}: {names}. |
| `api.field.listing.more` | Fields of {where}: {names} (+{more} more). | Campos de {where}: {names} (y {more} más). |
| `api.field.listing.more_tool` | Fields of {where}: {names} (+{more} more; {tool} lists them). | Campos de {where}: {names} (y {more} más; {tool} los lista). |
| `api.value.not_one_of` | {where}: {raw!r} is not one of {options}. | {where}: {raw!r} no es ninguno de {options}. |
| `api.value.null` | {where} cannot be null. | {where} no puede ser nulo. |
| `api.value.not_a` | {where}: {raw!r} is not a {type}. | {where}: {raw!r} no es un {type}. |
| `api.value.list` | {where} must be a list, got {raw!r}. | {where} tiene que ser una lista, y es {raw!r}. |
| `api.value.object` | {where} must be an object, got {raw!r}. | {where} tiene que ser un objeto, y es {raw!r}. |
| `api.value.bool` | {where} must be true or false, got {raw!r}. | {where} tiene que ser true o false, y es {raw!r}. |
| `api.value.int` | {where} must be an integer, got {raw!r}. | {where} tiene que ser un entero, y es {raw!r}. |
| `api.value.number` | {where} must be a number, got {raw!r}. | {where} tiene que ser un número, y es {raw!r}. |
| `api.value.finite` | {where} must be finite, got {raw!r}. | {where} tiene que ser finito, y es {raw!r}. |
| `api.value.string` | {where} must be a string, got {raw!r}. | {where} tiene que ser un texto, y es {raw!r}. |
| `api.value.section` | {where} is a whole section; set its fields one by one (e.g. '{where}.&lt;field>'). | {where} es una sección entera; da sus campos uno a uno (por ejemplo, «{where}.&lt;campo>»). |
| `api.value.point` | {where} must be [x, y], got {raw!r}. | {where} tiene que ser [x, y], y es {raw!r}. |
| `api.value.points` | {where} must be a list of [x, y] pairs. | {where} tiene que ser una lista de pares [x, y]. |
| `api.value.points.few` | {where} needs at least {minimum} points, got {count}. | {where} necesita al menos {minimum} puntos, y tiene {count}. |
| `api.job.busy` | Job {job_id} is still running. | La tarea {job_id} sigue en marcha. |
| `api.job.busy.hint` | Wait for it with {wait_op}('{job_id}', wait_seconds=...) or stop it with {cancel_op}. | Espérala con {wait_op}('{job_id}', wait_seconds=...) o detenla con {cancel_op}. |
| `api.job.crashed` | The analysis process ended without reporting a result. | El proceso del análisis terminó sin dar un resultado. |
| `api.model.none_open` | No model is open. | No hay ningún modelo abierto. |
| `api.model.none_open.hint` | Call {new_op} or {open_op} first. | Llama antes a {new_op} o a {open_op}. |
| `api.model.several` | Several models are open; say which one with project_id. | Hay varios modelos abiertos; di cuál con project_id. |
| `api.model.several.hint` | Open: {models} | Abiertos: {models} |
| `api.model.busy` | Model {model} is busy with {what} ({since:.0f} s). | El modelo {model} está ocupado con {what} ({since:.0f} s). |
| `api.model.another_operation` | another operation | otra operación |
| `api.model.read` | a read | una lectura |
| `api.retry` | Retry when it finishes. | Vuelve a intentarlo cuando termine. |
| `api.retry.window` | Retry when the window has finished. | Vuelve a intentarlo cuando la ventana haya terminado. |
| `api.path.empty` | A path must be a non-empty string. | Una ruta tiene que ser un texto no vacío. |
| `api.path.suffix` | {name!r} does not end in {suffix}. | {name!r} no termina en {suffix}. |
| `api.path.relative` | {path!r} is a relative path and no working directory was configured. | {path!r} es una ruta relativa y no se ha configurado ninguna carpeta de trabajo. |
| `api.path.relative.hint` | Pass an absolute path, or start the server with --workdir. | Da una ruta absoluta, o arranca el servidor con --workdir. |
| `api.path.no_folder` | The folder {folder} does not exist. | La carpeta {folder} no existe. |
| `api.path.exists` | {path} already exists. | {path} ya existe. |
| `api.path.exists.hint` | Pass overwrite=true to replace it. | Da overwrite=true para sustituirlo. |
| `api.path.missing` | {path} does not exist. | {path} no existe. |
| `api.bridge.no_pid` | No {program} window with pid {pid} has its agent bridge on. | Ninguna ventana de {program} con pid {pid} tiene activo su puente para agentes. |
| `api.bridge.none` | No {program} window has its agent bridge on. | Ninguna ventana de {program} tiene activo su puente para agentes. |
| `api.bridge.none.hint` | In the window: {menu}. | En la ventana: {menu}. |
| `api.bridge.several` | Several {program} windows have their bridge on; say which with --attach PID. | Hay varias ventanas de {program} con su puente activo; di cuál con --attach PID. |
| `api.bridge.listing.none` | None is running. | No hay ninguna en marcha. |
| `api.bridge.listing` | Running: {windows} | En marcha: {windows} |
| `api.bridge.listing.item` | pid {pid} ({title}) | pid {pid} ({title}) |
| `api.bridge.handshake_refused` | handshake refused | saludo rechazado |
| `api.bridge.closed` | The {program} window closed the bridge. | La ventana de {program} cerró el puente. |
| `api.bridge.no_window` | No {program} window is open with its agent bridge on. | No hay ninguna ventana de {program} abierta con su puente para agentes activo. |
| `api.bridge.no_window.hint` | Open {program} (the bridge starts with it) or turn on {menu}, then repeat the call. | Abre {program} (el puente arranca con él) o activa {menu}, y repite la llamada. |
| `api.bridge.lost` | The {program} window closed while answering this call. | La ventana de {program} se cerró mientras respondía a esta llamada. |
| `api.bridge.lost.hint` | It is not repeated automatically, because whether it ran there cannot be known: check the model ({summary_op}) and repeat it if needed. | No se repite sola, porque no se puede saber si llegó a hacerse allí: comprueba el modelo ({summary_op}) y repítela si hace falta. |
| `api.bridge.mode.window_only` | window only | solo la ventana |
| `api.bridge.mode.automatic` | automatic | automático |
| `api.bridge.next.window` | the open window | la ventana abierta |
| `api.bridge.next.nowhere` | nowhere: no window is open | a ningún sitio: no hay ninguna ventana abierta |
| `api.bridge.next.local` | the server's own models | los modelos del propio servidor |
| `api.bridge.unauthorized` | Wrong protocol or token. | Protocolo o token incorrectos. |
| `api.bridge.not_json` | Not a JSON line. | No es una línea JSON. |
| `api.bridge.bad_request` | A request is {{'id', 'op', 'kwargs'}}. | Una petición es {{'id', 'op', 'kwargs'}}. |
| `api.error` | error | error |
| `refine.bad_ratio` | the quality bound B = {ratio:.6g} is below sqrt(2) = 1.41421: Delaunay refinement is guaranteed to finish only for B >= sqrt(2) | el límite de calidad B = {ratio:.6g} es menor que sqrt(2) = 1.41421: el refinamiento de Delaunay solo tiene garantizado terminar con B >= sqrt(2) |
| `refine.bad_size` | the size bound at ({x:.6g}, {y:.6g}) is {h}: it must be a positive length, or infinity where there is no bound | el límite de tamaño en ({x:.6g}, {y:.6g}) es {h}: tiene que ser una longitud positiva, o infinito donde no hay límite |
| `refine.empty` | nothing to mesh: the input needs at least three vertices, one segment and one seed | no hay nada que mallar: la entrada necesita al menos tres vértices, un segmento y una semilla |
| `refine.bad_vertex` | vertex {i} is not a point of two finite coordinates | el vértice {i} no es un punto de dos coordenadas finitas |
| `refine.duplicate_vertex` | vertices {i} and {j} are the same point ({x:.6g}, {y:.6g}) | los vértices {i} y {j} son el mismo punto ({x:.6g}, {y:.6g}) |
| `refine.bad_segment` | segment {k} does not join two different input vertices ({u} and {v}) | el segmento {k} no une dos vértices distintos de la entrada ({u} y {v}) |
| `refine.duplicate_segment` | segments {k} and {j} join the same two vertices | los segmentos {k} y {j} unen los mismos dos vértices |
| `refine.crossing_segments` | segments {k} and {j} cross or overlap | los segmentos {k} y {j} se cruzan o se solapan |
| `refine.vertex_on_segment` | vertex {i} lies inside segment {k} | el vértice {i} queda dentro del segmento {k} |
| `refine.seed_on_segment` | the seed of region {region} at ({x:.6g}, {y:.6g}) lies on a segment or on a vertex | la semilla de la región {region} en ({x:.6g}, {y:.6g}) queda sobre un segmento o un vértice |
| `refine.void_on_segment` | the void point ({x:.6g}, {y:.6g}) lies on a segment or on a vertex | el punto de hueco ({x:.6g}, {y:.6g}) queda sobre un segmento o un vértice |
| `refine.seed_outside` | the seed of region {region} at ({x:.6g}, {y:.6g}) is outside the domain or in a void | la semilla de la región {region} en ({x:.6g}, {y:.6g}) queda fuera del dominio o en un hueco |
| `refine.void_outside` | the void point ({x:.6g}, {y:.6g}) is outside the domain | el punto de hueco ({x:.6g}, {y:.6g}) queda fuera del dominio |
| `refine.seeds_share_region` | the seeds of regions {first} and {second} are in the same region: no segments separate them | las semillas de las regiones {first} y {second} están en la misma región: ningún segmento las separa |
| `refine.region_without_seed` | a part of the domain bounded by segments has no seed; one of its points is ({x:.6g}, {y:.6g}) | una parte del dominio cerrada por segmentos no tiene semilla; uno de sus puntos es ({x:.6g}, {y:.6g}) |
| `refine.vertex_outside` | vertex {i} at ({x:.6g}, {y:.6g}) is outside the domain or in a void | el vértice {i} en ({x:.6g}, {y:.6g}) queda fuera del dominio o en un hueco |
| `refine.too_many_triangles` | the mesh reached {limit} triangles before it was finished: raise the limit, or relax the size bound | la malla llegó a {limit} triángulos antes de terminar: sube el límite, o relaja el límite de tamaño |
| `refine.too_fine` | the refinement made edges too short for the floating-point coordinates near ({x:.6g}, {y:.6g}) and cannot go on | el refinamiento dejó aristas demasiado cortas para las coordenadas en coma flotante cerca de ({x:.6g}, {y:.6g}) y no puede seguir |
| `refine.bad_arc` | the centre of the arc of segment {k} is not a point of two finite coordinates | el centro del arco del segmento {k} no es un punto de dos coordenadas finitas |
| `refine.arc_radii` | the ends of segment {k} are at {r1:.9g} and {r2:.9g} from the centre of its arc: they must be at the same distance | los extremos del segmento {k} están a {r1:.9g} y a {r2:.9g} del centro de su arco: tienen que estar a la misma distancia |
| `refine.arc_turn` | the arc of segment {k} turns {angle:.6g} degrees: at most 60; split it into pieces | el arco del segmento {k} gira {angle:.6g} grados: como mucho 60; divídelo en trozos |
| `refine.vertex_in_arc` | vertex {i} lies between segment {k} and its arc | el vértice {i} queda entre el segmento {k} y su arco |
| `refine.seed_in_arc` | the seed of region {region} at ({x:.6g}, {y:.6g}) lies between segment {k} and its arc | la semilla de la región {region} en ({x:.6g}, {y:.6g}) queda entre el segmento {k} y su arco |
| `refine.void_in_arc` | the void point ({x:.6g}, {y:.6g}) lies between segment {k} and its arc | el punto de hueco ({x:.6g}, {y:.6g}) queda entre el segmento {k} y su arco |
| `refine.segment_in_arc` | segment {j} enters the arc of segment {k}: between the arc and its chord, or across the arc | el segmento {j} entra en el arco del segmento {k}: entre el arco y su cuerda, o cruzando el arco |
| `refine.internal` | an internal check of the mesher failed near ({x:.6g}, {y:.6g}); no mesh is returned. Please report it | una comprobación interna del mallador falló cerca de ({x:.6g}, {y:.6g}); no se devuelve ninguna malla. Por favor, avisa del fallo |
| `refine.arc_unproven` | the input has arcs. Pav and Walkington prove that their algorithm ends, with arc pieces that turn up to {turn:.3g} degrees, for B > {ratio:.4g}. This mesher is not exactly that algorithm (concentric shells, the Terminator), and no source proves that it ends with arcs | la entrada tiene arcos. Pav y Walkington demuestran que su algoritmo termina, con trozos de arco que giran hasta {turn:.3g} grados, para B > {ratio:.4g}. Este mallador no es exactamente ese algoritmo (capas concéntricas, el Terminator), y ninguna fuente demuestra que termine con arcos |
| `refine.length_unit` | next to a vertex where two segments meet, the mesh splits the segments at distances that are powers of two of the unit of length: the same model in other units gives another mesh | junto a un vértice donde se unen dos segmentos, la malla divide los segmentos a distancias que son potencias de dos de la unidad de longitud: el mismo modelo en otras unidades da otra malla |

## 5. Qué tiene que hacer un programa

Nada: un programa que dice los mensajes del núcleo con `render(..., translate=tr)` y el `tr()` de
`ogr_ui` los ve en español al subir a la 0.1.2.

- **OGR FEM2D**: nada en su `say()`. Sus errores de `ogr_core.api` salen en español. Dos cosas que
  puede mirar:
  - `say()` dice con `render` los de `API_MESSAGES` y `FEM_MESSAGES`. Un mensaje de otro catálogo del
    núcleo (los del mallador, `REFINE_MESSAGES`) tiene ya su español, pero solo sale en español si
    `say()` lo busca también en su catálogo.
  - Los valores que pasa como menú o como operación (`{menu}`, `{tool}`) los traduce él.
  - Su `install()` sigue devolviendo `[]`. Su diccionario tiene una de estas plantillas, «Edit
    boundary ({op})» (su `fem.step.boundary_edit`, la misma inglesa que la de `STEP_NAMES`), con la
    misma traducción, «Editar contorno ({op})».
- **OGR Slip2D**, cuando adopte el paquete: puede quitar de su diccionario las 237 entradas de las
  plantillas del núcleo. Su `add_translations` le devolverá las cuatro de RF-9 (arriba) si las
  conserva: o adopta las de `ogr_ui` o las deja a propósito.
- **Un programa con un núcleo anterior a la v0.2.12** (FEM2D fija la v0.2.9) tiene traducciones de
  más, que no se usan.
