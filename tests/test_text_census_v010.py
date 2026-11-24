# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
v0.1.0 — the checks of rule 2 in ``ogr_ui.testing.texts`` find what they
must, and nothing they must not, on sources of their own.

WHAT INVARIANT THIS PROTECTS. Every program of the suite calls these
functions on its own interface (``tests/test_i18n_v010.py`` does on this
package), so a rule that went blind would go blind in all of them at once,
and a census of zero would read as success. Each rule is fed a small
source with the case it was written for, and a control that must stay
clean.

They were the census inside OGR Slip2D's ``tests/test_gui_spanish_v1318.py``
(v0.1.318, D300) and the key scan of ``tests/test_i18n_coverage_v141.py``
(v0.1.41), and checked themselves in Slip2D in:

* ``tests/test_spanish_texts_v1432.py`` (v0.1.432, D399), class
  ``TestTheCensusesCheckThemselves``: the canvas's ``status_message``
  signal, both branches of a conditional, an item's data in a role the
  user reads, a field filled with English (``english_fields``), the keys in
  both branches of ``tr()``;
* ``tests/test_spanish_paths_v1433.py`` (v0.1.433, D411), class
  ``TestTheNewCensusRulesCheckThemselves``: ``or``, every literal of a
  concatenation, a literal in a field of a translated text, an item's text,
  the texts on a figure, a tree item, a legend;
* ``tests/test_interpret_charts_v1435.py`` (v0.1.435, D413), class
  ``TestTheCensusRule``: a name carried into a field of a translated text,
  by every way the review of 0.1.435 measured, and its controls.

