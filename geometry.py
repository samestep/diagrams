import math
import random

import drawsvg as dw
import numpy as np

from diagram import normalize, rgb, rot90

Point = str
Segment = frozenset[Point]  # must have exactly two points
Angle = tuple[Point, Segment]  # vertex, then the other two points
Triangle = frozenset[Point]  # must have exactly three points


class Geometry:
    points: dict[Point, None]
    segments: set[Segment]
    midpoints: dict[Point, Segment]
    angles: set[Angle]
    triangles: set[Triangle]
    bisectors: set[Angle]
    perpendicular_bisectors: set[Segment]

    def __init__(self):
        self.points = {}
        self.segments = set()
        self.midpoints = {}
        self.angles = set()
        self.triangles = set()
        self.bisectors = set()
        self.perpendicular_bisectors = set()

    def point(self, p) -> Point:
        self.points[p] = None
        return p

    def segment(self, p, q) -> Segment:
        a = frozenset([p, q])
        self.segments.add(a)
        return a

    def midpoint(self, a, p) -> Point:
        self.points[p] = None
        self.midpoints[p] = a
        return p

    def angle(self, p, q, r) -> Angle:
        theta = (q, frozenset([p, r]))
        self.angles.add(theta)
        return theta

    def triangle(self, p, q, r) -> Triangle:
        t = frozenset([p, q, r])
        self.triangles.add(t)
        return t

    def bisector(self, theta) -> Angle:
        self.bisectors.add(theta)
        return theta

    def perpendicular_bisector(self, a) -> Segment:
        self.perpendicular_bisectors.add(a)
        return a


def euclidean(g: Geometry, *, seed):
    canvas = 800
    d = dw.Drawing(canvas, canvas)

    darkpurple = "#8c90c1"
    purple2 = rgb(0.106, 0.122, 0.54)

    stroke_width = 1.75
    text_padding = 25
    text_padding_2 = 40
    font_size = "35px"
    ray_length = 100
    point_radius = 4
    theta_radius = 30

    dim = 700
    gap = (canvas - dim) / 2
    d.append(
        dw.Rectangle(
            gap, gap, dim, dim, fill="#f3f4f9", stroke="#8e93c4", stroke_width=2
        )
    )
    d.append(
        dw.Text(
            "𝐄²",
            font_size,
            (canvas - gap) - text_padding_2,
            gap + text_padding_2,
            center=True,
            font_family="serif",
        )
    )

    random.seed(seed)
    rand = lambda: random.uniform(gap, canvas - gap)
    pos = {p: np.array([rand(), rand()]) for p in g.points.keys()}
    for p, (q, r) in g.midpoints.items():
        pos[p] = (pos[q] + pos[r]) / 2

    for p, q, r in g.triangles:
        d.append(
            dw.Lines(
                *pos[p],
                *pos[q],
                *pos[r],
                fill=purple2,
                fill_opacity=0.2,
            )
        )

    for theta in g.angles:
        q, (p, r) = theta
        c = pos[q]
        a = normalize(pos[p] - c)
        b = normalize(pos[r] - c)
        x, y = c + a * theta_radius
        ex, ey = c + b * theta_radius

        path = dw.Path(fill="none", stroke_width=2, stroke=darkpurple)
        path.M(x, y)
        path.A(
            rx=theta_radius,
            ry=theta_radius,
            rot=0,
            large_arc=False,
            sweep=np.cross(a, b) > 0,
            ex=ex,
            ey=ey,
        )
        d.append(path)

        if theta in g.bisectors:
            d.append(
                dw.Line(
                    *c,
                    *(c + normalize(a + b) * ray_length),
                    stroke_width=stroke_width,
                    stroke=darkpurple,
                )
            )

    for p, q in g.perpendicular_bisectors:
        s = pos[p]
        v = pos[q] - s
        m = s + v / 2
        t = normalize(v)
        n = rot90(t)

        mark_size = 10
        u = t * mark_size
        if random.choice([n[1], -n[1]]) < 0:
            n = -n
            u = -u

        d.append(
            dw.Lines(
                *(m + n * mark_size),
                *(m + n * mark_size + u),
                *(m + u),
                fill="none",
                stroke_width=2,
                stroke="black",
            )
        )

        d.append(
            dw.Line(
                *m, *(m + n * ray_length), stroke=darkpurple, stroke_width=stroke_width
            )
        )

    for p, q in g.segments:
        d.append(dw.Line(*pos[p], *pos[q], stroke="black", stroke_width=stroke_width))

    for p, (x, y) in pos.items():
        if p in g.midpoints:
            d.append(dw.Circle(x, y, point_radius, fill="white", stroke="black"))
        else:
            d.append(dw.Circle(x, y, point_radius))

        theta = random.uniform(0, math.tau)
        r = text_padding
        d.append(
            dw.Text(
                p,
                font_size,
                x + r * math.cos(theta),
                y - r * math.sin(theta),
                center=True,
                font_family="serif",
                font_style="italic",
            )
        )

    return d


def draw():
    g = Geometry()
    p = g.point("p")
    q = g.point("q")
    r = g.point("r")
    s = g.point("s")
    a = g.segment(p, q)
    g.segment(p, r)
    g.midpoint(a, "m")
    theta = g.angle(q, p, r)
    g.triangle(p, r, s)
    g.bisector(theta)
    g.perpendicular_bisector(a)
    return euclidean(g, seed=63)
