from tabulate import tabulate #Pour les tableaux


def netoyage(Pb):
    '''Fonction ayant pour objectif de nettoyer le tableau extrait du fichier txt'''
    for i in range(len(Pb)):  
        Pb[i] = Pb[i].split(' ') #A chaque fois que l'on observe un espace, on sépare les éléments, sous forme de tableau
        for j in range(len(Pb[i])):
            Pb[i][j] = int(Pb[i][j]) # On passe tous les éléments de String à Int


def afficher_matrice(Matrice):
    '''Affiche la Matrice'''
    print(tabulate(Matrice, tablefmt="fancy_grid"))

def ComEtProv(Matrice):
    NbProv = int(Matrice[0][0])
    NbCom = int(Matrice[0][1])
    LProv = []
    LCom = []
    Matrice = Matrice[1:]
    for i in range(NbProv):
        LProv.append(Matrice[i][NbCom])
    for i in range(NbCom):
        LCom.append(Matrice[NbProv][i])
    return (NbProv, NbCom, LProv, LCom)

def NordOuest(Matrice):
    (NbProv, NbCom, LProv, LCom) = ComEtProv(Matrice)
    LProv = [int(x) for x in LProv]
    LCom = [int(x) for x in LCom]

    Mat = [[0 for j in range(NbCom)] for i in range(NbProv)]
    i, j = 0, 0
    while i < NbProv and j < NbCom:
        qte = min(LProv[i], LCom[j])
        Mat[i][j] = qte
        LProv[i] -= qte
        LCom[j] -= qte

        if LProv[i] == 0:
            i += 1
        else:
            j += 1

    return Mat

def BalasHammer(Matrice):

    (NbProv, NbCom, LProv, LCom) = ComEtProv(Matrice)
    Matrice = Matrice[1:]
    Matrice = [[int(x) for x in ligne] for ligne in Matrice]
    LProv = [int(x) for x in LProv]
    LCom = [int(x) for x in LCom]
    Couts = [ligne[:NbCom] for ligne in Matrice[:NbProv]]
    Mat = [[0 for i in range(NbCom)] for j in range(NbProv)]

    lignes_actives = [True for i in range(NbProv)]
    colonnes_actives = [True for j in range(NbCom)]

    while sum(LProv) > 0 and sum(LCom) > 0:

        # Pénalités des lignes
        Pen_Ligne = []
        for i in range(NbProv):
            if lignes_actives[i] == False:
                Pen_Ligne.append(-1)
            else:
                ligne = []
                for j in range(NbCom):
                    if colonnes_actives[j] == True:
                        ligne.append(Couts[i][j])

                ligne_triee = sorted(ligne)
                if len(ligne_triee) >= 2:
                    penalite = ligne_triee[1] - ligne_triee[0]
                else:
                    penalite = 0
                Pen_Ligne.append(penalite)

        # Pénalités des colonnes
        Pen_Col = []
        for j in range(NbCom):
            if colonnes_actives[j] == False:
                Pen_Col.append(-1)
            else:
                colonne_j = []
                for i in range(NbProv):
                    if lignes_actives[i] == True:
                        colonne_j.append(Couts[i][j])

                colonne_triee = sorted(colonne_j)
                if len(colonne_triee) >= 2:
                    penalite = colonne_triee[1] - colonne_triee[0]
                else:
                    penalite = 0
                Pen_Col.append(penalite)

        print("Pénalités lignes :", Pen_Ligne)
        print("Pénalités colonnes :", Pen_Col)
        
        max_ligne = max(Pen_Ligne)
        max_col = max(Pen_Col)

        if max_ligne >= max_col:
            i = Pen_Ligne.index(max_ligne)

            min_cout = None
            j = None

            for col in range(NbCom):
                if colonnes_actives[col] == True:
                    if min_cout == None or Couts[i][col] < min_cout:
                        min_cout = Couts[i][col]
                        j = col

        else:
            j = Pen_Col.index(max_col)
            min_cout = None
            i = None

            for lig in range(NbProv):
                if lignes_actives[lig] == True:
                    if min_cout == None or Couts[lig][j] < min_cout:
                        min_cout = Couts[lig][j]
                        i = lig

        qte = min(LProv[i], LCom[j])
        Mat[i][j] = qte
        LProv[i] -= qte
        LCom[j] -= qte

        if LProv[i] == 0:
            lignes_actives[i] = False

        if LCom[j] == 0:
            colonnes_actives[j] = False
    
    return Mat
    
