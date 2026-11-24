# Spec 001 — Paquete inicial

> Estado: hecha (2026-11-24, v0.1.0).
>
> **Escrita después de implementarla**, el mismo día, al adoptar el flujo SDD en este repositorio:
> recoge lo que se pidió, lo que se decidió y cómo se validó, para que la 0.1.0 tenga su spec como
> todo lo que venga después. La petición de partida está fuera del repositorio
> (`FEM2D/Promts_desarrollo/2026_11_24_peticion_suite_paquete_ogr_gui.md`), y la respuesta a FEM2D,
> en `GUI/notas/2026_11_24_respuesta_a_fem2d_paquete_ogr_gui.md`.

## Contexto y objetivo

OGR FEM2D necesita para sus partes C y D (el modelador, el cálculo y la interpretación en la
interfaz) las mismas piezas de interfaz que OGR Slip2D, y la decisión P1 de su plan de desarrollo
y su ADR-0005 dicen que no las copie: que se extraigan a un paquete hermano, copiándolas de Slip2D
sin tocarlo, como se hizo con el núcleo. OGR Data ya tiene una copia a mano de parte de ellas, y esa
es la copia que diverge. Esta spec es ese paquete: las piezas genéricas de la interfaz de Slip2D
v0.1.486, sin nada del equilibrio límite ni del núcleo, y las comprobaciones de las reglas 2 y 3
para que digan lo mismo en toda la suite.

## Usuarios / actores

- OGR FEM2D, que lo fija en su spec 006 (T19) para escribir su ventana sobre estas piezas.
- OGR Slip2D y OGR Data, que lo adoptarán cuando sus sesiones lo decidan.
- El ingeniero que usa cualquiera de los tres, que encuentra el mismo aspecto y el mismo
  comportamiento.

## Historias de usuario

- H1: Como programa de la suite quiero los temas, los colores, los iconos y `tr()` de Slip2D para
  verme igual que él sin copiarlos.
- H2: Como programa con un lienzo quiero el enganche de Slip2D sin depender de su geometría, para
  dárselo a contornos con arcos.
- H3: Como programa que calcula quiero lanzar un cálculo en un hilo con progreso y un Cancelar que
  funcione, con el progreso de mi propio motor.
- H4: Como programa quiero comprobar en mis tests las reglas 2 y 3 con las mismas funciones que los
  demás, para que digan lo mismo en toda la suite.
- H5: Como Slip2D quiero poder instalar este paquete algún día sin renombrar mi interfaz ni subir
  mi núcleo a la etiqueta de otro.

## Requisitos funcionales (EARS)

**Aspecto**
- **RF-1** (ubicuo): EL SISTEMA ofrecerá los temas claro y oscuro de Slip2D, con su hoja de estilo
  y su paleta, y volverá a la paleta original con el claro.
- **RF-2** (ubicuo): EL SISTEMA dará el color de cada papel en cada tema, con los mismos papeles en
  los dos.
- **RF-3** (ubicuo): EL SISTEMA dará un icono por clave semántica, recoloreado para el tema activo.
- **RF-4** (no deseado): SI un programa intenta registrar o quitar una clave de icono de la suite,
  ENTONCES EL SISTEMA lo rechazará.

**Idioma**
- **RF-5** (evento): CUANDO se cambie el idioma, EL SISTEMA traducirá con `tr()` todo texto
  registrado y avisará a quien escuche.
- **RF-6** (ubicuo): EL SISTEMA tendrá en español todos los textos que sus piezas pasan por
  `tr()`, con las mismas palabras que Slip2D.
- **RF-7** (evento): CUANDO un programa añada sus traducciones, EL SISTEMA devolverá las claves de
  este paquete que haya cambiado.
- **RF-8** (evento): CUANDO se cambie el idioma, EL SISTEMA pondrá el catálogo de Qt de ese idioma
  en lugar del anterior.

**Piezas**
- **RF-9** (ubicuo): EL SISTEMA resolverá SNAP, ORTHO y OSNAP con tolerancias en píxeles sobre
  formas que dan sus vértices y sus segmentos por separado, sin la geometría del núcleo.
- **RF-10** (evento): CUANDO se acepte el diálogo de enganche, EL SISTEMA escribirá cada uno de
  sus controles en los ajustes que recibió, y solo entonces.
- **RF-11** (ubicuo): EL SISTEMA ofrecerá la barra de estado de Slip2D: palancas que se pulsan
  sobre la palabra, coordenadas, entrada X,Y y mensajes cortados con «…» y enteros en su *tooltip*.
- **RF-12** (ubicuo): EL SISTEMA pintará la leyenda de color con la función de color que recibe,
  en bandas o en degradado.
- **RF-13** (ubicuo): EL SISTEMA dará las paletas, los niveles y el rango de los contornos sin Qt,
  y un diálogo de opciones que recibe del programa sus campos y sus rangos de un clic.
- **RF-14** (evento): CUANDO se pida *Restore Defaults* en el diálogo de contornos, EL SISTEMA
  volverá a todos los valores de partida del campo elegido.
- **RF-15** (estado): MIENTRAS corra un cálculo lanzado con `run_task` en un hilo, EL SISTEMA
  mantendrá viva la ventana con un diálogo de progreso modal que no se cierra hasta que el cálculo
  vuelve.
- **RF-16** (evento): CUANDO se pulse Cancelar, EL SISTEMA parará el cálculo en su siguiente
  punto de control y lanzará `TaskCancelled` al llamante, sin publicar resultado.
- **RF-17** (opcional): DONDE el programa entregue sus puntos de control, su fase y los textos de
  cada fase, EL SISTEMA los usará; sin ellos, seguirá leyendo el Cancelar en cada llamada de
  progreso.
