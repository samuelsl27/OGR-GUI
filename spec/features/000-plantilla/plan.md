# Plan NNN — <Nombre del cambio>

Sin código. Cada apartado dice qué RF cubre.

## Decisiones

| Decisión | Alternativa descartada y por qué | RF |
|---|---|---|
| … | … | RF-1 |

## Módulos

Dentro de `ogr_ui`, sin importar el núcleo ni ningún programa:

- `ogr_ui/…` — …
- `ogr_ui/i18n/es.py` — textos nuevos

## Interfaces

Lo que un programa llama o entrega (un argumento, una clase pequeña, un registro), con un ejemplo de
uso desde un programa.

## Compatibilidad

Qué sigue funcionando igual para un programa que fija la versión anterior; qué no, y con qué
margen.

## Estrategia de tests

- La pieza sola, sin ventana de ningún programa: …
- Los dos idiomas y los dos temas: …
- Lo que puede variar entre plataformas: …
- Estado global restaurado (regla 5): …

## Riesgos

- …
