"""Load and validate pools.toml — the fiddle file.

All taste data (phoneme pools, suffix families, real stems, knobs) lives in
pools.toml at the project root so it can be edited without touching code.
This module turns it into a Pools object and complains helpfully when an
edit doesn't parse.
"""

import tomllib
from dataclasses import dataclass
from pathlib import Path

POOLS_FILE = Path(__file__).resolve().parent.parent / "pools.toml"

_VOWELISH = set("aeiouy")


class PoolsError(Exception):
    """A problem in pools.toml, with a message meant for the fiddler."""


@dataclass(frozen=True)
class Suffix:
    text: str
    weight: float
    family: str

    @property
    def vowel_initial(self) -> bool:
        return self.text[0] in _VOWELISH


@dataclass
class Pools:
    onsets: list
    onset_w: list
    vowels: list
    vowel_w: list
    codas: list
    coda_w: list
    suffixes: list  # of Suffix
    stems: list
    stem_w: list
    real_stem_p: float
    flow_trim_p: float
    retune_alpha: float
    retune_cap: float


def _weight_table(table, name):
    if not isinstance(table, dict) or not table:
        raise PoolsError(f"pools.toml: missing or empty [{name}] table")
    for piece, weight in table.items():
        if isinstance(weight, bool) or not isinstance(weight, (int, float)) \
                or weight <= 0:
            raise PoolsError(
                f"pools.toml: [{name}] {piece} = {weight!r} — "
                "weights must be positive numbers")
    return list(table.keys()), [float(w) for w in table.values()]


def _knob(knobs, name, lo, hi):
    value = knobs.get(name)
    if isinstance(value, bool) or not isinstance(value, (int, float)) \
            or not lo <= value <= hi:
        raise PoolsError(
            f"pools.toml: [knobs] {name} = {value!r} — "
            f"must be a number between {lo:g} and {hi:g}")
    return float(value)


def load_pools(path=POOLS_FILE) -> Pools:
    path = Path(path)
    if not path.exists():
        raise PoolsError(f"pools file not found: {path}")
    try:
        raw = tomllib.loads(path.read_text())
    except tomllib.TOMLDecodeError as e:
        raise PoolsError(f"pools.toml doesn't parse: {e}") from e

    onsets, onset_w = _weight_table(raw.get("onsets"), "onsets")
    vowels, vowel_w = _weight_table(raw.get("vowels"), "vowels")
    codas, coda_w = _weight_table(raw.get("codas"), "codas")
    stems, stem_w = _weight_table(raw.get("stems"), "stems")

    families = raw.get("suffixes")
    if not isinstance(families, dict) or not families:
        raise PoolsError("pools.toml: missing [suffixes.<family>] tables")
    suffixes = []
    for family in families:
        texts, weights = _weight_table(families[family], f"suffixes.{family}")
        suffixes += [Suffix(t, w, family) for t, w in zip(texts, weights)]

    knobs = raw.get("knobs", {})
    return Pools(
        onsets=onsets, onset_w=onset_w,
        vowels=vowels, vowel_w=vowel_w,
        codas=codas, coda_w=coda_w,
        suffixes=suffixes,
        stems=stems, stem_w=stem_w,
        real_stem_p=_knob(knobs, "real_stem_p", 0, 1),
        flow_trim_p=_knob(knobs, "flow_trim_p", 0, 1),
        retune_alpha=_knob(knobs, "retune_alpha", 0, 100),
        retune_cap=_knob(knobs, "retune_cap", 1, 100),
    )
