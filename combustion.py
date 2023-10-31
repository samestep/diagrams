import drawsvg as dw

from diagram import rgb


def reaction(reactants, products):
    width = 1248
    height = 702
    d = dw.Drawing(width, height)

    gray = rgb(0.5, 0.5, 0.5)

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

    d.append(
        dw.Text(
            "Methane Combustion Reaction",
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


def draw():
    return reaction([], [])
