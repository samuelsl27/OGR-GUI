---
name: sdd-validate
description: Valida una spec de OGR-GUI terminada contra sus requisitos (fase 6 del flujo SDD). Úsala cuando todas las tareas estén hechas y se pida validar, cerrar o dar por terminada una spec.
argument-hint: "<NNN de la spec>"
---

# Validación

1. Ejecuta la suite entera y apunta el resultado.
2. Recorre la spec RF a RF y devuelve una tabla:

   | RF | Test que lo cubre | Resultado |
   |---|---|---|

   Un RF sin test es un hueco: dilo, no lo des por bueno.
3. Marca la lista de diseño de la spec mirando la pieza de verdad
   (capturas offscreen con `QT_QPA_FONTDIR=C:/Windows/Fonts`, en inglés y
   español y en los dos temas) y di qué principio falla. Mira también la CI
   (Linux, Windows y macOS).
4. Comprueba los criterios de finalización de la spec y los «Hecho
   cuando» de `tasks.md`.
5. Veredicto: **completa** / **incompleta** (con la lista de lo que falta).
   Si es completa, propón actualizar el estado de la spec y
   `spec/constitution/roadmap.md`, y espera el OK.
