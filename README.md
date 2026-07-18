# phonetic-goblins

A generator for absurd character names: Robustaloid, Crudmond, Squelchior.

**Live at: https://csmather.github.io/phonetic-goblins/**

## The vibe

A phonetic goblin is a word that sounds like a real English, Latin, or
medieval word gone wrong. The good ones share a few traits: heavy consonant
onsets (thr-, gr-, squ-, spl-), back vowels (o, u), chunky endings (-nd,
-mb, -lch), and an obvious pronunciation — if you have to negotiate where
the stress goes, the word is dead. Above all it should be funny on first
read. A low hit rate per batch is expected; rerolling is part of the joy.

## How the names are built

Each name is a stem plus a suffix. Stems are either assembled from weighted
phoneme pools (onset + vowel + coda) or drawn from a pool of real chunky
words like crud, grist, and gourd. Suffixes are grouped into families that
each fake a different etymology: Latinate/medical (-ulus, -aloid, -uncle —
sounds like a doctor named it), medieval (-mond, -bald, -ard — sounds like
a man who held land in 1183), diminutive (-le, -ock), and mineral (-ite,
-ium — sounds discovered rather than born). The comedy comes from the
register collision: a gutter stem wearing formal morphology.

Junction rules keep everything pronounceable — silent e's drop before vowel
suffixes (sludge → Sludgular), short final consonants double before -ard
and -ock the way English does in sluggard (blub → Blubbard), and heavy
consonant clusters get trimmed before consonant suffixes so nothing like
"Grondmond" escapes.

There's some real linguistics behind the pool choices. A University of
Alberta study found that made-up words are funnier the more improbable
their letter combinations are (their star example: "snunkoople"), old
comedy lore holds that plosives — especially the k sound — are the
funniest consonants, and English has "phonaesthemes": sound clusters like
sn- and gr- that carry a vibe without a meaning. The pools lean on all
three.

Keeping a name feeds back into generation: each kept name's onset, coda,
suffix, and stem get a small weight boost, capped so no single pattern
takes over. A canon corpus is baked in; your own keeps live in your
browser.

## Files

- `pools.js` — all the taste: phoneme pools, suffix families, real stems,
  knobs, and the seed corpus, as commented `piece: weight` lines. Tune the
  generator by editing this file.
- `goblins.js` — the engine: assembly, junction rules, keeper storage,
  retuning.
- `app.js` / `index.html` / `style.css` — the UI.

No build step, no dependencies. Run locally by opening index.html, or
`python3 -m http.server`. Pushing to `main` deploys via GitHub Actions.

## Roadmap

Next up is scoring: a small character-level Markov model trained on the
keepers, used to rank candidates rather than generate them. The hook
already exists — `generateBatch(..., scorer)` oversamples and keeps the
top slice.

The original implementation was Python (same engine, a pools.toml, an
interactive CLI). It lives in git history at the `python-final` tag.