New here, because the rules are now functions over a package folder:
``census``, ``counted``, ``ghost_exceptions``, ``field_census`` and
``wrapped_keys`` on a temporary package (with the dictionary, a hidden
folder and a ``skip`` left out), and ``missing_translations`` and
``identical_translations`` on a table.
"""
from __future__ import annotations

import tempfile
from pathlib import Path


def _loose(src):
    from ogr_ui.testing.texts import loose
    return loose(src)


class TestWhatIsReadOnScreen:
    """The first two rules: the arguments a user reads."""

    def test_a_label_a_button_a_title(self):
        assert _loose('w = QLabel("Hello")\n') == [(1, "Hello")]
        assert _loose('b = QPushButton("Apply", self)\n') == [(1, "Apply")]
        assert _loose('self.setWindowTitle("Options")\n') == [(1, "Options")]
        assert _loose('f.addRow("Size:", spin)\n') == [(1, "Size:")]
        assert _loose('c.addItem("Linear", "linear")\n') == [(1, "Linear")]
        # controls: through tr()
        assert _loose('w = QLabel(tr("Hello"))\n') == []
        assert _loose('c.addItem(tr("Linear"), "linear")\n') == []

    def test_a_status_bar_message(self):
        assert _loose('self.statusBar().showMessage("Saved.", 3000)\n') == [
            (1, "Saved.")]
        assert _loose('self.statusBar().showMessage(tr("Saved."))\n') == []

    def test_a_message_box_and_an_input_dialog(self):
        assert _loose('QMessageBox.warning(self, "Title", "Text")\n') == [
            (1, "Text"), (1, "Title")]
        assert _loose('QInputDialog.getText(self, "Rename", "Name:")\n') == [
            (1, "Name:"), (1, "Rename")]
        assert _loose('QMessageBox.warning(self, tr("Title"), tr("Text"))\n'
                      ) == []

    def test_a_tab_and_a_table_header(self):
        assert _loose('t.addTab(page, "General")\n') == [(1, "General")]
        # a lone axis name is a symbol
        assert _loose('t.setHorizontalHeaderLabels(["Name", "X"])\n') == [
            (1, "Name")]

    def test_a_subclass_passes_its_title_up(self):
        src = ('class Results(QDockWidget):\n'
               '    def __init__(self, parent=None):\n'
               '        super().__init__("Results", parent)\n')
        assert _loose(src) == [(3, "Results")]
        assert _loose(src.replace('"Results"', 'tr("Results")')) == []

    def test_the_status_bar_signal_is_text(self):
        assert _loose('self.status_message.emit("Drawing cancelled.")\n') \
            == [(1, "Drawing cancelled.")]
        assert _loose('self.status_message.emit(tr("Drawing cancelled."))\n'
                      ) == []
        # control: another signal carries an action's name, not text
        assert _loose('self.boundary_action_requested.emit("delete", 3)\n') \
            == []

    def test_an_items_text_roles(self):
        assert _loose('c.setItemData(i, "Add one first.", Qt.ToolTipRole)\n'
                      ) == [(1, "Add one first.")]
        assert _loose('c.setItemData(i, "Add one first.", '
                      'Qt.ItemDataRole.StatusTipRole)\n') == [
                          (1, "Add one first.")]
        assert _loose('c.setItemData(i, tr("Add one first."), '
                      'Qt.ToolTipRole)\n') == []
        # control: the data behind an item is not text
        assert _loose('c.setItemData(i, "water_table", Qt.UserRole)\n') == []

    def test_notation_is_not_text(self):
        for src in ('w = QLabel("X")\n',             # an axis
                    'w.setText("#4b0082")\n',        # a colour
                    'w.setText("%d")\n',             # a field alone
                    'w.setText("{0}: {1:.2f}")\n',
                    'w.setText("<br>")\n',           # a tag alone
                    'w.setText(" - ")\n'):           # no letters
            assert _loose(src) == [], src


class TestBothBranchesAndEveryOperand:

    def test_both_branches_of_a_conditional(self):
        assert _loose(
            'a.setToolTip(tr("Auto") if k else "Define a grid by hand")\n'
        ) == [(1, "Define a grid by hand")]
        assert _loose('a.setToolTip("Define a grid" if k else tr("Auto"))\n'
                      ) == [(1, "Define a grid")]
        # nested, and in a status-bar message
        assert _loose('self.status_message.emit("One" if k else ("Two" if j '
                      'else tr("Three")))\n') == [(1, "One"), (1, "Two")]
        assert _loose('a.setToolTip(tr("Auto") if k else tr("By hand"))\n'
                      ) == []

    def test_or_concatenation_fields_items_figures(self):
        cases = {
            'w.setText("  |  ".join(p) or "no conditions")\n':
                [(1, "no conditions")],
            'self.s.showMessage(tr("Ready") + " — File → Open", 6)\n':
                [(1, " — File → Open")],
            'self.s.showMessage(tr("Filter: {0}").format(x or "nothing"))\n':
                [(1, "nothing")],
            't.setItem(0, 2, QTableWidgetItem((a + " [BC]").strip()))\n':
                [(1, " [BC]")],
            'ax.set_xlabel("Value")\nax.text(0, 0, "Empty")\n'
            'ax.axvline(1, label="mean")\n':
                [(1, "Value"), (2, "Empty"), (3, "mean")],
            'd = tr("Δ factor") if f else "ΔFoS"\n': [(1, "ΔFoS")],
            'QMessageBox.warning(p, t, tr("A %s") % (x or "none"))\n':
                [(1, "none")],
            'it = QTreeWidgetItem(["Name"])\n': [(1, "Name")],
            'ax.legend(["mean", "median"])\n': [(1, "mean"), (1, "median")],
        }
        for src, want in cases.items():
            assert _loose(src) == want, (src, _loose(src))
        # controls: through tr(), a colour, and data
        for src in ('w.setText("  |  ".join(p) or tr("no conditions"))\n',
                    'w.setText(c or "#4b0082")\n',
                    'ax.set_xlabel(tr("Value"))\n',
                    'c.addItem(tr("x"), "water_table")\n'):
            assert _loose(src) == [], (src, _loose(src))

    def test_implicit_concatenation_is_one_text(self):
        """Python joins adjacent literals: the census reports the text the
        user reads, not its first fragment."""
        src = ('w = QLabel("Press Preview to check the "\n'
               '           "geometry before importing.")\n')
        assert _loose(src) == [
            (1, "Press Preview to check the geometry before importing.")]


class TestEveryFString:
    """The third rule: any f-string with letters, wherever it is, unless it
    is not interface text."""

    def test_an_f_string_anywhere(self):
        assert _loose('msg = f"Saved {n} files"\n') == [
            (1, "Saved {} files")]
        assert _loose('w.setText(f"{x:.3f} m")\n') == [(1, "{} m")]

    def test_what_is_not_interface_text(self):
        for src in ('raise ValueError(f"bad value {x}")\n',
                    'w.setStyleSheet(f"color: {c}; border: none;")\n',
                    'w.setObjectName(f"panel_{i}")\n',
                    'c.addItem(tr("Linear"), f"key_{i}")\n',
                    'print(f"debug {x}")\n',
                    'stack.push(MoveCommand(f"Move {n} vertices"))\n',
                    'm = Material(name=f"Material {i}")\n',
                    'v = f"{x:.1f}"\n'):
            assert _loose(src) == [], (src, _loose(src))


class TestACarriedName:
    """A name carried into a field of a translated text is read where it is
    set (Slip2D v0.1.435, D413): «(none)» reached the screen so."""

    HEAD = 'def f(self, m, x):\n'
    FOUND = {
        "if-else": '    name = m.name if m else "(none)"\n'
                   '    self.s.showMessage(tr("A {0}.").format(name))\n',
        "%": '    x = "gone"\n'
             '    self.s.showMessage(tr("A %s") % x)\n',
        "keyword": '    name = "gone"\n'
                   '    self.s.showMessage(tr("A {n}.").format(n=name))\n',
        "% tuple": '    name = "gone"\n'
                   '    self.s.showMessage(tr("A %s %d") % (name, 1))\n',
        "% dict": '    name = "gone"\n'
                  '    self.s.showMessage(tr("A %(n)s") % {"n": name})\n',
        "% a name holding a tuple":
            '    args = ("gone", 1)\n'
            '    self.s.showMessage(tr("A %s %d") % args)\n',
        "*args": '    args = ["gone"]\n'
                 '    self.s.showMessage(tr("A {0}").format(*args))\n',
        "every target": '    name = other = "gone"\n'
                        '    self.s.showMessage(tr("A {0}").format(other))\n',
        "the first assignment":
            '    name = "gone"\n'
            '    name = m.name\n'
            '    self.s.showMessage(tr("A {0}").format(name))\n',
        "the last assignment":
            '    name = m.name\n'
            '    name = "gone"\n'
            '    self.s.showMessage(tr("A {0}").format(name))\n',
        "a tuple target": '    a, name = 1, "gone"\n'
                          '    self.s.showMessage(tr("A {0}").format(name))\n',
        "an annotation": '    name: str = "gone"\n'
                         '    self.s.showMessage(tr("A {0}").format(name))\n',
        "+=": '    name = m.name\n'
              '    name += " gone"\n'
              '    self.s.showMessage(tr("A {0}").format(name))\n',
        "for over literals":
            '    for name in ("head", "tail"):\n'
            '        self.s.showMessage(tr("A {0}").format(name))\n',
        ":=": '    if (name := "gone"):\n'
              '        self.s.showMessage(tr("A {0}").format(name))\n',
        "self.attr": '    self.name = "gone"\n'
                     '    self.s.showMessage(tr("A {0}").format(self.name))\n',
        "str(name)": '    name = "gone"\n'
                     '    self.s.showMessage(tr("A {0}").format(str(name)))\n',
        "name.strip()": '    name = "gone "\n'
                        '    self.s.showMessage(tr("A {0}").format('
                        'name.strip()))\n',
        "a second name": '    a = "gone"\n'
                         '    name = a\n'
                         '    self.s.showMessage(tr("A {0}").format(name))\n',
        "a template saved": '    msg = tr("A {0}")\n'
                            '    name = "gone"\n'
                            '    self.s.showMessage(msg.format(name))\n',
    }
    CLEAN = {
        "translated": '    name = m.name if m else tr("(none)")\n'
                      '    self.s.showMessage(tr("A {0}.").format(name))\n',
        "data": '    name = m.name\n'
                '    self.s.showMessage(tr("A {0}.").format(name))\n',
        "nested": '    name = m.name\n'
                  '    def g():\n'
                  '        name = "internal-id"\n'
                  '        return name\n'
                  '    self.s.showMessage(tr("A {0}.").format(name))\n',
        "translated in place": '    name = "Untitled"\n'
                               '    name = tr(name)\n'
                               '    self.s.showMessage(tr("A {0}.").format('
                               'name))\n',
        "not a translated text": '    name = "gone"\n'
                                 '    path = "{0}.csv".format(name)\n',
    }

    def test_every_way_it_is_carried(self):
        for why, body in self.FOUND.items():
            assert _loose(self.HEAD + body), why

    def test_what_it_names_is_the_literal(self):
        found = _loose(self.HEAD + self.FOUND["if-else"])
        assert found == [(2, "(none)")], found

    def test_and_its_controls(self):
        for why, body in self.CLEAN.items():
            assert not _loose(self.HEAD + body), (why,
                                                  _loose(self.HEAD + body))


class TestEnglishFields:

    def test_a_field_filled_with_english(self):
        from ogr_ui.testing.texts import english_fields
        assert english_fields(
            'm(tr("Added {0} with {1} vertices").format('
            'b.btype.display_name, n))\n') == [(1, "b.btype.display_name")]
        assert english_fields(
            'm(tr("Tension Crack: %s") % props.mode.value)\n') == [
                (1, "props.mode.value")]
        assert english_fields(
            'm(tr("%d: %s") % (i, o.kind.value))\n') == [(1, "o.kind.value")]
        assert english_fields(
            'm(tr("A {k}").format(k=T.DISPLAY_NAME))\n') == [
                (1, "T.DISPLAY_NAME")]
        # controls: a label, a stored name, and a text not translated
        assert english_fields(
            'm(tr("Added {0}").format(boundary_label(b)))\n'
            'm(tr("Added {0}").format(b.name))\n'
            'm("Added {0}".format(b.display_name))\n') == []


class TestTheKeys:

    def test_the_keys_in_both_branches_of_tr(self):
        from ogr_ui.testing.texts import wrapped_keys
        assert wrapped_keys(sources=[
            ("x.py", 'tr("Alpha" if c else "Beta")\n'
                     'tr("Gamma" if c else ("Delta" if d else "Eps"))\n')]
        ) == {"Alpha", "Beta", "Gamma", "Delta", "Eps"}

    def test_implicit_concatenation_is_one_key(self):
        from ogr_ui.testing.texts import wrapped_keys
        assert wrapped_keys(sources=[
            ("x.py", 'tr("Press Preview to check the "\n'
                     '   "geometry before importing.")\n')]
        ) == {"Press Preview to check the geometry before importing."}

    def test_what_is_not_a_literal_key(self):
        from ogr_ui.testing.texts import wrapped_keys
        assert wrapped_keys(sources=[
            ("x.py", 'tr(name)\ntr()\nself.tr("Method")\n'),
            ("broken.py", 'tr("Lost" \n'),          # not Python: skipped
        ]) == {"Method"}

    def test_missing_and_identical(self):
        from ogr_ui.testing.texts import (identical_translations,
                                          missing_translations)
        table = {"Cancel": "Cancelar", "Horizontal:": "Horizontal:",
                 "Snap": "Snap"}
        assert missing_translations({"Cancel", "Save", "Open"}, table) == [
            "Open", "Save"]
        assert identical_translations(table) == ["Horizontal:", "Snap"]
        assert identical_translations(table, allowed=("Snap",)) == [
            "Horizontal:"]


# ======================================================================
_FILES = {
    "__init__.py": '"""A package."""\n',
    "window.py": ('def build(self):\n'
                  '    self.setWindowTitle("Main")\n'
                  '    self.s.showMessage(tr("Ready"))\n'
                  '    self.s.showMessage(tr("Added {0}").format('
                  'b.display_name))\n'),
    "widgets/coords.py": ('def show(self, x, y):\n'
                          '    self.label.setText(f"X: {x}   Y: {y}")\n'),
    # the dictionary, a hidden folder and a folder the caller skips
    "i18n/es.py": 'w = QLabel("Ignored")\n',
    ".venv/lib.py": 'w = QLabel("Ignored too")\n',
    "samples/case.py": ('w = QLabel("A sample")\n'
                        'tr("Sample key")\n'),
}


class _Package:
    """A temporary package folder with :data:`_FILES`."""

    def __enter__(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="ogr_ui_census_")
        root = Path(self._tmp.name) / "pkg"
        for rel, src in _FILES.items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(src, encoding="utf-8")
        return root

    def __exit__(self, *exc):
        self._tmp.cleanup()
        return False


class TestOverAPackage:

    def test_census_reads_every_module_but_the_skipped(self):
        from ogr_ui.testing import texts
        with _Package() as pkg:
            assert texts.census(pkg) == {
                "samples/case.py": [(1, "A sample")],
                "widgets/coords.py": [(2, "X: {}   Y: {}")],
                "window.py": [(2, "Main")],
            }
            assert texts.census(pkg, skip=("i18n/", "samples/")) == {
                "widgets/coords.py": [(2, "X: {}   Y: {}")],
                "window.py": [(2, "Main")],
            }
            # with no skip the dictionary is read too; a hidden folder never
            assert "i18n/es.py" in texts.census(pkg, skip=())
            assert not any(rel.startswith(".")
                           for rel in texts.census(pkg, skip=()))

    def test_counted_less_the_exceptions(self):
        from ogr_ui.testing import texts
        exceptions = {("widgets/coords.py", "X: {}   Y: {}"):
                      "notation: the coordinates of the pointer"}
        with _Package() as pkg:
            skip = ("i18n/", "samples/")
            assert texts.counted(pkg, skip=skip) == [
                ("widgets/coords.py", 2, "X: {}   Y: {}"),
                ("window.py", 2, "Main")]
            assert texts.counted(pkg, exceptions, skip=skip) == [
                ("window.py", 2, "Main")]
            # an exception is of one file: the same text elsewhere counts
            assert texts.counted(
                pkg, {("window.py", "X: {}   Y: {}"): "elsewhere"},
                skip=skip) == [("widgets/coords.py", 2, "X: {}   Y: {}"),
                               ("window.py", 2, "Main")]

    def test_ghost_exceptions(self):
        from ogr_ui.testing import texts
        with _Package() as pkg:
            skip = ("i18n/", "samples/")
            real = ("widgets/coords.py", "X: {}   Y: {}")
            gone = ("window.py", "A text no longer there")
            assert texts.ghost_exceptions(pkg, {real: "notation"},
                                          skip=skip) == []
            assert texts.ghost_exceptions(pkg, {real: "notation",
                                                gone: "was here"},
                                          skip=skip) == [gone]
            # an exception with no reason is slack too
            assert texts.ghost_exceptions(pkg, {real: "  "},
                                          skip=skip) == [real]

    def test_field_census(self):
        from ogr_ui.testing import texts
        with _Package() as pkg:
            assert texts.field_census(pkg) == {
                "window.py": [(4, "b.display_name")]}

    def test_wrapped_keys_of_a_package(self):
        from ogr_ui.testing import texts
        with _Package() as pkg:
            assert texts.wrapped_keys(pkg) == {"Ready", "Added {0}",
                                               "Sample key"}
            assert texts.wrapped_keys(pkg, skip=("i18n/", "samples/")) == {
                "Ready", "Added {0}"}
