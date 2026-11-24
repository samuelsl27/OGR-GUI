# Principios innegociables

> **Aprobada por la propietaria (2026-11-24).**

Toda spec, plan y tarea de OGR-GUI los cumple. Si una tarea no puede cumplir alguno, se para y se
pregunta a la propietaria. Las reglas de detalle están en [`AGENTS.md`](../../AGENTS.md).

1. **La spec manda.** No se implementa nada que no esté en una spec aprobada. Si falta una
   decisión, se marca `[NECESITA ACLARACIÓN: …]` y se pregunta; no se rellena inventando.
2. **Cambio = primero la spec.** Un requisito nuevo o distinto actualiza el `spec.md`, se enseña
   el diff y después se toca el código.
3. **Una pieza no sabe de qué programa es.** `ogr_ui` no importa el núcleo ni ningún programa;
   lo que cambia de uno a otro (un nombre, un campo, un texto, una fase) llega como argumento por
   una interfaz pequeña.
4. **Se mueve, no se copia.** Una pieza entra aquí cuando dos programas la necesitan iguales, y
   sale de Slip2D sin tocarlo; un programa no copia ni rodea lo que hay aquí: lo pide.
5. **Tests como puerta.** Cada tarea termina con la suite entera en verde, sin fugas, en las tres
   plataformas de la CI. Se prohíbe avanzar en rojo.
6. **La interfaz respeta a la persona.** Toda pieza cumple las
   [referencias de diseño](referencias-de-diseno.md): convenciones de la plataforma, texto por
   `tr()`, nada que no se pueda cancelar, nada deshabilitado sin su porqué, accesible y sin
   patrones engañosos.
7. **Ningún ajuste puede no hacer nada.** Todo control lleva el test que demuestra que cambia lo
   que la pieza devuelve.
8. **Lo que se rompe en un programa se avisa.** Un cambio incompatible sube el segundo número de
   la versión, se anuncia con una versión de margen y su changelog dice qué tiene que cambiar cada
   programa.
9. **Idioma.** Código, identificadores y claves de traducción en inglés; la interfaz en inglés y
   español; specs, notas y `AGENTS.md` en español.
