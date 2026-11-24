---
name: sdd-tasks
description: Descompone el plan aprobado de una spec de OGR-GUI en tareas (fase 4 del flujo SDD). Úsala cuando el plan esté aprobado y se pidan las tareas o el tasks.md.
argument-hint: "<NNN de la spec>"
---

# Tareas

Requisito: spec y plan **aprobados**.

Escribe `spec/features/<NNN>-*/tasks.md` con la plantilla de
`spec/features/000-plantilla/tasks.md`:

- En orden de dependencia; cada tarea de 30 min como mucho.
- Cada tarea: identificador **Tn**, qué hace, qué RF cubre y una línea
  «Hecho cuando:» verificable (un test concreto en verde, una captura en
  los dos idiomas y los dos temas…).
- Los tests van dentro de la misma tarea que el código que prueban, y
  primero.
- Una tarea para los textos en español si no caben en las anteriores.
- La última, **Validación final**: cada RF con su test, la lista de diseño de la
  spec marcada y la suite entera en verde.
- Todos los RF de la spec aparecen en alguna tarea (dilo si alguno no).

Pide aprobación antes de implementar.
