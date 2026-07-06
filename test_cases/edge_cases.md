input/output1 == basic case

input/output2 == surplus resident, SUNNY unmatched, not flagged

input/output3 == one-sided preference (caught bug in matching.py)
    - The bug: when a resident proposes to a hospital that doesn't rank them (one-sided/mutually-unacceptable pair), the code appends them to matches[hospital] anyway and then crashes doing hospitals[hospital]["rank"][worst_resident].

    - The fix: check acceptability before appending, and if the hospital doesn't rank this resident, put the resident back on the free list to try their next choice instead of matching them somewhere invalid.

input/output4 == 0-slot hospital

input/output5 == resident with empty preference list