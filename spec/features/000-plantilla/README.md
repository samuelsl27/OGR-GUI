# Plantilla de spec (SDD)

Metodología: [hello-sdd](https://github.com/mouredev/hello-sdd), como el resto de la suite. Flujo
completo y puertas de aprobación en [`AGENTS.md`](../../../AGENTS.md) («Flujo SDD»).

Para cada cambio, copiar esta carpeta a `../NNN-nombre-en-kebab-case/` con el siguiente número
libre de tres cifras, y rellenar:

| Archivo | Fase | Qué contiene | Qué **no** contiene |
|---|---|---|---|
| [`spec.md`](spec.md) | Especificación (+ clarificación) | Qué y por qué: historias, requisitos RF-n en EARS, casos límite, fuera de alcance, diseño, qué cambia para los programas, criterios de finalización, dudas | Stack, archivos, algoritmos, firmas |
| [`plan.md`](plan.md) | Planificación | Cómo: decisiones con la alternativa descartada, módulos, interfaces, compatibilidad, estrategia de tests; cada parte con los RF que cubre | Código |
| [`tasks.md`](tasks.md) | Tareas | Tareas pequeñas (≤ 30 min) en orden, cada una con sus RF y su «Hecho cuando» | Tareas sin criterio verificable |

Cada fase termina con la aprobación explícita de la propietaria antes de pasar a la siguiente.
