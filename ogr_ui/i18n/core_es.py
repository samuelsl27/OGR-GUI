# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
The Spanish of the coded messages of OGR Core (spec 003, OGR GUI 0.1.2).

The core does not translate: a message leaves ``ogr_core`` with a code,
an English template and its values, and ``ogr_core.messages.render``
says it with the program's ``tr()``. The templates are the same in every
program, so their Spanish lives here, once, and :func:`ogr_ui.i18n.tr`
has it from the start.

Every template of the coded catalogues of ``ogr_core`` v0.2.12 (the tag
of the ``[test]`` extra), the singular forms included, grouped by
catalogue, with the code of each entry in a comment. Written once from
two sources, and edited by hand from then on:

* OGR Slip2D's dictionary (``ogr_gui/i18n/__init__.py`` at ``67faf4f``,
  v0.1.492, on the core v0.2.12): the same words, entry by entry (RF-3).
  Four of them keep the fields of their template instead of Slip2D's
  quotes (RF-9; ``tests/test_core_messages_v012.py`` and the changelog
  of 0.1.2 name them);
* the entries Slip2D does not have (``ogr_core.api`` and the mesher's
  ``REFINE_MESSAGES``), written for 0.1.2 in Slip2D's terms and marked
  "new in 0.1.2".

A template with no words (only fields and signs, such as
``{first}; {second}``) has no entry: it reads the same in every language.
This module imports nothing: ``ogr_ui`` does not import the core.
"""
from __future__ import annotations

CORE_ES: dict[str, str] = {
    # ==================================================================
    # ogr_core.api.API_MESSAGES
    # ==================================================================
    # api.did_you_mean.one; new in 0.1.2
    "Did you mean '{name}'?":
        '¿Querías decir «{name}»?',
    # api.did_you_mean.many; new in 0.1.2
    "Did you mean {names} or '{last}'?":
        '¿Querías decir {names} o «{last}»?',
    # api.unknown; new in 0.1.2
    'Unknown {kind} {word!r}.':
        '{kind} desconocido: {word!r}.',
    # api.known; new in 0.1.2
    'Known: {names}.':
        'Los que hay: {names}.',
    # api.known.more; new in 0.1.2
    'Known: {names} (+{more} more).':
        'Los que hay: {names} (y {more} más).',
    # api.field.empty_path; new in 0.1.2
    'An empty {root} path.':
        'Una ruta de {root} vacía.',
    # api.field.empty_path.hint; new in 0.1.2
    "Use 'section.field', e.g. '{example}'.":
        'Usa «sección.campo», por ejemplo «{example}».',
    # api.field.empty_path.hint.plain; new in 0.1.2
    "Use 'section.field'.":
        'Usa «sección.campo».',
    # api.field.too_deep; new in 0.1.2
    "'{walked}' is a value, not a section; '{path}' goes too deep.":
        '«{walked}» es un valor, no una sección; «{path}» baja demasiado.',
    # api.field.retired; new in 0.1.2
    "'{path}' is not a {root} any more.":
        '«{path}» ya no es un {root}.',
    # api.field.unknown; new in 0.1.2
    "'{name}' is not a field of {where}.":
        '«{name}» no es un campo de {where}.',
    # api.field.listing; new in 0.1.2
    'Fields of {where}: {names}.':
        'Campos de {where}: {names}.',
    # api.field.listing.more; new in 0.1.2
    'Fields of {where}: {names} (+{more} more).':
        'Campos de {where}: {names} (y {more} más).',
    # api.field.listing.more_tool; new in 0.1.2
    'Fields of {where}: {names} (+{more} more; {tool} lists them).':
        'Campos de {where}: {names} (y {more} más; {tool} los lista).',
    # api.value.not_one_of; new in 0.1.2
    '{where}: {raw!r} is not one of {options}.':
        '{where}: {raw!r} no es ninguno de {options}.',
    # api.value.null; new in 0.1.2
    '{where} cannot be null.':
        '{where} no puede ser nulo.',
    # api.value.not_a; new in 0.1.2
    '{where}: {raw!r} is not a {type}.':
        '{where}: {raw!r} no es un {type}.',
    # api.value.list; new in 0.1.2
    '{where} must be a list, got {raw!r}.':
        '{where} tiene que ser una lista, y es {raw!r}.',
    # api.value.object; new in 0.1.2
    '{where} must be an object, got {raw!r}.':
        '{where} tiene que ser un objeto, y es {raw!r}.',
    # api.value.bool; new in 0.1.2
    '{where} must be true or false, got {raw!r}.':
        '{where} tiene que ser true o false, y es {raw!r}.',
    # api.value.int; new in 0.1.2
    '{where} must be an integer, got {raw!r}.':
        '{where} tiene que ser un entero, y es {raw!r}.',
    # api.value.number; new in 0.1.2
    '{where} must be a number, got {raw!r}.':
        '{where} tiene que ser un número, y es {raw!r}.',
    # api.value.finite; new in 0.1.2
    '{where} must be finite, got {raw!r}.':
        '{where} tiene que ser finito, y es {raw!r}.',
    # api.value.string; new in 0.1.2
    '{where} must be a string, got {raw!r}.':
        '{where} tiene que ser un texto, y es {raw!r}.',
    # api.value.section; new in 0.1.2
    "{where} is a whole section; set its fields one by one (e.g. '{where}.<field>').":
        '{where} es una sección entera; da sus campos uno a uno (por ejemplo, «{where}.<campo>»).',
    # api.value.point; new in 0.1.2
    '{where} must be [x, y], got {raw!r}.':
        '{where} tiene que ser [x, y], y es {raw!r}.',
    # api.value.points; new in 0.1.2
    '{where} must be a list of [x, y] pairs.':
        '{where} tiene que ser una lista de pares [x, y].',
    # api.value.points.few; new in 0.1.2
    '{where} needs at least {minimum} points, got {count}.':
        '{where} necesita al menos {minimum} puntos, y tiene {count}.',
    # api.job.busy; new in 0.1.2
    'Job {job_id} is still running.':
        'La tarea {job_id} sigue en marcha.',
    # api.job.busy.hint; new in 0.1.2
    "Wait for it with {wait_op}('{job_id}', wait_seconds=...) or stop it with {cancel_op}.":
        "Espérala con {wait_op}('{job_id}', wait_seconds=...) o detenla con {cancel_op}.",
    # api.job.crashed; new in 0.1.2
    'The analysis process ended without reporting a result.':
        'El proceso del análisis terminó sin dar un resultado.',
    # api.model.none_open; new in 0.1.2
    'No model is open.':
        'No hay ningún modelo abierto.',
    # api.model.none_open.hint; new in 0.1.2
    'Call {new_op} or {open_op} first.':
        'Llama antes a {new_op} o a {open_op}.',
    # api.model.several; new in 0.1.2
    'Several models are open; say which one with project_id.':
        'Hay varios modelos abiertos; di cuál con project_id.',
    # api.model.several.hint; new in 0.1.2
    'Open: {models}':
        'Abiertos: {models}',
    # api.model.busy; new in 0.1.2
    'Model {model} is busy with {what} ({since:.0f} s).':
        'El modelo {model} está ocupado con {what} ({since:.0f} s).',
    # api.model.another_operation; new in 0.1.2
    'another operation':
        'otra operación',
    # api.model.read; new in 0.1.2
    'a read':
        'una lectura',
    # api.retry; new in 0.1.2
    'Retry when it finishes.':
        'Vuelve a intentarlo cuando termine.',
    # api.retry.window; new in 0.1.2
    'Retry when the window has finished.':
        'Vuelve a intentarlo cuando la ventana haya terminado.',
    # api.path.empty; new in 0.1.2
    'A path must be a non-empty string.':
        'Una ruta tiene que ser un texto no vacío.',
    # api.path.suffix; new in 0.1.2
    '{name!r} does not end in {suffix}.':
        '{name!r} no termina en {suffix}.',
    # api.path.relative; new in 0.1.2
    '{path!r} is a relative path and no working directory was configured.':
        '{path!r} es una ruta relativa y no se ha configurado ninguna carpeta de trabajo.',
    # api.path.relative.hint; new in 0.1.2
    'Pass an absolute path, or start the server with --workdir.':
        'Da una ruta absoluta, o arranca el servidor con --workdir.',
    # api.path.no_folder; new in 0.1.2
    'The folder {folder} does not exist.':
        'La carpeta {folder} no existe.',
    # api.path.exists; new in 0.1.2
    '{path} already exists.':
        '{path} ya existe.',
    # api.path.exists.hint; new in 0.1.2
    'Pass overwrite=true to replace it.':
        'Da overwrite=true para sustituirlo.',
    # api.path.missing; new in 0.1.2
    '{path} does not exist.':
        '{path} no existe.',
    # api.bridge.no_pid; new in 0.1.2
    'No {program} window with pid {pid} has its agent bridge on.':
        'Ninguna ventana de {program} con pid {pid} tiene activo su puente para agentes.',
    # api.bridge.none; new in 0.1.2
    'No {program} window has its agent bridge on.':
        'Ninguna ventana de {program} tiene activo su puente para agentes.',
    # api.bridge.none.hint; new in 0.1.2
    'In the window: {menu}.':
        'En la ventana: {menu}.',
    # api.bridge.several; new in 0.1.2
    'Several {program} windows have their bridge on; say which with --attach PID.':
        'Hay varias ventanas de {program} con su puente activo; di cuál con --attach PID.',
    # api.bridge.listing.none; new in 0.1.2
    'None is running.':
        'No hay ninguna en marcha.',
    # api.bridge.listing; new in 0.1.2
    'Running: {windows}':
        'En marcha: {windows}',
    # api.bridge.listing.item; new in 0.1.2
    'pid {pid} ({title})':
        'pid {pid} ({title})',
    # api.bridge.handshake_refused; new in 0.1.2
    'handshake refused':
        'saludo rechazado',
    # api.bridge.closed; new in 0.1.2
    'The {program} window closed the bridge.':
        'La ventana de {program} cerró el puente.',
    # api.bridge.no_window; new in 0.1.2
    'No {program} window is open with its agent bridge on.':
        'No hay ninguna ventana de {program} abierta con su puente para agentes activo.',
    # api.bridge.no_window.hint; new in 0.1.2
    'Open {program} (the bridge starts with it) or turn on {menu}, then repeat the call.':
        'Abre {program} (el puente arranca con él) o activa {menu}, y repite la llamada.',
    # api.bridge.lost; new in 0.1.2
    'The {program} window closed while answering this call.':
        'La ventana de {program} se cerró mientras respondía a esta llamada.',
    # api.bridge.lost.hint; new in 0.1.2
    'It is not repeated automatically, because whether it ran there cannot be known: check the model ({summary_op}) and repeat it if needed.':
        'No se repite sola, porque no se puede saber si llegó a hacerse allí: comprueba el modelo ({summary_op}) y repítela si hace falta.',
    # api.bridge.mode.window_only; new in 0.1.2
    'window only':
        'solo la ventana',
    # api.bridge.mode.automatic; new in 0.1.2
    'automatic':
        'automático',
    # api.bridge.next.window; new in 0.1.2
    'the open window':
        'la ventana abierta',
    # api.bridge.next.nowhere; new in 0.1.2
    'nowhere: no window is open':
        'a ningún sitio: no hay ninguna ventana abierta',
    # api.bridge.next.local; new in 0.1.2
    "the server's own models":
        'los modelos del propio servidor',
    # api.bridge.unauthorized; new in 0.1.2
    'Wrong protocol or token.':
        'Protocolo o token incorrectos.',
    # api.bridge.not_json; new in 0.1.2
    'Not a JSON line.':
        'No es una línea JSON.',
    # api.bridge.bad_request; new in 0.1.2
    "A request is {{'id', 'op', 'kwargs'}}.":
        "Una petición es {{'id', 'op', 'kwargs'}}.",
    # api.error; new in 0.1.2
    'error':
        'error',
    # ==================================================================
    # ogr_core.dxf.messages.EXPORT_MESSAGES
    # ==================================================================
    # dxf.export.ezdxf_missing
    "The 'ezdxf' package is required to export DXF files.":
        "Hace falta el paquete 'ezdxf' para exportar archivos DXF.",
    # dxf.export.write_failed
    'Could not write the DXF file: {error}':
        'No se ha podido escribir el archivo DXF: {error}',
    # dxf.export.failed
    'failed':
        'falló',
    # dxf.export.summary
    '{total} entities — {layers}':
        '{total} entidades — {layers}',
    # dxf.export.skipped_mesh
    'mesh ({error})':
        'malla ({error})',
    # dxf.export.skipped_surface
    '{method_id} critical surface ({kind})':
        'superficie crítica de {method_id} ({kind})',
    # dxf.export.skipped_picture
    'image {path} (file not found or not readable): drawn as its frame':
        'imagen {path} (no se encuentra el archivo o no se puede leer): se dibuja su marco',
    # ==================================================================
    # ogr_core.dxf.messages.MESSAGES
    # ==================================================================
    # dxf.empty
    'No geometry was assigned to any layer.':
        'No se asignó geometría a ninguna capa.',
    # dxf.external
    'The external boundary has fewer than three vertices.':
        'El contorno exterior tiene menos de tres vértices.',
    # dxf.external_gap
    'The external boundary was open by {gap:.3f} units and has been closed with a straight segment; check the result.':
        'El contorno exterior estaba abierto {gap:.3f} unidades y se ha cerrado con un segmento recto; revisa el resultado.',
    # dxf.external_missing
    'No layer was assigned to the external boundary; the model cannot define regions without one.':
        'Ninguna capa se ha asignado al contorno exterior; sin él, el modelo no puede definir regiones.',
    # dxf.external_multiple
    '{count} external boundaries were found; the largest will be used and the rest ignored.':
        'Se han encontrado {count} contornos exteriores; se usará el mayor y se ignorará el resto.',
    # dxf.dangling_end
    'A material boundary end does not reach any other boundary, so the region will not close.':
        'Un extremo de un contorno de material no llega a ningún otro contorno, así que la región no se cerrará.',
    # dxf.regions
    'Regions could not be built: {error}':
        'No se pudieron construir las regiones: {error}',
    # dxf.area_mismatch
    'The region areas ({regions:.2f}) do not add up to the external boundary ({external:.2f}): at least one region did not close.':
        'Las áreas de las regiones ({regions:.2f}) no suman la del contorno exterior ({external:.2f}): al menos una región no se cerró.',
    # dxf.unreadable
    'Could not read the DXF file: {error}':
        'No se pudo leer el archivo DXF: {error}',
    # dxf.ezdxf_missing
    "The 'ezdxf' package is required to import DXF files.":
        'Para importar archivos DXF hace falta el paquete «ezdxf».',
    # dxf.no_layer_assigned
    'No layer has been assigned a geometry type. Use the table to say what each layer represents.':
        'Ninguna capa tiene asignado un tipo de geometría. Usa la tabla para decir qué representa cada capa.',
    # ==================================================================
    # ogr_core.fem.messages.REFINE_MESSAGES
    # ==================================================================
    # refine.bad_ratio; new in 0.1.2
    'the quality bound B = {ratio:.6g} is below sqrt(2) = 1.41421: Delaunay refinement is guaranteed to finish only for B >= sqrt(2)':
        'el límite de calidad B = {ratio:.6g} es menor que sqrt(2) = 1.41421: el refinamiento de Delaunay solo tiene garantizado terminar con B >= sqrt(2)',
    # refine.bad_size; new in 0.1.2
    'the size bound at ({x:.6g}, {y:.6g}) is {h}: it must be a positive length, or infinity where there is no bound':
        'el límite de tamaño en ({x:.6g}, {y:.6g}) es {h}: tiene que ser una longitud positiva, o infinito donde no hay límite',
    # refine.empty; new in 0.1.2
    'nothing to mesh: the input needs at least three vertices, one segment and one seed':
        'no hay nada que mallar: la entrada necesita al menos tres vértices, un segmento y una semilla',
    # refine.bad_vertex; new in 0.1.2
    'vertex {i} is not a point of two finite coordinates':
        'el vértice {i} no es un punto de dos coordenadas finitas',
    # refine.duplicate_vertex; new in 0.1.2
    'vertices {i} and {j} are the same point ({x:.6g}, {y:.6g})':
        'los vértices {i} y {j} son el mismo punto ({x:.6g}, {y:.6g})',
    # refine.bad_segment; new in 0.1.2
    'segment {k} does not join two different input vertices ({u} and {v})':
        'el segmento {k} no une dos vértices distintos de la entrada ({u} y {v})',
    # refine.duplicate_segment; new in 0.1.2
    'segments {k} and {j} join the same two vertices':
        'los segmentos {k} y {j} unen los mismos dos vértices',
    # refine.crossing_segments; new in 0.1.2
    'segments {k} and {j} cross or overlap':
        'los segmentos {k} y {j} se cruzan o se solapan',
    # refine.vertex_on_segment; new in 0.1.2
    'vertex {i} lies inside segment {k}':
        'el vértice {i} queda dentro del segmento {k}',
    # refine.seed_on_segment; new in 0.1.2
    'the seed of region {region} at ({x:.6g}, {y:.6g}) lies on a segment or on a vertex':
        'la semilla de la región {region} en ({x:.6g}, {y:.6g}) queda sobre un segmento o un vértice',
    # refine.void_on_segment; new in 0.1.2
    'the void point ({x:.6g}, {y:.6g}) lies on a segment or on a vertex':
        'el punto de hueco ({x:.6g}, {y:.6g}) queda sobre un segmento o un vértice',
    # refine.seed_outside; new in 0.1.2
    'the seed of region {region} at ({x:.6g}, {y:.6g}) is outside the domain or in a void':
        'la semilla de la región {region} en ({x:.6g}, {y:.6g}) queda fuera del dominio o en un hueco',
    # refine.void_outside; new in 0.1.2
    'the void point ({x:.6g}, {y:.6g}) is outside the domain':
        'el punto de hueco ({x:.6g}, {y:.6g}) queda fuera del dominio',
    # refine.seeds_share_region; new in 0.1.2
    'the seeds of regions {first} and {second} are in the same region: no segments separate them':
        'las semillas de las regiones {first} y {second} están en la misma región: ningún segmento las separa',
    # refine.region_without_seed; new in 0.1.2
    'a part of the domain bounded by segments has no seed; one of its points is ({x:.6g}, {y:.6g})':
        'una parte del dominio cerrada por segmentos no tiene semilla; uno de sus puntos es ({x:.6g}, {y:.6g})',
    # refine.vertex_outside; new in 0.1.2
    'vertex {i} at ({x:.6g}, {y:.6g}) is outside the domain or in a void':
        'el vértice {i} en ({x:.6g}, {y:.6g}) queda fuera del dominio o en un hueco',
    # refine.too_many_triangles; new in 0.1.2
    'the mesh reached {limit} triangles before it was finished: raise the limit, or relax the size bound':
        'la malla llegó a {limit} triángulos antes de terminar: sube el límite, o relaja el límite de tamaño',
    # refine.too_fine; new in 0.1.2
    'the refinement made edges too short for the floating-point coordinates near ({x:.6g}, {y:.6g}) and cannot go on':
        'el refinamiento dejó aristas demasiado cortas para las coordenadas en coma flotante cerca de ({x:.6g}, {y:.6g}) y no puede seguir',
    # refine.bad_arc; new in 0.1.2
    'the centre of the arc of segment {k} is not a point of two finite coordinates':
        'el centro del arco del segmento {k} no es un punto de dos coordenadas finitas',
    # refine.arc_radii; new in 0.1.2
    'the ends of segment {k} are at {r1:.9g} and {r2:.9g} from the centre of its arc: they must be at the same distance':
        'los extremos del segmento {k} están a {r1:.9g} y a {r2:.9g} del centro de su arco: tienen que estar a la misma distancia',
    # refine.arc_turn; new in 0.1.2
    'the arc of segment {k} turns {angle:.6g} degrees: at most 60; split it into pieces':
        'el arco del segmento {k} gira {angle:.6g} grados: como mucho 60; divídelo en trozos',
    # refine.vertex_in_arc; new in 0.1.2
    'vertex {i} lies between segment {k} and its arc':
        'el vértice {i} queda entre el segmento {k} y su arco',
    # refine.seed_in_arc; new in 0.1.2
    'the seed of region {region} at ({x:.6g}, {y:.6g}) lies between segment {k} and its arc':
        'la semilla de la región {region} en ({x:.6g}, {y:.6g}) queda entre el segmento {k} y su arco',
    # refine.void_in_arc; new in 0.1.2
    'the void point ({x:.6g}, {y:.6g}) lies between segment {k} and its arc':
        'el punto de hueco ({x:.6g}, {y:.6g}) queda entre el segmento {k} y su arco',
    # refine.segment_in_arc; new in 0.1.2
    'segment {j} enters the arc of segment {k}: between the arc and its chord, or across the arc':
        'el segmento {j} entra en el arco del segmento {k}: entre el arco y su cuerda, o cruzando el arco',
    # refine.internal; new in 0.1.2
    'an internal check of the mesher failed near ({x:.6g}, {y:.6g}); no mesh is returned. Please report it':
        'una comprobación interna del mallador falló cerca de ({x:.6g}, {y:.6g}); no se devuelve ninguna malla. Por favor, avisa del fallo',
    # refine.arc_unproven; new in 0.1.2
    'the input has arcs. Pav and Walkington prove that their algorithm ends, with arc pieces that turn up to {turn:.3g} degrees, for B > {ratio:.4g}. This mesher is not exactly that algorithm (concentric shells, the Terminator), and no source proves that it ends with arcs':
        'la entrada tiene arcos. Pav y Walkington demuestran que su algoritmo termina, con trozos de arco que giran hasta {turn:.3g} grados, para B > {ratio:.4g}. Este mallador no es exactamente ese algoritmo (capas concéntricas, el Terminator), y ninguna fuente demuestra que termine con arcos',
    # refine.length_unit; new in 0.1.2
    'next to a vertex where two segments meet, the mesh splits the segments at distances that are powers of two of the unit of length: the same model in other units gives another mesh':
        'junto a un vértice donde se unen dos segmentos, la malla divide los segmentos a distancias que son potencias de dos de la unidad de longitud: el mismo modelo en otras unidades da otra malla',
    # ==================================================================
    # ogr_core.fem.messages.SEEPAGE_NOTES
    # ==================================================================
    # seepage.empty_mesh
    'empty mesh':
        'malla vacía',
    # seepage.no_dirichlet
    'no Dirichlet (head) boundary condition: the problem is singular. Prescribe Total Head, Pressure Head or Zero Pressure somewhere on the boundary.':
        'no hay ninguna condición de contorno de altura (Dirichlet): el problema es singular. Impón Altura total, Altura de presión o Presión nula en algún tramo del contorno.',
    # seepage.linear_failed
    'linear solve failed':
        'falló la resolución del sistema lineal',
    # seepage.picard_linear_failed
    'linear solve failed at Picard iteration {it}':
        'falló la resolución del sistema lineal en la iteración de Picard {it}',
    # seepage.final_failed
    'final solve failed':
        'falló la resolución final',
    # seepage.face_unsettled
    "the seepage face never settled: {unsettled} boundary node(s) still want to switch between 'P = 0' and 'no flow' ({frozen} were frozen by the switch budget of {budget}). The free surface this reports is not the converged one.":
        'la cara de rezume no se estabilizó: {unsettled} nodo(s) del contorno siguen queriendo cambiar entre «P = 0» y «sin flujo» ({frozen} quedaron congelados por el límite de {budget} cambios). La superficie libre que se da no es la convergida.',
    # seepage.picard_no_rescue
    'Picard iteration did not converge in {steps} steps (last change {change:.3e} m), and the rescue is switched off.':
        'La iteración de Picard no convergió en {steps} pasos (último cambio {change:.3e} m), y el rescate está desactivado.',
    # seepage.picard_rescue_failed
    "Picard iteration did not converge in {steps} steps (last change {change:.3e} m), and neither did the rescue (Anderson acceleration, then continuation with Newton's method; last change {rescue_change:.3e} m). A permeability function that drops many decades over a short suction range is the usual cause: check the curves of the materials near the water table.":
        'La iteración de Picard no convergió en {steps} pasos (último cambio {change:.3e} m), y el rescate tampoco (aceleración de Anderson y después continuación con el método de Newton; último cambio {rescue_change:.3e} m). La causa habitual es una función de permeabilidad que cae muchos órdenes de magnitud en un intervalo corto de succión: revisa las curvas de los materiales cerca del nivel freático.',
    # seepage.picard_rescue_piecewise_na
    "Picard iteration did not converge in {steps} steps (last change {change:.3e} m), and neither did the rescue (Anderson acceleration, then continuation with Newton's method; last change {rescue_change:.3e} m). The continuation stopped where its path of solutions turns back; the road that follows the path across such turns works only when every material has a User Defined permeability curve, and this model has others.":
        'La iteración de Picard no convergió en {steps} pasos (último cambio {change:.3e} m), y el rescate tampoco (aceleración de Anderson y después continuación con el método de Newton; último cambio {rescue_change:.3e} m). La continuación se detuvo donde su camino de soluciones da la vuelta; el camino que sigue esas vueltas solo funciona cuando todos los materiales tienen una curva de permeabilidad definida por el usuario, y este modelo tiene otras.',
    # seepage.initial_failed
    'initial steady state failed':
        'falló el estado permanente inicial',
    # seepage.initial_failed_why
    'initial steady state failed: {why}':
        'falló el estado permanente inicial: {why}',
    # seepage.no_time_step
    'no time step computed':
        'no se calculó ningún paso de tiempo',
    # seepage.stage_steps
    'stage {k}: some time steps did not converge; try more time steps or more Picard iterations per step':
        'etapa {k}: algunos pasos de tiempo no convergieron; prueba con más pasos de tiempo o más iteraciones de Picard por paso',
    # seepage.initial_not_converged
    'the initial steady state did not converge':
        'el estado permanente inicial no convergió',
    # seepage.initial_not_converged_why
    'the initial steady state did not converge: {why}':
        'el estado permanente inicial no convergió: {why}',
    # seepage.mesh_flat
    'the mesh has {n} flat element(s) (three collinear nodes): nodes under them do not count as boundary and the conductivity matrix is badly conditioned. Regenerate the mesh.':
        'la malla tiene {n} elemento(s) plano(s) (tres nodos alineados): los nodos bajo ellos no cuentan como contorno y la matriz de conductividad está mal condicionada. Regenera la malla.',
    # ==================================================================
    # ogr_core.file_messages.FILE_MESSAGES
    # ==================================================================
    # file.support_type_unknown
    'Unknown support type: {type_id}':
        'Tipo de soporte desconocido: «{type_id}»',
    # file.strength_model_unknown
    "Unknown strength model: '{model_id}'. Available: {available}":
        'Modelo de resistencia desconocido: «{model_id}». Los que hay: {available}',
    # file.parameter_unknown
    "{model_id}: unknown parameter '{key}'. Valid: {valid}":
        '{model_id}: parámetro desconocido «{key}». Los que admite: {valid}',
    # file.boundary_type_unknown
    "Unknown boundary type: '{value}'":
        'Tipo de contorno desconocido: «{value}»',
    # file.enum_unknown
    "'{value}' is not a valid value for {enum}":
        '«{value}» no es un valor válido para {enum}',
    # file.not_a_project
    'The file does not hold a project: it is {found}, not an object.':
        'El archivo no contiene un proyecto: es {found}, no un objeto.',
    # file.no_project_key
    'The file does not hold a project: it has none of the keys of one.':
        'El archivo no contiene un proyecto: no tiene ninguna de las claves de un proyecto.',
    # file.section_shape
    "The section '{section}' of the file must be {expected}, not {found}.":
        'La sección «{section}» del archivo tiene que ser {expected}, no {found}.',
    # file.item_shape
    "Item {n} of the section '{section}' of the file must be an object, not {found}.":
        'El elemento {n} de la sección «{section}» del archivo tiene que ser un objeto, no {found}.',
    # file.value_unknown
    "Unknown value of '{field}': '{value}'. Known: {known}":
        'Valor desconocido de «{field}»: «{value}». Los que conoce: {known}',
    # file.field_type
    "The field '{field}' of item {n} of the section '{section}' of the file must be {expected}, not {found}.":
        'El campo «{field}» del elemento {n} de la sección «{section}» del archivo tiene que ser {expected}, no {found}.',
    # ==================================================================
    # ogr_core.geometry.messages.GEOMETRY_MESSAGES
    # ==================================================================
    # geometry.vertex_ref
    'A vertex is an index or an [x, y] point.':
        'Un vértice es un índice o un punto [x, y].',
    # geometry.vertex_out_of_range
    'Vertex index {ref} is outside 0..{last}.':
        'El índice de vértice {ref} está fuera de 0..{last}.',
    # geometry.not_a_vertex
    '({x:g}, {y:g}) is not a vertex of the External boundary.':
        '({x:g}, {y:g}) no es un vértice del contorno exterior.',
    # geometry.toe_is_crest
    'The toe and the crest are the same vertex.':
        'El pie y la coronación son el mismo vértice.',
    # geometry.toe_not_lower
    'The toe must be lower than the crest.':
        'El pie tiene que estar más bajo que la coronación.',
    # geometry.face_not_on_ground
    'The toe and the crest are not joined by the ground surface.':
        'El pie y la coronación no están unidos por la superficie del terreno.',
    # geometry.slope_mode_unknown
    'mode is one of {modes}.':
        'mode es uno de {modes}.',
    # geometry.angle_out_of_range
    'The new overall angle must be between 0° and 90°.':
        'El ángulo global nuevo debe estar entre 0° y 90°.',
    # geometry.at_toe_elevation
    "A face vertex at the toe's elevation cannot be projected horizontally.":
        'Un vértice de la cara a la cota del pie no se puede proyectar en horizontal.',
    # geometry.vertical_face
    'A vertical face cannot be projected vertically.':
        'Una cara vertical no se puede proyectar en vertical.',
    # geometry.above_toe
    'A face vertex above the toe cannot be projected vertically.':
        'Un vértice de la cara justo encima del pie no se puede proyectar en vertical.',
    # geometry.no_external
    'The model has no External boundary.':
        'El modelo no tiene contorno exterior.',
    # geometry.keep_benches_rotate
    "keep_benches is only read by the horizontal and vertical projections, not by 'rotate'.":
        "keep_benches solo lo leen las proyecciones horizontal y vertical, no 'rotate'.",
    # geometry.change_or_target
    'Give exactly one of change_deg or target_deg.':
        'Indica solo uno de change_deg y target_deg.',
    # geometry.face_runs_into
    'At that angle the face runs into the rest of the External boundary (past the next vertex of the crest or the toe).':
        'Con ese ángulo la cara choca con el resto del contorno exterior (pasa del vértice siguiente a la coronación o al pie).',
    # geometry.supports_not_moved
    '{n} support(s) had their head on the old face and were not moved: {names}.':
        'Soportes con la cabeza en la cara anterior que no se han movido ({n}): {names}.',
    # geometry.loads_not_moved
    '{n} load(s) were on the old face and were not moved: {names}.':
        'Cargas sobre la cara anterior que no se han movido ({n}): {names}.',
    # geometry.tolerance_not_positive
    'the simplification tolerance must be positive':
        'la tolerancia de simplificación tiene que ser positiva',
    # geometry.tolerance_too_coarse
    'a tolerance of {epsilon:g} leaves {n} vertices; this boundary needs at least {need}':
        'una tolerancia de {epsilon:g} deja {n} vértices; este contorno necesita al menos {need}',
    # geometry.external_not_closed
    'External must be a closed polyline.':
        'El contorno exterior tiene que ser una polilínea cerrada.',
    # geometry.external_too_few
    'External has too few vertices.':
        'El contorno exterior tiene muy pocos vértices.',
    # geometry.polyline_too_few
    'Polyline needs at least 2 vertices.':
        'La polilínea necesita al menos 2 vértices.',
    # geometry.endpoints_off_external
    'Both endpoints of the polyline must lie on the External Boundary (use snap — green cross).':
        'Los dos extremos de la polilínea tienen que estar sobre el contorno exterior (usa el forzado: cruz verde).',
    # geometry.expand_smaller
    'Expand produced a smaller polygon — intermediate points are probably INSIDE the External. Use Shrink, or redraw with points outside.':
        'Expandir ha dado un polígono más pequeño: los puntos intermedios están probablemente DENTRO del contorno exterior. Usa Contraer, o vuelve a dibujar con los puntos fuera.',
    # geometry.offset_needs_polygon
    'offset_polygon requires a closed polygon with ≥3 vertices':
        'offset_polygon necesita un polígono cerrado con ≥3 vértices',
    # ==================================================================
    # ogr_core.loads.messages.SEISMIC_NOTES
    # ==================================================================
    # seismic.no_numeric_data
    'no numeric data':
        'no hay datos numéricos',
    # seismic.too_few_samples
    'fewer than two samples':
        'menos de dos muestras',
    # seismic.time_not_increasing
    'non-increasing time column':
        'la columna de tiempo no es creciente',
    # seismic.step_not_constant
    'time step is not constant':
        'el paso de tiempo no es constante',
    # seismic.needs_interval
    'single-column file needs a time interval':
        'un archivo de una sola columna necesita un intervalo de tiempo',
    # ==================================================================
    # ogr_core.materials.messages.CALCULATOR_NOTES
    # ==================================================================
    # calc.d_clamped
    'D = 2 makes mb undefined (28 − 14 D = 0); it has been clamped to 1.999.':
        'Con D = 2, mb queda indefinido (28 − 14 D = 0); se ha limitado a 1.999.',
    # calc.gsi_clamped
    'GSI was clamped to the range 0 to 100.':
        'El GSI se ha limitado al intervalo de 0 a 100.',
    # ==================================================================
    # ogr_core.materials.messages.FACTORING_NOTES
    # ==================================================================
    # factoring.legacy_points
    'a table saved as points before 0.1.218 is refused by the analysis, so it was not factored':
        'una tabla guardada como puntos antes de la 0.1.218 la rechaza el análisis, así que no se le han aplicado los coeficientes',
    # factoring.legacy_snowden
    'a material saved before 0.1.229 is refused by the analysis, so it was not factored':
        'un material guardado antes de la 0.1.229 lo rechaza el análisis, así que no se le han aplicado los coeficientes',
    # factoring.no_factor
    '{model}: this strength model declares no partial factor, so it was NOT factored.':
        '{model}: este modelo de resistencia no declara ningún coeficiente parcial, así que NO se le han aplicado.',
    # factoring.child_unbuilt
    '{label}: its model cannot be built, so it was not factored':
        '{label}: su modelo no se puede construir, así que no se le han aplicado los coeficientes',
    # factoring.snowden_unbuilt.bedding
    'its bedding function cannot be built, so it was not factored':
        'su función de la estratificación no se puede construir, así que no se le han aplicado los coeficientes',
    # factoring.snowden_unbuilt.rock_mass
    'its rock mass function cannot be built, so it was not factored':
        'su función del macizo rocoso no se puede construir, así que no se le han aplicado los coeficientes',
    # factoring.snowden_note.bedding
    'bedding: {note}':
        'estratificación: {note}',
    # factoring.snowden_note.rock_mass
    'rock mass: {note}':
        'macizo rocoso: {note}',
    # ==================================================================
    # ogr_core.project.design_messages.DESIGN_NOTES
    # ==================================================================
    # design.none
    'no partial factors applied':
        'sin coeficientes parciales aplicados',
    # design.summary
    '{standard}: {materials} material(s) and {loads} load(s) factored':
        '{standard}: {materials} material(es) y {loads} carga(s) afectados por los coeficientes',
    # design.material
    'Material {name!r}: {note}.':
        'En el material {name!r}: {note}.',
    # design.seismic_not_applied
    'Seismic: the factor {factor:g} is not applied — the run seeks the critical seismic coefficient, so there is no coefficient to factor.':
        'Sismo: no se aplica el coeficiente {factor:g}, porque el análisis busca el coeficiente sísmico crítico y no hay coeficiente que afectar.',
    # design.seismic
    'Seismic: kh and kv multiplied by {factor:g}.':
        'Sismo: kh y kv multiplicados por {factor:g}.',
    # design.weight_single
    'Soil weight: the permanent-action factor {factor:g} multiplies the weight of every slice (single source assumption).':
        'Peso del terreno: el coeficiente de las acciones permanentes {factor:g} multiplica el peso de cada dovela (hipótesis de fuente única).',
    # design.weight
    'Soil weight: the permanent-action factor {unfavourable:g} multiplies the weight of the slices whose base drives the sliding, and {favourable:g} that of the others.':
        'Peso del terreno: el coeficiente de las acciones permanentes {unfavourable:g} multiplica el peso de las dovelas cuya base empuja el deslizamiento, y {favourable:g} el de las demás.',
    # design.loads_by_action
    'Loads: each one is factored as a whole, by its action and by whether it drives the sliding of the surface: a permanent load by {pu:g} or {pf:g}, a variable one by {vu:g} or {vf:g}.':
        'Cargas: cada una se afecta entera, según su acción y según empuje o no el deslizamiento de la superficie: una carga permanente por {pu:g} o {pf:g}, una variable por {vu:g} o {vf:g}.',
    # design.loads_variable
    'Every load takes the variable-action factor ({factor:g}): a load carries no action type in this version.':
        'Todas las cargas toman el coeficiente de las acciones variables ({factor:g}): en esta versión una carga no lleva tipo de acción.',
    # design.identity
    'The standard is enabled but every factor is 1.0, so nothing changed.':
        'La norma está activada pero todos los coeficientes valen 1.0, así que no ha cambiado nada.',
    # ==================================================================
    # ogr_core.project.messages.IMPORT_NOTES
    # ==================================================================
    # import.water_dropped; RF-9: the fields of the template
    '{name!r} used a water surface of the other project; assign one of this model to it.':
        '{name!r} usaba una superficie de agua del otro proyecto; asígnale una de este modelo.',
    # import.anisotropic_dropped; RF-9: the fields of the template
    '{name!r} lost its anisotropic surface, which belonged to the other project.':
        '{name!r} ha perdido su superficie anisótropa, que era del otro proyecto.',
    # import.link_renamed; RF-9: the fields of the template
    '{name!r}: {who} now takes the strength of {here!r}, the material of that name in this model.':
        '{name!r}: {who} toma ahora la resistencia de {here!r}, el material de ese nombre en este modelo.',
    # import.link_dropped; RF-9: the fields of the template
    '{name!r}: {who} linked a material this model cannot link; it keeps the strength it had, unlinked.':
        '{name!r}: {who} enlazaba un material que este modelo no puede enlazar; conserva la resistencia que tenía, sin enlace.',
    # import.max_materials
    '{n} material(s) not imported: the model already has the maximum of {limit}.':
        'Materiales no importados ({n}): el modelo ya tiene el máximo de {limit}.',
    # import.range
    'range {n}':
        'el rango {n}',
    # ==================================================================
    # ogr_core.project.messages.REFUSALS
    # ==================================================================
    # rule.optimize_technique_unknown
    'Unknown optimisation technique {value!r}: it has to be one of {allowed}.':
        'Técnica de optimización desconocida {value!r}: tiene que ser una de {allowed}.',
    # rule.slope_limit_windows_overlap
    'The two sets of Slope Limits overlap ([{a0:g}, {a1:g}] and [{b0:g}, {b1:g}]). With two sets, a Grid Search generates the circles that run from one window to the other, a rule measured on separate windows only: on the stretch two windows share it gives every crossing to the window that starts further left, which nothing measured supports, and with a window inside one that starts further left it generates no circle at all. Make the two windows separate, or use a single set.':
        'Los dos juegos de límites del talud se solapan ([{a0:g}, {a1:g}] y [{b0:g}, {b1:g}]). Con dos juegos, una búsqueda por rejilla genera los círculos que van de una ventana a la otra, una regla medida solo con ventanas separadas: en el tramo que comparten dos ventanas da cada corte a la ventana que empieza más a la izquierda, algo que nada medido respalda, y con una ventana dentro de otra que empieza más a la izquierda no genera ningún círculo. Separa las dos ventanas o usa un solo juego.',
    # rule.block_polyline_overlap
    '{other} overlaps the lateral extent of the Block Search Polyline {polyline} (x from {lo:g} to {hi:g}){where}. This is not allowed: the trial surface follows the polyline between its two points, and a vertex of another object inside that range would cut the stretch.{way_out}':
        '{other} se solapa con la extensión lateral de la polilínea de búsqueda por bloques {polyline} (x de {lo:g} a {hi:g}){where}. No se permite: la superficie de tanteo sigue la polilínea entre sus dos puntos, y un vértice de otro objeto dentro de ese tramo cortaría el recorrido.{way_out}',
    # rule.block_overlap_group
    ' (both in Group ID {group})':
        ' (los dos en el identificador de grupo {group})',
    # rule.block_overlap_way_grouped
    ' Give them different Group IDs to search them separately.':
        ' Dales identificadores de grupo distintos para buscarlos por separado.',
    # rule.block_overlap_way_ungrouped
    ' To search them separately, turn Multiple Groups on and give them different Group IDs.':
        ' Para buscarlos por separado, activa Grupos múltiples y dales identificadores de grupo distintos.',
    # rule.seismic_not_a_number
    '{name} must be a number, got {value!r}.':
        '{name} tiene que ser un número; vale {value!r}.',
    # rule.seismic_out_of_range
    '|{name}| must be below 1 (a fraction of g), got {value}.':
        '|{name}| tiene que ser menor que 1 (una fracción de g); vale {value}.',
    # rule.seismic_kh_negative
    'kh must not be negative, got {value}. It is the magnitude of the horizontal seismic force, which always acts in the sliding direction of each surface, out of the slope; its sign does not choose a direction.':
        'kh no puede ser negativo; vale {value}. Es la magnitud de la fuerza sísmica horizontal, que siempre actúa en el sentido de deslizamiento de cada superficie, hacia fuera del talud; su signo no elige un sentido.',
    # rule.design_permanent_below_one
    'The partial factor on unfavourable permanent actions must be at least 1, got {value}: below 1 it would make the driving weight lighter than the characteristic one.':
        'El coeficiente parcial de las acciones permanentes desfavorables tiene que ser al menos 1; vale {value}: por debajo de 1 haría el peso que moviliza más ligero que el característico.',
    # rule.design_permanent_favourable_above_one
    'The partial factor on favourable permanent actions must be at most 1, got {value}: above 1 it would make the resisting weight heavier than the characteristic one.':
        'El coeficiente parcial de las acciones permanentes favorables tiene que ser como mucho 1; vale {value}: por encima de 1 haría el peso que resiste más pesado que el característico.',
    # rule.design_permanent_favourable_not_positive
    'The partial factor on favourable permanent actions must be above 0, got {value}: a permanent action keeps its sign, and at 0 the slices that resist would have no weight.':
        'El coeficiente parcial de las acciones permanentes favorables tiene que ser mayor que 0; vale {value}: una acción permanente conserva su signo, y con 0 las dovelas que resisten no tendrían peso.',
    # rule.design_variable_below_one
    'The partial factor on unfavourable variable actions must be at least 1, got {value}: below 1 it would make a load that drives the sliding lighter than its characteristic value.':
        'El coeficiente parcial de las acciones variables desfavorables tiene que ser al menos 1; vale {value}: por debajo de 1 haría una carga que moviliza el deslizamiento más ligera que su valor característico.',
    # rule.design_variable_favourable_above_one
    'The partial factor on favourable variable actions must be at most 1, got {value}: above 1 it would make a load that resists the sliding heavier than its characteristic value.':
        'El coeficiente parcial de las acciones variables favorables tiene que ser como mucho 1; vale {value}: por encima de 1 haría una carga que se opone al deslizamiento más pesada que su valor característico.',
    # rule.design_variable_favourable_negative
    'The partial factor on favourable variable actions must not be negative, got {value}: at 0 the load is left out, which is the most a favourable variable action can be discounted.':
        'El coeficiente parcial de las acciones variables favorables no puede ser negativo; vale {value}: con 0 la carga queda fuera, que es lo más que se puede descontar una acción variable favorable.',
    # rule.line_load_needs_ground
    'Line load {name}: an orientation relative to the boundary needs the ground surface.':
        'Carga lineal «{name}»: una orientación relativa al contorno necesita la superficie del terreno.',
    # rule.line_load_off_ground
    'Line load {name} at ({x:g}, {y:g}) is not on the ground surface, so it has no boundary to be normal to.':
        'La carga lineal «{name}» en ({x:g}, {y:g}) no está sobre la superficie del terreno, así que no tiene contorno al que ser normal.',
    # rule.design_not_a_number.factor_permanent
    'The partial factor on permanent actions, unfavourable must be a finite number, got {raw!r}.':
        'El coeficiente parcial de las acciones permanentes desfavorables tiene que ser un número finito; vale {raw!r}.',
    # rule.design_not_a_number.factor_permanent_favourable
    'The partial factor on permanent actions, favourable must be a finite number, got {raw!r}.':
        'El coeficiente parcial de las acciones permanentes favorables tiene que ser un número finito; vale {raw!r}.',
    # rule.design_not_a_number.factor_variable
    'The partial factor on variable actions, unfavourable must be a finite number, got {raw!r}.':
        'El coeficiente parcial de las acciones variables desfavorables tiene que ser un número finito; vale {raw!r}.',
    # rule.design_not_a_number.factor_variable_favourable
    'The partial factor on variable actions, favourable must be a finite number, got {raw!r}.':
        'El coeficiente parcial de las acciones variables favorables tiene que ser un número finito; vale {raw!r}.',
    # ==================================================================
    # ogr_core.project.messages.RULES
    # ==================================================================
    # rule.no_boundaries
    'No model to compute. Add an external boundary first.':
        'No hay modelo que calcular. Añade primero un contorno exterior.',
    # rule.no_materials
    'No materials defined.':
        'No hay materiales definidos.',
    # rule.block_object_empty
    'A Block Search object needs at least one vertex.':
        'Un objeto de búsqueda por bloques necesita al menos un vértice.',
    # rule.block_point_vertices
    'A Block Search Point is a single point; this one has {n} vertices.':
        'Un punto de búsqueda por bloques es un único punto; este tiene {n} vértices.',
    # rule.block_line_vertices
    'A Block Search Line is one segment given by two points; this one has {n} vertices. A path of several segments that the surface should follow is a Block Search Polyline.':
        'Una línea de búsqueda por bloques es un segmento dado por dos puntos; esta tiene {n} vértices. Un camino de varios segmentos que la superficie deba seguir es una polilínea de búsqueda por bloques.',
    # rule.block_window_open
    'A Block Search Window is a closed polygon of at least three vertices.':
        'Una ventana de búsqueda por bloques es un polígono cerrado de al menos tres vértices.',
    # rule.block_polyline_shape
    'A Block Search Polyline is an open line of at least two vertices.':
        'Una polilínea de búsqueda por bloques es una línea abierta de al menos dos vértices.',
    # rule.block_polyline_not_monotone
    'A Block Search Polyline has to advance in x from one end to the other: the trial surface follows it between its two points, and a polyline that doubles back (or has a vertical segment) would give a surface that reverses direction.':
        'Una polilínea de búsqueda por bloques tiene que avanzar en x de un extremo al otro: la superficie de tanteo la sigue entre sus dos puntos, y una polilínea que vuelve sobre sí misma (o que tiene un tramo vertical) daría una superficie que cambia de sentido.',
    # rule.block_polyline_segment_mode
    'The Left / Right Line Segment option places its point on the end segment of that side, which needs a polyline of at least two segments; this one has one. Use Any Line Segment or End Point.':
        'La opción Segmento izquierdo / derecho pone su punto en el segmento extremo de ese lado, y eso necesita una polilínea de al menos dos segmentos; esta tiene uno. Usa Cualquier segmento o Extremo.',
    # rule.block_angle_reread_left
    'The left projection angles are written from {start:g}° to {end:g}°, and the reference measures them counter-clockwise from the positive x axis with the Start Angle less than the End Angle. They were read as {lo:g}° to {hi:g}°: the arc between the two that avoids 0°, a direction no left projection can take.':
        'Los ángulos de proyección izquierdos están escritos de {start:g}° a {end:g}°, y la referencia los mide en sentido antihorario desde el eje x positivo, con el ángulo inicial menor que el final. Se leyeron como {lo:g}° a {hi:g}°: el arco entre los dos que evita 0°, una dirección que ninguna proyección izquierda puede tomar.',
    # rule.block_angle_reread_right
    'The right projection angles are written from {start:g}° to {end:g}°, and the reference measures them counter-clockwise from the positive x axis with the Start Angle less than the End Angle. They were read as {lo:g}° to {hi:g}°: the arc between the two that avoids 180°, a direction no right projection can take.':
        'Los ángulos de proyección derechos están escritos de {start:g}° a {end:g}°, y la referencia los mide en sentido antihorario desde el eje x positivo, con el ángulo inicial menor que el final. Se leyeron como {lo:g}° a {hi:g}°: el arco entre los dos que evita 180°, una dirección que ninguna proyección derecha puede tomar.',
    # rule.block_angle_out_left_left_facing
    'The left projection angles, {lo:g}° to {hi:g}°, go outside {limit_lo:g}° to {limit_hi:g}°, the range the reference gives for kinematically valid surfaces on a left-facing slope. The search uses them as given; a projection that cannot reach the ground leaves its surface invalid.':
        'Los ángulos de proyección izquierdos, de {lo:g}° a {hi:g}°, se salen de {limit_lo:g}° a {limit_hi:g}°, el intervalo que da la referencia para superficies cinemáticamente válidas en un talud orientado a la izquierda. La búsqueda los usa tal cual; una proyección que no llega al terreno deja inválida su superficie.',
    # rule.block_angle_out_left_right_facing
    'The left projection angles, {lo:g}° to {hi:g}°, go outside {limit_lo:g}° to {limit_hi:g}°, the range the reference gives for kinematically valid surfaces on a right-facing slope. The search uses them as given; a projection that cannot reach the ground leaves its surface invalid.':
        'Los ángulos de proyección izquierdos, de {lo:g}° a {hi:g}°, se salen de {limit_lo:g}° a {limit_hi:g}°, el intervalo que da la referencia para superficies cinemáticamente válidas en un talud orientado a la derecha. La búsqueda los usa tal cual; una proyección que no llega al terreno deja inválida su superficie.',
    # rule.block_angle_out_right_left_facing
    'The right projection angles, {lo:g}° to {hi:g}°, go outside {limit_lo:g}° to {limit_hi:g}°, the range the reference gives for kinematically valid surfaces on a left-facing slope. The search uses them as given; a projection that cannot reach the ground leaves its surface invalid.':
        'Los ángulos de proyección derechos, de {lo:g}° a {hi:g}°, se salen de {limit_lo:g}° a {limit_hi:g}°, el intervalo que da la referencia para superficies cinemáticamente válidas en un talud orientado a la izquierda. La búsqueda los usa tal cual; una proyección que no llega al terreno deja inválida su superficie.',
    # rule.block_angle_out_right_right_facing
    'The right projection angles, {lo:g}° to {hi:g}°, go outside {limit_lo:g}° to {limit_hi:g}°, the range the reference gives for kinematically valid surfaces on a right-facing slope. The search uses them as given; a projection that cannot reach the ground leaves its surface invalid.':
        'Los ángulos de proyección derechos, de {lo:g}° a {hi:g}°, se salen de {limit_lo:g}° a {limit_hi:g}°, el intervalo que da la referencia para superficies cinemáticamente válidas en un talud orientado a la derecha. La búsqueda los usa tal cual; una proyección que no llega al terreno deja inválida su superficie.',
    # rule.orphan_region
    'The region at ({x:.2f}, {y:.2f}) is assigned a material that no longer exists. Assign it another material (Properties > Assign Materials); a surface through it cannot be analysed.':
        'La región en ({x:.2f}, {y:.2f}) tiene asignado un material que ya no existe. Asígnale otro material (Propiedades > Asignar materiales); una superficie que pase por ella no se puede analizar.',
    # rule.migration_cooling
    'This model carries {shadow} = {old}, removed in v0.1.103: it held a geometric cooling rate that no analysis ever read; the coefficient the schedule does use is {survivor}. The stored value was NOT converted.':
        'Este modelo lleva {shadow} = {old}, retirado en v0.1.103: guardaba un ritmo de enfriamiento geométrico que ningún análisis llegó a leer; el coeficiente que sí usa el programa de enfriamiento es {survivor}. El valor guardado NO se convirtió.',
    # rule.migration_frame
    "This model carries {shadow} = {old}, removed in v0.1.103: it held an angle in the search's own toe-to-crest frame and the field replacing it is absolute, so converting it needs the failure direction, which is not part of this block. The field to set is {survivor}. The stored value was NOT converted.":
        'Este modelo lleva {shadow} = {old}, retirado en v0.1.103: guardaba un ángulo en el sistema propio de la búsqueda, del pie a la coronación, y el campo que lo sustituye es absoluto, así que convertirlo necesita la dirección de rotura, que no forma parte de este bloque. El campo que hay que poner es {survivor}. El valor guardado NO se convirtió.',
    # rule.migration_toe_angle_lower
    "This model was saved before v0.1.103, and its Path Search lower Initial Angle at Toe is ON at {angle}°. That number was read in the search's own toe-to-crest frame then and is read as ABSOLUTE now — counter-clockwise from the +x axis — so it does not describe the same limit. It was NOT converted: doing so needs the failure direction, which is not part of this block. Check path_initial_angle_at_toe_lower_deg before trusting this run.":
        'Este modelo se guardó antes de v0.1.103, y su ángulo inicial en el pie inferior de la búsqueda por caminos está ACTIVADO a {angle}°. Ese número se leía entonces en el sistema propio de la búsqueda, del pie a la coronación, y ahora se lee como ABSOLUTO — en sentido antihorario desde el eje +x —, así que no describe el mismo límite. NO se convirtió: hacerlo necesita la dirección de rotura, que no forma parte de este bloque. Revisa path_initial_angle_at_toe_lower_deg antes de fiarte de este cálculo.',
    # rule.migration_toe_angle_upper
    "This model was saved before v0.1.103, and its Path Search upper Initial Angle at Toe is ON at {angle}°. That number was read in the search's own toe-to-crest frame then and is read as ABSOLUTE now — counter-clockwise from the +x axis — so it does not describe the same limit. It was NOT converted: doing so needs the failure direction, which is not part of this block. Check path_initial_angle_at_toe_upper_deg before trusting this run.":
        'Este modelo se guardó antes de v0.1.103, y su ángulo inicial en el pie superior de la búsqueda por caminos está ACTIVADO a {angle}°. Ese número se leía entonces en el sistema propio de la búsqueda, del pie a la coronación, y ahora se lee como ABSOLUTO — en sentido antihorario desde el eje +x —, así que no describe el mismo límite. NO se convirtió: hacerlo necesita la dirección de rotura, que no forma parte de este bloque. Revisa path_initial_angle_at_toe_upper_deg antes de fiarte de este cálculo.',
    # rule.migration_path_optimize
    'This model carries path_optimize = True, removed in v0.1.104. Path Search used to optimise its best surfaces whether or not anything asked it to, because that field defaulted to True and the interface never showed it. The optimisation is now the Optimize Surfaces checkbox, which is UNTICKED here, so this run does not optimise. Tick it to get the old behaviour.':
        'Este modelo lleva path_optimize = True, retirado en v0.1.104. La búsqueda por caminos optimizaba sus mejores superficies tanto si se le pedía como si no, porque ese campo valía True por defecto y la interfaz nunca lo enseñaba. La optimización es ahora la casilla Optimizar superficies, que aquí está DESMARCADA, así que este cálculo no optimiza. Márcala para volver al comportamiento de antes.',
    # ==================================================================
    # ogr_core.project.messages.STRENGTH_REFUSALS
    # ==================================================================
    # strength.material
    'Material {name!r}, {model}: {why}':
        'En el material {name!r}, {model}: {why}',
    # strength.point_not_finite
    'Point {i} holds a value that is not finite.':
        'El punto {i} tiene un valor que no es finito.',
    # strength.row_not_finite
    'Row {i} holds a value that is not finite.':
        'La fila {i} tiene un valor que no es finito.',
    # strength.row_strength
    'Row {i}: the cohesion must be ≥ 0 and the friction angle in [0, 90), got c = {c:g}, phi = {phi:g}.':
        'Fila {i}: la cohesión tiene que ser ≥ 0 y el ángulo de rozamiento estar en [0, 90); vale c = {c:g}, phi = {phi:g}.',
    # strength.last_range_end
    'The last range must end at +90 degrees; it ends at {end:g}.':
        'El último rango tiene que acabar en +90°; acaba en {end:g}.',
    # strength.points.not_list
    'The table must be a list of (normal stress, shear strength) points.':
        'La tabla tiene que ser una lista de puntos (tensión normal, resistencia al corte).',
    # strength.points.empty
    'The table has no points: at least one (normal stress, shear strength) point is needed.':
        'La tabla no tiene puntos: hace falta al menos un punto (tensión normal, resistencia al corte).',
    # strength.points.not_two
    'Point {i} is not two numbers (normal stress, shear strength): {point}.':
        'El punto {i} no son dos números (tensión normal, resistencia al corte): {point}.',
    # strength.points.negative
    'Point {i}: the shear strength must be zero or more, got {tau:g}.':
        'Punto {i}: la resistencia al corte tiene que ser cero o más; vale {tau:g}.',
    # strength.points.order
    'The normal stresses must increase strictly: point {next} ({s_next:g}) does not exceed point {i} ({s_i:g}).':
        'Las tensiones normales tienen que crecer estrictamente: el punto {next} ({s_next:g}) no supera al punto {i} ({s_i:g}).',
    # strength.discrete.type
    'The function type must be one of {choices}, got {value}.':
        'El tipo de función tiene que ser uno de {choices}; vale {value}.',
    # strength.discrete.method
    'The interpolation method must be one of {choices}, got {value}.':
        'El método de interpolación tiene que ser uno de {choices}; vale {value}.',
    # strength.discrete.not_list
    'The table must be a list of {what} points.':
        'La tabla tiene que ser una lista de puntos {what}.',
    # strength.discrete.empty
    'The table has no points: at least one {what} point is needed.':
        'La tabla no tiene puntos: hace falta al menos un punto {what}.',
    # strength.discrete.not_point
    'Point {i} is not {what}: {point}.':
        'El punto {i} no es {what}: {point}.',
    # strength.discrete.cohesion
    'Point {i}: the cohesion must be zero or more, got {c:g}.':
        'Punto {i}: la cohesión tiene que ser cero o más; vale {c:g}.',
    # strength.discrete.angle
    'Point {i}: the friction angle must be in [0, 90), got {phi:g}.':
        'Punto {i}: el ángulo de rozamiento tiene que estar en [0, 90); vale {phi:g}.',
    # strength.discrete.repeated
    'Point {i} repeats the place ({x:g}, {y:g}): two strengths for one point.':
        'El punto {i} repite el lugar ({x:g}, {y:g}): dos resistencias para un mismo punto.',
    # strength.cphi.not_list
    'The table must be a list of (normal stress, cohesion, friction angle) rows.':
        'La tabla tiene que ser una lista de filas (tensión normal, cohesión, ángulo de rozamiento).',
    # strength.cphi.empty
    'The table has no rows: at least one (normal stress, cohesion, friction angle) row is needed.':
        'La tabla no tiene filas: hace falta al menos una fila (tensión normal, cohesión, ángulo de rozamiento).',
    # strength.cphi.not_three
    'Row {i} is not three numbers (normal stress, cohesion, friction angle): {row}.':
        'La fila {i} no son tres números (tensión normal, cohesión, ángulo de rozamiento): {row}.',
    # strength.cphi.order
    'The normal stresses must increase strictly: row {next} ({s_next:g}) does not exceed row {i} ({s_i:g}).':
        'Las tensiones normales tienen que crecer estrictamente: la fila {next} ({s_next:g}) no supera a la fila {i} ({s_i:g}).',
    # strength.aniso.not_list
    'The table must be a list of (angle to, c, phi) rows.':
        'La tabla tiene que ser una lista de filas (ángulo hasta, c, phi).',
    # strength.aniso.empty
    'The table has no rows: at least one range, ending at +90 degrees, is needed.':
        'La tabla no tiene filas: hace falta al menos un rango, que acabe en +90°.',
    # strength.aniso.not_three
    'Row {i} is not three numbers (angle to, c, phi): {row}.':
        'La fila {i} no son tres números (ángulo hasta, c, phi): {row}.',
    # strength.aniso.start
    "The first range starts at -90 degrees, so its 'angle to' must be above -90; got {first:g}.":
        'El primer rango empieza en -90°, así que su «ángulo hasta» tiene que ser mayor que -90; vale {first:g}.',
    # strength.aniso.order
    'The ranges must be ordered counter-clockwise: row {next} ends at {end_next:g} degrees, not after row {i} ({end_i:g}).':
        'Los rangos tienen que ir en sentido antihorario: la fila {next} acaba en {end_next:g}°, no después de la fila {i} ({end_i:g}).',
    # strength.aniso.legacy
    'The Anisotropic Strength Function of material {name!r} was saved as interpolated points by a version before 0.1.218. Its table is now a list of angular RANGES (angle to, c, phi), as the reference documents this strength type, so the same rows would mean something else. Open the material, review the table as ranges and accept it.':
        'La función de resistencia anisótropa del material {name!r} se guardó como puntos interpolados con una versión anterior a la 0.1.218. Su tabla es ahora una lista de RANGOS angulares (ángulo hasta, c, phi), como documenta la referencia este tipo de resistencia, así que las mismas filas significarían otra cosa. Abre el material, revisa la tabla como rangos y acéptala.',
    # strength.snowden.ab
    'A{side} and B{side} must satisfy 0 <= A{side} <= B{side} <= 90 degrees; got A{side} = {a:g}, B{side} = {b:g}.':
        'A{side} y B{side} tienen que cumplir 0 <= A{side} <= B{side} <= 90°; valen A{side} = {a:g}, B{side} = {b:g}.',
    # strength.snowden.not_function
    '{model} is not a shear-normal or a C/Phi function.':
        '{model} no es una función tangencial/normal ni una función c/φ.',
    # strength.snowden.legacy
    'The Snowden Modified Anisotropic Linear material {name!r} was saved by a version before 0.1.229, with c1, phi1, c2, phi2 and a single B and a cosine transition of the friction ANGLE. The model is now the one the reference documents: a linear transition of the shear strength between a bedding and a rock mass strength function, with A1, B1, A2 and B2. The material shows the nearest such form (A1 = A2 = 0, B1 = B2 = B, one C/Phi row per function), whose numbers are not the old ones: review it and accept it.':
        'El material anisótropo lineal modificado de Snowden {name!r} se guardó con una versión anterior a la 0.1.229, con c1, phi1, c2, phi2, una sola B y una transición coseno del ÁNGULO de rozamiento. El modelo es ahora el que documenta la referencia: una transición lineal de la resistencia al corte entre una función de resistencia de la estratificación y otra del macizo rocoso, con A1, B1, A2 y B2. El material enseña la forma así más cercana (A1 = A2 = 0, B1 = B2 = B, una fila c/φ por función), cuyos números no son los de antes: revísalo y acéptalo.',
    # strength.aniso_linear.ab
    'A and B must satisfy 0 <= A <= B degrees; got A = {a:g}, B = {b:g}.':
        'A y B tienen que cumplir 0 <= A <= B grados; valen A = {a:g}, B = {b:g}.',
    # strength.hoek_brown.domain
    'The envelope needs sigci > 0, mb > 0, s >= 0 and 0 < a <= 1, all finite; got sigci = {sigci:g}, mb = {mb:g}, s = {s:g}, a = {a:g}.':
        'La envolvente necesita sigci > 0, mb > 0, s >= 0 y 0 < a <= 1, todos finitos; valen sigci = {sigci:g}, mb = {mb:g}, s = {s:g}, a = {a:g}.',
    # strength.hoek_brown_classic.domain
    'The envelope needs sigci > 0, m > 0 and s >= 0, all finite; got sigci = {sigci:g}, m = {m:g}, s = {s:g}.':
        'La envolvente necesita sigci > 0, m > 0 y s >= 0, todos finitos; valen sigci = {sigci:g}, m = {m:g}, s = {s:g}.',
    # strength.gen.not_list
    'The rules must be a list of {{angle_min, angle_max, model}} objects.':
        'Las reglas tienen que ser una lista de objetos {{angle_min, angle_max, model}}.',
    # strength.gen.empty
    'There are no rules: at least one range, from -90 to +90 degrees, with its strength model, is needed.':
        'No hay reglas: hace falta al menos un rango, de -90 a +90°, con su modelo de resistencia.',
    # strength.gen.not_rule
    'Rule {i} is not an {{angle_min, angle_max, model}} object: {rule}.':
        'La regla {i} no es un objeto {{angle_min, angle_max, model}}: {rule}.',
    # strength.gen.angles_nan
    'The angles of rule {i} are not numbers.':
        'Los ángulos de la regla {i} no son números.',
    # strength.gen.angles
    'Rule {i} must go from a lower to a higher angle within [-90, 90] degrees; it goes from {amin:g} to {amax:g}.':
        'La regla {i} tiene que ir de un ángulo menor a otro mayor dentro de [-90, 90]°; va de {amin:g} a {amax:g}.',
    # strength.gen.start
    'The first range starts at -90 degrees; it starts at {first:g}.':
        'El primer rango empieza en -90°; empieza en {first:g}.',
    # strength.gen.gap
    'Rule {next} must start where rule {i} ends ({end:g} degrees); it starts at {start:g}, which leaves the angles between {end:g} and {start:g} degrees with no strength.':
        'La regla {next} tiene que empezar donde acaba la regla {i} ({end:g}°); empieza en {start:g}, lo que deja sin resistencia los ángulos entre {end:g} y {start:g}°.',
    # strength.gen.overlap
    'Rule {next} must start where rule {i} ends ({end:g} degrees); it starts at {start:g}, which overlaps it, so part of a range can never be reached.':
        'La regla {next} tiene que empezar donde acaba la regla {i} ({end:g}°); empieza en {start:g}, lo que la solapa, así que parte de un rango no se puede alcanzar nunca.',
    # strength.gen.no_model
    'Rule {i} has no strength model.':
        'La regla {i} no tiene modelo de resistencia.',
    # strength.gen.model_error
    'The strength model of rule {i} cannot be built: {error}':
        'El modelo de resistencia de la regla {i} no se puede construir: {error}',
    # strength.gen.input_type
    'the input is one of {choices}, not {value}.':
        'la entrada es una de {choices}, no {value}.',
    # strength.gen.parent_water
    'use_parent_water must be true or false, not {value}.':
        'use_parent_water tiene que ser verdadero o falso, no {value}.',
    # strength.gen.surface_legacy
    "The Generalized Anisotropic material {name!r} links an anisotropic surface. Its angle ranges are ABSOLUTE slice base inclinations, measured from the horizontal, as the reference defines this input; until 0.1.225 OGR subtracted the surface's bedding from the base angle first, so the same ranges would now select other rules. Open the material, review the ranges as absolute inclinations and accept it: the link is removed.":
        'El material anisótropo generalizado {name!r} enlaza una superficie anisótropa. Sus rangos de ángulos son inclinaciones ABSOLUTAS de la base de la dovela, medidas desde la horizontal, como define la referencia esta entrada; hasta la 0.1.225, OGR restaba antes la estratificación de la superficie al ángulo de la base, así que los mismos rangos elegirían ahora otras reglas. Abre el material, revisa los rangos como inclinaciones absolutas y acéptalo: el enlace se quita.',
    # strength.aos.definition
    "The anisotropy is defined by 'angle' or 'surface', not {value}.":
        "La anisotropía se define por 'angle' o 'surface', no {value}.",
    # strength.aos.mapping
    'The mapping function is one of {choices}, not {value}.':
        'La función de transición es una de {choices}, no {value}.',
    # strength.aos.selection
    'The joint selection is one of {choices}, not {value}.':
        'La selección de juntas es una de {choices}, no {value}.',
    # strength.aos.base_if_weaker
    'use_base_if_weaker must be true or false, not {value}.':
        'use_base_if_weaker tiene que ser verdadero o falso, no {value}.',
    # strength.aos.base
    'The base needs a strength: a material or a model of its own.':
        'La base necesita una resistencia: un material o un modelo propio.',
    # strength.aos.joints
    'At least one joint is needed, with its angle and its strength.':
        'Hace falta al menos una junta, con su ángulo y su resistencia.',
    # strength.aos.joint_model
    'Joint {j} needs a strength: a material or a model of its own.':
        'La junta {j} necesita una resistencia: un material o un modelo propio.',
    # strength.aos.joint_surface
    'Joint {j} must name its anisotropic surface.':
        'La junta {j} tiene que nombrar su superficie anisótropa.',
    # strength.aos.joint_angle
    'The angle of joint {j} must be a number of degrees.':
        'El ángulo de la junta {j} tiene que ser un número de grados.',
    # strength.aos.ab
    'Joint {j}: A and B must satisfy 0 <= A <= B <= 90 degrees; got A = {a}, B = {b}.':
        'Junta {j}: A y B tienen que cumplir 0 <= A <= B <= 90°; valen A = {a}, B = {b}.',
    # strength.aos.model_error
    'The strength model of {child} cannot be built: {error}':
        'El modelo de resistencia de {child} no se puede construir: {error}',
    # strength.aos.nested
    '{child} holds a Generalized Anisotropic model; it takes a plain strength.':
        '{child} tiene un modelo anisótropo generalizado; necesita una resistencia simple.',
    # strength.child.rules
    'rule {n}':
        'la regla {n}',
    # strength.child.base
    'the base':
        'la base',
    # strength.child.joints
    'joint {n}':
        'la junta {n}',
    # strength.child_cap.rules
    'Rule {n}':
        'La regla {n}',
    # strength.child_cap.base
    'The base':
        'La base',
    # strength.child_cap.joints
    'Joint {n}':
        'La junta {n}',
    # strength.link.missing
    '{who} links a material that is not in the project.':
        '{who} enlaza un material que no está en el proyecto.',
    # strength.link.self
    '{who} links the material itself.':
        '{who} se enlaza a sí mismo.',
    # strength.link.generalized
    '{who} links {other}, another Generalized Anisotropic material; a range takes a plain strength model.':
        '{who} enlaza {other}, otro material anisótropo generalizado; un rango necesita un modelo de resistencia simple.',
    # strength.surface_missing
    'joint {j} names an anisotropic surface that is not in the model.':
        'la junta {j} nombra una superficie anisótropa que no está en el modelo.',
    # strength.surface_in_use
    'The anisotropic surface is read by the joints of {users}; change them first.':
        'La superficie anisótropa la leen las juntas de {users}; cámbialas antes.',
    # strength.snowden.function.bedding
    'The bedding strength function: {why}':
        'La función de resistencia de la estratificación: {why}',
    # strength.snowden.function.rock_mass
    'The rock mass strength function: {why}':
        'La función de resistencia del macizo rocoso: {why}',
    # strength.snowden.function_error.bedding
    'The bedding strength function: {error}.':
        'La función de resistencia de la estratificación: {error}.',
    # strength.snowden.function_error.rock_mass
    'The rock mass strength function: {error}.':
        'La función de resistencia del macizo rocoso: {error}.',
    # strength.snowden.not_a_function.bedding
    'the bedding function must be a Shear/Normal Function or a C/Phi Function, got {data}':
        'la función de la estratificación tiene que ser una función tangencial/normal o una función c/φ; es {data}',
    # strength.snowden.not_a_function.rock_mass
    'the rock mass function must be a Shear/Normal Function or a C/Phi Function, got {data}':
        'la función del macizo rocoso tiene que ser una función tangencial/normal o una función c/φ; es {data}',
    # strength.snowden.cannot_build.bedding
    'the bedding function cannot be built: {error}':
        'la función de la estratificación no se puede construir: {error}',
    # strength.snowden.cannot_build.rock_mass
    'the rock mass function cannot be built: {error}':
        'la función del macizo rocoso no se puede construir: {error}',
    # ==================================================================
    # ogr_core.project.reported.REPORTED_NOTES
    # ==================================================================
    # reported.standard_overdesign
    'Design standard applied: {summary} — the reported value is an over-design factor, not a factor of safety, and must exceed 1.':
        'Norma de diseño aplicada: {summary} — el valor indicado es un factor de sobredimensionamiento, no un factor de seguridad, y debe ser mayor que 1.',
    # reported.standard_ky
    'Design standard applied: {summary} — the reported value is the critical seismic coefficient with the partial factors applied, not an over-design factor.':
        'Norma de diseño aplicada: {summary} — el valor indicado es el coeficiente sísmico crítico con los coeficientes parciales aplicados, no un factor de sobredimensionamiento.',
    # reported.standard_newmark
    'Design standard applied: {summary} — the reported value is the Newmark displacement with the partial factors applied, not an over-design factor.':
        'Norma de diseño aplicada: {summary} — el valor indicado es el desplazamiento de Newmark con los coeficientes parciales aplicados, no un factor de sobredimensionamiento.',
    # reported.standard_ky_factor
    'Design standard applied: {summary} — the critical seismic coefficient is computed with the partial factors applied, and the factor shown for the critical surface is an over-design factor, not a factor of safety, and must exceed 1.':
        'Norma de diseño aplicada: {summary} — el coeficiente sísmico crítico se calcula con los coeficientes parciales aplicados, y el factor que se indica de la superficie crítica es un factor de sobredimensionamiento, no un factor de seguridad, y debe ser mayor que 1.',
    # reported.standard_newmark_factor
    'Design standard applied: {summary} — the critical seismic coefficient and the Newmark displacement are computed with the partial factors applied, and the factor shown for the critical surface is an over-design factor, not a factor of safety, and must exceed 1.':
        'Norma de diseño aplicada: {summary} — el coeficiente sísmico crítico y el desplazamiento de Newmark se calculan con los coeficientes parciales aplicados, y el factor que se indica de la superficie crítica es un factor de sobredimensionamiento, no un factor de seguridad, y debe ser mayor que 1.',
    # ==================================================================
    # ogr_core.project.step_names.STEP_NAMES
    # ==================================================================
    # step.paint_material
    'Paint material at ({x:.2f}, {y:.2f})':
        'Pintar material en ({x:.2f}, {y:.2f})',
    # step.offset_external
    'Offset External ({distance:+.2f} m)':
        'Desplazar contorno exterior ({distance:+.2f} m)',
    # step.expand_external
    'Expand/Shrink (expand)':
        'Expandir contorno exterior',
    # step.shrink_external
    'Expand/Shrink (shrink)':
        'Contraer contorno exterior',
    # step.edit_boundary
    'Edit boundary ({op})':
        'Editar contorno ({op})',
    # step.hydraulic
    'Hydraulic properties of {material}':
        'Propiedades hidráulicas de {material}',
    # step.random_variable
    'Random variable {key}':
        'Variable aleatoria {key}',
    # step.delete_random_variable
    'Delete random variable {key}':
        'Eliminar variable aleatoria {key}',
    # step.delete_all_random_variables
    'Delete random variable all':
        'Eliminar todas las variables aleatorias',
    # ==================================================================
    # ogr_core.statistics.messages.SWEEP_NOTES
    # ==================================================================
    # sweep.no_method
    'No analysis method selected.':
        'No hay ningún método de análisis seleccionado.',
    # sweep.needs_drawdown
    'The drawdown level sweep needs a Rapid Drawdown analysis: enable it in Project Settings > Groundwater > Advanced.':
        'El barrido de niveles de desembalse necesita un análisis de desembalse rápido: actívalo en Ajustes de proyecto > Agua subterránea > Avanzado.',
}
