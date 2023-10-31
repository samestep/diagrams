import random
from dataclasses import dataclass
from math import cos, radians, sin, sqrt

import drawsvg as dw
import numpy as np
from numpy.linalg import norm

from diagram import normalize, rgb, vec2, vec3


@dataclass(kw_only=True)
class Molecule:
    name: str
    formula: str
    atoms: list[tuple[str, np.ndarray]]
    single: list[tuple[int, int]]
    double: list[tuple[int, int]]


def reaction(*, title: str, reactants: list[Molecule], products: list[Molecule], seed):
    width = 1248
    height = 702
    d = dw.Drawing(width, height)

    gray = rgb(0.5, 0.5, 0.5)
    turquoise = rgb(0.1, 0.7, 0.6)

    atom_colors = {"H": gray, "C": "black", "O": "red"}

    atom_radius = 25
    bond_length = 80

    atom_radii = {"H": 0.75 * atom_radius, "C": atom_radius, "O": atom_radius}

    font_family = (
        "Palatino, Palatino Linotype, Palatino LT STD, Book Antiqua, Georgia, serif"
    )

    d.append(
        dw.Rectangle(0, 0, width, height, fill="none", stroke=gray, stroke_width=8)
    )

    reaction_box_size = 0.75 * width / 2
    reaction_box_top = height / 2 - reaction_box_size / 2
    reaction_box_bottom = height / 2 + reaction_box_size / 2

    reactant_center = width / 4
    d.append(
        dw.Rectangle(
            reactant_center - reaction_box_size / 2,
            reaction_box_top,
            reaction_box_size,
            reaction_box_size,
            fill_opacity=0.1,
            rx=20,
        )
    )
    d.append(
        dw.Text(
            "reactants",
            "30px",
            reactant_center,
            reaction_box_bottom + 24,
            center=True,
            font_family=font_family,
            font_weight="bold",
        )
    )

    product_center = width * 3 / 4
    d.append(
        dw.Rectangle(
            product_center - reaction_box_size / 2,
            reaction_box_top,
            reaction_box_size,
            reaction_box_size,
            fill_opacity=0.1,
            rx=20,
        )
    )
    d.append(
        dw.Text(
            "products",
            "30px",
            product_center,
            reaction_box_bottom + 24,
            center=True,
            font_family=font_family,
            font_weight="bold",
        )
    )

    random.seed(seed)

    labels = dw.Group()

    def molecule(mol: Molecule, center):
        labels.append(
            dw.Text(
                f"{mol.name} ({mol.formula})",
                "22.5px",
                x,
                y + atom_radius,
                center=True,
                font_family=font_family,
            )
        )
        for a, loc in mol.atoms:
            d.append(
                dw.Circle(
                    *(center + vec2(loc[0], loc[1]) * bond_length),
                    atom_radii[a],
                    fill="white",
                    stroke=atom_colors[a],
                    stroke_width=3,
                )
            )
        for i, j in mol.single + mol.double:
            a, p = mol.atoms[i]
            b, q = mol.atoms[j]
            v = q - p
            t = normalize(v)
            s = p * bond_length + t * atom_radii[a]
            e = q * bond_length - t * atom_radii[b]
            d.append(
                dw.Line(
                    *(center + vec2(s[0], s[1])),
                    *(center + vec2(e[0], e[1])),
                    stroke=turquoise,
                    stroke_width=10,
                    stroke_linecap="round",
                )
            )
            d.append(
                dw.Line(
                    *(center + vec2(s[0], s[1])),
                    *(center + vec2(e[0], e[1])),
                    stroke="white",
                    stroke_width=4,
                    stroke_linecap="round",
                )
            )

    for mol in reactants:
        x = random.uniform(
            reactant_center - reaction_box_size / 2,
            reactant_center + reaction_box_size / 2,
        )
        y = random.uniform(reaction_box_top, reaction_box_bottom)
        molecule(mol, vec2(x, y))

    for mol in products:
        x = random.uniform(
            product_center - reaction_box_size / 2,
            product_center + reaction_box_size / 2,
        )
        y = random.uniform(reaction_box_top, reaction_box_bottom)
        molecule(mol, vec2(x, y))

    d.append(labels)

    d.append(
        dw.Text(
            title,
            "50px",
            width / 2,
            reaction_box_top / 2,
            center=True,
            font_family=font_family,
            font_variant="small-caps",
        )
    )

    Rc = reactant_center
    Pc = product_center
    s = reaction_box_size
    p = 10
    d.append(
        dw.Line(
            Rc + (0.5 * s) + p,
            height / 2,
            Pc - (0.5 * s) - p,
            height / 2,
            stroke="black",
            stroke_width=5,
        )
    )

    return d


def o2():
    return Molecule(
        name="oxygen",
        formula="O₂",
        atoms=[("O", vec3(0, 0, 0)), ("O", vec3(1, 0, 0))],
        single=[],
        double=[(0, 1)],
    )


def co2():
    return Molecule(
        name="carbon dioxide",
        formula="CO₂",
        atoms=[("C", vec3(0, 0, 0)), ("O", vec3(-1, 0, 0)), ("O", vec3(1, 0, 0))],
        single=[],
        double=[(0, 1), (0, 2)],
    )


def h2o():
    theta = radians(104.5)
    return Molecule(
        name="water",
        formula="H₂O",
        atoms=[
            ("O", vec3(0, 0, 0)),
            ("H", vec3(1, 0, 0)),
            ("H", vec3(cos(theta), sin(theta), 0)),
        ],
        single=[(0, 1), (0, 2)],
        double=[],
    )


def ch4():
    r = 1 / sqrt(3)
    return Molecule(
        name="methane",
        formula="CH₄",
        atoms=[
            ("C", vec3(0, 0, 0)),
            ("H", vec3(-r, r, r)),
            ("H", vec3(r, -r, r)),
            ("H", vec3(r, r, -r)),
            ("H", vec3(-r, -r, -r)),
        ],
        single=[(0, 1), (0, 2), (0, 3), (0, 4)],
        double=[],
    )


def draw():
    return reaction(
        title="Methane Combustion Reaction",
        reactants=[ch4(), o2(), o2()],
        products=[co2(), h2o(), h2o()],
        seed=0,
    )
