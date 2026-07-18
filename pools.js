// pools.js — the fiddle file.
//
// Every entry is  piece: weight  (higher = rolled more often; weights are
// relative within their table). Add a line to add a piece, delete a line to
// retire one, nudge a number to taste. Keeper counts add on top of these at
// runtime — see knobs at the bottom.
//
// Suffix families are flavor groupings for you and the stats display.
// Junction behavior (can it follow a heavy coda, does it strip a silent e)
// is derived from the suffix's own spelling, so a suffix can live in any
// family you think it belongs to.

const POOLS = {
  // heavy consonant clusters; the phonaestheme gangs (gr-, sn-, squ-)
  onsets: {
    thr: 8, gr: 8, cr: 8,
    spl: 6, squ: 6,
    br: 5, cl: 5,
    bl: 4, gl: 4, str: 4, scr: 4,
    dr: 3, sn: 3, pl: 3, fl: 3, sl: 3, tr: 3, sp: 3, fr: 3, b: 3, g: 3,
    sk: 2, chr: 2, gn: 2, sw: 2, shr: 2, dw: 2, d: 2, m: 2,
    w: 1, thw: 1,
    z: 1,  // Westbury-approved improbable letter; ration it
  },

  // back vowels dominate; goblins are bouba objects
  vowels: {
    o: 10, u: 9, a: 5,
    oi: 2,  // the goiter diphthong
    oo: 2,  // snunkoople doubling
    aw: 2, ou: 2, e: 2, i: 2,
  },

  // chunky endings
  codas: {
    nd: 7, mb: 6, ng: 6,
    lch: 4, nk: 4, b: 4, g: 4,
    d: 3, mp: 3, nch: 3, nt: 3,
    n: 2, rk: 2, rb: 2, dge: 2, nge: 2, lk: 2, lp: 2, sk: 2,
    x: 2,  // k-sound plus improbable letter, double Westbury points
    bb: 2, gg: 2,
    lb: 1, zz: 1,
  },

  suffixes: {
    // fake Latin/Greek/medical: "a doctor named this"
    latinate: {
      ulus: 4, ular: 4,
      ulant: 3, ior: 3,
      uncle: 3,  // carbuncle, peduncle
      ulum: 3,   // frenulum, speculum
      ax: 3,
      aloid: 2,  // rationed on purpose
      obulus: 2, ulor: 2, icus: 2, ulon: 2, ombulus: 2, undular: 2,
      us: 2, ius: 2, oid: 2,
      ellum: 2,  // flagellum, cerebellum
      oma: 2,    // medical growth suffix, quietly horrifying
      odon: 2,   // mastodon
      yx: 2,     // coccyx, onyx
      aster: 2,  // Latin pejorative: a Crudaster is inferior imitation crud
      ygmus: 1,  // the Borborygmus lineage
      o: 1,
    },
    // "this man held land in 1183"
    medieval: {
      mond: 4,
      mund: 3,
      bald: 3,  // Theobald
      ard: 3,   // drunkard, sluggard: a guy who does the stem too much
      bert: 2, wick: 2, fred: 2, dor: 2, gar: 2,
      oth: 2,   // Behemoth tier
      ington: 1,
      wulf: 1,  // ration it
    },
    // bare/pathetic endings
    diminutive: {
      ble: 3,
      ock: 3,    // bullock, hummock, buttock
      kin: 2, let: 2, le: 2,
      ollop: 2,  // wallop, dollop, trollop
      kins: 1,
    },
    // sounds discovered rather than born
    mineral: {
      ite: 2,  // lignite, anthracite
      ium: 2,  // element suffix
    },
  },

  // real chunky words fed into the same suffix machinery
  stems: {
    crud: 1, grist: 1, gunk: 1, clomp: 1, throb: 1, squelch: 1, wallop: 1,
    thrum: 1, clod: 1, chunk: 1, grub: 1, blub: 1, sludge: 1, dredge: 1,
    trudge: 1, plod: 1, thud: 1, scrum: 1, clump: 1, stump: 1, gulch: 1,
    husk: 1, grout: 1, bort: 1, marl: 1, curd: 1, gourd: 1, girth: 1,
    loam: 1, bog: 1, sump: 1, skulk: 1, bulb: 1, goiter: 1,
  },

  knobs: {
    realStemP: 0.4,   // chance a goblin starts from a real stem
    flowTrimP: 0.35,  // chance a synthetic coda trims for flow (throb-ulus)
    retuneAlpha: 1.0, // weight added per keeper occurrence of a piece
    retuneCap: 3.0,   // tuned weight never exceeds this multiple of base
  },
};

// The canonical corpus: seeds the tuning and the keepers display.
// Visitors' own keeps live in their browser (localStorage) on top of these.
const SEED_KEEPERS = [
  "Robustaloid", "Squelchior", "Throbulus", "Crembulant", "Throngle",
  "Grondular", "Crudmond", "Splanchnic", "Blubthazar", "Grondombulus",
  "Drankular", "Brudulant", "Crobmund", "Thruntax", "Squonius",
  "Bombastaloid", "Borborygmus", "Snogular", "Gunkoid", "Groulchombulus",
];
