# Phonetic Goblin Generator

A generator for absurd character names in the style of the user's personal naming
tradition (video game characters: Darktide, etc.). This project focuses on the
**phonetic goblin engine** — pure invented words that sound like real words gone
wrong. Think "Robustaloid," "Crudmond," "Squelchior."

## The vibe (read this first)

The target aesthetic is hard to fully distill and is ultimately a taste call by
the user. Do not over-systematize. Emergent rules are useful but should be held
loosely — when the user says a batch leans too hard on one pattern, vary it.
A low hit rate per batch is expected and fine; rerolling is part of the joy.
Optimize for occasional bangers, not consistent mediocrity.

Qualities of a good goblin:
- Sounds like it could be a real English/Latin/medieval word but isn't
- Heavy consonant onsets: thr-, gr-, cr-, spl-, squ-, br-, gl-
- Back vowels dominate: o, u; or back vowel diphthongs: oi, au, ui
- Chunky codas: -nd, -mb, -ng, -lch, -nk
- Rolls off the tongue — pronounceability is non-negotiable
- Funny on first read ("Crudmond made me laugh on reading it")

## Canonical corpus (the keepers)

Goblins (primary training data / few-shot seeds):
Robustaloid, Squelchior, Throbulus, Crembulant, Throngle,
Grondular, Crudmond, Splanchnic, Blubthazar, Grondombulus,
Drankular, Brudulant, Crobmund, Thruntax, Squonius, Bombastaloid

Real words that are honorary goblins: Splanchnic, Borborygmus
(nature did the work — real anatomical terms that sound invented)

Suffix families observed in the keepers:
- Latinate/medical: -ulus, -ular, -ulant, -aloid, -obulus ("Robustaloid" lineage)
- Medieval guy: -mond, -mund, -ior ("Crudmond," "Squelchior" lineage)
- Bare/diminutive: -le, -ax ("Throngle" lineage)

## Anti-patterns (from user feedback)

- Consonant pileups at stem/suffix junctions ("Blelbmond," "Crurgleulence") —
  junction smoothing matters
- Over-reliance on any single suffix, especially -aloid — ration it
- Unpronounceable clusters
- Secretion/moisture words used gratuitously — mineral/industrial/chunky beats wet
  (exception: "squelch" earned its place)

## Wider context: the other engines (background only, NOT this project's scope)

The user's full naming tradition has several engines. Know these for vibe
alignment, but this codebase only implements the goblin engine:

1. **Celebrity first-name puns, minimal phonetic distance**: Wiener Herzog,
   Gourd Vidal, Girth Brooks, Clod Debussy, Loam Chomsky, Glans Zimmer,
   Bone Didion. One sound off, not a whole word swap. Requires semantic
   knowledge — this engine stays LLM-few-shot territory, don't try to code it.
2. **Substance + civilian surname**: Butane Wallace (the all-time #1, came from
   a dream), Fishface Hydrogen, Creosote Jenkins, Bismuth T. Crandall,
   Spleen Whitaker, Sorghum Blevins, Spackle Dupree. Industrial/mineral
   substance wearing a normal surname. Surnames often "county sheriff /
   session bassist" flavored, but don't lean on that too hard.
3. **Scholarly brainrot one-offs**: Foucault's Frenulum. Not a real engine,
   lightning in a bottle.
4. Others in the roster: Ball Atreides, Warpus Callosum, Morsel DuChamp,
   Crouton Baskerville, Ganglion Beaumont.

Words the user has flagged as generally good raw material: ganglion, crembulant,
spleen, naphtha, creosote, bismuth, gravy, ennui, crouton.

## Current state

`goblins/` package (evolved from the `gen.py` prototype, now removed):
- `data.py` — weighted onset/vowel/coda pools, suffix families (vowel-initial
  Latinate + consonant-initial medieval), real-stem pool
- `generator.py` — assembly + junction smoothing: consonant-initial suffixes
  require clean codas and heavy coda clusters get trimmed before them
  (except l-initial suffixes: throngle, crumble); vowel-initial suffixes
  sometimes trim the coda for flow ("throb-ulus")
- `keepers.py` — keepers persist to `keepers.txt` (one name per line, seeded
  with the canonical corpus); onset/coda/suffix/stem counts in keepers add to
  base weights, capped at 3x base so no pattern dominates
- `cli.py` — interactive batch/keep/reroll loop (`python3 -m goblins`),
  one-shot mode (`-n 20`)

## Roadmap ideas (discussed with user, in rough priority order)

1. ~~**Real-stem pool**~~ DONE: real chunky monosyllables mixed into the
   synthetic stems at ~40% (`REAL_STEM_P` in data.py).
2. ~~**Keeper feedback loop**~~ DONE: see keepers.py above.
3. **N-gram scoring**: train a char-level order-2/3 Markov model on the keeper
   corpus, use it to SCORE rule-generated candidates (not generate), surface
   only the top slice. Viable even with a ~30-name corpus. The hook exists:
   `generate_batch(..., scorer=fn)` oversamples and keeps the top n.
4. **Later, if corpus grows to hundreds**: makemore-style char-level model as
   a learning project. NOT a LoRA/LLM fine-tune — corpus is far too small and
   would just memorize.
