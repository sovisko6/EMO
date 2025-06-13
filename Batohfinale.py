import matplotlib.pyplot as plt
import random
def generovani_batohu(pocet = 10, max_velikost = 10, max_cena = 10): #funguje
    batoh = [1]*pocet
    for i in range(len(batoh)):
        batoh[i] = [random.randint(1, max_velikost), random.randint(1, max_cena)] 
    return batoh #vrací v levo vaha a v pravo cenu

def pocitani(seznam): #funguje
    vaha = 0
    cena = 0
    for i in range(len(seznam)):
        vaha += seznam[i][0] 
        cena += seznam[i][1]
    return (vaha, cena) 

def testovani(seznam, velikost = 25): #funguje
    dopocitani = pocitani(seznam)
    if dopocitani[0] <= velikost:
        return(dopocitani[1])
    elif dopocitani[0] > (velikost): 
        return(-(dopocitani[0]))

def generovani_bin_souradnic(pocet = 20): #funguje
    generovany_prosotr = ["?"]*(pocet)
    for i in range(len(generovany_prosotr)):
        generovany_prosotr[i] = random.randint(0,1)
    return generovany_prosotr
 #1 = objekt tam je 0 = objekt tam neni

def prepis_bin(bin_souradnice, dokument): #funguje
    soubor = []
    for i in range(len(bin_souradnice)):
        if bin_souradnice[i] == 1:
            soubor.append(dokument[i])
    return(soubor) #prepise informace z dokumentu podle bin souradnic

def velke_testovani(seznam, batoh = generovani_batohu()): #funguje
    aktualne_tesstovany = []
    nejlepsi_test = []
    nejlepsi_bin = []
    
    for i in range(len(seznam)):
        aktualne_tesstovany = prepis_bin(seznam[i], batoh)
        if nejlepsi_test == []:
            nejlepsi_bin = seznam[i]
            nejlepsi_test = testovani(aktualne_tesstovany)
            
        elif testovani(aktualne_tesstovany) > nejlepsi_test:
            nejlepsi_bin = seznam[i]
            nejlepsi_test = testovani(aktualne_tesstovany)
    return(nejlepsi_bin)

def slepevyhledaní(kolikrát = 1000, batoh = generovani_batohu(), grafi = False): #funguje
    seznam = []
    graf = []
    for i in range(kolikrát):
        seznam.append(generovani_bin_souradnic(len(batoh)))
        if i % 100 == 0 and grafi == True:
            graf.append(pocitani(prepis_bin(velke_testovani(seznam, batoh), batoh)))
    if grafi == True:
        return(graf)
    else:
        nejlepsi_bin = velke_testovani(seznam, batoh)
        return(nejlepsi_bin)

def horolezecke_se_zakazaným_prohledávaním(batoh = generovani_batohu(), grafi = False, pocet = 300, nejlepsi = [], kolikrát = 200, graf = [], pouzite = []):
    if nejlepsi == []:
        nejlepsi = slepevyhledaní(kolikrát, batoh, False)
        pouzite.append(nejlepsi)
        if grafi == True:
            graf.append(pocitani(prepis_bin(nejlepsi, batoh)))
    generace = []
    while len(generace) < kolikrát:
        generovane = []
        for i in range(len(nejlepsi)):
            if random.random() < 0.3:
                generovane.append(1 - nejlepsi[i])
            else:
                generovane.append(nejlepsi[i])
        if generovane not in pouzite:  
            generace.append(generovane)
    nejlepsi = velke_testovani(generace, batoh)
    pouzite.append(nejlepsi)
    if grafi == True:
        graf.append(pocitani(prepis_bin(velke_testovani(pouzite, batoh), batoh)))
    if pocet != 0:
      return(horolezecke_se_zakazaným_prohledávaním(batoh, grafi, pocet - 1, nejlepsi, kolikrát, graf, pouzite))
    else:
        if grafi == True:
            return(graf)
        else:
            return(nejlepsi)

def nakresleni_grafu(graf):
    cena = []
    vaha = []
    hranice = []
    for i in range(len(graf)):
        cena.append(graf[i][1])
        vaha.append(graf[i][0])
        hranice.append(25)
    plt.plot(cena, linestyle='-', color='blue')
    plt.plot(hranice, linestyle='-', color='red')
    plt.plot(vaha, linestyle='-', color='g')
    plt.title('Průběh - Výsledeků')
    plt.xlabel('Pořadí pokusu')
    plt.ylabel('Výsledek')
    plt.grid(True)
    plt.show()

