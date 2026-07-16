import random

# Analysis of the seed corpus:
# robustaloid = real stem + latinate suffix
# throbulus   = chunky monosyllable + -ulus
# grondular   = goblin stem + -ular
# crudmond    = gross word + name suffix (-mond)
# squelchior  = wet verb + wise-man suffix (-ior)
# throngle    = throng + -le
# splanchnic  = nature's own goblin
# crembulant  = goblin stem + -ulant
#
# Common DNA: heavy onset clusters (thr, gr, cr, spl, squ),
# back vowels (o, u), chunky codas (nd, mb, ng, lch, nk, b),
# then a suffix that sounds either latinate-medical or like a
# guy's name from 1340.

ONSETS = ["thr","gr","cr","spl","squ","br","bl","gl","str","scr",
          "dr","sn","pl","fl","sk","chr","sl","tr","wr","gn","kn",
          "b","g","d","m","w","h"]
ONSET_W = [8,8,8,6,6,5,4,4,4,4,3,3,3,3,2,2,3,3,1,2,1,3,3,2,2,2,1]

VOWELS = ["o","u","a","e","i","aw","ou"]
VOWEL_W = [10,9,5,2,2,2,2]

CODAS = ["nd","mb","ng","lch","nk","b","g","rb","lb","mp","nch",
         "dg","rk","lg","nt","zz","lp","rgle"]
CODA_W = [6,6,6,4,4,4,4,3,3,3,3,3,2,2,3,1,2,1]

# Suffix families, each with its own flavor
SUF_LATINATE = ["ulus","ular","ulant","aloid","ulence","obulus",
                "ulor","icus","ulon","atron","ulite","oidal"]
SUF_MEDIEVAL = ["mond","mund","ior","bert","ulf","wick","fred","gard"]
SUF_DIMIN    = ["le","el","o","ers","kin"]

def syl():
    o = random.choices(ONSETS, ONSET_W)[0]
    v = random.choices(VOWELS, VOWEL_W)[0]
    c = random.choices(CODAS, CODA_W)[0]
    return o+v+c

def goblin():
    stem = syl()
    fam = random.choices(["lat","med","dim","bare"], [5,3,2,1])[0]
    if fam == "lat":
        s = random.choice(SUF_LATINATE)
        # drop coda sometimes so suffix flows (throb-ulus not thromb-ulus... actually both ok)
        if random.random() < 0.4:
            stem = stem[:-1] if stem[-1] in "bgdk" else stem
        return stem + s
    if fam == "med":
        return stem + random.choice(SUF_MEDIEVAL)
    if fam == "dim":
        return stem + random.choice(SUF_DIMIN)
    return stem + random.choice(["us","ax","ox","ung"])

random.seed(87)
for i in range(40):
    print(goblin().capitalize())
