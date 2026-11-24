# Referencias de diseño de la suite

> **Estado: propuesta (2026-11-24), pendiente de la aprobación de la propietaria.** Parte de la
> constitución de OGR-GUI. Se consulta antes de añadir o cambiar cualquier pieza de `ogr_ui`
> (un tema, un color, un icono, un diálogo, un widget, un texto) y al revisar una.

## Para qué es y cómo se usa

OGR-GUI es donde vive el aspecto común de la suite: lo que hace que OGR Slip2D, OGR FEM2D y, cuando
lo adopte, OGR Data se vean y se comporten igual. Este documento reúne las referencias de diseño
de las que salen esas piezas: las decisiones que Slip2D tomó a lo largo de 486 versiones, las guías
que FEM2D (`spec/constitution/guia-de-interfaz.md`) y OGR Data (`spec/constitution/ux-guidelines.md`)
escribieron el 2026-11-24 a partir de las mismas fuentes, y las ocho fuentes externas, leídas de
nuevo para este documento.

1. **Mandan las reglas** (`AGENTS.md` de este repositorio y las siete de la suite). Si una
   referencia choca con una regla, gana la regla.
2. **Este documento es la base común; las guías de cada programa la concretan** para su contenido
   (los campos de un material, las fases de un cálculo, los resultados de un método). No las
   sustituye ni las corrige: donde dicen cosas distintas, se recoge abajo («Dónde difieren las
   guías de la suite») y lo decide la propietaria.
3. **La base es la estética de OGR Slip2D.** Las fuentes sirven para mejorarla, no para cambiarla
   por gusto. Una mejora se hace aquí, en una versión de `ogr-gui`, y llega a todos los programas
   a la vez cuando suben su fijación; nunca en la copia de un programa.
4. **Las fuentes se citan y se enlazan; su texto no se copia.** Laws of UX es CC BY-NC-ND 4.0 y
   Growth.Design se reserva los derechos: lo de abajo es nuestra lectura, con nuestras palabras.
5. Toda pieza nueva o cambiada pasa la lista del final («Lista de comprobación de una pieza»).

## Las fuentes

