from typing import Dict, List, Tuple, Union
 
Matching = Union[Dict[str, List[str]], Dict[str, "str | None"]]
 
_WORST = float('inf')  # stand-in rank for "not acceptable / no partner"
 
 
def _normalize_matching(hospitals: dict, matching: Matching) -> Dict[str, List[str]]:
    
    normalized = {h: [] for h in hospitals}
 
    if not matching:
        return normalized
 
    sample_value = next(iter(matching.values()))
 
    if isinstance(sample_value, (list, tuple, set)):
        # already hospital -> [residents]
        for h, assigned in matching.items():
            normalized.setdefault(h, [])
            normalized[h] = list(assigned)
        return normalized
 
    if sample_value is None or isinstance(sample_value, str):
        # resident -> hospital (or none)
        for resident, h in matching.items():
            if h is None:
                continue
            normalized.setdefault(h, [])
            normalized[h].append(resident)
        return normalized
 
    raise TypeError(
        "Unrecognized matching format: expected {hospital: [residents]} "
        "or {resident: hospital_or_None}."
    )
 
 
def build_resident_to_hospital(norm_matching: Dict[str, List[str]]) -> Dict[str, str]:

    r2h: Dict[str, str] = {}
    for h, assigned in norm_matching.items():
        for r in assigned:
            if r in r2h:
                raise ValueError(
                    f"Resident '{r}' appears assigned to more than one hospital "
                    f"({r2h[r]} and {h})."
                )
            r2h[r] = h
    return r2h
 
 
def check_feasibility(hospitals: dict, residents: dict, matching: Matching) -> List[str]:

    # Checks matching before stability
    # Returns a list of problems; empty list == feasible.
 
    problems: List[str] = []
    norm = _normalize_matching(hospitals, matching)
    seen_residents = set()
 
    for h, assigned in norm.items():
        if h not in hospitals:
            problems.append(f"Matching references unknown hospital '{h}'.")
            continue
 
        capacity = hospitals[h]['slots']
        if len(assigned) > capacity:
            problems.append(
                f"Hospital '{h}' is over capacity: "
                f"{len(assigned)} assigned but only {capacity} slot(s)."
            )
 
        for r in assigned:
            if r not in residents:
                problems.append(f"Matching references unknown resident '{r}'.")
                continue
            if r in seen_residents:
                problems.append(f"Resident '{r}' is assigned to more than one hospital.")
            seen_residents.add(r)
 
            if r not in hospitals[h]['rank']:
                problems.append(
                    f"'{r}' is assigned to '{h}', but '{h}' does not rank '{r}' "
                    f"(not on its preference list)."
                )
            if h not in residents[r]['rank']:
                problems.append(
                    f"'{r}' is assigned to '{h}', but '{r}' does not rank '{h}' "
                    f"(not on its preference list)."
                )
 
    return problems
 
 
def find_unstable_pairs(
    hospitals: dict, residents: dict, matching: Matching) -> List[Tuple[str, str, str]]:

    # Returns every blocking pair found, as (hospital, resident, reason).
    # An empty list means the matching is stable.
 
    norm = _normalize_matching(hospitals, matching)
    r2h = build_resident_to_hospital(norm)
    unstable: List[Tuple[str, str, str]] = []
 
    for h, hinfo in hospitals.items():
        capacity = hinfo['slots']
        if capacity == 0:
            continue  # hospital offers no positions
 
        assigned = norm.get(h, [])
        assigned_set = set(assigned)
        h_rank = hinfo['rank']
 
        if len(assigned) < capacity:
            # any acceptable resident beats an empty slot
            worst_assigned_resident = None
            worst_assigned_rank = _WORST
        else:
            worst_assigned_resident = max(assigned, key=lambda r: h_rank.get(r, _WORST))
            worst_assigned_rank = h_rank.get(worst_assigned_resident, _WORST)
 
        # only residents h finds acceptable at all can block
        for s_prime in hinfo['prefs']:
            if s_prime in assigned_set:
                continue  # already matched to this hospital
 
            if not (h_rank[s_prime] < worst_assigned_rank):
                continue  # h doesn't prefer s' enough to bump anyone or fill a slot
 
            s_info = residents.get(s_prime)
            if s_info is None or h not in s_info['rank']:
                continue  # h isn't acceptable to s'; can't be a blocking pair
 
            current_h = r2h.get(s_prime)  # none if unmatched
 
            if current_h is None:
                s_prefers_h = True  # any acceptable hospital beats staying unmatched
                if worst_assigned_resident is not None:
                    reason = (
                        f"Type 1: {h} prefers unassigned resident {s_prime} over "
                        f"its currently assigned resident {worst_assigned_resident}."
                    )
                else:
                    reason = (
                        f"{h} has an open slot and {h}/{s_prime} are mutually "
                        f"acceptable, but {s_prime} is unassigned."
                    )
            else:
                s_prefers_h = s_info['rank'][h] < s_info['rank'].get(current_h, _WORST)
                reason = (
                    f"Type 2: {h} prefers {s_prime} (currently at {current_h}) over "
                    f"its assigned resident {worst_assigned_resident}, and "
                    f"{s_prime} prefers {h} to {current_h}."
                )
 
            if s_prefers_h:
                unstable.append((h, s_prime, reason))
 
    return unstable
 
 
def is_stable(hospitals: dict, residents: dict, matching: Matching) -> bool:
    # True if the matching is feasible AND has no blocking pairs 
    if check_feasibility(hospitals, residents, matching):
        return False
    return not find_unstable_pairs(hospitals, residents, matching)
 
 
def check_matching(hospitals: dict, residents: dict, matching: Matching) -> dict:

    # For use by main.py and the test cases
 
    feasibility_problems = check_feasibility(hospitals, residents, matching)
    feasible = len(feasibility_problems) == 0
    unstable_pairs = find_unstable_pairs(hospitals, residents, matching) if feasible else []
 
    return {
        'feasible': feasible,
        'feasibility_problems': feasibility_problems,
        'stable': feasible and len(unstable_pairs) == 0,
        'unstable_pairs': unstable_pairs,
    }
 
 
def print_report(report: dict) -> None:
    # Prints a check_matching() report
    if not report['feasible']:
        print("INFEASIBLE matching:")
        for p in report['feasibility_problems']:
            print(f"  - {p}")
        return
 
    if report['stable']:
        print("Matching is STABLE.")
    else:
        print("Matching is UNSTABLE. Blocking pairs found:")
        for h, s, reason in report['unstable_pairs']:
            print(f"  - ({h}, {s}): {reason}")