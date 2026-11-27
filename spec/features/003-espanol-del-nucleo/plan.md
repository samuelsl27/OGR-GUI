# Plan 003 — El español de los mensajes del núcleo

Sin código. Cada apartado dice qué RF cubre.

## Lo que se encontró al leer el código

- **Los catálogos** (`ogr_core` v0.2.12): 20 diccionarios de `MessageSpec`, con 346 códigos, en 13
  módulos. OGR Slip2D lee 17 de ellos en `ogr_gui/core_messages.py`. Los tres que no lee son
  `ogr_core.api.API_MESSAGES` (72), `ogr_core.fem.messages.REFINE_MESSAGES` (28) y
  `ogr_core.project.reported.REPORTED_NOTES` (5). Slip2D importa este último de `ogr_slip2d.reported`.
- **El español de Slip2D** está en `ogr_gui/i18n/__init__.py`, `_DICTS["es"]`, en el commit
  `67faf4f` (v0.1.492, que fija el núcleo v0.2.12). Tiene 232 de las plantillas del núcleo.
- **`tr()` de `ogr_ui`** arranca con `_DICTS["es"] = dict(ES)`. `package_translations("es")`
  devuelve una copia de `ES`, y `add_translations` compara lo que da un programa con la tabla activa.
  Un test de la 0.1.0 (`test_package_translations_is_a_copy`) pide que `package_translations("es")`
  sea igual a `ES`.
- **`test_no_lazy_identity_translations`** rechaza una entrada traducida por sí misma salvo que esté
  en la lista `IDENTICAL`, con su porqué. Del núcleo, al menos `api.error` («error») se traduce por sí
  mismo.
- **El runner** se niega a correr si el núcleo instalado no es el que fija el extra `[test]`. Al
  subir a v0.2.12, el `.venv` de este repositorio necesita esa etiqueta instalada. Es la que la
  propietaria eligió, no una dependencia nueva.

## Decisiones

| Decisión | Alternativa descartada y por qué | RF |
|---|---|---|
| El español del núcleo va en un archivo propio, `ogr_ui/i18n/core_es.py` (`CORE_ES`), ordenado por catálogo y con el código de cada entrada en un comentario | Mezclarlo en `es.py`: su nota dice «the texts of this package, and nothing else», y 340 entradas ajenas a las piezas esconderían las 72 de las piezas | RF-1 |
| `tr()` arranca con `ES` y `CORE_ES` juntos, y `package_translations("es")` devuelve los dos | Una función que el programa llama para añadirlo: RF-2 pide que no haga nada; además `add_translations` ya avisa de lo que un programa cambia | RF-2 |
| `CORE_ES` es un archivo de texto generado **una vez**, con un guion que no se queda en el repositorio, desde el diccionario de Slip2D en `67faf4f` y los catálogos del núcleo v0.2.12. Lo que Slip2D no tiene (unas 110) se escribe a mano | Leer el diccionario de Slip2D o el núcleo en tiempo de ejecución: `ogr_ui` no importa ni el núcleo ni un programa | RF-1, RF-3 |
| Las 110 traducciones nuevas usan la terminología de las 232 de Slip2D (por ejemplo, cómo dice «model», «path», «job», «window» y «bridge») | Traducirlas sueltas: dos mensajes del mismo error dirían lo mismo con palabras distintas | RF-1, RF-3 |
| **RF-8**: se buscan en las traducciones de Slip2D palabras de equilibrio límite («dovela», «talud», «superficie de deslizamiento», «factor de seguridad», «FS», «método») cuya palabra inglesa («slice», «slope», «slip surface», «factor of safety», «FoS», «method») no está en la plantilla. Cada candidata se revisa a mano; la que no vale se cambia por una neutra y va al changelog con la de Slip2D al lado | Revisar las 232 a ojo sin la lista: se pasaría alguna. Aceptar la lista sin revisar: una palabra puede estar bien aunque el inglés no la diga | RF-8 |
| **RF-9**: las cuatro de Slip2D que cambian `{name!r}` por `«{name}»` (`import.water_dropped`, `import.anisotropic_dropped`, `import.link_renamed`, `import.link_dropped`) toman las palabras de Slip2D con `{name!r}`, y van al changelog con la de Slip2D al lado (decisión de la propietaria, 2026-11-27) | Tomarlas como están: el valor saldría con otras comillas que en inglés, y RF-4 dejaría de mirar la conversión | RF-3, RF-4, RF-9 |
| La prueba de RF-3 compara con una copia congelada de las palabras de Slip2D en `67faf4f`: `tests/data/slip2d_core_es_67faf4f.json`, las 232 entradas tal como estaban | Leer el repositorio de Slip2D desde el test: no está en la CI. Darlo por bueno al generarlo: un cambio a mano posterior en `CORE_ES` no lo vería nadie | RF-3, RF-8 |
| Las plantillas sin palabras (solo campos, signos y espacios) no llevan entrada; el test las reconoce quitando los campos y mirando si queda alguna letra | Darles una entrada idéntica: las pondría en `IDENTICAL` sin decir nada | RF-6 |
| Una plantilla con palabras y traducida por sí misma («error») va a `IDENTICAL` con su porqué, como las de las piezas | Dejarla sin entrada: el test de RF-5 la daría por que falta | RF-1, RF-5 |
| Los campos se comparan con el analizador de formato de Python: nombre, conversión (`!r`) y formato (`:.0f`) de cada campo, como multiconjunto; las llaves dobles son literales | Comparar solo los nombres: un `{since:.0f}` traducido como `{since}` cambiaría el número que se lee | RF-4 |
| Los catálogos se descubren en el test recorriendo los módulos de `ogr_core` y quedándose con los diccionarios de `MessageSpec` | Una lista fija de 20: un catálogo nuevo del núcleo se quedaría sin comprobar al subir la etiqueta | RF-1, RF-5 |
| El extra `[test]` pasa a `ogr-core @ …@v0.2.12`, y se instala esa etiqueta en el `.venv` | — (decisión de la propietaria) | RF-1, RF-5 |

