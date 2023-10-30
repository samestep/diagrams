import colorsys
import math

import drawsvg as dw


def flatten(l):
    return [x for r in l for x in r]


def hsv(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def draw():
    d = dw.Drawing(100, 100)

    x0 = 50
    y0 = 50

    rounding = 2

    def petal(theta0, color):
        h, s, v = color
        n = 25
        points1 = []
        points2 = []
        for i in range(n):
            frac = i / (n - 1)
            r = frac * 50
            theta1 = theta0 - 0.4 * (math.sin(frac * math.pi) + 1)
            theta2 = theta0 + 0.4 * (math.cos(frac * math.pi))
            points1.append(
                (
                    round(x0 + r * math.cos(theta1), rounding),
                    round(y0 + r * math.sin(theta1), rounding),
                )
            )
            points2.append(
                (
                    round(x0 + r * math.cos(theta2), rounding),
                    round(y0 + r * math.sin(theta2), rounding),
                )
            )
        d.append(
            dw.Lines(
                *flatten([points1[0], points1[1], points2[1]]),
                close=True,
                fill=hsv(h, s, v),
            )
        )
        for i in range(1, n - 1):
            d.append(
                dw.Lines(
                    *flatten([points1[i - 1], points1[i], points2[i - 1]]),
                    close=True,
                    fill=hsv(h, s * (i / n), v),
                )
            )
            d.append(
                dw.Lines(
                    *flatten([points2[i - 1], points1[i], points2[i]]),
                    close=True,
                    fill=hsv(h, s, v * (i / n)),
                )
            )
        d.append(
            dw.Lines(
                *flatten([points1[-2], points1[-1], points2[-2]]),
                close=True,
                fill=hsv(h, s, v),
            ),
        )

    def circle(r):
        n = 25
        thetas = [i * 2 * math.pi / n for i in range(n)]
        points = [
            (
                round(x0 + r * math.cos(theta), rounding),
                round(y0 + r * math.sin(theta), rounding),
            )
            for theta in thetas
        ]
        d.append(dw.Lines(*flatten(points), close=True, fill="#ffffff"))

    half_n = 5
    half_indices = range(half_n)
    indices = [i * 2 for i in half_indices] + [1 + i * 2 for i in half_indices]
    n = half_n * 2
    for i in indices:
        petal((i / n) * 2 * math.pi, (i / n, 1, 1))
    circle(5)
    return d
