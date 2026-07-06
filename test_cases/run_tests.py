import sys, os, glob, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
CASES = os.path.dirname(os.path.abspath(__file__))

def main():
    inputs = sorted(glob.glob(os.path.join(CASES, "sample_input*.txt")))
    failures = 0
    for input_path in inputs:
        n = os.path.basename(input_path).replace("sample_input", "").replace(".txt", "")
        expected_path = os.path.join(CASES, f"sample_output{n}.txt")
        with open(input_path, "rb") as f:
            result = subprocess.run(
                [sys.executable, os.path.join(SRC, "main.py")],
                stdin=f, capture_output=True, text=True
            )
        actual = result.stdout
        if not os.path.exists(expected_path):
            print(f"[SKIP] {input_path}: no expected output yet")
            continue
        expected = open(expected_path).read()
        if actual.strip() == expected.strip():
            print(f"[PASS] {input_path}")
        else:
            failures += 1
            print(f"[FAIL] {input_path}")
            print("  expected:", expected.strip())
            print("  actual:  ", actual.strip())
    print(f"\n{len(inputs) - failures}/{len(inputs)} passed.")

if __name__ == "__main__":
    main()