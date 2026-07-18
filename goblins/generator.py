"""Goblin assembly: stems + suffixes + junction smoothing.

generate_batch() takes an optional `scorer` callable (name -> float).
When given, it oversamples candidates and returns only the top slice —
this is the plug-in point for the roadmap-step-3 n-gram scorer.
"""

import random
import re
from dataclasses import dataclass

from . import data


@dataclass
class Weights:
    """A full set of pools + weights, possibly tuned by keeper counts."""
    onsets: list
    onset_w: list
    vowels: list
    vowel_w: list
    codas: list
    coda_w: list
    suf_v: list
    suf_v_w: list
    suf_c: list
    suf_c_w: list
    stems: list
    stem_w: list


def base_weights() -> Weights:
    return Weights(
        onsets=data.ONSETS, onset_w=list(data.ONSET_W),
        vowels=data.VOWELS, vowel_w=list(data.VOWEL_W),
        codas=data.CODAS, coda_w=list(data.CODA_W),
        suf_v=data.SUF_V, suf_v_w=list(data.SUF_V_W),
        suf_c=data.SUF_C, suf_c_w=list(data.SUF_C_W),
        stems=data.REAL_STEMS, stem_w=[1] * len(data.REAL_STEMS),
    )


def _pick(rng, pool, weights):
    return rng.choices(pool, weights)[0]


def _ends_clean(stem: str) -> bool:
    """Can a consonant-initial suffix follow this stem?"""
    return stem[-2:] in data.OK_BEFORE_C or stem[-1] in data.OK_BEFORE_C


def _pick_suffix(rng, pool, weights, stem):
    """Pick a suffix, retrying to avoid a doubled letter at the junction."""
    s = _pick(rng, pool, weights)
    for _ in range(5):
        if s[0] != stem[-1]:
            break
        s = _pick(rng, pool, weights)
    return s


def _smooth_junction(stem: str, suf: str) -> str:
    """Trim a heavy coda cluster before a consonant-initial suffix
    (Blelbmond prevention: grond+mond -> gronmond). l-initial suffixes
    blend fine as-is (throngle, crumble), so they keep the cluster.
    """
    if suf[0] == "l":
        return stem
    m = re.search(r"[^aeiou]+$", stem)
    if m and len(m.group()) >= 2:
        return stem[: m.start() + 1]
    return stem


def _real_stem_goblin(rng, w: Weights) -> str:
    stem = _pick(rng, w.stems, w.stem_w)
    if rng.random() >= 0.7 and _ends_clean(stem):
        s = _pick_suffix(rng, w.suf_c, w.suf_c_w, stem)
        return _smooth_junction(stem, s) + s
    if stem.endswith("e"):  # sludge + ular -> sludgular, not sludgeular
        stem = stem[:-1]
    return stem + _pick_suffix(rng, w.suf_v, w.suf_v_w, stem)


def _synthetic_goblin(rng, w: Weights) -> str:
    o = _pick(rng, w.onsets, w.onset_w)
    v = _pick(rng, w.vowels, w.vowel_w)
    c = _pick(rng, w.codas, w.coda_w)
    if rng.random() < 0.65:
        # vowel-initial suffix: trim coda to its first consonant 35% of the
        # time for flow (throb-ulus vs thromb-ulus)
        stem = o + v + (c[0] if rng.random() < 0.35 else c)
        return stem + _pick_suffix(rng, w.suf_v, w.suf_v_w, stem)
    # consonant-initial suffix: force a compatible coda
    for _ in range(10):
        if c in data.OK_BEFORE_C:
            break
        c = _pick(rng, w.codas, w.coda_w)
    else:
        c = "nd"
    stem = o + v + c
    s = _pick_suffix(rng, w.suf_c, w.suf_c_w, stem)
    return _smooth_junction(stem, s) + s


def make_goblin(rng, w: Weights) -> str:
    if rng.random() < data.REAL_STEM_P:
        return _real_stem_goblin(rng, w)
    return _synthetic_goblin(rng, w)


def generate_batch(n, rng=None, weights=None, exclude=(), scorer=None,
                   oversample=4):
    """Generate n unique goblins, skipping anything in `exclude`.

    With a scorer, generates n * oversample candidates and returns the
    n highest-scoring ones (roadmap step 3 slots in here).
    """
    rng = rng or random.Random()
    w = weights or base_weights()
    target = n * oversample if scorer else n
    seen = {name.lower() for name in exclude}
    out = []
    for _ in range(target * 50):  # hard cap so a tiny pool can't loop forever
        if len(out) >= target:
            break
        g = make_goblin(rng, w).capitalize()
        if g.lower() not in seen:
            seen.add(g.lower())
            out.append(g)
    if scorer:
        out.sort(key=scorer, reverse=True)
        out = out[:n]
    return out
