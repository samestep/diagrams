#!/usr/bin/env python3

import argparse
import importlib
from pathlib import Path

import drawsvg as dw
import numpy as np


def rgb(r, g, b) -> str:
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


def vec2(x, y) -> np.ndarray:
    return np.array([x, y])


def vec3(x, y, z) -> np.ndarray:
    return np.array([x, y, z])


def normalize(v: np.ndarray) -> np.ndarray:
    return v / np.linalg.norm(v)


def rot90(v: np.ndarray) -> np.ndarray:
    return vec2(-v[1], v[0])


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
