def match_residents(hospitals, residents):

    # All residents start unmatched
    free_residents = list(residents.keys())

    # Each resident starts at the first hospital in their preference list
    next_choice = {}
    for resident in residents:
        next_choice[resident] = 0

    # Each hospital starts with no matched residents
    matches = {}
    for hospital in hospitals:
        matches[hospital] = []

    # Loop for checking each residents proposals to hospitals
    while len(free_residents) > 0:
        current_resident = free_residents.pop(0)

        # If current resident has no hospitals left to try, skip them
        if next_choice[current_resident] >= len(residents[current_resident]["prefs"]):
            continue

        hospital = residents[current_resident]["prefs"][next_choice[current_resident]]
        next_choice[current_resident] = next_choice[current_resident] + 1

        # skip mutually unacceptable pairs instead of crashing
        if current_resident not in hospitals[hospital]["rank"]:
            free_residents.append(current_resident)
            continue
            
        matches[hospital].append(current_resident)

        slots = hospitals[hospital]["slots"]

        if len(matches[hospital]) > slots:
            worst_resident = matches[hospital][0]
            worst_rank = hospitals[hospital]["rank"][worst_resident]

            for resident in matches[hospital]:
                resident_rank = hospitals[hospital]["rank"][resident]

                if resident_rank > worst_rank:
                    worst_resident = resident
                    worst_rank = resident_rank

            matches[hospital].remove(worst_resident)

            if next_choice[worst_resident] < len(residents[worst_resident]["prefs"]):
                free_residents.append(worst_resident)

    return matches