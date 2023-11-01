import random
from dataclasses import dataclass
from math import cos, radians, sin, sqrt, tau

import drawsvg as dw
from numpy import cross, dot
from numpy.linalg import norm

from diagram import Vec3, normalize, rgb, rot90, vec2, vec3


# https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation
@dataclass(kw_only=True)
class Rotation:
    e: Vec3
    theta: float

    def rotate(self, v: Vec3) -> Vec3:
        return (
            cos(self.theta) * v
            + sin(self.theta) * cross(self.e, v)
            + (1 - cos(self.theta)) * dot(self.e, v) * self.e
        )


def random_rotation() -> Rotation:
    def random_in_cube():
        return vec3(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))

    v = random_in_cube()
    while norm(v) > 1:
        v = random_in_cube()

    return Rotation(e=normalize(v), theta=random.uniform(0, tau))


@dataclass(kw_only=True)
class Molecule:
    name: str
    formula: str
    atoms: list[tuple[str, Vec3]]
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

    random.seed(seed)

    shadows = dw.Group()
    molecules = dw.Group()
    labels = dw.Group()

    def molecule(mol: Molecule, center):
        count = len(mol.atoms)

        rotation = random_rotation()
        locs = [rotation.rotate(v) for _, v in mol.atoms]
        order = sorted(range(count), key=lambda i: locs[i][2])
        single = [[] for _ in range(count)]
        double = [[] for _ in range(count)]

        for i, j in mol.single:
            single[i].append(j)
            single[j].append(i)

        for i, j in mol.double:
            double[i].append(j)
            double[j].append(i)

        done = [False for _ in range(count)]

        for i in order:
            a, _ = mol.atoms[i]
            p = locs[i]

            shadows.append(
                dw.Ellipse(
                    *(center + vec2(p[0], p[2] / 2 + 1.5) * bond_length),
                    2 * atom_radii[a],
                    atom_radii[a],
                    fill=rgb(0.95, 0.95, 0.95),
                    stroke="none",
                )
            )

            molecules.append(
                dw.Circle(
                    *(center + vec2(p[0], p[1]) * bond_length),
                    atom_radii[a],
                    fill="white",
                    stroke=atom_colors[a],
                    stroke_width=3,
                )
            )

            for j in single[i]:
                if done[j]:
                    continue

                b, _ = mol.atoms[j]
                q = locs[j]

                v = q - p
                t = normalize(v)

                s = p * bond_length + t * atom_radii[a]
                e = q * bond_length - t * atom_radii[b]

                molecules.append(
                    dw.Line(
                        *(center + vec2(s[0], s[1])),
                        *(center + vec2(e[0], e[1])),
                        stroke=turquoise,
                        stroke_width=10,
                        stroke_linecap="round",
                    )
                )
                molecules.append(
                    dw.Line(
                        *(center + vec2(s[0], s[1])),
                        *(center + vec2(e[0], e[1])),
                        stroke="white",
                        stroke_width=4,
                        stroke_linecap="round",
                    )
                )

            for j in double[i]:
                if done[j]:
                    continue

                b, _ = mol.atoms[j]
                q = locs[j]

                v = q - p
                t = normalize(v)

                s = p * bond_length + t * atom_radii[a]
                e = q * bond_length - t * atom_radii[b]

                u = rot90(normalize(vec2(v[0], v[1]))) * atom_radius / 4

                molecules.append(
                    dw.Line(
                        *(center + vec2(s[0], s[1]) - u),
                        *(center + vec2(e[0], e[1]) - u),
                        stroke=turquoise,
                        stroke_width=10,
                        stroke_linecap="round",
                    )
                )
                molecules.append(
                    dw.Line(
                        *(center + vec2(s[0], s[1]) - u),
                        *(center + vec2(e[0], e[1]) - u),
                        stroke="white",
                        stroke_width=4,
                        stroke_linecap="round",
                    )
                )

                molecules.append(
                    dw.Line(
                        *(center + vec2(s[0], s[1]) + u),
                        *(center + vec2(e[0], e[1]) + u),
                        stroke=turquoise,
                        stroke_width=10,
                        stroke_linecap="round",
                    )
                )
                molecules.append(
                    dw.Line(
                        *(center + vec2(s[0], s[1]) + u),
                        *(center + vec2(e[0], e[1]) + u),
                        stroke="white",
                        stroke_width=4,
                        stroke_linecap="round",
                    )
                )

            done[i] = True

        labels.append(
            dw.Text(
                f"{mol.name} ({mol.formula})",
                "22.5px",
                *(center + vec2(0, bond_length * 0.75)),
                center=True,
                font_family=font_family,
                stroke="white",
                stroke_width=5,
                paint_order="stroke",
            )
        )

    reaction_box_size = 0.75 * width / 2
    reaction_box_top = height / 2 - reaction_box_size / 2
    reaction_box_bottom = height / 2 + reaction_box_size / 2

    reactant_center = width / 4
    product_center = width * 3 / 4

    radius = reaction_box_size / 5

    reactant_angle = random.uniform(0, tau)
    for i, mol in enumerate(reactants):
        c = vec2(reactant_center, height / 2 - bond_length / 2)
        theta = reactant_angle + i * tau / len(reactants)
        molecule(mol, c + radius * vec2(cos(theta) * 1.5, sin(theta)))

    product_angle = random.uniform(0, tau)
    for i, mol in enumerate(products):
        c = vec2(product_center, height / 2 - bond_length / 2)
        theta = product_angle + i * tau / len(reactants)
        molecule(mol, c + radius * vec2(cos(theta) * 1.5, sin(theta)))

    d.append(shadows)

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

    d.append(molecules)
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
        atoms=[("O", vec3(-0.5, 0, 0)), ("O", vec3(0.5, 0, 0))],
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
