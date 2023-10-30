import math

from diagram import Drawing, hsv

x0 = 50
y0 = 50

rounding = 2


def petal(dwg, theta0, color):
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
    dwg.add(
        dwg.polygon(
            points=[points1[0], points1[1], points2[1]],
            fill=hsv(h, s, v),
        )
    )
    for i in range(1, n - 1):
        dwg.add(
            dwg.polygon(
                points=[points1[i - 1], points1[i], points2[i - 1]],
                fill=hsv(h, s * (i / n), v),
            )
        )
        dwg.add(
            dwg.polygon(
                points=[points2[i - 1], points1[i], points2[i]],
                fill=hsv(h, s, v * (i / n)),
            )
        )
    dwg.add(
        dwg.polygon(
            points=[points1[-2], points1[-1], points2[-2]],
            fill=hsv(h, s, v),
        ),
    )


def circle(dwg, r):
    n = 25
    thetas = [i * 2 * math.pi / n for i in range(n)]
    points = [
        (
            round(x0 + r * math.cos(theta), rounding),
            round(y0 + r * math.sin(theta), rounding),
        )
        for theta in thetas
    ]
    dwg.add(dwg.polygon(points=points, fill="#ffffff"))


def draw():
    dwg = Drawing()
    dwg.viewbox(minx=0, miny=0, width=100, height=100)
    half_n = 5
    half_indices = range(half_n)
    indices = [i * 2 for i in half_indices] + [1 + i * 2 for i in half_indices]
    n = half_n * 2
    for i in indices:
        petal(dwg, (i / n) * 2 * math.pi, (i / n, 1, 1))
    circle(dwg, 5)
    return dwg
