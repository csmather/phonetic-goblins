"""Keeper persistence + weight retuning.

Keepers live in keepers.txt at the project root, one name per line —
deliberately plain so it doubles as the training corpus for the future
n-gram scorer (roadmap step 3).

Retuning is a gentle nudge, not a takeover: each keeper occurrence of an
onset/coda/suffix/stem adds `retune_alpha` to its base weight, capped at
`retune_cap` x base so no single pattern (looking at you, -aloid) can
dominate. Both knobs live in pools.toml. Vowels aren't retuned — parsing
them out of finished names is too unreliable to be worth it.
"""

import re
from collections import Counter
from dataclasses import replace
from pathlib import Path

from .pools import Pools, Suffix

KEEPERS_FILE = Path(__file__).resolve().parent.parent / "keepers.txt"


def load_keepers():
    if not KEEPERS_FILE.exists():
        return []
    lines = KEEPERS_FILE.read_text().splitlines()
    return [ln.strip() for ln in lines if ln.strip()]


def save_keeper(name):
    keepers = load_keepers()
    if name.lower() in (k.lower() for k in keepers):
        return False
    keepers.append(name)
    KEEPERS_FILE.write_text("\n".join(keepers) + "\n")
    return True


def remove_keeper(name):
    keepers = load_keepers()
    kept = [k for k in keepers if k.lower() != name.lower()]
    if len(kept) == len(keepers):
        return False
    KEEPERS_FILE.write_text("\n".join(kept) + "\n" if kept else "")
    return True


def parse_features(name, p: Pools):
    """Pull recognizable onset/coda/suffix/stem out of a keeper name.

    Best-effort: anything that doesn't match a known pool piece just
    contributes nothing (Blubthazar's -thazar is a one-off, that's fine).
    """
    n = name.strip().lower()
    feats = {}

    by_len = sorted((s.text for s in p.suffixes), key=len, reverse=True)
    suffix = next((s for s in by_len
                   if n.endswith(s) and len(n) - len(s) >= 3
                   and re.search(r"[aeiou]", n[: -len(s)])), None)
    if suffix:
        feats["suffix"] = suffix
    rest = n[: -len(suffix)] if suffix else n

    onset = next((o for o in sorted(p.onsets, key=len, reverse=True)
                  if n.startswith(o)), None)
    if onset:
        feats["onset"] = onset

    # undo gemination and silent-e stripping when matching real stems
    for candidate in (rest, rest + "e", rest[:-1] if len(rest) > 3 else rest):
        if candidate in p.stems:
            feats["stem"] = candidate
            break

    m = re.search(r"[^aeiou]+$", rest)
    if m and m.group() in p.codas:
        feats["coda"] = m.group()

    return feats


def feature_counts(keepers, p: Pools):
    counts = {"onset": Counter(), "coda": Counter(),
              "suffix": Counter(), "stem": Counter()}
    for name in keepers:
        for kind, value in parse_features(name, p).items():
            counts[kind][value] += 1
    return counts


def tuned_pools(p: Pools, keepers=None) -> Pools:
    """A copy of `p` with keeper counts blended into the weights."""
    keepers = load_keepers() if keepers is None else keepers
    counts = feature_counts(keepers, p)

    def tune(pool, base, counter):
        return [min(b * p.retune_cap, b + p.retune_alpha * counter.get(x, 0))
                for x, b in zip(pool, base)]

    suf_counter = counts["suffix"]
    suffixes = [
        Suffix(s.text,
               min(s.weight * p.retune_cap,
                   s.weight + p.retune_alpha * suf_counter.get(s.text, 0)),
               s.family)
        for s in p.suffixes]

    return replace(
        p,
        onset_w=tune(p.onsets, p.onset_w, counts["onset"]),
        coda_w=tune(p.codas, p.coda_w, counts["coda"]),
        stem_w=tune(p.stems, p.stem_w, counts["stem"]),
        suffixes=suffixes,
    )
