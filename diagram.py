#!/usr/bin/env python3

import argparse
import importlib
from pathlib import Path

import drawsvg as dw


def rgb(r, g, b):
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mod", required=True)
    parser.add_argument("-f", "--func", required=True)
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    d = getattr(importlib.import_module(args.mod), args.func)()
    if isinstance(d, dw.Drawing):
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        d.save_svg(args.out)
    else:
        raise TypeError(f"Expected Drawing, got {type(d)}")


if __name__ == "__main__":
    main()
