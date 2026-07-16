Read CLAUDE.md first — it has the full context, corpus, and taste guidelines
for this project.

Quick version: this is a generator for absurd "phonetic goblin" character
names (Robustaloid, Crudmond, Squelchior tier). gen.py is a working prototype
from a prior session: weighted phoneme pools + suffix families + junction
smoothing. It works but is rudimentary.

First task: turn it into a small interactive CLI — generate a batch of ~12,
let me keep/skip each (or keep by number), append keepers to keepers.txt,
loop. Keep it simple and readable; I want to see what's happening.

After that works, next up is roadmap item 1 from CLAUDE.md (real-stem pool).
Don't refactor into a big architecture — this is a tinker project.
