import random
from itertools import pairwise
from math import cos, sin, tau

import drawsvg as dw
import networkx as nx

from diagram import normalize, rot90


def hamiltonian(nodes, other, *, seed):
    red_orange = "#FE4A49"

    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(other)
    graph.add_edges_from(pairwise(nodes), color=red_orange)
    graph.add_edge(nodes[-1], nodes[0], color=red_orange)
    pos = nx.spring_layout(graph, scale=150, center=[200, 200], seed=seed)

    d = dw.Drawing(400, 400)

    for u, v, data in graph.edges.data():
        color = data.get("color", "black")

        a = pos[u]
        b = pos[v]
        d.append(dw.Line(*a, *b, stroke=color))

        t = normalize(b - a)
        n = rot90(t)
        m = (a + b) / 2
        x = 6
        y = 4
        d.append(
            dw.Lines(
                *(m - x * t + y * n), *(m + x * t), *(m - x * t - y * n), fill=color
            )
        )

    random.seed(seed)

    for v, [x, y] in pos.items():
        fill = red_orange if v == nodes[0] else "black"
        d.append(dw.Circle(x, y, 5, fill=fill))

        theta = random.uniform(0, tau)
        r = 15
        d.append(
            dw.Text(
                v,
                "18px",
                x + r * cos(theta),
                y - r * sin(theta),
                center=True,
                font_family="serif",
                fill=fill,
                stroke="white",
                stroke_width=4,
                paint_order="stroke",
            )
        )

    return d


def draw():
    return hamiltonian(
        ["a", "b", "c", "d", "e", "f", "g"],
        [
            ("a", "d"),
            ("b", "e"),
            ("b", "f"),
            ("c", "g"),
            ("d", "f"),
        ],
        seed=17,
    )
