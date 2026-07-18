"""Phoneme pools, suffix families, and the real-stem pool.

Base weights live here. Keeper-derived tuning (roadmap step 2) happens in
keepers.py — it never edits these, it blends keeper counts on top at runtime.
"""

# --- synthetic stem pools (onset + vowel + coda) ---

ONSETS = ["thr", "gr", "cr", "spl", "squ", "br", "bl", "gl", "str", "scr",
          "dr", "sn", "pl", "fl", "sk", "chr", "sl", "tr", "gn",
          "b", "g", "d", "m", "w"]
ONSET_W = [8, 8, 8, 6, 6, 5, 4, 4, 4, 4,
           3, 3, 3, 3, 2, 2, 3, 3, 2,
           3, 3, 2, 2, 1]

VOWELS = ["o", "u", "a", "aw", "ou", "e", "i"]
VOWEL_W = [10, 9, 5, 2, 2, 2, 2]

CODAS = ["nd", "mb", "ng", "lch", "nk", "b", "g", "d", "n", "mp",
         "nch", "rk", "nt", "rb", "dge", "zz"]
CODA_W = [7, 6, 6, 4, 4, 4, 4, 3, 2, 3,
          3, 2, 3, 2, 2, 1]

# --- suffix families ---

# Vowel-initial: safe after any coda (Latinate/medical lineage, mostly).
SUF_V = ["ulus", "ular", "ulant", "aloid", "obulus", "ulor", "icus", "ulon",
         "ombulus", "undular", "ax", "o", "us", "ington", "ius", "oid", "ior"]
SUF_V_W = [4, 4, 3, 2, 2, 2, 2, 2,
           2, 2, 3, 1, 2, 1, 2, 2, 3]  # -aloid deliberately rationed

# Consonant-initial: need a clean coda ahead of them (medieval-guy lineage).
SUF_C = ["mond", "mund", "bert", "wick", "fred", "dor", "gar", "ble", "kin", "let"]
SUF_C_W = [4, 3, 2, 2, 2, 2, 2, 3, 2, 2]

# Codas/final sounds that tolerate a consonant-initial suffix
# (crudmond works because d -> m is a clean junction).
OK_BEFORE_C = {"nd", "ng", "nk", "mp", "nt", "rk", "mb", "st",
               "b", "d", "g", "m", "n"}

# --- real-stem pool (roadmap step 1) ---
# Real chunky/gross English words used as stems. Several top keepers are
# real word + fake suffix (Robustaloid, Squelchior, Crudmond, Throbulus).
# Mineral/industrial/chunky beats wet. All end in a consonant or silent e.

REAL_STEMS = ["crud", "grist", "gunk", "clomp", "throb", "squelch", "wallop",
              "thrum", "clod", "chunk", "grub", "blub", "sludge", "dredge",
              "trudge", "plod", "thud", "scrum", "clump", "stump", "gulch",
              "husk", "grout", "bort", "marl", "curd", "gourd", "girth",
              "loam", "bog", "sump"]

# Chance a generated goblin starts from a real stem instead of a synthetic one.
REAL_STEM_P = 0.4
