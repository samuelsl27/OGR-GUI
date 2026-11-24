# Spec NNN — <Nombre del cambio>

> Estado: borrador | en clarificación | aprobada (AAAA-MM-DD) | hecha (AAAA-MM-DD, vX.Y.Z)

## Contexto y objetivo

Qué problema resuelve y por qué merece la pena (un párrafo). Quién lo pide (el escrito de la
sesión de un programa, una candidata de `roadmap.md`) y la evidencia.

## Usuarios / actores

- El programa que … (OGR FEM2D, OGR Slip2D, OGR Data)
- El ingeniero que usa ese programa y …

## Historias de usuario

- H1: Como <rol> quiero <acción> para <beneficio>.

## Requisitos funcionales (EARS)

Un requisito, una frase, verificable. Un patrón por requisito:

- **RF-1** (ubicuo): EL SISTEMA <hará …>.
- **RF-2** (evento): CUANDO <disparador>, EL SISTEMA <hará …>.
- **RF-3** (estado): MIENTRAS <estado>, EL SISTEMA <hará …>.
- **RF-4** (opcional): DONDE <característica>, EL SISTEMA <hará …>.
- **RF-5** (no deseado): SI <condición>, ENTONCES EL SISTEMA <hará …>.

## Requisitos no funcionales

Solo los que apliquen: plataformas (Linux, Windows, macOS), idiomas (EN/ES), temas (claro,
oscuro), rendimiento (< 400 ms al editar), capas (sin el núcleo ni ningún programa).

## Diseño

Qué principios de las [referencias de diseño](../../constitution/referencias-de-diseno.md) aplica
(D-1 … D-14) y cómo. Copiar aquí la parte de su «Lista de comprobación de una pieza» que toque y
marcarla al validar.

## Qué cambia para los programas

Compatible o incompatible (y entonces sube el segundo número de la versión, con una versión de
margen); qué tiene que cambiar cada programa que lo fije.

## Casos límite

- …

## Fuera de alcance

- …

## Criterios de finalización

- Todos los RF con su test en verde y la suite entera en verde en las tres plataformas de la CI.
- La lista de diseño marcada.
- El changelog de la versión dice qué se encontró y qué tiene que cambiar cada programa.

## Dudas abiertas

- [NECESITA ACLARACIÓN: pregunta concreta]