- **RF-18** (ubicuo): EL SISTEMA guardará el idioma y el tema de cada programa bajo su propio
  nombre, sin que dos programas lean los del otro.
- **RF-19** (ubicuo): EL SISTEMA impedirá que un diálogo corte sus botones o sus notas en español,
  que la rueda cambie un campo sin foco y que el recolector destruya objetos de Qt en otro hilo.
- **RF-20** (ubicuo): EL SISTEMA abrirá el gráfico XY no modal y cada diálogo de archivo en la
  última carpeta usada, la del proyecto o Documentos.
- **RF-21** (evento): CUANDO el puntero pase por una entrada de menú deshabilitada, EL SISTEMA
  pondrá su motivo en la barra de estado.

**Comprobaciones para los programas**
- **RF-22** (ubicuo): EL SISTEMA dará, sobre la carpeta de un paquete, el censo de los textos
  visibles fuera de `tr()`, las claves sin traducción y las traducidas como sí mismas.
- **RF-23** (ubicuo): EL SISTEMA dará, sobre una ventana, las acciones registradas que no están en
  ningún menú y las entradas deshabilitadas que no dicen por qué.

**Capas y distribución**
- **RF-24** (no deseado): SI una pieza importara el núcleo, un programa o el SDK de MCP, ENTONCES
  EL SISTEMA fallará en sus tests.
- **RF-25** (ubicuo): EL SISTEMA se instalará desde su etiqueta sin traer `ogr-core`.

## Requisitos no funcionales

- Python 3.11 a 3.13; Linux, Windows y macOS, sin pantalla.
- Inglés y español; temas claro y oscuro.
- Cada archivo con su cabecera SPDX; los iconos atribuidos (CC BY 4.0).
- Slip2D no se toca: sus piezas son las de su commit `03b6c2d`.

## Diseño

Esta spec trae las piezas tal como estaban; las
[referencias de diseño](../../constitution/referencias-de-diseno.md) se escribieron después y
recogen lo que estas piezas ya hacían («Lo que la suite ya decidió») y lo que todavía no cumplen
(«Lo que falta»). Lo que falta va a `roadmap.md`, no a esta spec.

## Qué cambia para los programas

Es la primera versión: nada que cambiar. Para adoptarla, la tabla de `docs/consumidores.md`.

## Casos límite

- Un programa que no entrega progreso (RF-17): Cancelar sigue funcionando.
- Un contorno con arcos (RF-9): las cuerdas no son vértices.
- Un campo de contorno sin valores de partida (RF-13): empieza automático.
- macOS, donde un desplegable no editable nace sin foco de rueda (RF-19).
- Dos programas en la misma máquina (RF-18).

## Fuera de alcance

- La ventana, el lienzo, la interpretación y los diálogos de contenido de Slip2D.
- `data_tips.py` (usa las etiquetas del equilibrio límite) y el escritor del archivo de resultados.
- Los campos de contorno de Slip2D (`SCALAR_FIELDS`, `available_fields`) y su 0–6.
- Cambiar el comportamiento de una pieza respecto a Slip2D, salvo lo que exigen los cortes con el
  núcleo y el programa.

## Criterios de finalización

- Todos los RF con su test en verde; la suite entera en verde en serie y con `--jobs 4`, sin
  fugas, y en la CI de Linux, Windows y macOS.
- Etiqueta `v0.1.0`, instalable desde ella; changelog con lo que se encontró.

## Dudas abiertas

Ninguna. Las dos decisiones que la petición no preveía las tomó la propietaria el 2026-11-24: el
paquete se importa como `ogr_ui` y no depende de `ogr-core` en ejecución.

## Validación

La suite entera de la 0.1.0: 421 casos, en verde en Windows (en serie y con `--jobs 4`) y en la CI
(run 45436738545: Linux y Windows con 3.11, 3.12 y 3.13; macOS con 3.12).

| RF | Tests que lo cubren | Resultado |
|---|---|---|
| RF-1, RF-2 | `test_themes_icons_v010.py` | en verde |
| RF-3, RF-4 | `test_themes_icons_v010.py` (`TestAProgramsOwnKeys`, `TestASuiteKeyCannotBeRemoved`) | en verde |
| RF-5, RF-7 | `test_i18n_v010.py` | en verde |
| RF-6 | `test_i18n_v010.py` (la regla 2 sobre `ogr_ui`) | en verde |
| RF-8 | `test_qt_catalog_v010.py` | en verde |
| RF-9 | `test_snap_engine_v010.py` | en verde |
| RF-10 | `test_snap_dialog_v010.py` | en verde |
| RF-11 | `test_status_bar_v010.py` | en verde |
| RF-12 | `test_legend_v010.py` | en verde |
| RF-13, RF-14 | `test_contours_v010.py` (`TestRestoreDefaultsIsTheFieldsStart`) | en verde |
| RF-15, RF-16, RF-17 | `test_background_tasks_v010.py` | en verde |
| RF-18 | `test_preferences_v010.py` | en verde |
| RF-19 | `test_dialog_guards_v010.py`, `test_gc_guard_v010.py` | en verde |
| RF-20 | `test_xy_chart_files_v010.py` | en verde |
| RF-21, RF-23 | `test_menus_v010.py` | en verde |
| RF-22 | `test_text_census_v010.py`, `test_i18n_v010.py` | en verde |
| RF-24 | `test_layering_v010.py` | en verde |
| RF-25 | `test_version_v010.py`; instalación desde la etiqueta en un entorno limpio (2026-11-24) | en verde |
