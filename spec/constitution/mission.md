# Misión

> **Aprobada por la propietaria (2026-11-24).**

OGR-GUI es la **biblioteca de interfaz común** de la suite OpenGeoRock: las piezas de Qt que hacen
que los programas de la suite se vean y se comporten igual, para que un ingeniero que sabe usar
uno sepa usar los demás.

Nace de OGR Slip2D, el primer programa de la suite, que en 486 versiones fue resolviendo los
problemas de una interfaz de ingeniería en PySide6 (diálogos que cortaban el español, la rueda que
cambiaba números sin querer, entradas grises que no decían por qué, cálculos que congelaban la
ventana). OGR FEM2D, el segundo, pidió esas piezas para no copiarlas (su ADR-0005). OGR Data ya
tiene una copia a mano de parte de ellas.

## Objetivos

1. **Una sola apariencia**: los temas claro y oscuro, los colores con nombre de papel, los iconos
   con clave semántica (spec 001).
2. **Un solo idioma de la interfaz**: `tr()`, el cambio de idioma en caliente para el diccionario y
   el catálogo de Qt, y el español de las piezas comunes (spec 001).
3. **Las piezas que se repiten de un programa a otro**: el enganche del lienzo, la barra de estado,
   la leyenda de color, los contornos, las tareas en segundo plano con progreso y Cancelar, las
   preferencias guardadas, los diálogos comunes (spec 001).
4. **Las guardas que mantienen usable una ventana de Qt**: el tamaño de los diálogos, el suelo de
   los botones, la rueda del ratón, el recolector de basura (spec 001).
5. **Las mismas comprobaciones en toda la suite**: que todo texto pase por `tr()` y tenga su
   traducción, y que toda acción esté en un menú y diga por qué está deshabilitada (spec 001).
6. **Las referencias de diseño de la suite**, en un solo sitio
   ([`referencias-de-diseno.md`](referencias-de-diseno.md)), y las mejoras que pidan, hechas aquí
   para que lleguen a todos los programas a la vez.

## No objetivos

- **La ventana, el lienzo, la interpretación y los diálogos de contenido de cada programa.**
  Mezclan lo común con lo que calcula cada uno; cada programa escribe los suyos sobre estas piezas.
- **Nada del núcleo ni de ningún programa**: ni geometría, ni proyecto, ni cálculo. `ogr_ui` no
  importa `ogr_core` (`tech-stack.md`).
- **Otra tecnología de interfaz** (web, Qt Quick): la suite es de escritorio, en Qt Widgets.

## Quién lo usa

| Programa | Relación |
|---|---|
| OGR FEM2D | Lo pidió (spec 006, D1 (ii); ADR-0005); lo fija en su spec 006, T19 |
| OGR Slip2D | De donde sale el código; lo adopta cuando su sesión lo decida |
| OGR Data | Lleva una copia a mano de los temas, de `tr()` y del patrón de operaciones; lo adopta cuando su sesión lo decida |

Quién fija qué versión: [`docs/consumidores.md`](../../docs/consumidores.md).
