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

`gen.py` (from prior prototyping): weighted onset/vowel/coda pools + three
suffix families + junction-compatibility rules (consonant-initial suffixes
require sonorant-ish codas; vowel-initial suffixes sometimes trim the coda
for flow, e.g. "throb-ulus").

## Roadmap ideas (discussed with user, in rough priority order)

1. **Real-stem pool**: mix real chunky/gross English monosyllables (grist,
   throb, gunk, clomp, crud, squelch, wallop...) into the synthetic stems.
   Several top keepers are real-word + fake-suffix.
2. **Keeper feedback loop**: persist kept names; use them to retune pool
   weights (count onset/coda/suffix frequencies in keepers).
3. **N-gram scoring**: train a char-level order-2/3 Markov model on the keeper
   corpus, use it to SCORE rule-generated candidates (not generate), surface
   only the top slice. Viable even with a ~30-name corpus.
4. **Later, if corpus grows to hundreds**: makemore-style char-level model as
   a learning project. NOT a LoRA/LLM fine-tune — corpus is far too small and
   would just memorize.
