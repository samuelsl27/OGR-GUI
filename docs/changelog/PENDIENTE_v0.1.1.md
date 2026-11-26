# OGR GUI 0.1.1 — sin etiquetar

> Borrador del changelog de la 0.1.1. Se renombra a `CHANGELOG_v0.1.1.md` en el commit que pone la
> versión en `0.1.1` y se etiqueta: `tests/test_version_v010.py` pide que, mientras la versión sea
> `0.1.1.dev0`, ningún changelog sea de la 0.1.1 o posterior.

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
verde. 447 casos en 24 archivos, en verde en Windows, con `--jobs 4`, sin fugas.

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
