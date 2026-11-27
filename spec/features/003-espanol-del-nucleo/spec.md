# Spec 003 — El español de los mensajes del núcleo

> Estado: aprobada (2026-11-27)

## Contexto y objetivo

El núcleo no traduce (regla 2 de la suite): un mensaje sale de `ogr_core` con un código, una
plantilla inglesa y sus valores, y cada interfaz lo dice en el idioma del lector con
`ogr_core.messages.render`, que traduce la plantilla con el `tr()` del programa. Esas plantillas
son **las mismas en todos los programas**, así que su español tiene que vivir en un sitio. Hoy vive
en el diccionario de OGR Slip2D (232 de las plantillas del núcleo) y en ningún otro: en OGR FEM2D
los errores de sus operaciones, que están sobre `ogr_core.api`, salen en inglés.

Lo pide la sesión de OGR FEM2D por escrito el 2026-11-25 (segunda parte del escrito que dio la spec
002, `FEM2D/Promts_desarrollo/2026_11_24_peticion_ogr_gui_rango_entero.md`) para las 72 plantillas
de `ogr_core.api`. Decisiones de la propietaria (2026-11-27): que entren **todos los catálogos del
núcleo**, no solo los de `ogr_core.api`; que el extra `[test]` fije `ogr-core` **v0.2.12**; y que
una traducción de Slip2D con palabras de equilibrio límite que no valen para otro programa se
cambie por una neutra y se avise a Slip2D. Y, al hacer el plan (2026-11-27), que una traducción de Slip2D que
no conserva los campos de su plantilla tome los de la plantilla y se avise igual (RF-9: cuatro de
`IMPORT_NOTES` cambian `{name!r}` por `«{name}»`).

Evidencia (`ogr_core` v0.2.12, la última etiqueta): 20 catálogos con código, 346 códigos. OGR
Slip2D tiene el español de 232 plantillas de los 17 catálogos que traduce
(`ogr_gui/core_messages.py`); faltan las 72 de `ogr_core.api`, las 28 de `REFINE_MESSAGES` y unas
pocas más. OGR FEM2D (núcleo v0.2.9) no tiene ninguna.

## Usuarios / actores

- OGR FEM2D, que dice los errores de sus operaciones y del núcleo con `render` y el `tr()` de
  `ogr_ui`.
- OGR Slip2D y OGR Data, cuando adopten el paquete: dejan de llevar su propio español de estas
  plantillas.
- El ingeniero que lee un error o una nota del núcleo en español.

## Historias de usuario

- H1: Como programa de la suite quiero que el español de los mensajes del núcleo me llegue con
  `ogr_ui`, para no escribirlo ni copiarlo.
- H2: Como ingeniero que trabaja en español quiero leer en español los errores de las operaciones
  («No hay ningún modelo abierto.»), no en inglés.
- H3: Como Slip2D quiero que el español de `ogr_ui` diga lo mismo que el mío, para adoptarlo sin
  cambiar lo que leen mis usuarios.

## Requisitos funcionales (EARS)

- **RF-1** (ubicuo): EL SISTEMA dará, por `tr()` en español, la traducción de cada plantilla inglesa
  de los catálogos con código de `ogr_core` en la etiqueta del núcleo que fija su extra `[test]`,
  incluida la forma singular de las que la tienen.
- **RF-2** (ubicuo): EL SISTEMA tendrá esas traducciones sin que el programa haga nada más que usar
  `tr()` de `ogr_ui`, como las de sus piezas.
- **RF-3** (ubicuo): EL SISTEMA usará, para cada plantilla que OGR Slip2D ya traduce, las mismas
  palabras que el diccionario de Slip2D, salvo las de RF-8 y las de RF-9.
- **RF-4** (ubicuo): EL SISTEMA conservará en cada traducción los mismos campos (`{nombre}` y su
  formato) que su plantilla inglesa, ni uno más ni uno menos.
- **RF-5** (no deseado): SI una plantilla de un catálogo del núcleo de esa etiqueta no tiene su
  traducción, ENTONCES EL SISTEMA fallará un test que la nombra con su catálogo y su código.
