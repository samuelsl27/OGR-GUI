# OGR GUI 0.2.0 — sin publicar

**Un cambio incompatible**, la [spec 006](../../spec/features/006-coma-separa-coordenadas/spec.md):
en la entrada X,Y de la barra de estado, la coma separa las dos coordenadas y el punto es el
separador decimal (`x.x,x.x`). Es el criterio de la propietaria del 2026-11-28, el mismo que la D12
modificada de OGR FEM2D, y completa la spec 005: en `ogr_ui` ya no hay ningún sitio donde una coma
sea un decimal. Sube el segundo número (regla 8). El aviso de margen es el escrito a FEM2D, el
único programa que fija `ogr-gui`, que sigue en la 0.1.4 hasta que suba a propósito.

Lleva además, a petición de la propietaria, la gemela de un cambio de OGR Slip2D 0.1.506: la
paleta de partida de un campo sin `start` pasa a Viridis.

## 1. Qué cambia

| Pieza | 0.1.4 | 0.2.0 |
|---|---|---|
| Lo que lee la entrada X,Y | dos números separados por `;`, por espacios (con o sin coma antes) o por una coma sola; coma o punto decimal | dos números separados por **una coma**, con o sin espacios alrededor; **solo el punto decimal** |
| Cada número | su propia expresión, con `[.,]` | `ogr_ui.numbers.read_number`, el mismo de las casillas (spec 005) |
| Lo que deja de leerse | — | la coma decimal (`1,5; 2,5`, `1,5 2,5`, `@1,5<30`), el espacio solo (`12.5 3.2`) y el punto y coma (`12.5;3.2`) |
| El motivo de rechazo | «Write a point as x, y (or x; y with decimal commas), @dx, dy or @distance<angle.» | «Write a point as x, y with a decimal point (1.5, 2.5), @dx, dy or @distance<angle.» |
| La ayuda de la entrada | «… x, y (or x; y with decimal commas), …» | «… x, y with a decimal point, …» |
| El texto guía | `x, y · @dx, dy · @d<a` | el mismo |
| `ContourSettings.automatic(field)` | «Hot to cold», 8 bandas | `FIELD_PALETTE = "Viridis"`, 8 bandas |
| D-7 (referencias de diseño) | «coma o punto decimal, `12.5, 3.2` o `12.5 3.2`» | el decimal es siempre el punto; en la entrada X,Y la coma separa (enmendado con la spec 006) |
| `i18n/es.py` | — | las mismas entradas: cambian el motivo y la ayuda |

## 2. Qué se encontró

- **`x.x,x.x` ya se leía**: `1.5,2.5`, `1.5, 2.5` y `@1.5,2` daban el punto en la 0.1.4. Lo que
  cambia es quitar los otros separadores y la coma decimal, no añadir nada.
- **`12.5 3.2` y `12.5;3.2` se aceptaban desde la 0.1.0**, y la spec 004 (RF-16) los mantenía.
  Dejan de leerse porque la propietaria eligió «solo la coma».
- **`1,5` es el punto (1, 5)**, sin aviso. Ya lo era en la 0.1.3 («una sola coma sin espacios
  separa»). Ahora la coma solo puede separar, así que no hay otra lectura.
- **Tests que decían lo contrario**, cambiados a propósito, cada uno con su porqué:
  - en `test_point_entry_v013.py`: `test_every_separator`, `test_one_comma_with_no_space_separates`,
    `test_the_numbers`, `test_the_reference_does_not_move_an_absolute_point`,
    `test_what_010_took_gives_the_same_point`, `test_by_a_shift`, `test_polar_forms`,
    `test_each_form_by_the_keyboard`, `test_the_old_signal_of_the_entry_too`,
    `test_it_imports_only_the_standard_library` (ahora también `ogr_ui.numbers`, sin Qt), y las
    constantes `WRITE_A_POINT` y `HELP`;
  - en `test_status_bar_v010.py`: `test_every_separator_gives_the_same_point_to_the_bit` y
    `test_its_texts_are_translated`;
  - en `test_contours_v010.py`: `test_automatic` (Viridis).
- **Viridis**: Slip2D 0.1.506 (`c4c46df`) hace empezar en Viridis todo campo que no es el factor
  (propuesta D5 de FEM2D), y la gemela aquí, `automatic`, seguía en «Hot to cold». Un test nuevo
  calcula la L* de CIE 1976 de cada parada de Viridis y comprueba que crece (de 14,9 a 90,9). Las
  entradas de Ky y Newmark de «Pendiente de OGR Slip2D», en `consumidores.md`, también se corrigen.

## 3. Tests

`tests/test_coordinate_comma_v020.py`, 16 casos:

- **El lector**:
  - una coma con o sin espacios, los números, el relativo y el polar con punto;
  - el espacio solo y el punto y coma, rechazados; la coma decimal, también en el polar; una coma
    de más o de menos;
  - lo que ya se rechazaba sigue rechazado, con su motivo;
  - lo que la 0.1.4 aceptaba con punto y coma de separador, al bit;
  - el lector lee los números con `read_number` y no importa Qt.
- **La entrada en una barra**: `1.5,2.5` se entrega; `1,5; 2,5`, `1.5 2.5` y `1.5;2.5` se quedan con
  el motivo nuevo, en inglés y en español.
- **Lo que se dice**: el motivo y la ayuda nuevos con su español, los viejos fuera, ninguno habla de
  la coma decimal, y el texto guía es el mismo.

`test_contours_v010.py`: `test_the_field_palette_grows_in_lightness`.

## 4. Qué tiene que hacer un programa

**Incompatible.** Un programa en la 0.1.x no nota nada hasta que suba su fijación. Al subir a la
0.2.0, la entrada X,Y deja de leer la coma decimal, el espacio solo y el punto y coma. Lo que se
escribía con punto decimal y coma de separador da el mismo punto, por la misma señal.

- **OGR FEM2D**:
  - sus tests de `read_point` (el contrato de la v0.1.3, que aceptan la coma decimal) cambian a
    este criterio;
  - si da su propia ayuda a la entrada, deja de hablar de la coma decimal y del punto y coma;
  - sus puntos escritos en tests con punto y coma (`"1; 0"` en `test_gui_case006_v0014`,
    `"0; 20"` en `test_gui_tools_v0014`) pasan a `"1, 0"` y `"0, 20"`;
  - Viridis no cambia lo que dibuja, porque da su propio `start` a cada campo. Pero
    `test_gui_interpret_v0015::TestTheDefaultPalette::test_its_lightness_grows_with_the_value`
    usa `ContourSettings.automatic` como ejemplo de la paleta divergente que Viridis sustituyó, y
    falla con la 0.2.0. Esa comparación tiene que tomar «Hot to cold» por su nombre.

  Su suite contra este árbol: 857 casos, 852 en verde. Fallan los cinco esperados: los cuatro de
  arriba y `test_the_installed_one`, que fija la v0.1.3.
- **OGR Slip2D y OGR Data**, cuando adopten el paquete: la entrada lee solo `x.x,x.x`, y un campo
  sin `start` empieza en Viridis, como ya hace Slip2D.
