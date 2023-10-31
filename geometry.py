import drawsvg as dw


def draw():
    canvas = 800
    d = dw.Drawing(canvas, canvas)

    text_padding_2 = 40

    dim = 700
    gap = (canvas - dim) / 2
    d.append(
        dw.Rectangle(
            gap, gap, dim, dim, fill="#f3f4f9", stroke="#8e93c4", stroke_width=2
        )
    )
    d.append(
        dw.Text(
            "E²",
            "35px",
            (canvas - gap) - text_padding_2,
            gap + text_padding_2,
            center=True,
        )
    )

    return d
