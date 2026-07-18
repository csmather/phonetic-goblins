# phonetic-goblins

Generator for absurd character names: Robustaloid, Crudmond, Squelchior tier.
See CLAUDE.md for the vibe, the corpus, and the taste rules; ideas.md for the
research and theory behind the pools.

**Live at: https://csmather.github.io/phonetic-goblins/**

Static site, no build step, no dependencies. Pushing to `main` deploys via
GitHub Actions.

## How it works

- **`pools.js`** — the fiddle file. All phonaestheme pools, suffix families
  (latinate/medieval/diminutive/mineral), real stems, knobs, and the seed
  keeper corpus live here as commented `piece: weight` lines. Tune taste by
  editing this; no other code involved.
- `goblins.js` — the engine: assembles stems + suffixes with junction rules
  (silent-e stripping, gemination like blub+ard → Blubbard, heavy-coda
  trimming before consonant suffixes so there are no pileups), plus keeper
  storage and weight retuning. Keeper counts of each onset/coda/suffix/stem
  gently boost its weight, capped so no single pattern dominates.
- `app.js` / `index.html` / `style.css` — the UI. Click a name to keep it;
  the seed corpus is baked in and each visitor's own keeps persist in their
  browser's localStorage.

Run locally: open index.html in a browser, or `python3 -m http.server`.

## Roadmap hooks

`generateBatch(..., scorer)` accepts any `name -> number` callable: it
oversamples candidates and returns the top slice. Roadmap step 3 is writing
that scorer (char-level order-2/3 Markov model trained on the keepers).

## History

The original implementation was Python (same engine, `pools.toml`,
interactive CLI). It lives in git history at the `python-final` tag.
