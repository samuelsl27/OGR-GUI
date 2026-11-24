# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
Internationalization (i18n): one ``tr()`` for every program of the suite.

Lightweight in-memory translation system. Dictionaries are loaded at
startup; the user selects the active language in Preferences and all
``tr()`` calls pick it up. English is the reference: a key is its own
English text, and a key with no translation is shown as it is.

From OGR Slip2D's ``ogr_gui/i18n/__init__.py`` (v0.1.486): **the mechanism
only** (its last forty lines) and the translations of the texts of this
package (:mod:`ogr_ui.i18n.es`). Slip2D's 3 488 entries stay in Slip2D.
Each program registers its own dictionary at start with
:func:`add_translations`; a key this package already translates keeps the
package's translation unless the program says otherwise, which it does
only on purpose (:func:`add_translations` returns the keys it changed).

Why not Qt Linguist .ts/.qm files? Because shipping a pure-Python dict is
much simpler, easier to edit without compiling, and fully dynamic. The
``tr(...)`` signature would not change if that were ever done.

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

from typing import Callable

from .es import ES as _ES

_DICTS: dict[str, dict[str, str]] = {
    "en": {},  # English is the reference; keys == values
    "es": dict(_ES),
}

_LANG = "en"
_LISTENERS: list[Callable[[str], None]] = []


def set_language(code: str) -> None:
    """Switch the active language. Emits a notification to listeners."""
    global _LANG
    if code not in _DICTS:
        raise KeyError(f"Unknown language '{code}'. Available: {list(_DICTS)}")
    _LANG = code
    for cb in list(_LISTENERS):
        try:
            cb(code)
        except Exception:  # noqa: BLE001
            pass


def current_language() -> str:
    return _LANG


def available_languages() -> list[str]:
    return list(_DICTS.keys())


def on_language_changed(cb: Callable[[str], None]) -> None:
    _LISTENERS.append(cb)


def remove_language_listener(cb: Callable[[str], None]) -> None:
    """Undo :func:`on_language_changed` (for a window that closes, and for
    the tests: rule 5)."""
    try:
        _LISTENERS.remove(cb)
    except ValueError:
        pass


def tr(key: str) -> str:
    """Translate ``key`` into the active language (falls back to the key)."""
    return _DICTS.get(_LANG, {}).get(key, key)


def add_translations(lang: str, mapping: dict[str, str]) -> list[str]:
    """Register a program's translations for ``lang``.

    Returns the keys whose translation was already there and is now
    different, so that a program that overrides one of this package's
    texts does it knowingly (its tests can assert the list is empty)."""
    table = _DICTS.setdefault(lang, {})
    changed = sorted(k for k, v in mapping.items()
                     if k in table and table[k] != v)
    table.update(mapping)
    return changed


def package_translations(lang: str) -> dict[str, str]:
    """The translations this package ships for ``lang`` (a copy)."""
    return dict(_ES) if lang == "es" else {}
