from math import cos, pi, sin, tau

import drawsvg as dw

from diagram import normalize, vec2


def penrose(
    path: dw.Path,
    *,
    center,
    radius=50,
    hole_size=0.35,
    angle=0,
    n_sides=5,
    chirality="ccw",
):
    n = n_sides
    assert isinstance(n, int) and n >= 3
    R = radius  # shorthand for outer radius
    r = hole_size * R  # inner radius
    alpha = pi * (n - 2) / n  # interior angle of regular n-gon
    w = (R - r) / (4 * cos(alpha / 2))  # half-width
    s = 1 if chirality == "cw" else -1

    # inner and outer polygons
    a = []
    b = []
    for k in range(n):
        theta = angle + (k * tau) / n
        p = vec2(s * sin(theta), -cos(theta))
        a.append(center + r * p)
        b.append(center + R * p)

    # unit edge vectors
    u = []
    for i in range(n):
        j = (i + 1) % n
        u.append(normalize(a[j] - a[i]))

    # inner and outer midpoints
    c = []
    d = []
    for i in range(n):
        l = (i - 1 + n) % n
        c.append(a[i] - w * u[i])
        d.append(b[i] - w * u[l])

    # add polygons to path
    for i in range(n):
        j = (i + 1) % n
        k = (i + 2) % n

        path.M(*d[i])
        path.L(*b[i])
        path.L(*d[j])
        path.L(*c[k])
        path.L(*a[k])
        path.L(*c[j])
        path.Z()

    return path


def draw():
    width = 1920
    height = 1080
    d = dw.Drawing(width, height)

    background = dw.RadialGradient(cx=960, cy=540, r=1352.8455844)
    background.add_stop(0.1477348, "gray")
    background.add_stop(0.8133731, "#262626")
    d.append(dw.Rectangle(0, 0, width, height, fill=background))

    mask = dw.ClipPath()
    glows = dw.Group(clip_path=mask)

    for j in range(3):
        for i in range(4):
            n = max(3, 1 + j * 4 + i)
            center = vec2(width / 2 + 400 * (i - 1.5), height / 2 - 350 * (j - 1))

            d.append(
                penrose(
                    dw.Path(
                        fill="none",
                        stroke="#888",
                        stroke_width=5,
                        stroke_linejoin="round",
                    ),
                    center=center,
                    radius=150,
                    hole_size=0.5,
                    n_sides=n,
                )
            )

            glows.append(
                penrose(
                    dw.Path(
                        fill="none",
                        stroke="#fffb",
                        stroke_width=5,
                        style="filter:blur(10px);",
                    ),
                    center=center,
                    radius=150,
                    hole_size=0.5,
                    n_sides=n,
                )
            )

    c = vec2(width / 2, height / 2 - 60)
    R = 350

    logo = lambda: penrose(
        dw.Path(fill="#3fb4f7bb", stroke="#555", stroke_width=6),
        center=c,
        radius=R,
    )

    icon = dw.Group(style="filter: drop-shadow(0px 50px 20px #0008);")
    icon.append(logo())
    icon.append(
        dw.Text(
            "Penrose",
            "172px",
            *(c + vec2(0, R + 25)),
            center=True,
            font_family="HelveticaNeue-CondensedBold,Helvetica,Arial,Geneva,Tahoma,sans-serif",
            fill="#fff",
            stroke="#555",
            stroke_width=12,
            paint_order="stroke",
        )
    )
    d.append(icon)

    mask.append(logo())
    d.append(glows)

    return d
