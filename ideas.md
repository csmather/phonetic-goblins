# Ideas: phoneme candidates + goblin theory

Scratchpad of research findings, candidate pool additions, and thoughts on
what makes a good phonetic goblin. The pool candidates below were adopted
into `pools.toml` in the v2 refactor — this file remains the idea log and
the theory reference.

Framing reminder: this project is not "names for goblins." A phonetic goblin
is a word whose *phonetics* are the joke — a ridiculous mishmash of phonemes,
either random sounds or sounds borrowed from real language patterns (the
Latinate -aloid family, medieval -mond, etc.).

## Research notes (light pass)

**The Westbury entropy finding.** A University of Alberta study on why
made-up words like "snunkoople" are funny: nonwords with *improbable letter
combinations* (low entropy relative to English) were consistently rated
funniest — improbable letters like z and k, and uncommon doublings like oo
and rr, drove the effect. The bigger the entropy gap, the more reliably
people found the word funnier. Dr. Seuss's coinages turn out to be
measurably low-entropy — he was doing this by ear.
Implication for us: a goblin needs a measurable *wrongness*, but see the
"wrongness budget" idea below — the winners are mostly-plausible words with
one improbable region, not uniform noise. Also directly relevant to roadmap
step 3: the Markov scorer is basically an entropy meter. We may want to
surface candidates in a *band* (weird enough, but not gibberish) rather than
just the top of the plausibility ranking.

**Plosives and the K tradition.** Old comedy lore, partially backed up:
plosives (p, b, t, d, k, g) read as the funniest consonants, especially in
short words, and /k/ specifically has a century of vaudeville pedigree
(Mencken on Kalamazoo, Hoboken). Our pools are already plosive-heavy on
codas but light on /k/ — worth adding k-flavored codas and suffixes.

**Phonaesthemes.** The linguistic term for what the pools already do by
instinct: sub-morphemic sound clusters that carry a meaning-vibe without a
meaning. English sn- clusters around nose/mouth words (snort, snout, sniff),
gl- around light (glow, gleam), and the gr-/-ump/-udge families around
heaviness and disgust. A goblin works partly by triggering these
meaning-echoes with no referent — "Grondular" *feels* like it means
something ponderous and damp. When adding pool pieces, prefer clusters that
already have a phonaesthetic gang behind them in English.