def calcul_cout(MatCout, MatRemp):
    Cout = 0
    (NbProv, NbCom, LProv, LCom) = ComEtProv(MatCout)
    MatCout = MatCout[1:]
    for i in range(NbProv):
        for j in range(NbCom):
            Cout += MatCout[i][j]* MatRemp[i][j]
    return Cout


def construire_graphe(Mat, Occupied, NbProv, NbCom):
    """Renvoie un dict d'adjacence."""
    adj = {('P', i): [] for i in range(NbProv)}
    adj.update({('C', j): [] for j in range(NbCom)})
    for i in range(NbProv):
        for j in range(NbCom):
            if Occupied[i][j]:
                adj[('P', i)].append(('C', j))
                adj[('C', j)].append(('P', i))
    return adj


def bfs_cycle(adj):
    """Renvoie la liste des sommets formant un cycle, ou None."""
    visite = set()
    for depart in adj:
        if depart in visite:
            continue
        parent = {depart: None}
        file = [depart]
        visite.add(depart)
        while file:
            u = file.pop(0)
            for w in adj[u]:
                if w not in visite:
                    visite.add(w)
                    parent[w] = u
                    file.append(w)
                elif parent[u] != w:
                    return reconstruire_cycle(u, w, parent)
    return None

def reconstruire_cycle(u, w, parent):
    """L'arête (u,w) ferme le cycle. Reconstruit le cycle complet."""
    ancetres_u = []
    x = u
    while x is not None:
        ancetres_u.append(x)
        x = parent[x]
    set_u = set(ancetres_u)
    chemin_w = []
    x = w
    while x not in set_u:
        chemin_w.append(x)
        x = parent[x]
    lca = x
    cycle = []
    for a in ancetres_u:
        cycle.append(a)
        if a == lca:
            break
    cycle.extend(reversed(chemin_w))
    cycle.append(u)
    return cycle

def maximiser_cycle(Mat, Occupied, cycle):
    """cycle = [v0, v1, ..., vn, v0] (fermé). Arêtes paires = +, impaires = −."""
    def case(a, b):
        return (a[1], b[1]) if a[0] == 'P' else (b[1], a[1])
    
    n = len(cycle) - 1
    cases = [case(cycle[k], cycle[k+1]) for k in range(n)]
    plus  = cases[0::2]
    moins = cases[1::2]
    
    theta = min(Mat[i][j] for (i, j) in moins)
    print(f"  θ = {theta}, + sur {plus}, − sur {moins}")
    
    for (i, j) in plus:  Mat[i][j] += theta
    for (i, j) in moins: Mat[i][j] -= theta
    
    supprimees = [(i, j) for (i, j) in moins if Mat[i][j] == 0]
    for (i, j) in supprimees:
        Occupied[i][j] = False
    return supprimees


def bfs_composantes(adj):
    visite = set()
    comps = []
    for depart in adj:
        if depart in visite: continue
        comp, file = [], [depart]
        visite.add(depart)
        while file:
            u = file.pop(0); comp.append(u)
            for w in adj[u]:
                if w not in visite:
                    visite.add(w); file.append(w)
        comps.append(comp)
    return comps


def calcul_potentiels(Mat, Couts, Occupied, NbProv, NbCom):
    u = [None]*NbProv; v = [None]*NbCom
    u[0] = 0
    change = True
    while change:
        change = False
        for i in range(NbProv):
            for j in range(NbCom):
                if not Occupied[i][j]: continue
                if u[i] is not None and v[j] is None:
                    v[j] = Couts[i][j] - u[i]; change = True
                elif u[i] is None and v[j] is not None:
                    u[i] = Couts[i][j] - v[j]; change = True
    return u, v

def calcul_marginaux(Couts, u, v, Occupied, NbProv, NbCom):
    marg = [[0]*NbCom for _ in range(NbProv)]
    meilleure = None
    val_min = 0
    for i in range(NbProv):
        for j in range(NbCom):
            marg[i][j] = Couts[i][j] - (u[i] + v[j])
            if not Occupied[i][j] and marg[i][j] < val_min:
                val_min = marg[i][j]
                meilleure = (i, j)
    return marg, meilleure

def ajouter_arete_zero(Occupied, Couts, comps, NbProv, NbCom):
    """Reconnecte deux composantes en ajoutant une arête vide (qte = 0)."""
    comp_de = {}
    for k, comp in enumerate(comps):
        for sommet in comp:
            comp_de[sommet] = k
    meilleure, cout_min = None, None
    for i in range(NbProv):
        for j in range(NbCom):
            if Occupied[i][j]:
                continue
            if comp_de[('P', i)] != comp_de[('C', j)]:
                if cout_min is None or Couts[i][j] < cout_min:
                    cout_min = Couts[i][j]
                    meilleure = (i, j)
    if meilleure is not None:
        i, j = meilleure
        Occupied[i][j] = True
        print(f"  Dégénérescence : ajout arête fictive P{i}-C{j} (qte=0)")


