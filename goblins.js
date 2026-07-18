// goblins.js — the engine. Taste lives in pools.js; this is the linguistics.
//
// Junction rules (ported 1:1 from the Python version, see git history):
// - vowel-initial suffixes attach anywhere; silent-e stems drop the e
//   (sludge + ular -> sludgular), and a few English-y suffixes geminate a
//   short final consonant (blub + ard -> blubbard, like sluggard)
// - consonant-initial suffixes need a clean coda, and heavy coda clusters
//   get trimmed first (grond + mond -> gronmond) — except before l-initial
//   suffixes, which blend fine as-is (throngle, crumble)
//
// generateBatch() takes an optional scorer (name -> number): it oversamples
// candidates and returns only the top slice. This is the plug-in point for
// the roadmap-step-3 n-gram scorer.

"use strict";

const VOWELISH = new Set("aeiouy");

// Stem endings that tolerate a consonant-initial suffix
// (crudmond works because d -> m is a clean junction).
const OK_BEFORE_C = new Set(["nd", "ng", "nk", "mp", "nt", "rk", "mb", "st",
                             "b", "d", "g", "m", "n"]);

// Suffixes that double a short final consonant, the way English does
// in sluggard and hummock.
const GEMINATING = new Set(["ard", "ock", "ollop"]);

// ---- pool plumbing ----

function entries(table) {
  return Object.entries(table); // [[piece, weight], ...]
}

function flattenSuffixes(pools) {
  const out = [];
  for (const [family, table] of Object.entries(pools.suffixes)) {
    for (const [text, weight] of Object.entries(table)) {
      out.push({ text, weight, family });
    }
  }
  return out;
}

function weightedPick(pairs) {
  // pairs: [[item, weight], ...]
  let total = 0;
  for (const [, w] of pairs) total += w;
  let roll = Math.random() * total;
  for (const [item, w] of pairs) {
    roll -= w;
    if (roll <= 0) return item;
  }
  return pairs[pairs.length - 1][0];
}

function vowelInitial(suffixText) {
  return VOWELISH.has(suffixText[0]);
}

// ---- assembly ----

function pickSuffix(suffixes, vowelOnly = false) {
  const pool = vowelOnly ? suffixes.filter((s) => vowelInitial(s.text))
                         : suffixes;
  return weightedPick(pool.map((s) => [s, s.weight]));
}

function endsClean(stem) {
  return OK_BEFORE_C.has(stem.slice(-2)) || OK_BEFORE_C.has(stem.slice(-1));
}

function join(stem, suf) {
  if (vowelInitial(suf.text)) {
    if (stem.endsWith("e")) stem = stem.slice(0, -1);
    if (GEMINATING.has(suf.text) && /[aeiou][bdgmnpt]$/.test(stem)) {
      stem += stem.slice(-1);
    }
    return stem + suf.text;
  }
  if (suf.text[0] !== "l") {
    const m = stem.match(/[^aeiou]+$/);
    if (m && m[0].length >= 2) {
      stem = stem.slice(0, stem.length - m[0].length + 1);
    }
  }
  return stem + suf.text;
}

function realStemGoblin(pools, suffixes) {
  const stem = weightedPick(entries(pools.stems));
  let suf = pickSuffix(suffixes);
  if (!vowelInitial(suf.text) && !endsClean(stem)) {
    suf = pickSuffix(suffixes, true);
  }
  return join(stem, suf);
}

function syntheticGoblin(pools, suffixes) {
  const onset = weightedPick(entries(pools.onsets));
  const vowel = weightedPick(entries(pools.vowels));
  let coda = weightedPick(entries(pools.codas));
  const suf = pickSuffix(suffixes);
  if (vowelInitial(suf.text)) {
    // sometimes trim the coda to its first consonant for flow
    // (throb-ulus instead of thromb-ulus)
    if (Math.random() < pools.knobs.flowTrimP) coda = coda[0];
  } else {
    for (let i = 0; i < 10 && !OK_BEFORE_C.has(coda); i++) {
      coda = weightedPick(entries(pools.codas));
    }
    if (!OK_BEFORE_C.has(coda)) coda = "nd";
  }
  return join(onset + vowel + coda, suf);
}

function makeGoblin(pools, suffixes) {
  return Math.random() < pools.knobs.realStemP
    ? realStemGoblin(pools, suffixes)
    : syntheticGoblin(pools, suffixes);
}