Sources:
- [How funny is this word? The 'snunkoople' effect (ScienceDaily)](https://www.sciencedaily.com/releases/2015/11/151130131847.htm)
- [The snunkoople effect (U Alberta)](https://www.ualberta.ca/en/science/news/2015/november/the-snunkoople-effect.html)
- [Slate on the Westbury study](https://slate.com/human-interest/2015/12/why-is-the-nonsense-word-snunkoople-funnier-than-the-equally-made-up-word-filisma-research-explains.html)
- [Inherently funny word (Wikipedia)](https://en.wikipedia.org/wiki/Inherently_funny_word)
- [Sound symbolism / phonaesthemes (Wikipedia)](https://en.wikipedia.org/wiki/Phonaesthesia)

## Candidate pool additions

### Onsets
- **cl-** — glaring gap: clomp/clod/clump are already stems but cl- can't
  start a synthetic goblin ("Clombulus")
- **sp-** — spl- exists but plain sp- doesn't ("Spongulor")
- **dw-** — dweeb energy; rare in English so it reads instantly wrong in a
  good way ("Dwombulus," "Dwungle")
- **thw-** — thwack, thwart; nearly extinct cluster ("Thwondular")
- **fr-** — frump, fromage adjacent ("Frundulus")
- **sw-** — swab, swonk ("Swombert")
- **shr-** — shrub, shrivel ("Shrogulant")
- **z-** — Westbury-approved improbable letter; ration hard ("Zungulor")

### Vowels
- **oi** — CLAUDE.md explicitly names oi/au/ui as target diphthongs and the
  pool doesn't have oi. Goiter is the patron saint ("Gloinkulus," "Throindor")
- **oo** — Westbury's funny doubling; snunkoople itself ("Snoodular,"
  "Broombulus")

### Codas
- **lk** — skulk, bulk ("Grolkulus")
- **lb** — bulb; genuinely ugly little cluster ("Squolbior")
- **lp** — gulp, wallop ("Thrulpax")
- **sk** — husk, mollusk ("Bruskulon")
- **x** — crux, flux; k-sound plus improbable letter, double Westbury points
  ("Snoxular")
- **nge** — grunge, plunge; only before vowel suffixes ("Splungeior"? needs
  the e-strip rule: "Splungior")
- **bb / gg / zz-style doublings** before -le suffixes specifically
  ("Snobble," "Druggle")

### Suffixes — Latinate/medical lineage
- **-uncle** — carbuncle, peduncle, furuncle. Possibly the single best
  candidate in this file: "Throbuncle," "Grunduncle," "Squonkuncle"
- **-ulum** — frenulum, speculum, pendulum; the Foucault's Frenulum
  bloodline ("Throbulum," "Crudulum")
- **-ellum** — flagellum, cerebellum ("Grondellum")
- **-ygmus** — the Borborygmus lineage deserves descendants ("Splonkygmus")
- **-oma** — medical growth suffix; quietly horrifying ("Gunkoma,"
  "Throboma")
- **-odon** — mastodon, iguanodon ("Crudodon," "Squelchodon")
- **-yx** — coccyx, onyx, Bombyx (real genus!) ("Grondyx," "Thrulyx")
- **-aster** — real Latin pejorative suffix meaning "fake/inferior"
  (poetaster = bad poet). Etymologically perfect: a Crudaster is an inferior
  imitation of crud

### Suffixes — medieval-guy lineage
- **-bald** — Theobald, Archibald; reads as both a name suffix and male
  pattern baldness ("Grumbald," "Crudbald," "Squelchbald")
- **-ard** — real English pejorative suffix (drunkard, sluggard, dullard).
  A -ard goblin is definitionally a guy who does the stem too much:
  "Blubbard," "Gunkard," "Thrombard"
- **-oth** — Behemoth, Ashdoth; Old Testament heavyweight ("Grondoth")
- **-wulf** — Beowulf tier; ration it ("Crudwulf")

### Suffixes — bare/diminutive lineage
- **-ock** — bullock, hummock, buttock. Chunky English diminutive, huge
  potential: "Grondock," "Splodock," "Thrunnock"
- **-ollop** — wallop, dollop, trollop; two-syllable flop sound
  ("Grondollop," "Snodollop")
- **-kins** — already have -kin; the plural is somehow more pathetic
  ("Crudkins")

### Suffixes — mineral/industrial (new sub-family?)
The substance engine is out of scope but its *morphology* isn't:
- **-ite** — mineral suffix (lignite, anthracite): "Gunkite," "Splonkite"
  (watch the crudité collision — maybe that's a feature)
- **-ium** — element suffix: "Crudium," "Thrombium"
These make the goblin sound like it was discovered rather than born, which
is a different and possibly great flavor of ridiculous.

## What makes a good phonetic goblin (theory section)

**The wrongness budget.** The research says improbable = funny, but the
corpus says something sharper: every keeper is ~80% plausible with the
wrongness concentrated in one place. "Crudmond" is two impeccable pieces
improbably married. "Snunkoople" spends its budget on one cluster.
Uniform weirdness reads as noise, not comedy — the ear needs a baseline of
plausibility for the wrong part to be wrong *against*. This is also why
pronounceability is non-negotiable: an unpronounceable word has overspent
the budget and the reader stops rendering it as a word at all.

**Fake etymology is the engine.** The suffix families work because they
supply a counterfeit provenance. -ulus/-aloid says "a doctor named this."
-mond/-bald says "this man held land in 1183." The joke is the brain
auto-completing a history for a word that has none — "Robustaloid" sounds
like it has a chemical formula; "Squelchior" sounds like he brought
frankincense. A goblin with no detectable language-of-origin is weaker than
one that convincingly fakes the wrong one.

**Register collision.** Corollary of fake etymology: maximum comedy is a
low, gross stem wearing high, formal morphology. Crud (gutter) + -mond
(heraldry). The suffix dignifies the crud, and the dignity is the punchline.
This predicts -uncle and -aster will hit: they're formal Latin machinery
whose *real* English survivors (carbuncle, poetaster) are already
undignified.

**Stress must be self-evident.** Every keeper has an obvious stress pattern
on first read: THROB-u-lus, gron-DOM-bu-lus, CRUD-mond. If a reader has to
negotiate where the stress goes, the word dies in their mouth. This is a
hidden strength of the Latinate suffixes — they import Latin's predictable
antepenultimate stress for free. Three syllables is the sweet spot; four
works only when the suffix carries the rhythm (-ombulus); five is a spell,
not a name.

**Bouba, never kiki.** Back vowels + voiced plosives + nasal codas make a
word feel round, heavy, and slightly damp — goblins are bouba objects.
Front vowels (ee, i) miniaturize and cutesify; that's elf morphology, wrong
project. The existing o/u dominance is correct and worth defending even as
pools grow.

**Near-collision with real words is a feature.** The generator once coined
"Drummond" (real surname) and "-ite" risks "crudité." Hovering one phoneme
off a real word is the goblin equivalent of the pun engine's
minimal-phonetic-distance rule — the reader's dictionary lookup *almost*
succeeds, and the near-miss is where the laugh lives. The step-3 scorer
could deliberately surface these: candidates with high similarity to a real
word that aren't one.

**The anti-goblin checklist** (inverse of the above): wrongness spread
evenly instead of concentrated; no detectable fake etymology; ambiguous
stress; front-vowel lightness; more than four syllables; a junction pileup.
Any two of these and the word is compost.
