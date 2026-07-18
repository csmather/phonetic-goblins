"""Keeper persistence + weight retuning (roadmap step 2).

Keepers live in keepers.txt at the project root, one name per line —
deliberately plain so it doubles as the training corpus for the future
n-gram scorer (roadmap step 3).

Retuning is a gentle nudge, not a takeover: each keeper occurrence of an
onset/coda/suffix/stem adds ALPHA to its base weight, capped at CAP x base
so no single pattern (looking at you, -aloid) can dominate. Vowels aren't
retuned — parsing them out of finished names is too unreliable to be worth it.
"""

import re
from collections import Counter
from pathlib import Path

from . import data
from .generator import Weights, base_weights

KEEPERS_FILE = Path(__file__).resolve().parent.parent / "keepers.txt"

ALPHA = 1.0  # weight added per keeper occurrence
CAP = 3.0    # tuned weight never exceeds CAP x base weight

_ONSETS_BY_LEN = sorted(data.ONSETS, key=len, reverse=True)
_SUFFIXES_BY_LEN = sorted(data.SUF_V + data.SUF_C, key=len, reverse=True)


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


def parse_features(name):
    """Pull recognizable onset/coda/suffix/stem out of a keeper name.

    Best-effort: anything that doesn't match a known pool piece just
    contributes nothing (Blubthazar's -thazar is a one-off, that's fine).
    """
    n = name.strip().lower()
    feats = {}

    suffix = next((s for s in _SUFFIXES_BY_LEN
                   if n.endswith(s) and len(n) - len(s) >= 3
                   and re.search(r"[aeiou]", n[: -len(s)])), None)
    if suffix:
        feats["suffix"] = suffix
    rest = n[: -len(suffix)] if suffix else n

    onset = next((o for o in _ONSETS_BY_LEN if n.startswith(o)), None)
    if onset:
        feats["onset"] = onset

    if rest in data.REAL_STEMS:
        feats["stem"] = rest
    elif rest + "e" in data.REAL_STEMS:  # sludgular -> sludge
        feats["stem"] = rest + "e"

    m = re.search(r"[^aeiou]+$", rest)
    if m and m.group() in data.CODAS:
        feats["coda"] = m.group()

    return feats


def feature_counts(keepers):
    counts = {"onset": Counter(), "coda": Counter(),
              "suffix": Counter(), "stem": Counter()}
    for name in keepers:
        for kind, value in parse_features(name).items():
            counts[kind][value] += 1
    return counts


def _tune(pool, base, counter):
    return [min(b * CAP, b + ALPHA * counter.get(p, 0))
            for p, b in zip(pool, base)]


def tuned_weights(keepers=None) -> Weights:
    keepers = load_keepers() if keepers is None else keepers
    counts = feature_counts(keepers)
    w = base_weights()
    w.onset_w = _tune(w.onsets, w.onset_w, counts["onset"])
    w.coda_w = _tune(w.codas, w.coda_w, counts["coda"])
    w.suf_v_w = _tune(w.suf_v, w.suf_v_w, counts["suffix"])
    w.suf_c_w = _tune(w.suf_c, w.suf_c_w, counts["suffix"])
    w.stem_w = _tune(w.stems, w.stem_w, counts["stem"])
    return w