def normaliser_cycle(cycle, arete_plus):
    pi, cj = ('P', arete_plus[0]), ('C', arete_plus[1])
    n = len(cycle) - 1
    for k in range(n):
        if {cycle[k], cycle[k+1]} == {pi, cj}:
            rot = cycle[k:n] + cycle[:k]
            rot.append(rot[0])
            return rot
    return cycle

def marche_pied(Mat, Couts, NbProv, NbCom):
    Occupied = [[Mat[i][j] > 0 for j in range(NbCom)] for i in range(NbProv)]
    arete_a_proteger = None

    iteration = 0
    while True:
        iteration += 1
        print(f"\nItération {iteration}")

        adj = construire_graphe(Mat, Occupied, NbProv, NbCom)
        cyc = bfs_cycle(adj)
        while cyc is not None:
            if arete_a_proteger is not None:
                cyc = normaliser_cycle(cyc, arete_a_proteger)
                arete_a_proteger = None
            print("Cycle:", cyc)
            maximiser_cycle(Mat, Occupied, cyc)
            adj = construire_graphe(Mat, Occupied, NbProv, NbCom)
            cyc = bfs_cycle(adj)

        comps = bfs_composantes(adj)
        while len(comps) > 1:
            ajouter_arete_zero(Occupied, Couts, comps, NbProv, NbCom)
            adj = construire_graphe(Mat, Occupied, NbProv, NbCom)
            comps = bfs_composantes(adj)

        u, v = calcul_potentiels(Mat, Couts, Occupied, NbProv, NbCom)
        print("u =", u, "v =", v)

        marg, meilleure = calcul_marginaux(Couts, u, v, Occupied, NbProv, NbCom)
        print("\nProposition de transport actuelle :")
        afficher_matrice(Mat)
        print("Table des coûts marginaux :")
        afficher_matrice(marg)

        if meilleure is None:
            print("Solution optimale")
            return Mat

        i, j = meilleure
        print(f"Ajout de l'arête P{i}-C{j} (marginal {marg[i][j]})")
        Occupied[i][j] = True
        arete_a_proteger = (i, j)


def traiter_probleme(Num_Graph):
    """Traite un problème de transport : lecture, choix de l'algo initial, marche-pied."""
    try:
        with open("./transport/trans" + str(Num_Graph) + ".txt", "r") as file:
            Contenu = file.read()
            Contenu = Contenu.split('\n')
    except FileNotFoundError:
        print(f"\n[Erreur] Fichier ./transport/trans{Num_Graph}.txt introuvable.")
        return

    netoyage(Contenu)
    print("\n>>> Matrice des coûts (provisions à droite, commandes en bas) :")
    afficher_matrice(Contenu[1:])

    print("\nChoix de l'algorithme pour la proposition initiale :")
    print(" 1. Nord-Ouest")
    print(" 2. Balas-Hammer")
    choix = input("Votre choix (1/2) : ").strip()

    if choix == "1":
        print("\nAlgorithme : Nord-Ouest")
        Mat = NordOuest(Contenu)
    else:
        print("\nAlgorithme : Balas-Hammer")
        Mat = BalasHammer(Contenu)

    print("\nProposition de transport initiale :")
    afficher_matrice(Mat)
    print("Coût total initial :", calcul_cout(Contenu, Mat))

    (NbProv, NbCom, LProv, LCom) = ComEtProv(Contenu)
    Mat = marche_pied(Mat, Contenu[1:], NbProv, NbCom)

    print("\nProposition de transport OPTIMALE :")
    afficher_matrice(Mat)
    print("Coût total optimal :", calcul_cout(Contenu, Mat))


def menu():
    """Boucle principale du programme."""
    while True:
        Num_Graph = input("Numéro du problème à étudier (1-12, q pour quitter) : ").strip()

        if Num_Graph.lower() in ("q", "quit", "exit"):
            print("Au revoir !")
            break

        traiter_probleme(Num_Graph)

        rep = input("\nTester un autre problème ? (o/n) : ").strip().lower()
        if rep not in ("o", "oui", "y", "yes", ""):
            print("Au revoir !")
            break


menu()