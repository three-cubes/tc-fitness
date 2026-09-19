import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name")
    if "--help" in sys.argv:
        raise SystemExit(1)
    parser.parse_args()


if __name__ == "__main__":
    main()