- **RF-6** (no deseado): SI una plantilla no tiene palabras que traducir (solo campos y signos,
  como `{first}; {second}`), ENTONCES EL SISTEMA la dará por traducida sin entrada en el
  diccionario.
- **RF-7** (ubicuo): EL SISTEMA dejará en inglés, como hoy, una plantilla de una versión del núcleo
  posterior a la de su extra `[test]` que todavía no tenga traducción (`render` cae en la
  plantilla inglesa).
- **RF-8** (no deseado): SI la traducción de Slip2D de una plantilla del núcleo usa palabras de
  equilibrio límite donde la plantilla inglesa es general, ENTONCES EL SISTEMA dará una traducción
  neutra y la nombrará, con la de Slip2D al lado, en el changelog de la versión.
- **RF-9** (no deseado): SI la traducción de Slip2D de una plantilla del núcleo no conserva sus
  campos como pide RF-4 (por ejemplo, `«{name}»` donde la plantilla dice `{name!r}`), ENTONCES EL
  SISTEMA dará las palabras de Slip2D con los campos de la plantilla y la nombrará, con la de Slip2D
  al lado, en el changelog de la versión.

## Requisitos no funcionales

- Capas: `ogr_ui` sigue sin importar el núcleo en tiempo de ejecución; las traducciones son textos.
  El núcleo entra solo en los tests, por el extra `[test]`.
- El extra `[test]` sube de `ogr-core` v0.2.8 (que no tiene `ogr_core.api`) a **v0.2.12**, la
  última etiqueta (decisión de la propietaria). Los catálogos de la v0.2.9, la que fija FEM2D, son
  un subconjunto de los de la v0.2.12: un programa con un núcleo anterior tiene traducciones de
  más, que no se usan.
- Las tres plataformas de la CI.

## Diseño

- **D-6**: el texto, en presente y en la terminología de la suite (la de Slip2D, RF-3).
- Lista de comprobación: «Sus textos pasan por `tr()` y tienen su español» y «Corto, en presente,
  con el verbo, sin claves internas ni signos de exclamación» (este último, para las plantillas
  nuevas; las de Slip2D se toman como están). No aplica lo demás: no hay pieza visible nueva.

## Qué cambia para los programas

**Compatible** (sube el tercer número). Un programa que dice los mensajes del núcleo con `render` y
`translate=tr` los ve en español sin cambiar nada. OGR FEM2D: nada que cambiar en su `say()`.
OGR Slip2D, cuando adopte el paquete: puede quitar de su diccionario estas entradas;
`add_translations` le dice cuáles de las suyas cambiarían una de `ogr_ui` (deberían ser ninguna,
por RF-3, salvo las de RF-8 y RF-9, que el changelog lista).

## Casos límite

- Una plantilla con singular (`one`): las dos formas, cada una con su traducción.
- Los valores que el núcleo mete en una plantilla (la clave de un campo, una ruta, un número) no se
  traducen aquí; un valor que es otro mensaje con código (anidado) se traduce con su propia
  plantilla, que también está.
- Los valores de un tipo declarado (`kinds`: un método, una etiqueta, un modelo de resistencia) los
  muestra el programa con su `show`; no entran.
- Llaves dobles (`{{'id', 'op', 'kwargs'}}`): literales, se conservan igual en la traducción.
- Dos catálogos con la misma plantilla inglesa: una sola entrada.
- Una plantilla que Slip2D traduce con palabras de equilibrio límite que no valen para otro
  programa: RF-8. Slip2D, al adoptar, ve la diferencia en lo que le devuelve `add_translations` y
  decide.

## Fuera de alcance

- Los catálogos de los programas (`ogr_slip2d.messages`, los de FEM2D): son de cada programa.
- Una función de `ogr_ui` que haga lo de `render`: el programa ya la tiene en el núcleo.
- Los valores de tipo declarado (`kinds`) y cómo se muestran.
- Cambiar el inglés de una plantilla: es del núcleo.
- La entrada X,Y: spec 004.

## Criterios de finalización

- Todos los RF con su test en verde y la suite entera en verde en las tres plataformas de la CI.
- La lista de diseño marcada.
- El changelog de la versión dice qué se encontró y qué puede quitar cada programa.

## Dudas abiertas

- Ninguna.
