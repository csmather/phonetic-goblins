# phonetic-goblins

Generator for absurd character names: Robustaloid, Crudmond, Squelchior tier.
See CLAUDE.md for the vibe, the corpus, and the taste rules.

## Usage

```sh
python3 -m goblins            # interactive: roll batches, keep the bangers
python3 -m goblins -n 20      # one-shot: print 20 names and exit
python3 -m goblins --seed 7   # reproducible rolls
```

Interactive commands: enter/`r` reroll, `2 7` keep those numbers, `k` list
keepers, `d <name>` drop one, `s` show weight tuning, `q` quit.

## How it works

- **`pools.toml`** — the fiddle file. All phonaestheme pools, suffix
  families, real stems, and knobs live here as `piece = weight` lines.
  Tune taste by editing this; no code required. Bad edits get a friendly
  error naming the line.
- `goblins/pools.py` — loads and validates pools.toml.
- `goblins/generator.py` — assembles stems + suffixes with junction rules:
  silent-e stripping, gemination (blub+ard → Blubbard), and heavy-coda
  trimming before consonant suffixes so there are no consonant pileups.
- `goblins/keepers.py` — keepers persist to `keepers.txt`; onset/coda/suffix/
  stem counts in the keepers gently retune the weights (capped so no single
  pattern dominates). Every reroll uses the freshly tuned weights.

Requires Python 3.11+ (stdlib only). The research and theory behind the
pool contents is in `ideas.md`.

## Roadmap hooks

`keepers.txt` is one name per line on purpose — it's the training corpus for
the step-3 n-gram scorer. `generate_batch(..., scorer=fn)` already accepts any
`name -> float` callable: it oversamples candidates and returns the top slice.
Step 3 is just writing that callable (char-level order-2/3 Markov model
trained on the keepers) and passing it in from the CLI.
