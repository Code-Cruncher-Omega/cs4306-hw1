from collections import defaultdict
def parse_input(text: str) ->[dict, dict]:
    blocks = text.strip().split('\n\n, 1')
    if len(blocks) != 2:
        raise ValueError("error")
    hospital_block, resident_block = blocks
    hospitals: dict = {}
    for line in hospital_block.strip().splitlines(): parts = [p.strip() for p in line.split(",")]
    if len(parts) <2:
        raise ValueError("error 2")
    name = parts[0]
    try:
        slots = int(parts[1])
    except ValueError:
            raise ValueError("error 3")
    prefs = parts[2:]
    hospitals[name] = {
        'slots' : slots,
        'prefs' : prefs,
        'rank' : {r: i+1 for i, r in enumerate(prefs)},
    }
    residents: dict ={}
    for line in resident_block.strip().splitlines():
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(',')]
        name = parts[0]
        prefs = parts[1:]
        residents[name] = {
            'prefs': prefs,
            'rank' : {h: i+1 for i, h in enumerate(prefs)},
        }


        return hospitals, residents

def main():
    print("daonibudna")