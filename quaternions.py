from typing import Any, Callable

import drawsvg as dw
from sympy import Quaternion

from diagram import rgb


def cayley_table(group, *, texify: Callable[[Any], str]):
    d = dw.Drawing(220, 220)

    def equation(g, x, y, **kwargs):
        s = texify(g)
        d.append(
            dw.Text(
                s,
                "8px",
                x,
                y,
                center=True,
                font_family="serif",
                font_style=None if s and s[-1].isdigit() else "italic",
                **kwargs,
            )
        )

    dark_gray = rgb(0.4, 0.4, 0.4)

    table_width = 180
    table_height = 180

    box_padding = 2

    n = len(group)
    w = table_width / n
    h = table_height / n

    box_colors = {}
    label_colors = {}

    for m, g in enumerate(group):
        t = 0.1 + 0.8 * (1 - (m + 1) / n)
        s = max(0, min(1, t))
        red = 1 - (1 - max(0, min(1, 3 * t))) ** 2
        green = 3 * s * s - 2 * s * s * s
        blue = max(0, min(1, 3 * t - 2))
        box_colors[g] = rgb(red, green, blue)
        label_colors[g] = rgb(0.75 * red, 0.75 * green, 0.75 * blue)

        u = (m + 1.5) * w
        v = (m + 1.5) * h
        equation(g, w / 2, v, fill=dark_gray)
        equation(g, u, h / 2, fill=dark_gray)

    for x, b in enumerate(group):
        for y, c in enumerate(group):
            a = b * c

            box = box_colors.get(a)
            if box is not None:
                d.append(
                    dw.Rectangle(
                        (x + 1) * w + box_padding / 2,
                        (y + 1) * h + box_padding / 2,
                        w - box_padding,
                        h - box_padding,
                        rx=2,
                        fill=box,
                        fill_opacity=0.75,
                    )
                )

            label = label_colors.get(a)
            if label is not None:
                equation(a, (x + 1.5) * w, (y + 1.5) * h, fill=label)

    return d


def single(x, v):
    if v:
        if x == 1:
            return v
        elif x == -1:
            return f"−{v}"
    return f"−{-x}{v}" if x < 0 else f"{x}{v}"


def short(g):
    l = [
        single(x, v)
        for x, v in [(g.a, ""), (g.b, "i"), (g.c, "j"), (g.d, "k")]
        if x != 0
    ]
    if len(l) != 1:
        raise ValueError(f"Expected 1 non-zero term, got {len(l)}")
    return "".join(l)


def draw():
    one = Quaternion(1)
    i = Quaternion(0, 1)
    j = Quaternion(0, 0, 1)
    k = Quaternion(0, 0, 0, 1)
    return cayley_table([one, i, j, k, -one, -i, -j, -k], texify=short)