## Módulos

Dentro de `ogr_ui`, sin importar el núcleo ni ningún programa:

- `ogr_ui/i18n/core_es.py` — nuevo: `CORE_ES`, unas 340 entradas, con la nota de dónde sale cada
  parte (Slip2D `67faf4f`, escritas en esta versión, las de RF-8).
- `ogr_ui/i18n/__init__.py` — la tabla española arranca con `ES` y `CORE_ES`;
  `package_translations("es")`, lo mismo; la nota del módulo.
- `pyproject.toml` — el extra `[test]` a v0.2.12.
- `tests/test_core_messages_v012.py` — nuevo (abajo).
- `tests/data/slip2d_core_es_67faf4f.json` — nuevo, con su porqué en el test (es la evidencia de
  RF-3, no un diccionario que se use).
- `tests/test_i18n_v010.py` — `test_package_translations_is_a_copy` pasa a pedir `ES` más
  `CORE_ES`; `IDENTICAL`, con las del núcleo que se traducen por sí mismas.
- `docs/changelog/PENDIENTE_v0.1.2.md`, `docs/consumidores.md`, `spec/constitution/tech-stack.md` si
  nombra la etiqueta del extra.

## Interfaces

Ninguna nueva. Un programa sigue diciendo un mensaje del núcleo como FEM2D ya lo hace:

```text
from ogr_core.messages import render
from ogr_ui.i18n import tr
render(API_MESSAGES, err.code, err.args, str(err), translate=tr)
# en español: «No hay ningún modelo abierto.» en lugar de «No model is open.»
```

## Compatibilidad

**Compatible** (0.1.2). Para un programa que fija la 0.1.1:

- Ninguna clave de las piezas cambia.
- Lo que cambia es que `tr()` en español traduce las plantillas del núcleo. Un programa que ya
  las traducía (Slip2D al adoptar) recibe de `add_translations` las claves en que su español
  difiere del de `ogr_ui`. Serán las de RF-8 y ninguna más.
- `package_translations("es")` devuelve más entradas.
- FEM2D no tiene que hacer nada.

## Estrategia de tests

`tests/test_core_messages_v012.py`, con el núcleo del extra `[test]`, solo en el test:

- **RF-1, RF-5**: cada plantilla (inglesa y singular) de cada catálogo descubierto tiene su
  traducción. Si falta alguna, el mensaje nombra el módulo, el catálogo y el código. También se
  comprueba que se descubren los 20 catálogos de la v0.2.12, para que un descubrimiento roto no
  pase en silencio.
- **RF-2**: después de importar `ogr_ui.i18n`, y con el español activo, `tr()` de unas plantillas
  de varios catálogos da su traducción sin llamar a nada más; con `render` y `translate=tr`, un
  error de `ogr_core.api` sale en español con sus valores dentro.
- **RF-3, RF-8, RF-9**: cada entrada de la copia congelada de Slip2D es igual en `CORE_ES`, salvo
  las de las listas de RF-8 y RF-9, que tienen que ser distintas y estar en el changelog.
- **RF-4**: los campos de cada traducción son los de su plantilla, como multiconjunto, incluidas
  conversión y formato. Hay un caso de prueba con una traducción mala, para ver que el comparador la
  rechaza.
- **RF-6**: «`{first}; {second}`» y «`{type}: {text}`» se reconocen como sin palabras y no tienen
  entrada; una plantilla con una palabra no se reconoce así.
- **RF-7**: un `MessageSpec` inventado en el test, con una plantilla sin traducir, sale en inglés
  con `render` y `translate=tr` en español.
- **Regla 5**: el idioma se restaura en cada test; el runner vigila las fugas.
- **Las de siempre**: `test_i18n_v010` (con `IDENTICAL` ampliada y la copia de `package_translations`),
  `test_layering_v010` (`core_es.py` no importa nada), licencia (SPDX en los archivos nuevos;
  el JSON no lleva cabecera y se comprueba qué dice el test de licencia de los `.json`) y nombres
  de productos.
- **Plataformas**: nada depende de ella; la CI en las tres, con el núcleo v0.2.12.

## Diseño

- **D-6**: las 110 nuevas, cortas, en presente y sin signos de exclamación, con la terminología de
  Slip2D. Las de Slip2D se toman como están, salvo las de RF-8.
- No hay pieza visible nueva: el resto de la lista no aplica.

## Riesgos

- **La calidad del español de las 110 nuevas**: lo escribe el agente. Se lista en el changelog
  qué entradas son nuevas, para que la propietaria las lea.
- **Las plantillas que llevan una ruta de menú o un nombre de operación como valor**
  (`{menu}`, `{tool}`, `{new_op}`): el valor no se traduce aquí. Si el programa pasa un menú en
  inglés, la frase sale mezclada. Es del programa, y el changelog se lo dice a FEM2D.
- **Un núcleo nuevo con plantillas nuevas**: hasta que se suba el extra `[test]` y se traduzcan,
  salen en inglés (RF-7). El test de RF-5 lo hace visible al subir la etiqueta.
