import drawsvg as dw
from sympy import Quaternion

from diagram import rgb


def cayley_table(G, *, texify):
    d = dw.Drawing(220, 220)

    dark_gray = rgb(0.4, 0.4, 0.4)

    table_width = 180
    table_height = 180

    box_padding = 2

    n = len(G)
    w = table_width / n
    h = table_height / n

    box_colors = {}
    label_colors = {}

    for m, g in enumerate(G):
        t = 0.1 + 0.8 * (1 - (m + 1) / n)
        s = max(0, min(1, t))
        red = 1 - (1 - max(0, min(1, 3 * t))) ** 2
        green = 3 * s * s - 2 * s * s * s
        blue = max(0, min(1, 3 * t - 2))
        box_colors[g] = rgb(red, green, blue)
        label_colors[g] = rgb(0.75 * red, 0.75 * green, 0.75 * blue)

        u = (m + 1.5) * w
        v = (m + 1.5) * h
        d.append(dw.Text(texify(g), "8px", w / 2, v, center=True, fill=dark_gray))
        d.append(dw.Text(texify(g), "8px", u, h / 2, center=True, fill=dark_gray))

    for x, b in enumerate(G):
        for y, c in enumerate(G):
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
                d.append(
                    dw.Text(
                        texify(a),
                        "8px",
                        (x + 1.5) * w,
                        (y + 1.5) * h,
                        center=True,
                        fill=label,
                    )
                )

    return d


def single(x, v):
    if v:
        return v if x == 1 else f"-{v}" if x == -1 else f"{x}{v}"
    else:
        return str(x)


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
