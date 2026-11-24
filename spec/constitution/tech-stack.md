# Stack

> **Aprobada por la propietaria (2026-11-24).** Las decisiones del nombre del paquete, del
> núcleo y de macOS las había tomado ya ese mismo día.

| Decisión | Por qué | Alternativa descartada |
|---|---|---|
| **El paquete se importa como `ogr_ui`**; el repositorio es `OGR-GUI` y la distribución `ogr-gui` | `ogr_gui` es el paquete de interfaz de OGR Slip2D: con el mismo nombre, Slip2D no podría instalar este sin renombrar el suyo (decisión de la propietaria, 2026-11-24) | `ogr_gui` en todo (Slip2D tendría que renombrar 48 000 líneas para adoptarlo); `ogr-ui` en todo (cambiaba lo que ya decían el ADR-0005 y la spec 006 de FEM2D) |
| **Sin `ogr-core` en ejecución**; el núcleo entra solo por el extra `[test]`, fijado a una etiqueta, para el runner de la suite y su comprobación de fugas | pip no admite dos referencias git distintas a la misma distribución: si `ogr-gui` fijara una etiqueta del núcleo, cada programa tendría que fijar la misma. Y OGR Data no usa el núcleo (decisión de la propietaria, 2026-11-24) | Depender de `ogr-core` por etiqueta, como pedía la petición de FEM2D |
| **Python 3.11+** | El suelo de la suite; la CI prueba 3.11, 3.12 y 3.13 | — |
| **PySide6 ≥ 6.6, menos 6.12.0 en Python 3.11** | Qt Widgets, como los tres programas. La 6.12.0 en 3.11 aborta en Linux (D395 de Slip2D) | PyQt6 (GPL o comercial, y otro enlace de Qt que el de los tres programas, que ya son PySide6, LGPL) |
| **qtawesome ≥ 1.3, con Font Awesome 6 Free** | Iconos vectoriales que se recolorean con el tema. MIT; los iconos CC BY 4.0, atribuidos en `THIRD_PARTY.md` | Iconos propios en SVG (un juego entero que dibujar y mantener) |
| **Matplotlib ≥ 3.8** | El gráfico XY no modal (`xy_chart`), como en Slip2D | — |
| **Tests con el runner de la suite** (`ogr_core.testing.runner`), sin pytest real, siempre con `QT_QPA_PLATFORM=offscreen` | El mismo runner, la misma comprobación de fugas y la misma salida en toda la suite | pytest (otro runner, otra comprobación de fugas) |
| **CI en Linux y Windows con 3.11, 3.12 y 3.13, y en macOS con 3.12** | Qt no es la misma biblioteca en cada plataforma (la primera corrida encontró en macOS otra política de foco). macOS con un solo Python porque los ejecutores de GitHub iban cortos (decisión de la propietaria, 2026-11-24) | macOS con las tres versiones (seis de los once primeros trabajos se cancelaron sin arrancar); sin macOS |
| **Versiones propias desde 0.1.0**, `X.Y.Z` en la etiqueta y `X.Y.Z.dev0` entre etiquetas | Los programas fijan este paquete por etiqueta, como el núcleo, y comparan números | — |
