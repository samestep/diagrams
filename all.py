import importlib
from pathlib import Path

import drawsvg as dw


def main():
    out = "out"
    Path(out).mkdir(parents=True, exist_ok=True)
    for name in ["geometry", "hamiltonian", "ngon", "quaternions"]:
        d = getattr(importlib.import_module(name), "draw")()
        if isinstance(d, dw.Drawing):
            d.save_svg(f"{out}/{name}.svg")
        else:
            raise TypeError(f"Expected Drawing, got {type(d)}")


if __name__ == "__main__":
    main()
