LITERAL = 1
KLAUZULA = 2
FORMULA = 3
AND = 5
OR = 6
ALL = 7
NOT = 8
operators2 = { AND, OR }
convert = {
    "â\udc88§": AND,
    "â\udc88¨": OR,
    "â\udc88€": ALL,
    "Â¬": NOT,
    "&": AND,
    "AND": AND,
    "∧": AND,
    "OR": OR,
    "|": OR,
    "∨": OR,
    "NOT": NOT,
    "~": NOT,
    "¬": NOT,
    "FORALL": ALL,
    "∀": ALL
}
predicates = { "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" }
empty = { "", " ", "/" }

def neg(p):
    return { "\\": "/", "/": "\\" }[p[0]] + p[1:]

def lToStr(l): # make list comparable deeply with others
    if type(l) is list:
        l.sort()
        return " ".join(l)
    return l

while (1):
    zb = [] # zbior pomocniczy do tworzenia klauzul
    finalForm = [] # zawiera same klauzule
    dicts = [] # zawiera słowniki do wyszukiwania literałów
    strs = [] # postacie porownywalne
    done = False
    def mKlauzula(l):
        d = {}
        strk = lToStr(l)
        try:
            strs.index(strk) # nie dopuszcza dodania tej samej klauzuli
        except:
            strs.append(strk)
            if type(l) is list: # klauzula
                for p in l:
                    if d[neg(p)]: return 0 # iteraly komplementarne - klauzula jest prawdziwa
                    d[p] = True
                finalForm.append(l)
            else: # iteral
                d[l] = True
                finalForm.append([l])
            dicts.append(d)
            return 1
    def rez(a, b, db): # rezolwenta
        l = []
        for p in a:
            if not db.get(neg(p)):
                l.append(p)
        if l.__len__() == 0: # pusta klauzula
            print("NIESPEŁNIALNA")
            return 2
        return mKlauzula(l)
    form = input().split()
    for word in form:
        if (word in convert):
            word = convert[word]
            if (word == NOT):
                zb[zb.__len__() - 1] = neg(zb[zb.__len__() - 1]) # zmiana na zanegowany (bledy dla podwojnych negacji)
            elif (word == OR): # dba o klauzulę
                if type(zb[zb.__len__() - 2]) is list:
                    if (type(zb[zb.__len__() - 1]) is list):
                        zb[zb.__len__() - 2].extend(zb.pop())
                    else:
                        zb[zb.__len__() - 2].append(zb.pop())
                else:
                    if (type(zb[zb.__len__() - 1]) is list):
                        zb[zb.__len__() - 1].append(zb.pop(zb.__len__() - 2))
                    else:
                        l = []
                        l.append(zb.pop())
                        l.append(zb.pop())
                        zb.append(l)
            elif (word == AND): # moze byc FORM AND X, X AND X problem: X AND FORM AND X - fixed
                mKlauzula(zb.pop())
                if (finalForm.__len__() == 1):
                    mKlauzula(zb.pop())
            else: # ALL
                zb.pop(0)
        elif (word.__len__() == 1): # argument albo kwantyfikowana zmienna
            zb.append(word)
        else: # predykat
            word = word.split('/')
            pred = "\\" + word[0] # bez negacji
            for x in range(0, int(word[1], 10)):
                pred = pred + zb.pop()
            zb.append(pred)
    if (zb.__len__() > 0): 
        finalForm.append(zb) # Dodać nową klauzulę jesli zb nie jest pusty
    iters = [] # Przygotowanie listy iteracyjnej
    for x in finalForm:
        iters.append(1)
    change = True
    klauzule = iters.__len__()
    while change and not done: # szuka wszystkie rezolwenty
        change = False
        for i in range(len(finalForm)):
            while (iters[i] < klauzule):
                sol = rez(finalForm[i], finalForm[iters[i]], dicts[iters[i]])
                if sol == 2:
                    done = True # niespelnialna
                    break
                if sol == 1:
                    change = True
                    klauzule += 1
                iters[i] += 1
    if not done:
        print("SPEŁNIALNA") # koniec
