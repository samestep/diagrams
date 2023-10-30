import argparse
import colorsys
import importlib
from pathlib import Path

import svgwrite

Drawing = svgwrite.Drawing


def hsv(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mod", required=True)
    parser.add_argument("-f", "--func", required=True)
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    mod = importlib.import_module(args.mod)
    func = getattr(mod, args.func)
    dwg = func()
    if isinstance(dwg, svgwrite.Drawing):
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        dwg.filename = args.out
        dwg.save()
    else:
        raise TypeError(f"Expected Drawing, got {type(dwg)}")


if __name__ == "__main__":
    main()
