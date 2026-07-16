import random

ONSETS = ["thr","gr","cr","spl","squ","br","bl","gl","str","scr",
          "dr","sn","pl","fl","sk","chr","sl","tr","gn","b","g","d","m","w"]
ONSET_W = [8,8,8,6,6,5,4,4,4,4,3,3,3,3,2,2,3,3,2,3,3,2,2,1]

VOWELS = ["o","u","a","aw","ou","e","i"]
VOWEL_W = [10,9,5,2,2,2,2]

CODAS = ["nd","mb","ng","lch","nk","b","g","mp","nch","rk","nt","rb","dge","zz"]
CODA_W = [7,6,6,4,4,4,4,3,3,2,3,2,2,1]

SUF_V = ["ulus","ular","ulant","aloid","obulus","ulor","icus","ulon",
         "ombulus","undular","ax","o","us","ington","ius","oid"]   # start with vowel: safe after any coda
SUF_C = ["mond","mund","bert","wick","fred","dor","gar","ble","kin","let"]  # start with consonant: need clean coda

CLEAN_CODAS = {"nd","ng","nk","mp","nt","mb","rk"}  # codas that tolerate a consonant suffix
# but even then, trim to sonorant: crudmond works because d->m is fine. Let's allow single stops too.
OK_BEFORE_C = {"nd","ng","nk","mp","nt","b","g","d","m","n","rk","mb"}

def syl():
    o = random.choices(ONSETS, ONSET_W)[0]
    v = random.choices(VOWELS, VOWEL_W)[0]
    c = random.choices(CODAS, CODA_W)[0]
    return o, v, c

def goblin():
    o, v, c = syl()
    stem = o+v+c
    if random.random() < 0.65:
        s = random.choice(SUF_V)
        # vowel-initial suffix: drop coda 35% of the time for flow (throb-ulus vs thromb-ulus)
        if random.random() < 0.35:
            stem = o+v+c[0]
        return stem + s
    else:
        s = random.choice(SUF_C)
        # consonant-initial suffix: force a compatible coda
        tries = 0
        while c not in OK_BEFORE_C and tries < 10:
            c = random.choices(CODAS, CODA_W)[0]; tries += 1
        if c not in OK_BEFORE_C: c = "nd"
        return o+v+c + s

random.seed(1971)
out = set()
while len(out) < 44:
    out.add(goblin().capitalize())
print("\n".join(sorted(out)))
