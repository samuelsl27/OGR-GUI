# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
Rule 2 of the suite, the same in every program: **every visible text goes
through ``tr()``, and every text that does has its translation.**

From OGR Slip2D v0.1.486, where it was two test files of that program
(``tests/test_gui_spanish_v1318.py``, the census by the syntax tree of the
texts outside ``tr()``, and ``tests/test_i18n_coverage_v141.py``, every key
wrapped and translated, none left identical). Here the rules are functions
over a package's folder, so each program calls them on its own interface
and they say the same thing in all of them:

* :func:`census` — ``{file: [(line, text)]}`` of the interface texts
  outside ``tr()``, by the rules Slip2D learned (v0.1.318 to v0.1.435:
  constructors and setters, messages, f-strings, both branches of a
  conditional, a name carried into a field of a translated text...);
* :func:`counted` — the census less the program's exceptions, each with
  its reason; :func:`ghost_exceptions` — the exceptions no longer in the
  code;
* :func:`field_census` — fields of a translated text filled with an
  English attribute (``display_name``, an enum's ``value``);
* :func:`wrapped_keys`, :func:`missing_translations`,
  :func:`identical_translations` — the keys handed to ``tr()``, those
  with no translation, and those translated as themselves.

A program's test reads, for example::

    from ogr_ui.testing import texts
    left = texts.counted(PACKAGE, EXCEPTIONS)
    assert len(left) == BUDGET, left

Pure Python and the standard library: nothing here imports Qt.

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Iterable, Mapping, Optional

#: The folders of a package that hold dictionaries and not interface: they
#: are read by no census. A program with its dictionary elsewhere says so.
SKIP = ("i18n/",)

#: Calls whose FIRST argument is text the user reads.
_FIRST = {"setWindowTitle", "QLabel", "QPushButton", "QCheckBox",
          "QGroupBox", "QRadioButton", "QAction", "setText", "setToolTip",
          "setStatusTip", "setPlaceholderText", "setTitle", "setWhatsThis",
          "addRow", "showMessage", "QToolButton", "setSpecialValueText",
          # the titles of a tool bar, a dock and a menu
          "QToolBar", "QDockWidget", "QMenu", "addMenu", "addAction",
          "QProgressDialog", "setLabelText",
          # the text of a combo or list item (its data is the second)
          "addItem"}
#: QInputDialog.get*(parent, title, label, ...): the title and the label.
_INPUTS = ("getText", "getInt", "getDouble", "getItem", "getMultiLineText")
#: Calls whose SECOND argument is.
_SECOND = {"addTab", "setTabText", "insertTab", "insertItem"}
#: Calls whose first argument is a LIST of texts the user reads.
_HEADERS = {"setHorizontalHeaderLabels", "setVerticalHeaderLabels",
            "setHeaderLabels"}
_BOXES = ("information", "warning", "critical", "question")
#: v0.1.432 (D399) -- the roles of an item's data that reach the screen
#: (``setItemData(i, text, Qt.ToolTipRole)``); any other role is data.
_TEXT_ROLES = {"DisplayRole", "ToolTipRole", "StatusTipRole",
               "WhatsThisRole"}
#: v0.1.433 (D411) -- item constructors whose first argument is the text of
#: the cell or the row (the tree item's is a list): « [BC]» reached a cell
#: of the transient stages this way.
_ITEMS = {"QTableWidgetItem", "QListWidgetItem", "QStandardItem"}
#: v0.1.433 (D411) -- matplotlib calls whose first argument is text on the
#: figure; ``text(x, y, s)`` has it third. The axes of the random variable's
#: plot and two charts' empty-state messages were English this way.
_MPL_FIRST = {"set_title", "set_xlabel", "set_ylabel", "set_zlabel",
              "suptitle", "annotate"}
#: ... and the plotting calls whose ``label=`` (a legend entry) or
#: ``title=`` is text.
_MPL_LABELLED = {"plot", "axvline", "axhline", "bar", "barh", "scatter",
                 "fill_between", "hist", "step", "errorbar", "axvspan",
                 "axhspan", "stairs", "semilogx", "semilogy", "loglog",
                 "stem", "legend"}
#: String methods that hand back the same text: the census reads through
#: them (``QTableWidgetItem((label + " [BC]").strip())``).
_SAME_TEXT = {"strip", "rstrip", "lstrip", "upper", "lower", "capitalize",
              "title"}
#: A colour's hex code is notation, not text.
_COLOUR = re.compile(r"#[0-9A-Fa-f]{3,8}")

#: Calls whose arguments are not interface text, whatever they hold.
_NOT_TEXT = {
    # CSS, not words
    "setStyleSheet",
    # names the .ogr, the agent or a file keep
    "setObjectName", "setProperty",
    # the data behind a combo or list item, as opposed to its text
    "setData", "findData", "findText",
    # the console, not the interface
    "print",
}

#: A lone axis name is a symbol, the same in every language.
_AXES = {"X", "Y", "Z", "x", "y", "z"}


def _letters(text):
    """Letters outside replacement fields ({0:.2f} and %d alike) and HTML
    tags."""
    text = re.sub(r"%[-+ #0]*\d*(?:\.\d+)?[sdifgeEx]", "", text)
    text = re.sub(r"<[^>]*>", "", re.sub(r"[{][^}]*[}]", "", text))
    return any(c.isalpha() for c in text)


def _text(node):
    """The text of a string node, with {} for each field, or None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return "".join(v.value if isinstance(v, ast.Constant) else "{}"
                       for v in node.values)
    if isinstance(node, ast.BinOp) and isinstance(node.left, ast.Constant) \
            and isinstance(node.left.value, str):
        return node.left.value
    return None


def _call_name(node):
    f = node.func
    return getattr(f, "attr", None) or getattr(f, "id", None)


def loose(src):
    """``[(lineno, text)]`` of the interface texts of ``src`` outside
    ``tr()``, by the three rules of this module."""
    return sorted((n.lineno, _text(n)) for n in loose_nodes(ast.parse(src)))


def loose_nodes(tree):
    """The string nodes of ``tree`` that :func:`loose` reports."""
    parents = {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
    found = {}

    def flag(node):
        # v0.1.432 (D399) -- a conditional puts one of its two branches on
        # screen: in ``tr(a) if c else "b"`` the census saw an IfExp, not a
        # text, and "b" reached the tool tip in English
        if isinstance(node, ast.IfExp):
            flag(node.body)
            flag(node.orelse)
            return
        # v0.1.433 (D411) -- an ``or`` puts one of its operands on screen:
        # ``"  |  ".join(parts) or "no conditions"``
        if isinstance(node, ast.BoolOp):
            for value in node.values:
                flag(value)
            return
        # v0.1.433 (D411) -- every literal of a concatenation reaches the
        # screen, not only the first: «Listo — File → Load Demo Slope…» was
        # ``tr("Ready") + " — File → …"``
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            flag(node.left)
            flag(node.right)
            return
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            # v0.1.433 (D411) -- a literal in a field of a translated text
            # is on screen too: ``tr("…: {0}").format(… or "nothing
            # selectable")``
            if node.func.attr == "format" and _is_tr(node.func.value):
                for value in list(node.args) + [k.value
                                                for k in node.keywords]:
                    flag(value)
                return
            if node.func.attr in _SAME_TEXT:
                flag(node.func.value)
                return
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod) \
                and _is_tr(node.left):
            right = node.right
            for value in (right.elts if isinstance(right, ast.Tuple)
                          else [right]):
                flag(value)
            return
        text = _text(node)
        if text is not None and _letters(text) and text.strip() not in _AXES \
                and not _COLOUR.fullmatch(text.strip()):
            found[id(node)] = node

    # 1 and 2 — the arguments read on screen
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        args = node.args
        if name in _FIRST and args:
            flag(args[0])
        elif name in _SECOND and len(args) >= 2:
            flag(args[1])
        elif name in _HEADERS and args and isinstance(args[0],
                                                      (ast.List, ast.Tuple)):
            for el in args[0].elts:
                flag(el)
        elif name == "_info":                 # a window's message helper
            for a in args[:2]:
                flag(a)
        elif name == "emit" and args and isinstance(node.func, ast.Attribute) \
                and getattr(node.func.value, "attr", None) == "status_message":
            # v0.1.432 (D399) -- the canvas speaks through this signal, which
            # the window shows on its status bar; two of its messages were
            # in English, unseen, because ``emit`` was not a call read here
            flag(args[0])
        elif name == "setItemData" and len(args) >= 3 \
                and getattr(args[2], "attr", None) in _TEXT_ROLES:
            # v0.1.432 (D399) -- an item's data in a role the user reads: two
            # tool tips of the tension crack's combo were in English
            flag(args[1])
        elif name in _INPUTS and isinstance(node.func, ast.Attribute) \
                and getattr(node.func.value, "id", None) == "QInputDialog":
            for a in args[1:3]:
                flag(a)
        elif name in _BOXES and isinstance(node.func, ast.Attribute) \
                and getattr(node.func.value, "id", None) == "QMessageBox" \
                and len(args) >= 3:
            flag(args[1])
            flag(args[2])
        # v0.1.433 (D411) -- the text of an item, and the text on a figure
        elif name in _ITEMS and args:
            flag(args[0])
        elif name == "QTreeWidgetItem" and args \
                and isinstance(args[0], (ast.List, ast.Tuple)):
            for el in args[0].elts:
                flag(el)
        elif name in _MPL_FIRST and args:
            flag(args[0])
        elif name == "text" and len(args) >= 3:
            flag(args[2])
        elif name == "legend" and args \
                and isinstance(args[0], (ast.List, ast.Tuple)):
            for el in args[0].elts:
                flag(el)
        if name in _MPL_LABELLED:
            for kw in node.keywords:
                if kw.arg in ("label", "title"):
                    flag(kw.value)

    # v0.1.433 (D411) -- a conditional half through tr(), anywhere: its
    # other branch goes where the translated one goes («ΔFoS» beside
    # ``tr("Δ over-design factor")``, carried by a variable)
    for node in ast.walk(tree):
        if isinstance(node, ast.IfExp):
            branches = (node.body, node.orelse)
        elif isinstance(node, ast.BoolOp):
            branches = tuple(node.values)
        else:
            continue
        if any(_is_tr(b) for b in branches):
            for b in branches:
                if not _is_tr(b):
                    flag(b)

    # v0.1.435 (D413) -- a name carried into a field of a translated text:
    # every value assigned to it in its function reaches the screen as that
    # field. «Región pintada con «(none)».» came from
    # ``name = mat.name if mat else "(none)"`` and ``tr("…'{0}'.").format(name)``
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for value in carried_into_fields(fn):
                flag(value)

    # v0.1.324 (D315) — a subclass of one of those constructors passes its
    # text up with ``super().__init__("Results", parent)``: five dock titles
    # reached the screen in English that way, unseen by the rule above.
    for cls in ast.walk(tree):
        if not isinstance(cls, ast.ClassDef):
            continue
        bases = {getattr(b, "attr", None) or getattr(b, "id", None)
                 for b in cls.bases}
        if not bases & _FIRST:
            continue
        for node in ast.walk(cls):
            if isinstance(node, ast.Call) and node.args \
                    and isinstance(node.func, ast.Attribute) \
                    and node.func.attr == "__init__" \
                    and isinstance(node.func.value, ast.Call) \
                    and getattr(node.func.value.func, "id", None) == "super":
                flag(node.args[0])

    # 3 — every f-string with letters, unless it is not interface text
    def exempt(node):
        child = node
        p = parents.get(node)
        while p is not None:
            if isinstance(p, ast.FormattedValue) and p.format_spec is child:
                return True                       # a format spec (":.1f")
            if isinstance(p, ast.Raise):
                return True                       # an exception's message
            if isinstance(p, ast.Call):
                name = _call_name(p)
                if name in _NOT_TEXT:
                    return True
                if name and (name.endswith("Command")
                             or name in ("_model_step", "undo_step")) \
                        and p.args and p.args[0] is child:
                    return True                   # an undo step's name
                if name in ("addItem", "insertItem") and child in p.args[1:]:
                    return True                   # a combo item's data
                if any(kw is child and kw.arg == "name"
                       for kw in p.keywords):
                    return True                   # a name the .ogr keeps
            child, p = p, parents.get(p)
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr) and id(node) not in found \
                and not exempt(node):
            flag(node)
    return list(found.values())


#: Methods of a string that keep its text: ``name.strip()`` in a field is
#: ``name`` on screen (v0.1.435).
_SAME_NAME = {"strip", "lstrip", "rstrip", "lower", "upper", "title",
              "capitalize"}


def _own_nodes(fn):
    """The nodes of ``fn``'s body, not those of a function or class nested in
    it: each nested function is read on its own (review of 0.1.435: an
    assignment of a nested one was charged to the outer one). A lambda is
    part of the function that writes it."""
    nested = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    stack = [n for n in fn.body if not isinstance(n, nested)]
    while stack:
        node = stack.pop()
        yield node
        stack.extend(c for c in ast.iter_child_nodes(node)
                     if not isinstance(c, nested))


def _key(target):
    """What a value is bound to: a name, or ``self.<attr>`` in the function
    that sets it."""
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute) and isinstance(target.value,
                                                        ast.Name) \
            and target.value.id == "self":
        return "self." + target.attr
    return None


def _bind(target, value, assigned):
    key = _key(target)
    if key is not None:
        assigned.setdefault(key, []).append(value)
    elif isinstance(target, (ast.Tuple, ast.List)) \
            and isinstance(value, (ast.Tuple, ast.List)) \
            and len(value.elts) == len(target.elts):
        for t, v in zip(target.elts, value.elts):
            _bind(t, v, assigned)


def carried_into_fields(fn):
    """The values that reach a field of a translated text through a name
    ``fn`` sets (v0.1.435, D413).

    Set by ``=`` (every target, every assignment, a tuple target paired with
    a tuple), an annotation, ``+=``, ``:=`` or a ``for`` over literals;
    carried by another name, ``str(name)`` or a method that keeps the text;
    filled by ``.format(...)`` (also by keyword and ``*args``) or ``%`` (a
    tuple, a dict or a name holding one), on a ``tr()`` or on a name that
    holds one. A literal the function translates in place (``name =
    tr(name)``) is not English on screen. Those other ways were holes the
    review of 0.1.435 measured."""
    assigned, fills = {}, []
    for node in _own_nodes(fn):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                _bind(t, node.value, assigned)
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            if node.value is not None:
                _bind(node.target, node.value, assigned)
        elif isinstance(node, ast.NamedExpr):
            _bind(node.target, node.value, assigned)
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
            if isinstance(node.iter, (ast.Tuple, ast.List, ast.Set)):
                for elt in node.iter.elts:
                    _bind(node.target, elt, assigned)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr == "format":
            fills.append((node.func.value, list(node.args)
                          + [k.value for k in node.keywords]))
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
            fills.append((node.left, [node.right]))
    translated = {k for k, values in assigned.items()
                  if any(_is_tr(v) and v.args and _key(v.args[0]) == k
                         for v in values)}

    def template(node, seen=()):
        if _is_tr(node):
            return True
        k = _key(node)
        return k is not None and k not in seen and any(
            template(v, seen + (k,)) for v in assigned.get(k, ()))

    out = []

    def follow(f, seen, via_name):
        if isinstance(f, (ast.Tuple, ast.List)):
            for elt in f.elts:
                follow(elt, seen, via_name)
        elif isinstance(f, ast.Dict):
            for v in f.values:
                follow(v, seen, via_name)
        elif isinstance(f, ast.Starred):
            follow(f.value, seen, via_name)
        elif isinstance(f, ast.Call) and getattr(f.func, "id", None) == "str" \
                and len(f.args) == 1:
            follow(f.args[0], seen, via_name)
        elif isinstance(f, ast.Call) and isinstance(f.func, ast.Attribute) \
                and f.func.attr in _SAME_NAME and not f.args:
            follow(f.func.value, seen, via_name)
        elif _key(f) is not None:
            k = _key(f)
            if k in seen:
                return
            for v in assigned.get(k, ()):
                if k in translated and isinstance(v, ast.Constant):
                    continue
                follow(v, seen + (k,), True)
        elif via_name:
            out.append(f)

    for receiver, fields in fills:
        if template(receiver):
            for f in fields:
                follow(f, (), False)
    return out


#: v0.1.432 (D399) -- attributes that hold English whatever the language: a
#: type's ``display_name`` (a support type's ``DISPLAY_NAME``) and the
#: ``value`` of an enum, the identifier the ``.ogr`` keeps. Each needs its
#: label in the program, or in the dialog that names it.
_ENGLISH_ATTRS = {"display_name", "DISPLAY_NAME", "value"}


def _is_tr(node):
    return isinstance(node, ast.Call) and _call_name(node) == "tr"


def english_fields(src):
    """``[(lineno, expression)]`` of the fields of a translated text that are
    filled with one of :data:`_ENGLISH_ATTRS`.

    v0.1.432 (D399): ``tr("Added {0} with {1} vertices").format(
    b.btype.display_name, n)`` passes every rule above — the text goes
    through tr() — and put «Añadido External Boundary con 6 vértices» on the
    status bar after every boundary drawn in Spanish. A boundary's stored
    name is English too while the user keeps the default, but it is data
    this census cannot tell from a material's name: test_spanish_texts_v1432
    reads those messages through the window."""
    out = []
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr == "format" and _is_tr(node.func.value):
            fields = list(node.args) + [k.value for k in node.keywords]
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod) \
                and _is_tr(node.left):
            right = node.right
            fields = (list(right.elts) if isinstance(right, ast.Tuple)
                      else list(right.values) if isinstance(right, ast.Dict)
                      else [right])
        else:
            continue
        for f in fields:
            if isinstance(f, ast.Attribute) and f.attr in _ENGLISH_ATTRS:
                out.append((f.lineno, ast.unparse(f)))
    return sorted(out)




def _modules(package: Path, skip: Iterable[str] = SKIP):
    package = Path(package)
    for path in sorted(package.rglob("*.py")):
        rel = path.relative_to(package).as_posix()
        if any(rel.startswith(s) for s in skip):
            continue
        # a hidden folder (``.venv`` inside a tree, a tool's cache) is not
        # the package (OGR-Core 0.2.3, the same lesson)
        if any(part.startswith(".") for part in path.relative_to(package).parts):
            continue
        yield rel, path.read_text(encoding="utf-8")


def census(package, skip: Iterable[str] = SKIP) -> dict:
    """``{file: [(lineno, text)]}`` over every module of ``package`` (a
    folder) but ``skip``, before any exception."""
    out = {}
    for rel, src in _modules(package, skip):
        hits = loose(src)
        if hits:
            out[rel] = hits
    return out


def counted(package, exceptions: Mapping = (), skip: Iterable[str] = SKIP) -> list:
    """``[(file, lineno, text)]``: the census less ``exceptions``, a mapping
    ``{(file, text): reason}`` (the text with ``{}`` for each field)."""
    exceptions = dict(exceptions)
    out = []
    for rel, hits in census(package, skip).items():
        for lineno, text in hits:
            if (rel, text) not in exceptions:
                out.append((rel, lineno, text))
    return out


def ghost_exceptions(package, exceptions: Mapping, skip: Iterable[str] = SKIP) -> list:
    """The exceptions that name a text no longer in the code, and those
    with no reason: both are a control gone slack."""
    found = {(rel, text) for rel, hits in census(package, skip).items()
             for _ln, text in hits}
    ghosts = sorted(set(exceptions) - found)
    ghosts += sorted(k for k, why in dict(exceptions).items()
                     if not str(why).strip())
    return ghosts


def field_census(package, skip: Iterable[str] = SKIP) -> dict:
    """``{file: [(lineno, expression)]}`` of :func:`english_fields` over
    every module of ``package`` but ``skip``."""
    out = {}
    for rel, src in _modules(package, skip):
        hits = english_fields(src)
        if hits:
            out[rel] = hits
    return out


def wrapped_keys(package=None, skip: Iterable[str] = SKIP, sources=None) -> set:
    """Every key passed to ``tr()``, extracted with the syntax tree, from
    the modules of ``package`` or from ``sources`` (``[(name, source)]``).

    A regex cannot do this correctly: Python's implicit string
    concatenation means ``tr("Press Preview to check the " "geometry.")``
    passes ONE joined string at runtime, while a regex sees only the first
    fragment. ``tr(a if c else b)`` hands tr() one of two literals, and
    either can be the one on screen (Slip2D v0.1.432, D399)."""
    keys = set()
    pairs = _modules(package, skip) if sources is None else sources
    for _name, src in pairs:
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or _call_name(node) != "tr" \
                    or not node.args:
                continue
            todo = [node.args[0]]
            while todo:
                arg = todo.pop()
                if isinstance(arg, ast.IfExp):
                    todo += [arg.body, arg.orelse]
                elif isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    keys.add(arg.value)
    return keys


def missing_translations(keys: Iterable[str], table: Mapping[str, str]) -> list:
    """The keys with no entry in ``table``: a text routed through ``tr()``
    with no translation silently stays in English."""
    return sorted(k for k in keys if k not in table)


def identical_translations(table: Mapping[str, str],
                           allowed: Iterable[str] = ()) -> list:
    """The entries translated as themselves, less ``allowed`` (proper names,
    symbols, cognates, each a decision): usually a forgotten entry."""
    allowed = set(allowed)
    return sorted(k for k, v in table.items() if k == v and k not in allowed)