function capitalize(s) {
  return s[0].toUpperCase() + s.slice(1);
}

function generateBatch(n, pools, exclude = [], scorer = null, oversample = 4) {
  const suffixes = flattenSuffixes(pools);
  const target = scorer ? n * oversample : n;
  const seen = new Set(exclude.map((x) => x.toLowerCase()));
  const out = [];
  for (let i = 0; i < target * 50 && out.length < target; i++) {
    const g = capitalize(makeGoblin(pools, suffixes));
    if (!seen.has(g.toLowerCase())) {
      seen.add(g.toLowerCase());
      out.push(g);
    }
  }
  if (scorer) {
    out.sort((a, b) => scorer(b) - scorer(a));
    return out.slice(0, n);
  }
  return out;
}

// ---- keepers + retuning ----
// Seed corpus is baked into pools.js; the visitor's own keeps persist in
// localStorage. Retuning is a gentle nudge: each keeper occurrence of a
// piece adds retuneAlpha to its base weight, capped at retuneCap x base.

const STORAGE_KEY = "goblin-keepers";

function loadLocalKeepers() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

function saveLocalKeepers(names) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(names));
}

function allKeepers() {
  return SEED_KEEPERS.concat(loadLocalKeepers());
}

function keepName(name) {
  const local = loadLocalKeepers();
  const have = allKeepers().map((k) => k.toLowerCase());
  if (have.includes(name.toLowerCase())) return false;
  local.push(name);
  saveLocalKeepers(local);
  return true;
}

function dropName(name) {
  const local = loadLocalKeepers();
  const kept = local.filter((k) => k.toLowerCase() !== name.toLowerCase());
  if (kept.length === local.length) return false;
  saveLocalKeepers(kept);
  return true;
}

function parseFeatures(name, pools, suffixes) {
  // Best-effort: anything that doesn't match a known pool piece just
  // contributes nothing (Blubthazar's -thazar is a one-off, that's fine).
  const n = name.trim().toLowerCase();
  const feats = {};

  const byLen = suffixes.map((s) => s.text).sort((a, b) => b.length - a.length);
  const suffix = byLen.find(
    (s) => n.endsWith(s) && n.length - s.length >= 3 &&
           /[aeiou]/.test(n.slice(0, -s.length)));
  if (suffix) feats.suffix = suffix;
  const rest = suffix ? n.slice(0, -suffix.length) : n;

  const onset = Object.keys(pools.onsets)
    .sort((a, b) => b.length - a.length)
    .find((o) => n.startsWith(o));
  if (onset) feats.onset = onset;

  // undo gemination and silent-e stripping when matching real stems
  for (const cand of [rest, rest + "e",
                      rest.length > 3 ? rest.slice(0, -1) : rest]) {
    if (cand in pools.stems) { feats.stem = cand; break; }
  }

  const m = rest.match(/[^aeiou]+$/);
  if (m && m[0] in pools.codas) feats.coda = m[0];

  return feats;
}

function featureCounts(keepers, pools) {
  const suffixes = flattenSuffixes(pools);
  const counts = { onset: {}, coda: {}, suffix: {}, stem: {} };
  for (const name of keepers) {
    const feats = parseFeatures(name, pools, suffixes);
    for (const [kind, value] of Object.entries(feats)) {
      counts[kind][value] = (counts[kind][value] || 0) + 1;
    }
  }
  return counts;
}

function tunedPools(base) {
  const counts = featureCounts(allKeepers(), base);
  const { retuneAlpha: alpha, retuneCap: cap } = base.knobs;
  const tuneTable = (table, counter) => {
    const out = {};
    for (const [piece, w] of Object.entries(table)) {
      out[piece] = Math.min(w * cap, w + alpha * (counter[piece] || 0));
    }
    return out;
  };
  const suffixFams = {};
  for (const [family, table] of Object.entries(base.suffixes)) {
    suffixFams[family] = tuneTable(table, counts.suffix);
  }
  return {
    onsets: tuneTable(base.onsets, counts.onset),
    vowels: base.vowels,
    codas: tuneTable(base.codas, counts.coda),
    suffixes: suffixFams,
    stems: tuneTable(base.stems, counts.stem),
    knobs: base.knobs,
  };
}
