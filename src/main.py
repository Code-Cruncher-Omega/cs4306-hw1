from parser import parse_input
from matching import match_residents
import sys


def main():
    print("CS4306 Assignment 1")
    print("Paste input, then press Ctrl+Z then Enter on Windows:")

    text = sys.stdin.read()
    text = text.replace("\x1a", "").strip()

    hospitals, residents = parse_input(text)
    matches = match_residents(hospitals, residents)

    print("\nMatching:")
    for hospital, assigned_residents in matches.items():
        print(hospital + ", " + ", ".join(assigned_residents))


if __name__ == "__main__":
    main()