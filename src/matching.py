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