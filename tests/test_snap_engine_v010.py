# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
OGR GUI 0.1.0 — the snap engine (``ogr_ui.canvas.snap_engine``) on its
own interface.

The invariant: **the cursor goes where the active constraints say, and
only there.** A vertex wins over a segment, a segment over the grid; ORTHO
locks the movement to the axis through the reference point; OSNAP draws
extension lines only at vertices near the cursor; and every tolerance and
spacing the Snap dialog edits moves what the engine returns (rule 7).

What changed on the way out of OGR Slip2D: the engine read the core's
``Boundary`` (``b.polyline.vertices``, ``b.polyline.closed``) and now reads
:class:`SnapShape`, whose vertices and segments are given separately, and
returns :class:`SnapPoint`. The tests of that interface are new here: a
closed polyline gives its closing segment; an arc traced by chords, with
only its end points as vertices, snaps LINE onto a chord and never VERTEX
onto the end of an interior chord; and the cursor and the reference are
anything with ``x`` and ``y``.

Ported from OGR Slip2D (v0.1.486):

* ``tests/test_snap_engine.py`` (v0.1.3, the engine's first tests): vertex,
  line and ortho behaviour, every test. ``TestNiceStep`` is left out:
  ``nice_step`` is ``ogr_core.numbers.nice_step``, which Slip2D's engine
  re-exported and this one, importing nothing of the core, does not.
* ``tests/test_m1_datatips_snap_v151.py`` (v0.1.51, phase M1): its snap
  parts that need no main window, i.e. that the settings the Snap dialog
  edits (grid spacing, the per-kind capture tolerances) reach the engine.
  Its status-bar and keyboard tests need Slip2D's main window and stay
  there; its data tips stayed in Slip2D with ``data_tips.py``.

``SnapSettings.ortho_snap_angle_deg`` has no test that it moves the result:
the engine never reads it (reported, rule 6).
"""
from __future__ import annotations

import math
from collections import namedtuple

from ogr_ui.canvas.snap_engine import (
    SnapEngine,
    SnapKind,
    SnapPoint,
    SnapResult,
    SnapSettings,
    SnapShape,
)

#: Anything with x and y: what a program's own vertex looks like.
_XY = namedtuple("_XY", "x y")


class _Vertex:
    """A program's vertex class, not a tuple at all."""

    def __init__(self, x, y):
        self.x, self.y = x, y


def _square(closed=True) -> SnapShape:
    return SnapShape.polyline(
        [_XY(0, 0), _XY(10, 0), _XY(10, 10), _XY(0, 10)], closed=closed)


def _arc_by_chords(radius=10.0, chords=8) -> SnapShape:
    """A quarter circle about the origin, from (r, 0) to (0, r), traced by
    ``chords`` chords; only its two ends are vertices."""
    pts = [SnapPoint(radius * math.cos(0.5 * math.pi * i / chords),
                     radius * math.sin(0.5 * math.pi * i / chords))
           for i in range(chords + 1)]
    segs = tuple((pts[i], pts[i + 1]) for i in range(chords))
    return SnapShape(vertices=(pts[0], pts[-1]), segments=segs)


# ======================================================================
# Ported from Slip2D tests/test_snap_engine.py
# ======================================================================
class TestVertexSnap:
    def test_snaps_to_nearby_vertex(self):
        eng = SnapEngine(SnapSettings(snap=True))
        # Cursor near vertex (0,0) — well within tolerance at ppu=50
        result = eng.resolve(_XY(0.15, 0.05), [_square()],
                             pixels_per_unit=50.0)
        assert result.kind == SnapKind.VERTEX
        assert result.point.x == 0.0
        assert result.point.y == 0.0

    def test_no_snap_when_disabled(self):
        eng = SnapEngine(SnapSettings(snap=False))
        result = eng.resolve(_XY(0.15, 0.05), [_square()],
                             pixels_per_unit=50.0)
        assert result.kind == SnapKind.NONE
        assert result.point.x == 0.15

    def test_does_not_snap_when_far_away(self):
        eng = SnapEngine(SnapSettings(snap=True))
        # At ppu=50, tolerance in world units ~ 12/50 = 0.24
        result = eng.resolve(_XY(5.0, 5.0), [_square()],
                             pixels_per_unit=50.0)
        assert result.kind != SnapKind.VERTEX

    def test_a_vertex_wins_over_the_segment_it_ends(self):
        """(0.15, 0.05) is also 0.05 from the bottom edge: the vertex has
        precedence, or nobody could ever pick a corner."""
        eng = SnapEngine(SnapSettings(snap=True))
        r = eng.resolve(_XY(0.15, 0.05), [_square()], pixels_per_unit=50.0)
        assert r.kind == SnapKind.VERTEX


class TestLineSnap:
    def test_snaps_to_nearest_point_on_segment(self):
        eng = SnapEngine(SnapSettings(snap=True))
        # Cursor at (5.0, 0.1) — close to the bottom edge y=0
        result = eng.resolve(_XY(5.0, 0.1), [_square()],
                             pixels_per_unit=50.0)
        assert result.kind == SnapKind.LINE
        assert abs(result.point.x - 5.0) < 1e-9
        assert abs(result.point.y - 0.0) < 1e-9

    def test_a_segment_wins_over_the_grid(self):
        """(5.05, 0.1) is 5.6 px from the grid node (5, 0) and 5 px from
        the bottom edge: the segment comes first, so the point is the
        projection (5.05, 0) and not the node."""
        eng = SnapEngine(SnapSettings(snap=True))
        no_shapes = eng.resolve(_XY(5.05, 0.1), [], pixels_per_unit=50.0)
        assert no_shapes.kind == SnapKind.GRID          # the node is in reach
        r = eng.resolve(_XY(5.05, 0.1), [_square()], pixels_per_unit=50.0)
        assert r.kind == SnapKind.LINE
        assert abs(r.point.x - 5.05) < 1e-9 and abs(r.point.y) < 1e-9


class TestOrtho:
    def test_ortho_locks_to_horizontal(self):
        eng = SnapEngine(SnapSettings(snap=False, ortho=True))
        eng.set_reference(_XY(0, 0))
        # Cursor at (5, 1) — horizontal component bigger → lock to y=0
        r = eng.resolve(_XY(5.0, 1.0), [], pixels_per_unit=50.0)
        assert abs(r.point.y) < 1e-9
        assert r.ortho_active
        assert r.kind == SnapKind.ORTHO_H

    def test_ortho_locks_to_vertical(self):
        eng = SnapEngine(SnapSettings(snap=False, ortho=True))
        eng.set_reference(_XY(0, 0))
        r = eng.resolve(_XY(1.0, 5.0), [], pixels_per_unit=50.0)
        assert abs(r.point.x) < 1e-9
        assert r.kind == SnapKind.ORTHO_V

    def test_ortho_without_reference_is_no_op(self):
        eng = SnapEngine(SnapSettings(snap=False, ortho=True))
        eng.set_reference(None)
        r = eng.resolve(_XY(5.0, 3.0), [], pixels_per_unit=50.0)
        assert abs(r.point.x - 5.0) < 1e-9
        assert abs(r.point.y - 3.0) < 1e-9
        assert r.kind == SnapKind.NONE

    def test_ortho_on_a_segment_lands_where_the_axis_crosses_it(self):
        """Drawing horizontally from (0, 5) towards the right edge, the
        point is where y = 5 meets x = 10, not the cursor's projection."""
        shapes = [_square()]
        free = SnapEngine(SnapSettings(snap=True))
        free.set_reference(_XY(0, 5))
        r = free.resolve(_XY(9.9, 5.3), shapes, pixels_per_unit=50.0)
        assert r.kind == SnapKind.LINE
        assert abs(r.point.x - 10.0) < 1e-9
        assert abs(r.point.y - 5.3) < 1e-9
        locked = SnapEngine(SnapSettings(snap=True, ortho=True))
        locked.set_reference(_XY(0, 5))
        r = locked.resolve(_XY(9.9, 5.3), shapes, pixels_per_unit=50.0)
        assert r.kind == SnapKind.LINE and r.ortho_active
        assert abs(r.point.x - 10.0) < 1e-9
        assert abs(r.point.y - 5.0) < 1e-9


class TestOsnap:
    def test_extension_lines_only_with_osnap(self):
        shapes = [_square()]
        off = SnapEngine(SnapSettings(snap=True, osnap=False))
        on = SnapEngine(SnapSettings(snap=True, osnap=True))
        cursor = _XY(0.3, 0.3)
        assert off.resolve(cursor, shapes, 50.0).extension_lines == []
        lines = on.resolve(cursor, shapes, 50.0).extension_lines
        # one horizontal and one vertical line through (0, 0)
        assert len(lines) == 2
        for a, b in lines:
            assert (a.y == b.y == 0.0) or (a.x == b.x == 0.0)

    def test_snaps_onto_an_extension_line(self):
        """Lined up with a corner, away from every edge and grid node."""
        point = SnapShape.polyline([_XY(0, 0)])
        eng = SnapEngine(SnapSettings(snap=True, osnap=True,
                                      extension_tolerance_px=10.0))
        r = eng.resolve(_XY(0.5, 0.05), [point], pixels_per_unit=50.0)
        assert r.kind == SnapKind.EXTENSION
        assert abs(r.point.x - 0.5) < 1e-9 and abs(r.point.y) < 1e-9


# ======================================================================
# The settings the Snap dialog edits move the result (rule 7; Slip2D
# tests/test_m1_datatips_snap_v151.py made them reachable)
# ======================================================================
class TestEverySettingMovesTheResult:
    def test_vertex_tolerance(self):
        # 0.2 from the corner at 50 px/unit is 10 px
        cursor = _XY(0.2, 0.0)
        wide = SnapEngine(SnapSettings(vertex_tolerance_px=12.0))
        narrow = SnapEngine(SnapSettings(vertex_tolerance_px=8.0))
        assert wide.resolve(cursor, [_square()], 50.0).kind == \
            SnapKind.VERTEX
        assert narrow.resolve(cursor, [_square()], 50.0).kind != \
            SnapKind.VERTEX

    def test_line_tolerance(self):
        # 0.15 from the bottom edge is 7.5 px; no grid node within 8 px
        cursor = _XY(5.5, 0.15)
        wide = SnapEngine(SnapSettings(line_tolerance_px=10.0))
        narrow = SnapEngine(SnapSettings(line_tolerance_px=5.0))
        assert wide.resolve(cursor, [_square()], 50.0).kind == SnapKind.LINE
        assert narrow.resolve(cursor, [_square()], 50.0).kind == \
            SnapKind.NONE

    def test_grid_tolerance(self):
        # 0.1414 from (5, 5) is 7.07 px
        cursor = _XY(5.1, 5.1)
        wide = SnapEngine(SnapSettings(grid_tolerance_px=8.0))
        narrow = SnapEngine(SnapSettings(grid_tolerance_px=5.0))
        r = wide.resolve(cursor, [], 50.0)
        assert r.kind == SnapKind.GRID and r.point == SnapPoint(5.0, 5.0)
        assert narrow.resolve(cursor, [], 50.0).kind == SnapKind.NONE

    def test_extension_tolerance(self):
        # the corner is 0.50 away: extensions are built within three
        # times the tolerance, 0.48 at 8 px and 0.60 at 10 px
        point = SnapShape.polyline([_XY(0, 0)])
        cursor = _XY(0.5, 0.05)
        narrow = SnapEngine(SnapSettings(osnap=True,
                                         extension_tolerance_px=8.0))
        wide = SnapEngine(SnapSettings(osnap=True,
                                       extension_tolerance_px=10.0))
        r = narrow.resolve(cursor, [point], 50.0)
        assert r.kind == SnapKind.NONE and r.extension_lines == []
        assert wide.resolve(cursor, [point], 50.0).kind == \
            SnapKind.EXTENSION

    def test_horizontal_grid_spacing(self):
        cursor = _XY(7.52, 0.02)
        r = SnapEngine(SnapSettings(grid_h=2.5)).resolve(cursor, [], 50.0)
        assert r.kind == SnapKind.GRID
        assert abs(r.point.x - 7.5) < 1e-9 and abs(r.point.y) < 1e-9
        r = SnapEngine(SnapSettings(grid_h=1.0)).resolve(cursor, [], 50.0)
        assert r.kind == SnapKind.NONE

    def test_vertical_grid_spacing(self):
        cursor = _XY(0.02, 7.52)
        r = SnapEngine(SnapSettings(grid_v=2.5)).resolve(cursor, [], 50.0)
        assert r.kind == SnapKind.GRID
        assert abs(r.point.y - 7.5) < 1e-9 and abs(r.point.x) < 1e-9
        r = SnapEngine(SnapSettings(grid_v=1.0)).resolve(cursor, [], 50.0)
        assert r.kind == SnapKind.NONE

    def test_tolerances_are_pixels_at_any_zoom(self):
        """The same 10 px snaps at every scale: the canvas divides by the
        pixels per unit, so zooming out does not make snapping harder."""
        for ppu in (5.0, 50.0, 500.0, 5000.0):
            cursor = _XY(5.5, 8.0 / ppu)          # 8 px off the bottom edge
            r = SnapEngine(SnapSettings()).resolve(cursor, [_square()], ppu)
            assert r.kind == SnapKind.LINE, ppu

    def test_the_settings_object_is_read_live(self):
        """The dialog edits the engine's settings in place, so a change
        must take effect without a new engine."""
        s = SnapSettings(grid_tolerance_px=8.0)
        eng = SnapEngine(s)
        assert eng.resolve(_XY(5.1, 5.1), [], 50.0).kind == SnapKind.GRID
        s.grid_tolerance_px = 5.0
        assert eng.resolve(_XY(5.1, 5.1), [], 50.0).kind == SnapKind.NONE


# ======================================================================
# The new interface (OGR GUI 0.1.0)
# ======================================================================
class TestSnapShapePolyline:
    def test_a_closed_polyline_gives_the_closing_segment(self):
        shape = _square(closed=True)
        assert len(shape.vertices) == 4
        assert len(shape.segments) == 4
        assert shape.segments[-1] == (SnapPoint(0, 10), SnapPoint(0, 0))

    def test_an_open_one_does_not(self):
        shape = _square(closed=False)
        assert len(shape.segments) == 3
        assert (SnapPoint(0, 10), SnapPoint(0, 0)) not in shape.segments

    def test_the_closing_segment_is_snapped_to(self):
        """(0.1, 5.5) is only near the left edge, the one closing adds."""
        cursor = _XY(0.1, 5.5)
        eng = SnapEngine(SnapSettings())
        r = eng.resolve(cursor, [_square(closed=True)], 50.0)
        assert r.kind == SnapKind.LINE
        assert abs(r.point.x) < 1e-9 and abs(r.point.y - 5.5) < 1e-9
        assert eng.resolve(cursor, [_square(closed=False)], 50.0).kind == \
            SnapKind.NONE

    def test_segments_join_consecutive_points(self):
        shape = SnapShape.polyline([_XY(0, 0), _XY(3, 4), _XY(6, 0)])
        assert shape.segments == ((SnapPoint(0, 0), SnapPoint(3, 4)),
                                  (SnapPoint(3, 4), SnapPoint(6, 0)))

    def test_fewer_than_two_points_have_no_segments(self):
        assert SnapShape.polyline([]).segments == ()
        one = SnapShape.polyline([_XY(2, 3)], closed=True)
        assert one.vertices == (SnapPoint(2.0, 3.0),)
        assert one.segments == ()

    def test_points_of_any_class_become_snap_points(self):
        shape = SnapShape.polyline([_Vertex(1, 2), _Vertex(3, 4)])
        for v in shape.vertices:
            assert type(v) is SnapPoint
            assert isinstance(v.x, float) and isinstance(v.y, float)
        assert shape.vertices == (SnapPoint(1.0, 2.0), SnapPoint(3.0, 4.0))

    def test_an_empty_shape_snaps_to_nothing(self):
        r = SnapEngine(SnapSettings(grid_tolerance_px=1.0)).resolve(
            _XY(0.4, 0.4), [SnapShape()], 50.0)
        assert r.kind == SnapKind.NONE


class TestAnArcTracedByChords:
    def test_a_point_near_a_chord_snaps_line_onto_the_chord(self):
        arc = _arc_by_chords()
        a, b = arc.segments[3]
        mid = SnapPoint((a.x + b.x) / 2, (a.y + b.y) / 2)
        # just outside the chord, towards the arc
        n = math.hypot(mid.x, mid.y)
        cursor = _XY(mid.x * (1 + 0.01 / n), mid.y * (1 + 0.01 / n))
        r = SnapEngine(SnapSettings()).resolve(cursor, [arc], 50.0)
        assert r.kind == SnapKind.LINE
        assert abs(r.point.x - mid.x) < 1e-9
        assert abs(r.point.y - mid.y) < 1e-9

    def test_the_end_of_an_interior_chord_is_not_a_vertex(self):
        arc = _arc_by_chords()
        joint = arc.segments[3][1]                  # at 45°
        cursor = _XY(joint.x + 0.03, joint.y + 0.03)
        r = SnapEngine(SnapSettings()).resolve(cursor, [arc], 50.0)
        assert r.kind == SnapKind.LINE              # not VERTEX
        assert abs(r.point.x - joint.x) < 1e-9
        assert abs(r.point.y - joint.y) < 1e-9

    def test_the_ends_of_the_arc_are_vertices(self):
        arc = _arc_by_chords()
        for end in (arc.vertices[0], arc.vertices[-1]):
            cursor = _XY(end.x + 0.05, end.y + 0.05)
            r = SnapEngine(SnapSettings()).resolve(cursor, [arc], 50.0)
            assert r.kind == SnapKind.VERTEX
            assert r.point == end

    def test_no_extension_lines_at_an_interior_chord_end(self):
        arc = _arc_by_chords()
        joint = arc.segments[3][1]
        eng = SnapEngine(SnapSettings(osnap=True))
        r = eng.resolve(_XY(joint.x + 0.03, joint.y + 0.03), [arc], 50.0)
        assert r.extension_lines == []


class TestAnythingWithXAndY:
    def test_the_cursor(self):
        eng = SnapEngine(SnapSettings())
        for cursor in (_XY(0.15, 0.05), _Vertex(0.15, 0.05),
                       SnapPoint(0.15, 0.05)):
            r = eng.resolve(cursor, [_square()], 50.0)
            assert r.kind == SnapKind.VERTEX
            assert r.point == SnapPoint(0.0, 0.0)

    def test_the_reference(self):
        eng = SnapEngine(SnapSettings(snap=False, ortho=True))
        eng.set_reference(_Vertex(2, 7))
        assert type(eng.reference) is SnapPoint
        assert eng.reference == SnapPoint(2.0, 7.0)
        r = eng.resolve(_Vertex(9.0, 8.0), [], 50.0)
        assert r.point == SnapPoint(9.0, 7.0)

    def test_the_point_returned_is_always_a_snap_point(self):
        """Whatever came in, and whichever rule decided."""
        eng = SnapEngine(SnapSettings(snap=False))
        r = eng.resolve(_Vertex(1, 2), [], 50.0)
        assert isinstance(r, SnapResult)
        assert type(r.point) is SnapPoint
        assert r.point == SnapPoint(1.0, 2.0)
        assert isinstance(r.point.x, float)

    def test_shapes_may_be_a_generator(self):
        """The engine looks at the shapes more than once (vertices, then
        segments): a generator must not be spent by the first look."""
        shapes = (s for s in [_square()])
        r = SnapEngine(SnapSettings()).resolve(_XY(5.0, 0.1), shapes, 50.0)
        assert r.kind == SnapKind.LINE
