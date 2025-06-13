#had
import random
import pygame
souradnice_mapy = [30, 30]
class Had():
    def __init__(self, souradnicex=1, souradnicey=1, predchozi=None, pouzity=None, tahy=None):
        self.souradnicex = souradnicex
        self.souradnicey = souradnicey
        self.predchozi = predchozi
        self.pouzity = pouzity if pouzity is not None else []
        self.tahy = tahy if tahy is not None else []
        

    def testvani(self):
        if self.souradnicex > 0 and self.souradnicex <= souradnice_mapy[0]:
            if self.souradnicey > 0 and self.souradnicey <= souradnice_mapy[1]:
                return True
        return False

    def pohyb(self, smer):
        if smer != self.predchozi:  # zabráníme zpětnému pohybu
                  
            if smer == [1,0]:
                self.souradnicex += 1
                self.predchozi = [0,0]
            elif smer == [0,0]:
                self.souradnicex -= 1
                self.predchozi = [1,0]
            elif smer == [1,1]:
                self.souradnicey += 1
                self.predchozi = [0,1]
            elif smer == [0,1]:
                self.souradnicey -= 1
                self.predchozi = [1,1]
        self.pouzity.append((self.souradnicex, self.souradnicey))
        self.tahy.append(smer)
    
    def body(self):
        celkovypocet = len(self.pouzity)
        neduplikatni = len(set(self.pouzity))
        penalizace = celkovypocet - neduplikatni
        return max(neduplikatni*4 - penalizace*3, 0)


def random_start(): #fungue
    pes = Had()
    jablko = True
    while jablko == True:
        smer = random.choice(["vlevo", "vpravo", "nahoru", "dolu"])
        if smer == "vlevo":
            pes.pohyb([0,0])
        elif smer == "vpravo":
            pes.pohyb([1,0])
        elif smer == "nahoru":
            pes.pohyb([1,1])
        elif smer == "dolu":
            pes.pohyb([0,1])
        if pes.testvani() == False:
            jablko = False
    return pes
"""
def slepe_vyhledávaní():
    nejlepsi = random_start()
    druhy = None
    print(nejlepsi.body())
    for i in range(50):
        start = random_start()
        print(start.body())
        print(nejlepsi.body())
        if start.body() > nejlepsi.body():
            print(start.body())
            print(nejlepsi.body())
            druhy = nejlepsi
            nejlepsi = start
        elif druhy is None or start.body() > druhy.body():
            druhy = start
    return [nejlepsi, druhy]
"""
def slepe_vyhledávaní():
    vysledky = [random_start() for i in range(50)]
    vysledky.sort(key=lambda h: h.body(), reverse=True)
    return vysledky[:5]

def nova_generace(rodice = slepe_vyhledávaní(), velikost=50, mutace=0.1):
    nova_populace = []
    for i in range(velikost):
        otec = random.choice(rodice)
        matka = random.choice(rodice)
        nove_tahy = []
        for t1, t2 in zip(otec.tahy, matka.tahy):
            nove_tahy.append(random.choice([t1, t2]))
        if len(otec.tahy) > len(matka.tahy):
            nove_tahy += otec.tahy[len(matka.tahy):]
        else:
            nove_tahy += matka.tahy[len(otec.tahy):]
        nove_tahy = [
            t if random.random() > mutace else random.choice([[0,0],[1,0],[1,1],[0,1]])
            for t in nove_tahy
        ]
    
        potomek = Had()
        for tah in nove_tahy:
            potomek.pohyb(tah)
            if not potomek.testvani():
                break
        
        while potomek.testvani():
            smer = random.choice([[0,0],[1,0],[1,1],[0,1]])
            potomek.pohyb(smer)
            if not potomek.testvani():
                break
        nova_populace.append(potomek)
    return nova_populace




def vykresli(had):
    pygame.init()
    velikost_bunky = 20
    okno = pygame.display.set_mode((souradnice_mapy[0]*velikost_bunky, souradnice_mapy[1]*velikost_bunky))
    clock = pygame.time.Clock()
    navstivene = set()
    for idx, (x, y) in enumerate(had.pouzity):
        okno.fill((0, 0, 0))  # základní pole - černá
        
        for nx, ny in navstivene:
            pygame.draw.rect(okno, (0, 100, 0), (nx*velikost_bunky, ny*velikost_bunky, velikost_bunky, velikost_bunky))
        pygame.draw.rect(okno, (0, 255, 0), (x*velikost_bunky, y*velikost_bunky, velikost_bunky, velikost_bunky))

        pygame.display.update()
        pygame.time.wait(100)
        navstivene.add((x, y))
        clock.tick(60)

    pygame.time.wait(1000)
    pygame.quit()

def vyber_rodice(populace, pocet):
    # Výběr podle fitness (roulette wheel selection)
    body = [h.body() for h in populace]
    soucet = sum(body)
    if soucet == 0:
        return random.choices(populace, k=pocet)
    pravdepodobnosti = [b/soucet for b in body]
    return random.choices(populace, weights=pravdepodobnosti, k=pocet)

def turnajovy_vyber(populace, pocet, velikost_turnaje=3):
    vybrani = []
    for i in range(pocet):
        turnaj = random.sample(populace, velikost_turnaje)
        vybrani.append(max(turnaj, key=lambda h: h.body()))
    return vybrani

#----------------------------------------------------------------------#

pocet_generaci = 500
velikost_populace = 200
pocet_rodicu = 30
elita_pocet = 10  # kolik nejlepších jedinců uchovávat

# První generace
populace = [random_start() for _ in range(velikost_populace)]
elita = []

for gen in range(pocet_generaci):
    populace.sort(key=lambda h: h.body(), reverse=True)
    elita = populace[:elita_pocet] + elita
    elita = sorted(elita, key=lambda h: h.body(), reverse=True)[:elita_pocet]
    print(f"Generace {gen+1}: nejlepší body {populace[0].body()}")

    rodice = turnajovy_vyber(populace, pocet_rodicu)
    mutace = max(0.01, 0.2 * (1 - gen / pocet_generaci))
    populace = nova_generace(rodice, velikost=velikost_populace - elita_pocet, mutace=mutace)
    
    populace += elita
    
    pocet_nahodnych = max(1, velikost_populace // 50) 
    populace += [random_start() for _ in range(pocet_nahodnych)]
    
    populace = sorted(populace, key=lambda h: h.body(), reverse=True)[:velikost_populace]


elita.sort(key=lambda h: h.body(), reverse=True)
vykresli(elita[0])