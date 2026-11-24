---
name: sdd-plan
description: Escribe el plan técnico de una spec aprobada de OGR-GUI (fase 3 del flujo SDD). Úsala cuando la spec esté aprobada y se pida planificar o decidir cómo implementarla. Produce plan.md sin código.
argument-hint: "<NNN de la spec>"
---

# Plan (cómo)

Requisito: la spec está **aprobada** (si no, para y dilo).

1. Lee `AGENTS.md`, `spec/constitution/`, la spec y el código de los módulos
   afectados de `ogr_ui`.
2. Escribe `spec/features/<NNN>-*/plan.md` con la plantilla de
   `spec/features/000-plantilla/plan.md`. **Sin código.** Cada apartado
   dice qué RF cubre.
3. Cada decisión lleva la alternativa descartada y el porqué.
4. `ogr_ui` no importa el núcleo ni ningún programa: lo que cambia de un
   programa a otro llega por una interfaz pequeña; dila con un ejemplo de uso.
5. **Compatibilidad**: qué sigue igual para un programa que fija la versión
   anterior y qué no; un cambio incompatible sube el segundo número.
6. Cómo cumple cada principio de diseño de la spec, qué textos nuevos van a
   `ogr_ui/i18n/es.py` y cómo se prueban idiomas, temas y plataformas.
7. Pide aprobación. No escribas tareas ni código sin ella.
