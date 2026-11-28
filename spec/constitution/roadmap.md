# Hoja de ruta

> **Aprobada por la propietaria (2026-11-24).** Al empezar una
> spec se añade aquí; al terminarla se marca hecha. El orden lo decide la propietaria.

## Hecho

| Spec | Versión | Qué |
|---|---|---|
| [001 — Paquete inicial](../features/001-paquete-inicial/spec.md) | 0.1.0 (2026-11-24) | Las piezas de OGR Slip2D v0.1.486 que pidió OGR FEM2D, y las comprobaciones de las reglas 2 y 3 |
| [002 — El percentil del ajuste, por campo](../features/002-percentil-del-ajuste/spec.md) | 0.1.1 (2026-11-27) | Cada `ContourField` dice el percentil de su ajuste (FEM2D: el rango entero); D-12 enmendado |
| [003 — El español de los mensajes del núcleo](../features/003-espanol-del-nucleo/spec.md) | 0.1.2 (2026-11-27) | El español de las plantillas de los 20 catálogos con código de `ogr_core` v0.2.12, en `ogr_ui/i18n/core_es.py`; `tr()` lo tiene sin que el programa haga nada |
| [004 — La entrada X,Y con relativos, polares y coma decimal](../features/004-entrada-xy/spec.md) | 0.1.3 (2026-11-27) | La entrada X,Y lee `x; y` con coma decimal, `@dx, dy` y `@d<a` desde el punto que da el programa, y dice por qué rechaza lo que no puede leer (`ogr_ui/point_entry.py`) |
| [005 — Los números en pantalla, siempre con punto decimal](../features/005-punto-decimal/spec.md) | 0.1.4 (2026-11-28) | El punto decimal siempre, en los dos idiomas y en cualquier máquina: `ogr_ui.numbers` (`format_number`, `read_number`) y la casilla `NumberBox`, en la que la coma no se escribe; los diálogos de contornos y de enganche, la leyenda, la barra y el gráfico XY |
| [006 — En la entrada X,Y, la coma separa y el punto es el decimal](../features/006-coma-separa-coordenadas/spec.md) | 0.2.0 (2026-11-28) | Incompatible: la entrada X,Y lee solo `x.x,x.x`; deja de leer la coma decimal, el espacio solo y el punto y coma. D-7 enmendado. Con la gemela de Slip2D 0.1.506: `ContourSettings.automatic` en Viridis |

## En curso

Nada. Las specs 005 y 006, del 2026-11-28, están hechas.

## Pendiente de decidir

Lo que se encontró al hacer la 0.1.0 o al escribir las
[referencias de diseño](referencias-de-diseno.md) («Lo que falta»). Ninguno bloquea a FEM2D.

| Candidata | Qué es | Choca con |
|---|---|---|
| El control «Orthogonal window» | `SnapSettings.ortho_snap_angle_deg` no lo lee el motor: arreglarlo (ORTHO solo dentro de ese ángulo) o quitar el control. Igual en Slip2D | Regla 7; D-4 |
| Contraste AA del tema claro | `warning`, `accent` y `toggle_off` entre 4,08:1 y 4,48:1; subirlos a 4,5:1 y el test con ellos. Cambia el aspecto de Slip2D cuando lo adopte | D-10 |
| El progreso con espera | Que `run_task` abra su diálogo pasado 1 s, no al arrancar | D-5 |
| Rampa de espaciado y escala tipográfica con nombre | Que los márgenes y los tamaños de letra de un diálogo salgan de `ogr_ui`, como los colores | D-2, D-3 |
| Estado vacío | Una pieza para «nada todavía», «sin resultados» y «no se pudo cargar» | D-13 |
| «Fit to results» | Que se deshabilite cuando los valores no son del campo elegido | D-4, D-9 |
| Traductores de Qt | Que `switch_qt_translator` borre el que quita (hoy queda uno muerto por cambio de idioma). Igual en Slip2D | — |
| El mínimo del espaciado de la rejilla | El diálogo de enganche pide `lo=1e-6` con 4 decimales, y Qt lo redondea a 0: se puede escribir un espaciado 0. Igual en Slip2D. Encontrado con la spec 005 | Regla 7; D-7 |
| Notas largas en diálogos estrechos | `hold_wrapped_height` mide a la anchura mínima: con una nota muy larga y una anchura mínima pequeña, la altura puede pasar de la pantalla | D-10 |

## Para después

- La adopción por OGR Slip2D y por OGR Data, cuando sus sesiones lo decidan: lo que pidan para
  adoptarlo entra como spec aquí.
- Las piezas que FEM2D escriba sobre estas y que un segundo programa necesite igual (se mueven
  aquí, no se copian).
