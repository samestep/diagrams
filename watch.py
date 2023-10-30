import argparse
import subprocess

from watchfiles import watch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("cmd", nargs="*")
    args = parser.parse_args()

    for changes in watch(args.path):
        subprocess.run(args.cmd)


if __name__ == "__main__":
    main()
