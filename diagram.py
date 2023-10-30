#!/usr/bin/env python3

import argparse
import importlib
from pathlib import Path

import drawsvg as dw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mod", required=True)
    parser.add_argument("-f", "--func", required=True)
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    mod = importlib.import_module(args.mod)
    func = getattr(mod, args.func)
    dwg = func()
    if isinstance(dwg, dw.Drawing):
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        dwg.save_svg(args.out)
    else:
        raise TypeError(f"Expected Drawing, got {type(dwg)}")


if __name__ == "__main__":
    main()
