"""Goblin assembly: stems + suffixes + junction smoothing.

Taste lives in pools.toml; this module is the linguistics. Junction rules:
- vowel-initial suffixes attach anywhere; silent-e stems drop the e
  (sludge + ular -> sludgular), and a few English-y suffixes geminate a
  short final consonant (blub + ard -> blubbard, like sluggard)
- consonant-initial suffixes need a clean coda, and heavy coda clusters
  get trimmed first (grond + mond -> gronmond) — except before l-initial
  suffixes, which blend fine as-is (throngle, crumble)

generate_batch() takes an optional `scorer` callable (name -> float): it
oversamples candidates and returns only the top slice. This is the plug-in
point for the roadmap-step-3 n-gram scorer.
"""

import random
import re

from .pools import Pools

# Stem endings that tolerate a consonant-initial suffix
# (crudmond works because d -> m is a clean junction).
OK_BEFORE_C = {"nd", "ng", "nk", "mp", "nt", "rk", "mb", "st",
               "b", "d", "g", "m", "n"}

# Suffixes that double a short final consonant, the way English does
# in sluggard and hummock.
GEMINATING = {"ard", "ock", "ollop"}


def _pick(rng, pool, weights):
    return rng.choices(pool, weights)[0]


def _pick_suffix(rng, p: Pools, vowel_only=False):
    pool = [s for s in p.suffixes if s.vowel_initial] if vowel_only \
        else p.suffixes
    return rng.choices(pool, [s.weight for s in pool])[0]


def _ends_clean(stem: str) -> bool:
    return stem[-2:] in OK_BEFORE_C or stem[-1] in OK_BEFORE_C


def _join(stem: str, suf) -> str:
    if suf.vowel_initial:
        if stem.endswith("e"):
            stem = stem[:-1]
        if suf.text in GEMINATING and re.search(r"[aeiou][bdgmnpt]$", stem):
            stem += stem[-1]
        return stem + suf.text
    if suf.text[0] != "l":
        m = re.search(r"[^aeiou]+$", stem)
        if m and len(m.group()) >= 2:
            stem = stem[: m.start() + 1]
    return stem + suf.text


def _real_stem_goblin(rng, p: Pools) -> str:
    stem = _pick(rng, p.stems, p.stem_w)
    suf = _pick_suffix(rng, p)
    if not suf.vowel_initial and not _ends_clean(stem):
        suf = _pick_suffix(rng, p, vowel_only=True)
    return _join(stem, suf)


def _synthetic_goblin(rng, p: Pools) -> str:
    onset = _pick(rng, p.onsets, p.onset_w)
    vowel = _pick(rng, p.vowels, p.vowel_w)
    coda = _pick(rng, p.codas, p.coda_w)
    suf = _pick_suffix(rng, p)
    if suf.vowel_initial:
        # sometimes trim the coda to its first consonant for flow
        # (throb-ulus instead of thromb-ulus)
        if rng.random() < p.flow_trim_p:
            coda = coda[0]
    else:
        for _ in range(10):
            if coda in OK_BEFORE_C:
                break
            coda = _pick(rng, p.codas, p.coda_w)
        else:
            coda = "nd"
    return _join(onset + vowel + coda, suf)


def make_goblin(rng, p: Pools) -> str:
    if rng.random() < p.real_stem_p:
        return _real_stem_goblin(rng, p)
    return _synthetic_goblin(rng, p)


def generate_batch(n, rng=None, pools=None, exclude=(), scorer=None,
                   oversample=4):
    """Generate n unique goblins, skipping anything in `exclude`.

    With a scorer, generates n * oversample candidates and returns the
    n highest-scoring ones (roadmap step 3 slots in here).
    """
    from .pools import load_pools
    rng = rng or random.Random()
    p = pools or load_pools()
    target = n * oversample if scorer else n
    seen = {name.lower() for name in exclude}
    out = []
    for _ in range(target * 50):  # hard cap so a tiny pool can't loop forever
        if len(out) >= target:
            break
        g = make_goblin(rng, p).capitalize()
        if g.lower() not in seen:
            seen.add(g.lower())
            out.append(g)
    if scorer:
        out.sort(key=scorer, reverse=True)
        out = out[:n]
    return out
