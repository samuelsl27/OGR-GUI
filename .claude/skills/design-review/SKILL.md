---
name: design-review
description: Revisa una pieza de OGR-GUI (tema, color, icono, widget, diálogo, texto) contra las referencias de diseño de la constitución (Laws of UX, Fluent 2, Checklist Design, Autodesk HIG, Humane by Design, Growth.Design, GoodUI, Deceptive Design). Úsala cuando se pida revisar el diseño o la usabilidad de una pieza. Devuelve hallazgos con evidencia, no arreglos.
argument-hint: "<pieza o módulo de ogr_ui; vacío = todas>"
---

# Revisión de diseño

1. Lee `spec/constitution/referencias-de-diseno.md` (principios D-1…D-14,
   «Lo que no se hace», «Lo que falta» y la lista por pieza) y el código de la
   pieza en `ogr_ui/`.
2. **Mira la pieza de verdad**: captura offscreen con un script en el
   scratchpad (`QT_QPA_PLATFORM=offscreen`,
   `QT_QPA_FONTDIR=C:/Windows/Fonts`, `widget.grab().save(...)`), dentro de un
   `QMainWindow` o un `QDialog` de prueba, en inglés y español y en los dos
   temas; mide el contraste de lo que tenga color. Abre los diálogos con
   `show()`, nunca con `exec()`.
3. Para cada hallazgo: principio D-n (y la ley o fuente), dónde
   (`archivo:línea` o pantalla), evidencia (qué se ve, medida si la hay),
   impacto y prioridad:
   - **P0** bug visible (texto interno en pantalla, control roto, tema a medias, un control que no hace nada);
   - **P1** bloquea o confunde a un programa que use la pieza;
   - **P2** fricción o incoherencia;
   - **P3** pulido.
4. Separa lo que es bug (regla 6: se reporta antes de corregir) de lo que
   es mejora (necesita spec).
5. No cambies código. Si se pide convertir los hallazgos en trabajo, usa
   `/sdd-spec` con ellos como requisitos.
