from parser import parse_input
from matching import match_residents
from stability import check_stability
import sys


def main():
    print("CS4306 Assignment 1")
    print("Paste input, then press Ctrl+Z then Enter on Windows:")

    text = sys.stdin.read()

    hospitals, residents = parse_input(text)
    matches = match_residents(hospitals, residents)

    print("\nMatching:")
    for hospital, assigned_residents in matches.items():
        print(hospital + ", " + ", ".join(assigned_residents))

    stable = check_stability(hospitals, residents, matches)
    print("\nStable:", stable)


if __name__ == "__main__":
    main()