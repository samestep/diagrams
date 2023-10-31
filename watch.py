import argparse
import shlex
import subprocess

from watchfiles import watch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()

    cmd = [
        "./diagram.py",
        "-m",
        args.name,
        "-f",
        "draw",
        "-o",
        f"out/{args.name}.svg",
    ]

    def run():
        print("$", " ".join(shlex.quote(word) for word in cmd))
        subprocess.run(cmd)

    run()
    for changes in watch(f"./{args.name}.py"):
        print(changes)
        run()


if __name__ == "__main__":
    main()