| Fuente | Qué es | Lo que tomamos | Lo que no |
|---|---|---|---|
| [Laws of UX](https://lawsofux.com/articles/) (Jon Yablonski) | Unas treinta «leyes» de psicología aplicada al diseño: Jakob, Fitts, Hick, Miller, Tesler, Doherty, Postel, Peak-End, Von Restorff, Zeigarnik y las de la Gestalt; y artículos como «Design principles for reducing cognitive load» | El porqué de cada decisión de agrupación, tamaño, número de opciones y tiempo de respuesta | Su marco es la web: «los otros sitios» de Jakob son aquí los otros programas de ingeniería y el propio sistema operativo |
| [Fluent 2](https://fluent2.microsoft.design/) (Microsoft) | El sistema de diseño de Microsoft: principios, color, espaciado, tipografía, accesibilidad, redacción, *tokens* y la guía de esperas («Wait UX») | Windows es la plataforma principal de la suite: sus convenciones, el contraste WCAG 2.1 AA, la rampa de espaciado de 4 px, los umbrales de espera, la idea de *tokens* globales y de alias | La identidad de marca de Microsoft («Unmistakably Microsoft»), las paletas de sus productos, sus kits de Figma y lo que es de IA conversacional |
| [Checklist Design](https://www.checklist.design/) | Listas de comprobación por componente (botón, diálogo, campo, *tooltip*, *tokens*…), por pantalla (ajustes, estado vacío) y por flujo | La estructura de nuestra lista por pieza, y puntos concretos: el texto del botón dice qué pasa, el estado vacío distingue «nada todavía», «sin resultados» y «error», los *tokens* en tres niveles | Lo que es de cuentas, pagos, notificaciones o móvil |
| [Autodesk HIG / Weave](https://github.com/Autodesk/hig) (Apache-2.0) | El sistema de diseño de Autodesk como datos: papeles de color por esquema (claro, gris oscuro, azul oscuro), densidades, papeles por componente y estado; componentes como la entrada numérica, el árbol o la tabla | La referencia más cercana a un programa de ingeniería: el tema como datos con nombre de papel, la densidad alta como dimensión aparte, la entrada numérica que se escribe o se pasa paso a paso | Sus componentes son React; su número exacto de esquemas y densidades no queda claro en su propio README |
| [Humane by Design](https://humanebydesign.com/) | Siete principios para productos que respetan a la persona: resiliente, capacitador, finito, inclusivo, intencional, respetuoso, transparente | Dar el control (cancelar siempre; nada decide por la persona), tener fin, respetar la escala y el contraste del sistema, la fricción que sirve (confirmar lo irreversible), sin datos ni red sin decirlo | Lo que trata de redes sociales, notificaciones y moderación de comunidades |
| [Growth.Design, psicología](https://growth.design/psychology) | 106 sesgos y principios cognitivos en cuatro grupos (información, significado, tiempo, memoria) | Los que afectan al experto: el valor por defecto, el anclaje, el encuadre, la carga cognitiva, la revelación progresiva, reconocer frente a recordar, la retroalimentación y la anticipación | Todos los que se usan como palanca de crecimiento (escasez, prueba social, recompensa variable, aversión a la pérdida, coste hundido…): ver «Lo que no se hace» |
| [GoodUI](https://goodui.org/) | Patrones de interfaz contrastados con pruebas A/B, pensados para la conversión | Deshacer en lugar de confirmar, estilos distintos para lo pulsable y lo seleccionado, mostrar el estado, diseñar para cero datos, valores por defecto con sentido, menos campos, convenciones, atajos de teclado, transiciones cortas | Todo lo que es venta: urgencia, escasez, beneficios en los botones, *opt-out*. La propia página avisa de que el *opt-out* se presta al abuso |
| [Deceptive Patterns](https://deceptive.design/) (antes darkpatterns.org) | El catálogo de los patrones que engañan a la persona para que haga lo que no quería: dieciocho tipos | Lo que **nunca** se hace, con su forma en un programa de cálculo | — |

## Lo que la suite ya decidió

Antes que ninguna fuente, la experiencia de OGR Slip2D. Estas decisiones están en las piezas de
`ogr_ui` y en sus tests; cada una salió de un problema medido, con su número de decisión en Slip2D:

| Decisión | De dónde sale | Dónde está |
|---|---|---|
| Un tema claro, el de la plataforma más una hoja de estilo, y uno oscuro que también cambia la paleta: la hoja sola dejaba texto oscuro sobre fondo oscuro en lo que no nombraba | v0.1.316, D301 | `themes` |
| Los colores que los widgets escribían como literales pasan a tener nombre de papel (`ROLE_COLORS`, `theme_color(role)`): el valor claro es el literal de antes y el oscuro, uno legible sobre fondo oscuro | v0.1.316, D301 | `themes` |
| Lo deshabilitado se pinta más claro en los dos temas, y una cabecera deshabilitada del tema oscuro sigue siendo legible | v0.1.288, D289; v0.1.326, D319 | `themes` |
| Un botón nunca es más estrecho que su texto: el `min-width: 70px` de la hoja cortaba los botones en español; ahora hay un suelo por botón | v0.1.315, D293 | `button_floor` |
| Un diálogo no corta su texto en español: la altura que pide una nota que se parte en líneas, y las casillas que se parten como una etiqueta | v0.1.326, D319–D321; v0.1.421, D363 | `dialog_size` |
| La rueda del ratón no cambia el valor de un campo que no tiene el foco: al desplazar un diálogo largo, los números cambiaban solos | v0.1.285, D286 | `wheel_guard` |
| Una entrada deshabilitada dice por qué en la barra de estado: con los estilos Fusion y windows11, Qt no enseña nada de una entrada gris | v0.1.288, D289; v0.1.294, D289b; v0.1.328, D324 | `disabled_reasons` |
| La barra de estado corta con «…» lo que no cabe y lo da entero en su *tooltip*; las palancas SNAP, GRID, ORTHO y OSNAP se pulsan sobre la palabra | v0.1.328, D325; v0.1.418, D355 | `widgets/status_bar` |
| El enganche trabaja con tolerancias en píxeles de pantalla, y el diálogo lo dice: una tolerancia en metros sería más difícil de usar cuanto más se aleja el zoom | v0.1.3; v0.1.51 | `canvas/snap_engine`, `dialogs/snap_dialog` |
| La leyenda se pinta con la misma función de color que el dibujo, en bandas planas y con la última marcada «+»: una leyenda escrita a mano decía lo mismo fueran cuales fueran los resultados | v0.1.49; v0.1.82 | `widgets/legend`, `contours` |
| Un cálculo largo va en un hilo, con un diálogo de progreso que no se cierra hasta que el cálculo vuelve, y un Cancelar que lo para de verdad; una señal por punto porcentual | v0.1.365, D348; v0.1.366, D362; v0.1.386 | `background`, `dialogs/progress_dialog` |
| El idioma y el tema se guardan y se aplican al arrancar; cambiar de idioma lo anuncia una vez y solo si cambia | v0.1.289, D290; v0.1.291, D290b | `user_prefs`, `dialogs/preferences_dialog` |
| El catálogo de Qt (Sí, No, Guardar…) cambia con el idioma del programa | v0.1.292, D302; v0.1.329, D327 | `qt_catalog` |
| Cada diálogo de archivo empieza en la última carpeta usada, luego en la del proyecto, luego en Documentos | v0.1.418, D355 | `file_folders` |
| Los gráficos informativos son no modales | v0.1.308, D311 | `xy_chart` |
| La basura que el recolector encuentra en otro hilo se libera en el principal: la suite abortaba una vez de cada dos | v0.1.302, D310 | `gc_guard` |
| Todo texto pasa por `tr()` y tiene su español; toda acción está en un menú | reglas 2 y 3; v0.1.41, v0.1.42, v0.1.318 | `i18n`, `testing/texts`, `testing/menus` |

## Principios

Cada principio dice qué se hace, por qué (la fuente) y qué pieza lo lleva. Están numerados para
poder citarlos (`D-3`) en una spec, un test o una revisión.

### D-1. Lo conocido primero

- Las piezas siguen las convenciones de la plataforma: los botones de un diálogo con
  `QDialogButtonBox` (que pone el orden de cada sistema), Esc cierra sin aplicar, Intro acepta, la
  entrada de menú que abre un diálogo acaba en «...». El catálogo de Qt traduce los botones
  estándar.
- Lo mismo se llama igual y se ve igual en todos los programas: el mismo icono para la misma acción
  (`resources/icons`: una clave de la suite no se redefine), la misma palabra, el mismo atajo.
- *Por qué*: la ley de Jakob (la persona espera que funcione como lo que ya conoce) y el modelo
  mental; Fluent 2, «Natural on every platform»: reutilizar los componentes y patrones nativos la
  mayor parte del tiempo.

### D-2. Una sola apariencia, con nombre

- El color de un widget sale de un papel (`theme_color("warning")`), nunca de un literal en el
  widget. Hay tres niveles, como piden Checklist Design (*tokens* primitivos, semánticos y de
  componente) y Fluent 2 (globales y de alias): los valores de las hojas de estilo son los
  primitivos, `ROLE_COLORS` es el nivel semántico, y el estado de un componente (deshabilitado,
  con el foco) lo pone la hoja.
- Un papel nuevo es una decisión: se nombra por su uso («el texto de una nota»), no por su color
  («gris 600»), y se añade a los dos temas a la vez (un test lo exige).
- Los dos temas tienen los mismos papeles y el mismo significado. Weave trata el esquema de color y
  la densidad como dimensiones separadas: aquí hay esquema (claro, oscuro) y no hay todavía
  densidad (ver «Lo que falta»).

### D-3. Agrupar con el espacio

- Lo que va junto se pone junto, y lo distinto se separa con espacio antes que con líneas; un
  diálogo agrupa sus campos en bloques con título, de pocos campos cada uno.
- El espacio sale de una rampa en múltiplos de 4 px (la de Fluent 2: 4, 8, 12, 16, 20, 24…; 2, 6 y
  10 solo para alinear iconos).
- *Por qué*: las leyes de la Gestalt (proximidad, región común, semejanza, conexión) y el
  *chunking*; Miller como orden de magnitud, no como cifra exacta.

### D-4. Menos carga, sin esconder lo que decide

- Pocas opciones a la vista; las avanzadas pueden plegarse. **Pero un valor por defecto que cambia
  el resultado no se esconde**, y una opción que no mueve el número no existe (regla 7).
- Lo que no aplica se **deshabilita con su porqué**, no se oculta: así se descubre que existe y se
  sabe qué hacer antes (`disabled_reasons.gate`).
- *Por qué*: Hick y la sobrecarga de elección, la revelación progresiva; Tesler (la complejidad que
  no se puede quitar la asume el programa, no la persona); el sesgo del valor por defecto (el
  experto también acepta el defecto sin mirarlo); reconocer frente a recordar.

### D-5. Respuesta inmediata, espera honesta, salida siempre

- La ventana no se congela nunca: lo que tarda va en un hilo (`background.run_task`).
- Lo que tarda dice qué está haciendo, con un verbo en gerundio («Calculando...»), y cuánto lleva
  cuando se sabe; si no se sabe, una barra indeterminada solo mientras la espera es corta. Fluent 2
  da los umbrales: menos de 1 s, ningún indicador (un destello confunde); de 1 a 3 s, un indicador
  con su etiqueta; más de 3 s, progreso con lo que se hace.
- Siempre hay un Cancelar que para de verdad, y el diálogo dice «Cancelando...» hasta que el
  cálculo ha vuelto. Un cálculo cancelado no publica nada.
- Una sola señal de espera por acción, pegada a la acción; no varias compitiendo.
- *Por qué*: el umbral de Doherty (por debajo de 0,4 s la interacción fluye); Fluent 2, «Wait UX»;
  Growth.Design, «Labor Illusion» y «Provide Exit Points» (enseñar el trabajo real, nunca uno
  fingido); Humane by Design, «Finite» y «Empowering».

### D-6. El texto: pocas palabras, el verbo en el botón, la notación del oficio

- Todo texto visible pasa por `tr()` y tiene su español (regla 2); un texto que un programa pasa a
  una pieza (el título de la leyenda, la etiqueta de un campo, el texto de una fase) lo traduce el
  programa.
- El botón dice qué pasa al pulsarlo («Descartar cambios», «Restaurar valores»); «Aceptar» y
  «Cancelar» solo cuando el título del diálogo ya dice qué se acepta.
- La unidad va pegada a su campo; los símbolos y las unidades son los del oficio (φ, kPa, m); una
  clave interna (`total_head`) nunca llega a la pantalla.
- Frases cortas, en presente y en voz activa; sin signos de exclamación.
- *Por qué*: Checklist Design (botón y diálogo: la persona tiene que saber qué pasará antes de
  pulsar); Fluent 2, «Content design»; la terminología geotécnica castellana de Slip2D.

### D-7. Entradas tolerantes, nunca silenciosas

- Se acepta lo que no es ambiguo (espacios, coma o punto decimal, `12.5, 3.2` o `12.5 3.2` en la
  entrada X,Y de la barra de estado) y se rechaza lo ambiguo en el campo, al escribir, con un
  mensaje que dice qué falta.
- Un campo tiene su etiqueta, su unidad, su rango y su formato; si hace falta, una pista.
- *Por qué*: la ley de Postel, con su límite en un programa de ingeniería (lo que se acepta se
  enseña tal como se entendió); Checklist Design, «Input field».

### D-8. Deshacer antes que confirmar; confirmar lo irreversible

- Lo que se puede deshacer no pregunta. Se confirma solo lo irreversible (sobrescribir un archivo,
  descartar cambios sin guardar), con el verbo en el botón y diciendo qué se pierde.
- *Por qué*: GoodUI, «Undos instead of prompting for confirmation»; Humane by Design,
  «Intentional» (la fricción que sirve: un tope antes de lo que no tiene vuelta atrás); Checklist
  Design, la «zona de peligro» de los ajustes.

### D-9. Destacar solo lo que importa

- Un aviso destaca porque es el único: un color de aviso y un color de error, los papeles
  `warning` y `error`, y nunca como adorno. Lo obsoleto o incompleto no se puede confundir con lo
  válido.
- El color nunca va solo: lleva texto, un icono o un número (la leyenda lleva sus valores; una
  palanca de la barra de estado cambia de fondo y de peso).
- *Por qué*: el efecto Von Restorff y la atención selectiva; Fluent 2, «Semantic colors» (para
  información importante, no para decorar).

### D-10. Accesible

- Contraste WCAG 2.1 AA: 4,5:1 el texto normal y 3:1 el texto grande, los iconos y los controles
  frente a lo que tienen al lado (Fluent 2). Hoy no todo lo cumple (ver «Lo que falta»).
- Todo se hace con el teclado; el foco se ve, sigue el orden de lectura y no se pierde al cerrar un
  diálogo.
- Se respetan el tamaño de letra y la escala de pantalla del sistema: un diálogo que no cabe con la
  letra grande es un fallo, no una preferencia.
- Las paletas de contornos incluyen una apta para daltonismo («Accessible», derivada de
  Okabe-Ito) y una en grises para imprimir.
- *Por qué*: Fluent 2, «Accessibility» y «One for all, all for one»; Humane by Design,
  «Inclusive» («Give Control»: no desactivar el zoom, el contraste ni el tamaño de letra).

### D-11. Objetivos a la medida de la mano

- Botones e iconos de al menos 24 px de lado útil; lo frecuente, donde está el cursor y en un sitio
  fijo.
- Las tolerancias del enganche son píxeles de pantalla, convertidos a unidades del modelo con el
  zoom.
- *Por qué*: la ley de Fitts y el principio de Pareto.

### D-12. Leyendas y paletas que dicen la verdad

- La leyenda se pinta con la misma función que colorea el dibujo; en modo por bandas, una banda
  plana por intervalo, con la última abierta («6.000+»). El rango se elige por campo y es del
  programa (`ContourField`), igual que sus rangos de un clic (`RangePreset`).
- El rango automático ignora los valores extremos con un percentil; el fijo se fija a propósito.
- *Por qué*: la ley de semejanza y la de conexión; Deceptive Patterns, «Comparison prevention»
  (dos figuras con escalas distintas que parecen comparables).

### D-13. Un estado vacío enseña el siguiente paso

- Una vista sin datos dice qué falta y cómo llenarla («Sin resultados: Análisis → Calcular»).
- No es lo mismo «todavía no hay nada», «la búsqueda no encontró nada» (con una salida para
  ampliarla) y «no se pudo cargar» (un error, que no debe parecer que se han perdido los datos).
- *Por qué*: Checklist Design, «Empty state»; GoodUI, «Designing for zero data».

### D-14. Respeto: el programa calcula, la persona decide

- Sin telemetría, sin llamadas de red, sin avisos repetidos; lo que se dice, se dice una vez y se
  puede consultar.
- Nada decide por la persona ni «recomienda» un resultado; lo que el programa supone, lo dice.
- Sin animaciones decorativas; una transición, si la hay, corta y que no retrase nada.
- *Por qué*: Humane by Design, «Respectful» y «Transparent»; Fluent 2, «Built for focus».

## Lo que no se hace

Los patrones de Deceptive Patterns que podrían colarse sin querer en un programa de cálculo, y lo
que se hace en su lugar:

| Patrón | Cómo aparecería aquí | Qué se hace |
|---|---|---|
| Preselección | Una casilla marcada por defecto que cambia el resultado | El defecto se ve junto al resultado; la opción, en positivo |
| *Sneaking* (colar) | Un ajuste que cambia sin decirlo al importar, al cambiar de unidades o de versión | Se lista lo que cambió; cambiar de unidades no toca los valores |
| Redacción engañosa | «Aceptar / Cancelar» de sentido dudoso; dobles negaciones en una casilla | El verbo en el botón; las opciones en positivo |
| Interferencia visual | Un aviso en gris claro; un resultado obsoleto con el mismo aspecto que uno válido | Los papeles `warning` y `error` con su contraste; lo obsoleto marcado |
| Insistencia (*nagging*) | El mismo aviso en cada cálculo o cada arranque | Una vez, en la barra de estado o en el resumen |
| Difícil de cancelar | Un cálculo sin Cancelar, o un Cancelar que cierra el diálogo y deja el hilo corriendo (fue el D362 de Slip2D) | Cancelar que para de verdad, y el diálogo se queda hasta que el hilo vuelve |
| Obstrucción | Un «Restaurar valores» escondido; deshacer más difícil que hacer | Restaurar en el mismo diálogo; todo deshacible |
| Acción forzada | Pedir cuenta, registro o conexión para usar el programa | Nada de eso |
| Prevención de la comparación | Leyendas de dos figuras con rangos distintos que parecen iguales | El rango y la unidad en la leyenda; el rango fijo, a propósito |
| Urgencia o escasez falsas, prueba social falsa, *confirmshaming*, anuncios disfrazados, costes ocultos | — | No tienen sitio en un programa de cálculo y no se introducen |

Y de Growth.Design, las palancas que **no** se usan: escasez, prueba social, recompensa variable,
aversión a la pérdida, efecto señuelo, coste hundido, reciprocidad, curiosidad, bucles de
inversión. Lo que sí se usa de su lista es lo que protege a la persona: el valor por defecto con
sentido, la revelación progresiva, la retroalimentación y la anticipación, reconocer frente a
recordar, la salida a tiempo.

## Cuando chocan

| Choque | Se resuelve así |
|---|---|
| Revelación progresiva frente a «lo que decide no se esconde» | Un ajuste se puede plegar; su valor se ve siempre junto al resultado |
| Menos opciones (Hick) frente a la regla 7 | Una opción que no mueve el número no se añade; una que lo mueve no se quita por simplificar: se agrupa o se pliega |
| Entrada tolerante (Postel) frente a «nunca en silencio» | Se acepta lo no ambiguo y se enseña como se entendió; lo ambiguo se rechaza en el campo |
| Deshacer antes que confirmar frente a la fricción que sirve | Lo deshacible no pregunta; lo irreversible, sí, una vez y con el verbo |
| Ocultar lo que no aplica frente a descubrirlo | Se deshabilita con su porqué |
| Mejorar el aspecto frente a la coherencia con Slip2D | Se propone; si se acepta, se hace en `ogr-gui` y llega a todos |

## Dónde difieren las guías de la suite

Las guías de FEM2D y de OGR Data salen de las mismas fuentes y casi siempre dicen lo mismo con
otras palabras. Donde no, y donde una fuente dice otra cosa que lo que hace `ogr_ui`, queda aquí
para que lo decida la propietaria; hasta entonces cada programa sigue su guía y `ogr_ui` sigue a
Slip2D.

| Asunto | FEM2D | OGR Data | Fuente | `ogr_ui` hoy | Propuesta |
|---|---|---|---|---|---|
| Cuándo se enseña que algo tarda | Señal de vida desde 0,4 s; progreso con lo que se hace desde 2 s | Respuesta en menos de 400 ms o indicador de trabajo | Fluent 2: nada por debajo de 1 s; indicador de 1 a 3 s; progreso desde 3 s | `run_task` abre su diálogo en cuanto arranca el hilo, dure lo que dure | Respuesta en 0,4 s (Doherty) para lo que se edita; para un cálculo, el diálogo a partir de 1 s, con la etapa desde 3 s. Es un cambio de `background` |
| Mayúsculas de menús y botones en inglés | — | — | Fluent 2: tipo oración en Windows («Define hydraulic properties») | Tipo título, como Slip2D («Define Hydraulic Properties...») | Seguir con el tipo título: cambiarlo rompe la coherencia con Slip2D y con las claves de traducción. En español ya va en tipo oración |
| Puntos suspensivos | — | — | Fluent 2: «Cargando …» con un espacio duro antes | «Computing...», tres puntos sin espacio | Seguir como Slip2D; la convención de Windows para «abre un diálogo» es la misma |
| Contraste del texto | 4,5:1 | WCAG AA (4,5:1) en los dos temas | Fluent 2 y WCAG 2.1 AA: 4,5:1 | El test exige 4,0:1 (el mínimo del tema claro cuando Slip2D lo escribió, v0.1.316); `warning`, `accent` y `toggle_off` del tema claro se quedan entre 4,08 y 4,48 | Subir esos tres papeles a 4,5:1 en una versión de `ogr-gui` y el test con ellos (ver «Lo que falta») |
| Duración de una transición | ≤ 150 ms | — | GoodUI: a partir de 0,5 s estorba | No hay transiciones | Sin animaciones; si alguna vez hace falta, ≤ 150 ms |
| Número de menús | — | ≤ 9, ninguno de una sola entrada | Hick, sobrecarga de elección | — (es de cada ventana) | Lo decide cada programa; `ogr_ui.testing.menus` podría comprobarlo si se acuerda |

## Lo que falta

Lo que este documento pide y `ogr_ui` todavía no cumple. Cada punto es una spec futura, en
`roadmap.md`:

- **Tres colores de texto del tema claro por debajo de 4,5:1** (`warning` 4,37:1, `accent` 4,48:1,
  `toggle_off` 4,08:1 frente al fondo de la ventana o de la barra de estado). Se ven en Slip2D: el
  cambio se decide y se hace aquí.
- **El diálogo de progreso aparece sin esperar**, también para un cálculo de medio segundo
  (D-5).
- **No hay rampa de espaciado ni escala tipográfica con nombre** (D-3): cada diálogo escribe sus
  márgenes. Tampoco hay densidad (Weave) ni tema de alto contraste (Fluent 2, *tokens*).
- **Un control que no hace nada**: «Orthogonal window» del diálogo de enganche
  (`SnapSettings.ortho_snap_angle_deg`), que el motor no lee. Choca con la regla 7 y con D-4.
- **«Fit to results» habilitado cuando no hace nada**, al pasar entre dos campos automáticos del
  diálogo de contornos (D-4, D-9).
- **No hay pieza para el estado vacío** (D-13): cada programa lo escribe a mano.

## Lista de comprobación de una pieza

Al cerrar una tarea que añade o cambia una pieza de `ogr_ui`, cada punto se marca o se dice «no
aplica: …»; no se salta.

**Toda pieza**
- [ ] No importa el núcleo ni ningún programa; lo que es de un programa llega como argumento.
- [ ] Sus textos pasan por `tr()` y tienen su español en `i18n/es.py`; ningún texto queda fuera del
      censo (`testing/texts`) sin una excepción con su porqué.
- [ ] Sus colores salen de `theme_color()`; probada en los dos temas.
- [ ] Probada sin pantalla, sin `exec()` y sin dejar estado (regla 5).

**Diálogo**
- [ ] Título que dice qué se edita; campos en bloques con título; espacio en múltiplos de 4 px.
- [ ] Cada campo con su etiqueta, su unidad, su rango y su validación al escribir.
- [ ] `QDialogButtonBox`; el botón principal con el verbo; Esc cierra sin aplicar.
- [ ] Cabe en 1366×728 en español, con el catálogo de Qt, en los dos temas, sin cortar un botón ni
      una nota (`dialog_size`, `button_floor`).
- [ ] Cada control mueve lo que el diálogo devuelve (regla 7); «Restaurar» vuelve a los valores de
      partida, todos.

**Acción y entrada de menú**
- [ ] Deshabilitada con su porqué (`disabled_reasons.gate`), nunca oculta.
- [ ] El mismo icono y el mismo nombre que la misma acción en otro programa.

**Barra de estado, leyenda, gráfico**
- [ ] El color nunca va solo; la leyenda lleva números, unidad y lo que representa.
- [ ] Lo que no cabe se corta con «…» y se puede leer entero.
- [ ] Un gráfico informativo es no modal.

**Proceso largo**
- [ ] En un hilo; dice qué hace; Cancelar para de verdad; no publica nada si se cancela.

**Color, tema o icono**
- [ ] Un papel nuevo, con nombre de uso, en los dos temas; contraste 4,5:1 si es texto y 3:1 si es
      icono o control.
- [ ] Un icono nuevo de Font Awesome Free (CC BY 4.0, atribuido en `THIRD_PARTY.md`), con su texto
      al lado donde haya sitio.

**Texto**
- [ ] Corto, en presente, con el verbo en el botón, sin claves internas ni signos de exclamación.
- [ ] La notación y la unidad del oficio.

**Y siempre**
- [ ] Ninguno de los patrones de «Lo que no se hace».

---

© 2026 Samuel Sáez López — UPCT — AGPL-3.0-or-later
