TERM = 1
FORM = 2
VAR = 3
ATOM = 4
operators1 = {
    "NOT", "~", "¬"
}
operators2 = {
    "AND", "&", "∧",
    "OR", "|", "∨",
    "IMPLIES", "→",
    "IFF", "↔",
    "XOR", "⊕"
}
operators3 = {
    "FORALL", "∀",
    "EXISTS", "∃"
}
convert = {
    "â\udc88§": "∧",
    "â\udc88¨": "∨",
    "â†’": "→",
    "â†”": "↔",
    "âŠ•": "⊕",
    "â\udc88€": "∀",
    "â\udc88\udc83": "∃",
    "Â¬": "¬"
}
consts = { "a", "b", "c", "d", "e" }
funcs = { "f", "g", "h", "i", "j", "k", "l", "m", "n" }
predicates = { "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" }
empty = { "", " ", "/" }

def isVar(word):
    return word.isupper()
def isTerm(num):
    return num == TERM or num == VAR
def isForm(num):
    return num == FORM or num == ATOM

listaStr = []
listaTyp = []

def pOperator1(op):
    p = listaStr.__len__() - 1
    if (p < 0):
        raise IndexError("Negacja niczego.\n")
    if (not isForm(listaTyp[p])):
        raise SyntaxError("Negacja elementu nie będącego FORMem.\n")
    listaStr[p] = "(" + op + " " + listaStr[p] + ")"
    listaTyp[p] = FORM

def pOperator2(op):
    p = listaStr.__len__() - 2
    if (p < 0):
        raise IndexError("Operacja '" + op + "' na niczym.\n")
    if (not isForm(listaTyp[p]) or not isForm(listaTyp.pop())):
        raise SyntaxError("Operacja '" + op + "' na elementach nie będących FORMem.\n")
    listaStr[p] = "(" + listaStr[p] + " " + op + " " + listaStr.pop() + ")"
    listaTyp[p] = FORM

def pOperator3(op):
    p = listaStr.__len__() - 2
    if (p < 0):
        raise IndexError("Kwantyfikacja niczego.\n")
    if (listaTyp[p] != VAR):
        raise SyntaxError("Kwantyfikacja elementu nie będącego zmienną\n")
    if (not isForm(listaTyp.pop())):
        raise SyntaxError("Domknięcie elementu niebędącego formem\n")
    listaStr[p] = "(" + op + " " + listaStr[p] + " " + listaStr.pop() + ")"
    listaTyp[p] = FORM

def pFunc(op, num):
    numOps = int(num, 10)
    term = ")"
    p = listaStr.__len__() - numOps
    if (p < 0):
        raise IndexError("Argumentacja niczym.\n")
    if not type(numOps) is int:
        raise SyntaxError("Liczba argumentów funkcji nie jest liczbą\n")
    for i in range(numOps, 0, -1):
        if (not isTerm(listaTyp.pop())):
            raise SyntaxError("Argument funkcji nie jest termem\n")
        term = listaStr.pop() + term
        if (i == 1):
            term = op + "(" + term
        else:
            term = ", " + term
    listaStr.append(term)
    listaTyp.append(TERM)

def pPredicate(op, num):
    numOps = int(num, 10)
    form = ")"
    p = listaStr.__len__() - numOps
    if (p < 0):
        raise IndexError("Argumentacja niczym.\n")
    if not type(numOps) is int:
        raise SyntaxError("Liczba argumentów predykatu nie jest liczbą\n")
    for i in range(numOps, 0, -1):
        if (not isTerm(listaTyp.pop())):
            raise SyntaxError("Argument predykatu nie jest termem\n")
        form = listaStr.pop() + form
        if (i == 1):
            form = op + "(" + form
        else:
            form = ", " + form
    listaStr.append(form)
    listaTyp.append(ATOM)

form = ""
class Reader:
    idx = -1
    tab = ""
    def __init__(self, form):
        self.tab = form

    def readChar(self):
        self.idx += 1
        if (self.idx < self.tab.__len__()):
            return self.tab[self.idx]
        else:
            return ""

    def readWord(self):
        word = ""
        char = " "
        while (char == " "):
            char = self.readChar()
        while (char not in empty):
            word += char
            char = self.readChar()
        return word

while (1):
    try:
        form = Reader(input())
    except:
        break
    if (form.tab == ""):
        break
    pos = -1
    while (1):
        word = form.readWord()
        if (word == ""): 
            break
        if (convert.__contains__(word)):
            word = convert[word]
        if (word in operators1):
            pOperator1(word)
        elif (word in operators2):
            pOperator2(word)
        elif (word in operators3):
            pOperator3(word)
        elif (word in funcs):
            pFunc(word, form.readWord())
        elif (word in predicates):
            pPredicate(word, form.readWord())
        elif (word in consts):
            listaStr.append(word)
            listaTyp.append(TERM)
        elif (isVar(word)):
            listaStr.append(word)
            listaTyp.append(VAR)
        else:
            raise SyntaxError("Nie rozpoznany symbol: '" + word + "'")
    if (listaStr.__len__() > 1):
        raise SyntaxError("Niewłaściwa ilość argumentów w stosunku do operacji. Pozostałe argumenty: " + str(listaStr.__len__() - 1) + ". Ostatni: " + listaStr[listaStr.__len__() - 1])
    print(listaStr[0])
    listaStr.clear()
    listaTyp.clear()
    word = form.readWord()
