# OGR GUI 0.1.1 — 2026-11-27

Un cambio compatible, la [spec 002](../../spec/features/002-percentil-del-ajuste/spec.md), que pidió
OGR FEM2D el 2026-11-24: el percentil del ajuste del rango de un contorno, por campo.

## 1. Qué cambia

| Pieza | 0.1.0 | 0.1.1 |
|---|---|---|
| `ContourField` | `key`, `label`, `start` | además `fit_percentile`, 0,98 por defecto, en (0, 1]; uno fuera de ese intervalo, un booleano o algo que no es un número lanza `ValueError` al declarar el campo, con su clave |
| `ContourOptionsDialog` | ajustaba al percentil 98 en la casilla de rango automático, en «Fit to results» y en «Restore Defaults» | ajusta con el `fit_percentile` del campo elegido en los tres |
| La ayuda de la casilla «Automatic range from the results» | siempre decía que el máximo usa un percentil | lo dice si el campo elegido recorta; si su percentil es 1, dice que el rango va del menor valor al mayor; cambia al cambiar de campo |
| `ContourSettings.fit_to` | igual | igual |
| `i18n/es.py` | 71 entradas | 72: la ayuda nueva |

D-12 de las [referencias de diseño](../../spec/constitution/referencias-de-diseno.md) se enmendó con
esta versión (decisión de la propietaria del 2026-11-25): el rango automático es el del campo.

## 2. Qué se encontró

- **El dibujo no lo ajusta el diálogo.** Con el rango automático marcado, el programa vuelve a
  ajustar el rango él mismo al dibujar (Slip2D, `interpret_window.py`, `self.contours.fit_to(values)`).
  Si un programa da `fit_percentile` a un campo y no pasa el mismo percentil a `fit_to` al dibujar,
  el diálogo enseña un rango y el dibujo usa otro. `ogr_ui` no lo puede comprobar: el dibujo es del
  programa. Por eso el percentil va en `ContourField`, que el programa ya tiene a mano para dibujar,
  y no en un argumento del diálogo.
- **La ayuda de la casilla se ponía una vez**, al abrir el diálogo, y no seguía al cambio de campo.
  Con un solo percentil para todos daba igual; con uno por campo habría dicho lo de otro campo.
- **`fit_to` ya admitía el percentil** y con 1 ya tomaba el último valor: no ha cambiado. El
  tratamiento de los valores no finitos y del rango plano es el mismo con cualquier percentil.

## 3. Tests

`tests/test_fit_percentile_v011.py`, 18 casos: la declaración y su rechazo; el ajuste como
identidad (los máximos esperados escritos a mano desde el índice `round(p · (n − 1))`, entre ellos
el pico que pidió FEM2D: cien valores entre 1 y 2 y un 50 dan 1,98 con 0,98 y 50 con 1); los tres
ajustes del diálogo con dos campos y lo que devuelve al aceptar (regla 7); la ida y vuelta entre
campos; los rangos y la ayuda de la 0.1.0 para un programa sin percentiles; la ayuda en inglés y en
español; y el diálogo en español en 1366×728 con cada campo. `test_contours_v010.py`, sin tocar, en
verde. 447 casos en 24 archivos, en verde en Windows, en serie y con `--jobs 4`, sin fugas; la CI
de la PR #1, en verde en Linux, Windows y macOS.

La suite entera de OGR FEM2D (que fija la 0.1.0) contra este árbol, con el árbol por delante en el
`PYTHONPATH`: 779 casos, 778 en verde. El que falla es el suyo que compara el `ogr_ui` instalado con
la etiqueta que fija (`test_the_installed_one`: `0.1.1.dev0` contra `v0.1.0`): falla por correr
contra otro árbol, como tiene que fallar, y deja de fallar cuando FEM2D suba su fijación.

## 4. Qué tiene que hacer un programa

Nada, si no da percentiles: los mismos rangos y la misma ayuda que con la 0.1.0. Para usarlo:

```text
STRESS = ContourField("sigma_1", "Major principal stress", fit_percentile=1.0)

# al dibujar con el rango automático, el mismo percentil que el diálogo:
settings.fit_to(values, percentile=FIELDS[settings.field].fit_percentile)
```

- **OGR FEM2D**: da `fit_percentile=1.0` a sus campos, pasa ese percentil donde ajusta el rango al
  dibujar, y puede volver a ofrecer «Fit to results» (su spec 006, plan, «Parte D»). Conviene un
  test suyo que compare el rango que enseña el diálogo con el que usa el dibujo.
- **OGR Slip2D**, cuando adopte el paquete: nada (sus campos recortan al 0,98, el defecto).
