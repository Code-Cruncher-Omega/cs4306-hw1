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

    # Holds Rankings for each hospital
    hospital_rankings = {}
    for hospital in hospitals:
        hospital_rankings[hospital] = {}

        preferences = hospitals[hospital]["preferences"]

        for rank in range(len(preferences)):
            resident = preferences[rank]
            hospital_rankings[hospital][resident] = rank
    
    # Loop for checking each residents proposals to hospitals
    while len(free_residents) > 0:
        current_resident = free_residents.pop(0)

        # If current resident has no hospitals left yto try, skip them
        if next_choice[current_resident] >= len(residents[current_resident]):
            continue
        hospital = residents[current_resident][next_choice][current_resident]
        next_choice[current_resident] = next_choice[current_resident] + 1
        matches[hospital].append(current_resident)

        slots = hospital[hospital]["Slots"]

        if len(matches[hospital]) > slots:
            worst_resident = matches[hospital][0]
            worst_rank = hospital_rankings[hospital][worst_resident]

            for resident in matches[hospital]:
                resident_rank = hospital_rankings[hospital][resident]

                if resident_rank > worst_rank:
                    worst_resident = resident
                    worst_rank = resident_rank

            matches[hospital].remove(worst_resident)

            if next_choice[worst_resident] < len(residents[worst_resident]):
                free_residents.append(worst_resident)

    return matches