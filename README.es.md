# OGR GUI

**Las piezas de interfaz que comparten los programas de la suite [OpenGeoRock](https://opengeorock.org)**:
los temas claro y oscuro, los iconos, `tr()` y su diccionario, el motor de enganche, la barra de
estado, la leyenda de color, los contornos, las tareas en segundo plano, las preferencias guardadas
y las guardas que mantienen usable una ventana de Qt.

[English version](README.md)

> **Última versión: 0.1.0.** Las piezas son las de la interfaz de
> [OGR Slip2D](https://github.com/samuelsl27/OGR-Slip2D) en su v0.1.486 (commit `03b6c2d`),
> copiadas sin tocar ese programa. La distribución es `ogr-gui`; el paquete se importa como
> **`ogr_ui`**, porque `ogr_gui` es la interfaz propia de OGR Slip2D y las dos tienen que poder
> compartir un entorno.

## Qué es y qué no es

Es lo que dos programas necesitan para verse y comportarse igual: las hojas de estilo y el color de
cada papel (`ogr_ui.themes`), unas 90 claves semánticas de iconos (`ogr_ui.resources.icons`), un
solo `tr()` con el español de estas piezas (`ogr_ui.i18n`; cada programa añade su diccionario),
SNAP / ORTHO / OSNAP con tolerancias en píxeles (`ogr_ui.canvas.snap_engine`), y las
comprobaciones de dos reglas de la suite para los tests de cada programa: todo texto visible pasa
por `tr()` y toda acción está en un menú (`ogr_ui.testing`).

No es la ventana, el lienzo ni el visor de resultados de un programa: mezclan lo común con lo que
calcula cada uno, y cada programa escribe los suyos sobre estas piezas.

**No** depende de OGR Core. Cada programa fija su propia etiqueta del núcleo, y pip no admite dos
referencias git distintas a la misma distribución; las dos piezas que en Slip2D leían el núcleo
reciben lo que necesitan por una interfaz pequeña (`SnapShape`, `install_progress`).

## Desde un programa

```toml
# pyproject.toml del programa
dependencies = ["ogr-gui @ git+https://github.com/samuelsl27/OGR-GUI@v0.1.0"]
```

Qué programa fija qué versión: [`docs/consumidores.md`](docs/consumidores.md).

## Desarrollo

Hace falta Python 3.11 o posterior (la CI corre 3.11, 3.12 y 3.13 en Linux, Windows y macOS) y git.

```powershell
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -e ".[test]"
$env:QT_QPA_PLATFORM = "offscreen"; .venv\Scripts\python tests\_runner.py
```

El extra `[test]` instala OGR Core desde la etiqueta que fija, solo para el runner de la suite y su
comprobación de fugas. La suite está en verde cuando sus totales dicen `Failed: 0` sin `[LEAK]`.
Las reglas de trabajo están en [`AGENTS.md`](AGENTS.md), las mismas que en el resto de la suite.

## Licencia

**GNU Affero General Public License v3.0 o posterior**
(AGPL-3.0-or-later). El texto íntegro está en [`LICENSE`](LICENSE). Los iconos son de Font Awesome Free (CC BY 4.0): ver [`THIRD_PARTY.md`](THIRD_PARTY.md).

En la práctica:

- Puedes usar OGR Suite libremente, **incluso para trabajo profesional de
  ingeniería**, y facturar ese trabajo sin pagar nada ni publicar nada.
  Ejecutar un programa no es una actividad restringida.
- Si lo **modificas** y dejas que otros usen tu versión **en remoto a
  través de una red** (un servicio web o SaaS), debes ofrecerles el código
  de tu versión. Cobrar por ese servicio está permitido; mantenerlo cerrado
  no.
- **No hay garantía de ningún tipo.** Los resultados deben contrastarse con
  cálculos independientes antes de basarse en ellos. Quien firma un
  proyecto es una persona, no un programa.

Cada archivo lleva su identificador SPDX, y un test falla si a alguno le
falta. Las contribuciones se aceptan en los términos de [`CLA.md`](CLA.md);
ver [`CONTRIBUTING.md`](CONTRIBUTING.md).

© 2026 Samuel Sáez López — Universidad Politécnica de Cartagena.