def seradeni(seznam, batoh): #funguje 
    vysledek = []
    for i in range(len(seznam)):
        vysledek.append([testovani(prepis_bin(seznam[i], batoh)), i])
    ciselny_seznam = sorted(vysledek, key=lambda x: x[0])
    return(ciselny_seznam) #vraci v poradi seznam v poradi od nejlepšiho po nejhorsi

def vyber_rodicu(seznam, batoh): #funguje
    vysledek = []
    pripravene = seradeni(seznam, batoh)
    for count in range(2):
        i = True
        a = -1
        while i == True:
            if random.random() < 0.5 and -a < len(pripravene):
                a -= 1 
            else:
                vysledek.append(seznam[pripravene[a][1]])
                i = False
    return(vysledek)
    
def krizeni(seznam, batoh): #funguje
    deti = []
    if random.random() < 0.02:
        a = random.randrange(0, len(seznam[1])-1)
        if seznam[1][a] == 0:
            seznam[1][a] = 1 
        else:
            seznam[1][a] = 0
    elif seznam[1] == seznam[0]:
        seznam[1] = slepevyhledaní(100, batoh)
    for i in range(len(seznam[1])):
        deti.append(seznam[0][:i] + seznam[1][i:])
        deti.append(seznam[1][:i] + seznam[0][i:])
    return(deti)

def algoritmus_2(graf = True, pocet = 100, batoh = generovani_batohu()): #funguje
    nejlepsi = []
    grafi = []
    i = 0
    for a in range(2):
        nejlepsi.append(horolezecke_se_zakazaným_prohledávaním(batoh))
    testovane = nejlepsi[:]
    while i != pocet:
        seznam = (krizeni(testovane, batoh))  
        nejlepsi.append(velke_testovani(seznam, batoh))
        grafi.append(pocitani(prepis_bin(velke_testovani(nejlepsi, batoh), batoh)))
        testovane = vyber_rodicu(seznam, batoh)
        i += 1
    if graf == True:
        
        return grafi
    else:
        return nejlepsi


def spojovani(batoh, seznam = [], pocet = 2): #musí bý na 2
    arenas = []
    while len(seznam) < pocet:
        seznam.append(horolezecke_se_zakazaným_prohledávaním(batoh))
        print(1)
    for idx in range(100):
        nova = []
        for i in range(len(seznam[0])):
            if random.random() < 0.1: #mutace toho moc neovlini... proto tak často
                nova.append(random.randint(0, 1)) 
            else:
                cislo = random.randrange(0, pocet)
                nova.append(seznam[cislo][i]) #nahodně vybere z jednoho nebo druhého
        arenas.append(nova)
    return(arenas)

def arena(grafi = True, batoh = generovani_batohu(), opakovani = 100): #malo rodičů
    vyherci = []
    bojujici = spojovani(batoh) #vytvoří potomky
    idx = 0
    graf = []
    while idx != opakovani:
        skupina1 = []
        skupina2 = []
        for i in range(len(bojujici)):
            if random.random() < 0.5:
                skupina1.append(bojujici[i]) #nahodně rozděleni potomků do dvou skupin.
            else:
                skupina2.append(bojujici[i])
        skupina1 = velke_testovani(skupina1, batoh)
        skupina2 = velke_testovani(skupina2, batoh)
        dalsi = [skupina1, skupina2]
        vyherci.append(skupina1)
        vyherci.append(skupina2)
        bojujici = spojovani(batoh, dalsi)
        graf.append(pocitani(prepis_bin(velke_testovani(vyherci, batoh), batoh)))
        idx += 1
    if grafi == True:
        return(graf)
    return(vyherci)


batoh = [[2, 7], [5, 6], [2, 2], [6, 5], [6, 1], [6, 1], [10, 8], [9, 1], [1, 4], [8, 6], [9, 5], [3, 5], [5, 1], [10, 4], [1, 7], [5, 9], [2, 6], [4, 2], [4, 3], [3, 6], [3, 1], [10, 3], [5, 1], [3, 7], [10, 3], [9, 4], [6, 5], [6, 6], [1, 8], [1, 9]]

nakresleni_grafu(arena(True, batoh))
nakresleni_grafu(algoritmus_2(True, 100, batoh))