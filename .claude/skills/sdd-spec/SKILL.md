---
name: sdd-spec
description: Crea, cambia o revisa una spec de OGR-GUI (fase 1 y 7 del flujo SDD). Úsala cuando se pida una funcionalidad nueva, un cambio de requisitos o escribir/actualizar un spec.md. Entrevista, escribe spec/features/NNN-nombre/spec.md con RF en EARS y pide aprobación. No escribe código.
argument-hint: "<idea o número de spec a cambiar>"
---

# Spec (qué y por qué)

La spec es el contrato: si algo no está en ella, no se implementa.

## Proceso

1. **Lee el contexto**: `AGENTS.md`, `spec/constitution/` (principios,
   misión, stack, roadmap, referencias de diseño) y las specs relacionadas en `spec/features/`.
2. **Entrevista**: preguntas **de una en una**, como mucho 6, esperando
   cada respuesta. Céntrate en casos límite, comportamiento ante errores,
   qué programa lo pide y con qué evidencia, qué cambia para los programas que lo fijan, y fuera de alcance. Sin soluciones técnicas: si
   preguntan «¿cómo lo harías?», vuelve al qué. Sáltate lo que tenga un
   valor por defecto obvio.
3. **Número**: el siguiente libre de tres cifras en `spec/features/`;
   copia `spec/features/000-plantilla/` a `NNN-nombre-en-kebab-case/`.
4. **Escribe** `spec.md` con la plantilla, sin saltarte secciones.
   Requisitos numerados RF-1, RF-2… en EARS, verificables. Si toca la
   interfaz, rellena la sección «Diseño» con los principios D-1…D-14 de
   `spec/constitution/referencias-de-diseno.md` que aplican, y «Qué cambia para los programas».
5. **Lo desconocido** se marca `[NECESITA ACLARACIÓN: pregunta concreta]`.
   Nunca rellenes un hueco inventando.
6. **Pide aprobación explícita.** No pases al plan ni escribas código sin ella.
   Añade la spec al backlog de `spec/constitution/roadmap.md`.

## Cambio de una spec existente (fase 7)

No toques código. Edita el `spec.md`, enseña el diff y espera el OK.

## Reglas

- Solo qué y por qué: nada de stack, archivos, esquemas, algoritmos ni firmas.
- Siempre «Fuera de alcance».
- Un requisito, una frase. Sin adjetivos que no se miden («rápido»,
  «intuitivo»): «redibuja en < 400 ms», «cabe en 1366×728 en español».
- En español; los nombres de la interfaz entre comillas en inglés y
  español cuando ambos importen.

## EARS (un patrón por requisito)

| Patrón | Forma |
|---|---|
| Ubicuo | EL SISTEMA <hará> |
| Evento | CUANDO <disparador>, EL SISTEMA <hará> |
| Estado | MIENTRAS <estado>, EL SISTEMA <hará> |
| Opcional | DONDE <característica>, EL SISTEMA <hará> |
| No deseado | SI <condición>, ENTONCES EL SISTEMA <hará> |

Bien: «CUANDO se pulse Cancelar, EL SISTEMA parará el cálculo en su
siguiente punto de control y lanzará `TaskCancelled` al llamante.» Mal:
«El progreso funciona bien y se puede cancelar.»
