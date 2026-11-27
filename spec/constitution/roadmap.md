# Hoja de ruta

> **Aprobada por la propietaria (2026-11-24).** Al empezar una
> spec se añade aquí; al terminarla se marca hecha. El orden lo decide la propietaria.

## Hecho

| Spec | Versión | Qué |
|---|---|---|
| [001 — Paquete inicial](../features/001-paquete-inicial/spec.md) | 0.1.0 (2026-11-24) | Las piezas de OGR Slip2D v0.1.486 que pidió OGR FEM2D, y las comprobaciones de las reglas 2 y 3 |
| [002 — El percentil del ajuste, por campo](../features/002-percentil-del-ajuste/spec.md) | 0.1.1 (2026-11-27) | Cada `ContourField` dice el percentil de su ajuste (FEM2D: el rango entero); D-12 enmendado |

## En curso

Del escrito de OGR FEM2D del 2026-11-24 y 25 (tres specs, decisión de la propietaria del
2026-11-25).

| Spec | Versión prevista | Qué | Estado |
|---|---|---|---|
| [003 — El español de los mensajes del núcleo](../features/003-espanol-del-nucleo/spec.md) | 0.1.2 | El español de las plantillas de todos los catálogos con código de `ogr_core` (v0.2.12), en un sitio para todos los programas | Implementada en la rama `dev/003-espanol-del-nucleo`; por validar en la CI |
| 004 — La entrada X,Y con relativos, polares y coma decimal | — | `@dx, dy`, `@d<a`, la coma decimal y el rechazo de lo ambiguo en la barra de estado | Por especificar |

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
| Notas largas en diálogos estrechos | `hold_wrapped_height` mide a la anchura mínima: con una nota muy larga y una anchura mínima pequeña, la altura puede pasar de la pantalla | D-10 |

## Para después

- La adopción por OGR Slip2D y por OGR Data, cuando sus sesiones lo decidan: lo que pidan para
  adoptarlo entra como spec aquí.
- Las piezas que FEM2D escriba sobre estas y que un segundo programa necesite igual (se mueven
  aquí, no se copian).
