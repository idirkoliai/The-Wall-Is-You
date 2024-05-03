from drawings import *
home_wave_obj = sa.WaveObject.from_wave_file("Media/Music/Home_screen_OST.wav")
theme1_wave_obj = sa.WaveObject.from_wave_file("Media/Music/Theme1.wav")
theme2_wave_obj = sa.WaveObject.from_wave_file("Media/Music/Theme2.wav")  
theme3_wave_obj = sa.WaveObject.from_wave_file("Media/Music/Theme3.wav")  

players = ["goku", "gohan"]       # liste des joueurs

tombs = []     # liste des positions des ennemis morts
chemin_edit = [       # chemins utilisés pour l'éditeur de donjons
    "Media/rooms/FFFT.gif",
    "Media/rooms/FFTF.gif",
    "Media/rooms/FFTT.gif",
    "Media/rooms/FTFF.gif",
    "Media/rooms/FTFT.gif",
    "Media/rooms/FTTF.gif",
    "Media/rooms/FTTT.gif",
    "Media/rooms/TFFF.gif",
    "Media/rooms/TFFT.gif",
    "Media/rooms/TFTF.gif",
    "Media/rooms/TFTT.gif",
    "Media/rooms/TTFF.gif",
    "Media/rooms/TTFT.gif",
    "Media/rooms/TTTF.gif",
    "Media/rooms/TTTT.gif",
]


def window(
    lab,
    goku,
    current_player,
    ennemis,
    dragon_balls,
    nuage,
    senzu,
    load,
    map,
    fichier,
    fight_theme,
    play_obj,
):
    """Crée une fenêtre et dessine le labyrinthe, les ennemis et Goku gère la mécanique et touts les événements du jeu"""
    leave, main_menu, already_drawn, music, alreadySaved = (
        False,
        False,
        False,
        False,
        False,
    )
    play_obj.stop()
    play_obj = fight_theme.play()
    tombs = []
    tombs.clear()
    win = fin_partie(goku, ennemis)
    while not leave and not main_menu and win == 0:
        leave = False
        ball = None
        directions = [[None for _ in range(len(lab[0]))] for _ in range(len(lab))]
        deque = collections.deque()
        deque.append((goku["position"][0], goku["position"][1], 0, 0))
        way = goku_intention(lab, ennemis, ball, directions, deque)
        drawing(
            lab,
            goku,
            current_player,
            ennemis,
            nuage,
            senzu,
            ball,
            tombs,
            map,
            f.largeur_fenetre(),
            f.hauteur_fenetre(),
        )
        intention_draw(way, lab, f.largeur_fenetre(), f.hauteur_fenetre())
        while True and win == 0:
            if not already_drawn:
                directions = [
                    [None for _ in range(len(lab[0]))] for _ in range(len(lab))
                ]
                deque = collections.deque()
                deque.append((goku["position"][0], goku["position"][1], 0, 0))
                if way is not None:
                    for step in way:
                        f.efface("chemin" + str(step[0]) + str(step[1]))
                way = goku_intention(lab, ennemis, ball, directions, deque)
                intention_draw(way, lab, f.largeur_fenetre(), f.hauteur_fenetre())
                tombs_draw(tombs, f.largeur_fenetre(), f.hauteur_fenetre())
                goku_draw(
                    goku,
                    lab,
                    current_player,
                    map,
                    f.largeur_fenetre(),
                    f.hauteur_fenetre(),
                )
                ennemis_draw(
                    ennemis, lab, map, f.largeur_fenetre(), f.hauteur_fenetre()
                )
                nuage_draw(nuage, lab, f.largeur_fenetre(), f.hauteur_fenetre())
                senzu_draw(senzu, lab, f.largeur_fenetre(), f.hauteur_fenetre())
                ball_draw(ball, lab, f.largeur_fenetre(), f.hauteur_fenetre())
                already_drawn = True

            ev = f.donne_ev()
            ty = f.type_ev(ev)
            if ty == "Quitte":
                leave = True
                break
            elif ty == "ClicGauche":
                i, j = pixel_vers_case(
                    (f.abscisse(ev), f.ordonnee(ev)),
                    lab,
                    f.largeur_fenetre(),
                    f.hauteur_fenetre(),
                )
                pivoter(lab, (i, j))
                f.efface("a" + str(j) + str(i))
                f.image(
                    case_vers_pixel(
                        (i, j), lab, f.largeur_fenetre(), f.hauteur_fenetre()
                    )[0],
                    case_vers_pixel(
                        (i, j), lab, f.largeur_fenetre(), f.hauteur_fenetre()
                    )[1],
                    images[lab[i][j]],
                    largeur=f.largeur_fenetre() // len(lab[0]) + 1,
                    hauteur=f.hauteur_fenetre() // len(lab) + 1,
                    ancrage="center",
                    tag="map",
                )
                directions = [
                    [None for _ in range(len(lab[0]))] for _ in range(len(lab))
                ]
                deque = collections.deque()
                deque.append((goku["position"][0], goku["position"][1], 0, 0))
                if way is not None:
                    for step in way:
                        f.efface("chemin" + str(step[0]) + str(step[1]))
                way = goku_intention(lab, ennemis, ball, directions, deque)
                intention_draw(way, lab, f.largeur_fenetre(), f.hauteur_fenetre())
                tombs_draw(tombs, f.largeur_fenetre(), f.hauteur_fenetre())
                goku_draw(
                    goku,
                    lab,
                    current_player,
                    map,
                    f.largeur_fenetre(),
                    f.hauteur_fenetre(),
                )
                ennemis_draw(
                    ennemis, lab, map, f.largeur_fenetre(), f.hauteur_fenetre()
                )
                nuage_draw(nuage, lab, f.largeur_fenetre(), f.hauteur_fenetre())
                senzu_draw(senzu, lab, f.largeur_fenetre(), f.hauteur_fenetre())
                ball_draw(ball, lab, f.largeur_fenetre(), f.hauteur_fenetre())
            elif ty == "ClicDroit":
                i, j = pixel_vers_case(
                    (f.abscisse(ev), f.ordonnee(ev)),
                    lab,
                    f.largeur_fenetre(),
                    f.hauteur_fenetre(),
                )
                if dragon_balls > 0 and not ball:
                    if goku["position"] != (i, j):
                        on_ennemi = False
                        for ennemi in ennemis:
                            if ennemi["position"] == (i, j):
                                on_ennemi = True
                        if not on_ennemi:
                            ball = {
                                "position": (i, j),
                                "etoiles": f"Media/dragon_balls/dragonball{randint(1,7)}.gif",
                            }
                            already_drawn = False

            elif ty == "Touche":
                if f.touche(ev) == "space":
                    if oneTrySolve:
                        while way is not None and len(way) > 1:
                            (
                                nuage,
                                ball,
                                dragon_balls,
                                senzu,
                                died,
                                tombs,
                            ) = appliquer_chemin(
                                goku,
                                ennemis,
                                way,
                                f.largeur_fenetre(),
                                f.hauteur_fenetre(),
                                nuage,
                                ball,
                                dragon_balls,
                                senzu,
                            )
                            directions = [
                                [None for _ in range(len(lab[0]))]
                                for _ in range(len(lab))
                            ]
                            deque = collections.deque()
                            deque.append(
                                (goku["position"][0], goku["position"][1], 0, 0)
                            )
                            if way is not None:
                                for step in way:
                                    f.efface("chemin" + str(step[0]) + str(step[1]))
                            way = goku_intention(lab, ennemis, ball, directions, deque)
                            intention_draw(
                                way, lab, f.largeur_fenetre(), f.hauteur_fenetre()
                            )
                        if died or way is None:
                            if died:
                                f.efface("goku")
                                f.efface("goku_lvl")
                            goku = None
                            f.attente(2)
                            win = -1
                            tombs.clear()
                            break
                    else:
                        if way is not None:
                            (
                                nuage,
                                ball,
                                dragon_balls,
                                senzu,
                                died,
                                tombs,
                            ) = appliquer_chemin(
                                goku,
                                ennemis,
                                way,
                                f.largeur_fenetre(),
                                f.hauteur_fenetre(),
                                nuage,
                                ball,
                                dragon_balls,
                                senzu,
                            )
                            if died:
                                goku = None
                                win = -1
                                tombs.clear()
                                break
                    way = None
                    already_drawn = False
                elif f.touche(ev) == "r":
                    (
                        lab,
                        goku,
                        ennemis,
                        dragon_balls,
                        nuage,
                        senzu,
                        map,
                        leave,
                    ) = labyrinth_generator(f"maps/map{map}.txt")
                    tombs.clear()
                    f.efface_tout()
                    break
                elif f.touche(ev) == "p":
                    menu_pause(f.largeur_fenetre(), f.hauteur_fenetre())
                    f.mise_a_jour()
                    main_menu, leave, music = click_menu_pause(
                        music, play_obj, fight_theme, ball
                    )
                    if main_menu or leave:
                        break
                elif f.touche(ev) == "s":
                    save(
                        lab,
                        goku,
                        ennemis,
                        dragon_balls,
                        nuage,
                        senzu,
                        map,
                        alreadySaved,
                        load,
                        f"saved/file{fichier}.txt",
                    )
                    alreadySaved = True

            elif ty == "Redimension":
                f.efface_tout()
                drawing(
                    lab,
                    goku,
                    current_player,
                    ennemis,
                    nuage,
                    senzu,
                    ball,
                    tombs,
                    map,
                    f.largeur_fenetre(),
                    f.hauteur_fenetre(),
                )
                already_drawn = False
            f.mise_a_jour()
            if ev is not None:
                win = fin_partie(goku, ennemis)

    if win == 1:
        f.image(
            rapport(f.largeur_fenetre(), f.largeur_fenetre() / 2),
            rapport(f.hauteur_fenetre(), f.hauteur_fenetre() / 2),
            "Media/background_images/drip.gif",
            largeur=int(f.largeur_fenetre() * 1.01),
            hauteur=int(f.hauteur_fenetre() * 1.01),
            ancrage="center",
        )
        f.image(
            rapport(f.largeur_fenetre(), f.largeur_fenetre() / 2),
            rapport(f.hauteur_fenetre(), f.hauteur_fenetre() / 2),
            "Media/background_images/victory.gif",
            largeur=int(f.largeur_fenetre() * 1.01),
            hauteur=int(f.hauteur_fenetre() * 1.01),
            ancrage="center",
        )
        tombs = []
        f.mise_a_jour()
        f.attend_ev()
    elif win == -1:
        f.image(
            rapport(f.largeur_fenetre(), f.largeur_fenetre() / 2),
            rapport(f.hauteur_fenetre(), f.hauteur_fenetre() / 2),
            "Media/background_images/hhh.gif",
            largeur=int(f.largeur_fenetre() * 1.01),
            hauteur=int(f.hauteur_fenetre() * 1.01),
            ancrage="center",
        )
        f.image(
            rapport(f.largeur_fenetre(), f.largeur_fenetre() / 2),
            rapport(f.hauteur_fenetre(), f.hauteur_fenetre() / 2),
            "Media/background_images/gameover.gif",
            ancrage="center",
        )
        f.efface("goku")
        f.efface("goku_lvl")

        f.mise_a_jour()
        f.attend_ev()
    play_obj.stop()
    return leave, play_obj


def rencontre(goku, ennemis, nuage, ball, senzu):
    """Gère les rencontres entre Goku et les ennemis,nuage,senzu"""
    encounters = []
    for ennemi in ennemis:
        if goku["position"] == ennemi["position"]:
            if goku["level"] >= ennemi["level"]:
                tmp = ennemi
                ennemis.remove(ennemi)
                if goku["level"] == ennemi["level"]:
                    goku["level"] += 1
                encounters.append((1, tmp))
            else:
                encounters.append((-1, None))
    if ball is not None and goku["position"] == ball["position"]:
        encounters.append((3, ball["etoiles"]))
    if senzu and goku["position"] == senzu:
        goku["level"] += 1
        encounters.append((4, None))
    if nuage and goku["position"] == nuage:
        encounters.append((2, strongest_ennemis(ennemis)[0]))

    return encounters


def appliquer_chemin(
    goku, ennemis, chemin, width, length, nuage, ball, dragon_balls, senzu
):
    """Applique le chemin calculé par l'algorithme de plus court chemin"""
    nimbus, died = None, False

    for step in chemin:
        f.attente(0.5)
        goku["position"] = step
        f.efface("goku")
        f.efface("goku_lvl")
        encounters = rencontre(goku, ennemis, nuage, ball, senzu)
        for fight in encounters:
            if fight[0] == 1:
                tombs.append(case_vers_pixel(fight[1]["position"], lab, width, length))

                f.efface("v" + str(fight[1]["level"]))
                f.efface("v" + str(fight[1]["level"]) + "_lvl")

            elif fight[0] == -1:
                f.efface("goku")
                f.efface("goku_lvl")
                f.mise_a_jour()
                died = True
            elif fight[0] == 2:
                nimbus = fight
                goku["position"] = step
                goku_draw(goku, lab, current_player, map, width, length)
                f.efface("nuage")
                f.mise_a_jour()
                f.attente(0.5)
                break
            elif fight[0] == 3:
                goku["position"] = step
                goku_draw(goku, lab, current_player, map, width, length)
                f.efface("ball")
                f.mise_a_jour()
                f.attente(0.5)
                dragon_balls -= 1
                ball = None
            if fight[0] == 4:
                goku["position"] = step
                goku_draw(goku, lab, current_player, map, width, length)
                f.efface("senzu")
                f.mise_a_jour()
                f.attente(0.5)
                senzu = None
        if nimbus is not None:
            break

        goku_draw(goku, lab, current_player, map, width, length)
        f.efface("chemin" + str(step[0]) + str(step[1]))

    if nimbus is not None:
        for step in chemin:
            f.efface("chemin" + str(step[0]) + str(step[1]))
        goku["position"] = nimbus[1]
        f.efface("goku")
        f.efface("goku_lvl")
        fight = rencontre(goku, ennemis, nuage, ball, senzu)
        goku_draw(goku, lab, current_player, map, width, length)
        f.efface("v" + str(fight[0][1]["level"]))
        f.efface("v" + str(fight[0][1]["level"]) + "_lvl")
        tombs.append(case_vers_pixel(fight[0][1]["position"], lab, width, length))
        nuage = None
    return nuage, ball, dragon_balls, senzu, died, tombs


def fin_partie(goku, ennemis):
    """Gère la fin de partie"""
    if goku is None:
        return -1
    if len(ennemis) == 0:
        return 1
    return 0


def pivoter(donjon, position):
    """Fait pivoter la case à la position donnée"""
    i, j = position
    a, b, c, d = donjon[i][j]
    donjon[i][j] = (d, a, b, c)


def voisins(donjon, position):
    """Renvoie la liste des voisins de la case à la position donnée"""
    i, j = position
    voisins = []
    if j > 0:
        voisins.append((i, j - 1))
    if j < len(donjon[-1]) - 1:
        voisins.append((i, j + 1))
    if i > 0:
        voisins.append((i - 1, j))
    if i < len(donjon) - 1:
        voisins.append((i + 1, j))
    return voisins


def connecte(donjon, position1, position2):
    """Renvoie True si les deux cases sont connectées, False sinon"""
    i1, j1 = position1
    i2, j2 = position2
    if position2 in voisins(donjon, position1):
        if donjon[i1][j1][0] == donjon[i2][j2][2] == True and i1 > i2 and j1 == j2:
            return True
        if donjon[i1][j1][1] == donjon[i2][j2][3] == True and j1 < j2 and i1 == i2:
            return True
        if donjon[i1][j1][2] == donjon[i2][j2][0] == True and i1 < i2 and j1 == j2:
            return True
        if donjon[i1][j1][3] == donjon[i2][j2][1] == True and j1 > j2 and i1 == i2:
            return True
    return False


def intention(lab, position, ennemis, visited=set()):
    """version recursive de l'intention de l'aventurier"""
    for ennemi in ennemis:
        if ennemi["position"] == position:
            return [ennemi["position"]], ennemi["level"]
    visited.add(position)
    v = voisins(lab, position)
    temp = None
    for i in range(len(v)):
        if connecte(lab, position, v[i]) and v[i] not in visited:
            way = intention(lab, v[i], ennemis, visited)
            if way is not None:
                way = [position] + way[0], way[1]
            if temp != None and way != None:
                if temp[1] < way[1]:
                    temp = way
            elif temp is None:
                temp = way
    return temp


def check_ennemi(ennemis, position):
    """verifie si un ennemi se trouve la position fournie"""
    for ennemi in ennemis:
        if ennemi["position"] == position:
            return True
    return False


def check_dragon_balls(ball, position):
    """verifie si un tresor se trouve a la position fournie"""
    return ball is not None and ball["position"] == position


def strongest_ennemis(ennemis):
    "retourne une liste de positions des ennemis avec niveau croissant"
    position = []
    for ennemi in ennemis:
        position.append((ennemi["level"], ennemi["position"]))
    position.sort()
    return [i[1] for i in position]


def is_the_strongest_ennemi(ennemi, directions):
    """verifie si l'ennemi est accessible"""
    i, j = ennemi
    return not directions[i][j] == None


def goku_intention(lab, ennemis, ball, directions, deque):
    """retourne le chemins le plus courts vers le ennemis accessible le plus fort ou un tresor en priorité si il est accessible"""
    visited = set()
    the_goal = None
    b = True
    while len(deque) != 0:
        i, j, old_i, old_j = deque.popleft()
        if b:
            original_i, original_j = i, j
            b = not b
        if (i, j) in visited:
            continue
        visited.add((i, j))
        directions[i][j] = old_i, old_j
        if not check_ennemi(ennemis, (i, j)) and not check_dragon_balls(ball, (i, j)):
            for new_i, new_j in [(i, j - 1), (i + 1, j), (i - 1, j), (i, j + 1)]:
                if (
                    connecte(lab, (i, j), (new_i, new_j))
                    and (new_i, new_j) not in visited
                ):
                    deque.append((new_i, new_j, i, j))

    if ball is None or directions[ball["position"][0]][ball["position"][1]] is None:
        ennemis_ranking = strongest_ennemis(ennemis)
        k = len(ennemis_ranking) - 1
        while the_goal is None and k >= 0:
            if is_the_strongest_ennemi(ennemis_ranking[k], directions):
                the_goal = ennemis_ranking[k]
            k -= 1

    else:
        the_goal = ball["position"][0], ball["position"][1]
    if the_goal is not None:
        m, n = the_goal
        way = [the_goal]
        while (m, n) != (original_i, original_j):
            way.insert(0, directions[m][n])
            m, n = directions[m][n]
        return way
    return None


def int_checker(string):
    """verifie si la chaine de caractere est un entier"""
    try:
        int(string)
        return True
    except:
        return False


def position_level_extractor(ligne):
    """extrait la position d'une ligne de fichier de map"""
    tmpl = ligne[2:]
    datas = []
    data = ""
    for char in tmpl:
        if int_checker(char):
            data += char
        elif data != "":
            datas.append(int(data))
            data = ""
    return datas


def labyrinth_generator(fichier):
    """genere un labyrinthe a partir d'un fichier"""
    leave = False
    lab = []
    ennemis = []
    goku = {}
    map = 1
    dragon_balls, nuage, senzu = 3, None, None
    with open(fichier, "r", encoding="utf_8") as file:
        lines = file.readlines()
        for ligne in lines:

            L = []
            datas = position_level_extractor(ligne)
            if (
                ligne[0] != "A"
                and ligne[0] != "D"
                and ligne[0] != "T"
                and ligne[0] != "N"
                and ligne[0] != "S"
                and ligne[0] != "M"
            ):
                for char in ligne:
                    if char == "═":
                        L.append((False, True, False, True))
                    elif char == "║":
                        L.append((True, False, True, False))
                    elif char == "╔":
                        L.append((False, True, True, False))
                    elif char == "╗":
                        L.append((False, False, True, True))
                    elif char == "╚":
                        L.append((True, True, False, False))
                    elif char == "╝":
                        L.append((True, False, False, True))
                    elif char == "╠":
                        L.append((True, True, True, False))
                    elif char == "╣":
                        L.append((True, False, True, True))
                    elif char == "╦":
                        L.append((False, True, True, True))
                    elif char == "╩":
                        L.append((True, True, False, True))
                    elif char == "╨":
                        L.append((True, False, False, False))
                    elif char == "╡":
                        L.append((False, False, False, True))
                    elif char == "╥":
                        L.append((False, False, True, False))
                    elif char == "╞":
                        L.append((False, True, False, False))
                    elif char == "╬":
                        L.append((True, True, True, True))
                if L:
                    if len(lab) == 0:
                        first_line = len(L)
                    else:
                        if len(L) != first_line:
                            leave = True

                    lab.append(L)
            elif ligne[0] == "A":
                if len(datas) == 3:
                    if (0 <= datas[0] < len(lab)) and (0 <= datas[1] < first_line):
                        goku = {
                            "position": (datas[0], datas[1]),
                            "level": datas[2],
                        }
            elif ligne[0] == "D":
                if len(datas) == 3:
                    if (0 <= datas[0] < len(lab)) and (0 <= datas[1] < first_line):
                        ennemis.append(
                            {
                                "position": (datas[0], datas[1]),
                                "level": datas[2],
                            }
                        )
            elif ligne[0] == "T":
                if len(datas) == 1:
                    dragon_balls = int(ligne[2])
            elif ligne[0] == "N":
                if (
                    len(datas) == 2
                ):
                    if (0 <= datas[0] < len(lab)) and (
                        0 <= datas[1] < first_line
                    ):
                        nuage = (int(ligne[2]), int(ligne[4]))
            elif ligne[0] == "S":
                if (
                    len(datas) == 2
                ):
                    if (0 <= datas[0] < len(lab)) and (
                        0 <= datas[1] < first_line
                    ):
                        senzu = (int(ligne[2]), int(ligne[4]))
            elif ligne[0] == "M":
                if ligne[2] in '1234' and int_checker(ligne[2]):
                    map = int(ligne[2])
    return lab, goku, ennemis, dragon_balls, nuage, senzu, map, leave


def save(
    lab, goku, ennemis, dragon_balls, nuage, senzu, map, alreadySaved, load, fichier
):
    """sauvegarde la partie en cours dans un fichiers de même format que les maps originals"""
    if not load:
        if os.path.exists("saved/saved_files.txt"):
            with open("saved/saved_files.txt", "r") as file:
                count = len(file.readlines()) + 1
                file.close()
        else:
            count = 1
        if alreadySaved:
            count -= 1
        with open("saved/saved_files.txt", "a+") as file:
            if not alreadySaved and count < 5:
                file.write("saved/file" + str(count) + ".txt" + "\n")
                file.close()
        if count > 5:
            count = 1
        fich = "saved/file" + str(count) + ".txt"
    else:
        fich = fichier

    with open(fich, "w") as file:
        for row in lab:
            for room in row:
                if room == (False, False, False, False):
                    file.write(" ")
                if room == (False, True, False, True):
                    file.write("═")
                elif room == (True, False, True, False):
                    file.write("║")
                elif room == (False, True, True, False):
                    file.write("╔")
                elif room == (False, False, True, True):
                    file.write("╗")
                elif room == (True, True, False, False):
                    file.write("╚")
                elif room == (True, False, False, True):
                    file.write("╝")
                elif room == (True, True, True, False):
                    file.write("╠")
                elif room == (True, False, True, True):
                    file.write("╣")
                elif room == (False, True, True, True):
                    file.write("╦")
                elif room == (True, True, False, True):
                    file.write("╩")
                elif room == (True, False, False, False):
                    file.write("╨")
                elif room == (False, False, False, True):
                    file.write("╡")
                elif room == (False, False, True, False):
                    file.write("╥")
                elif room == (False, True, False, False):
                    file.write("╞")
                elif room == (True, True, True, True):
                    file.write("╬")
            file.write("\n")
        file.write(
            "A "
            + str(goku["position"][0])
            + " "
            + str(goku["position"][1])
            + " "
            + str(goku["level"])
            + "\n"
        )
        for ennemi in ennemis:
            file.write(
                "D "
                + str(ennemi["position"][0])
                + " "
                + str(ennemi["position"][1])
                + " "
                + str(ennemi["level"])
                + "\n"
            )
        if nuage is not None:
            file.write("N " + str(nuage[0]) + " " + str(nuage[1]) + ("\n"))
        if senzu is not None:
            file.write("S " + str(senzu[0]) + " " + str(senzu[1]) + ("\n"))
        file.write("M " + str(map) + "\n")
        file.write("T " + str(dragon_balls))
        file.close()


def click_game_options(oneTrySolve):
    """renvoie activation ou pas du mode de jeu one try solve par le joueur"""
    back = False
    leave, quit = False, False
    width, length = f.largeur_fenetre(), f.hauteur_fenetre()
    game_options(width, length)
    f.mise_a_jour()

    while True:
        ev = f.donne_ev()
        ty = f.type_ev(ev)

        if ty == "Quitte":
            quit = True
            break
        elif ty == "ClicGauche":
            x, y = f.abscisse(ev), f.ordonnee(ev)
            if rapport(width, 95) <= x <= rapport(width, 215) and rapport(
                length, 190
            ) <= y <= rapport(length, 260):
                oneTrySolve = True
                leave = True
            elif rapport(width, 372) <= x <= rapport(width, 487) and rapport(
                length, 190
            ) <= y <= rapport(length, 260):
                oneTrySolve = False
                leave = True
            elif rapport(width, 16) <= x <= rapport(width, 85) and 26 <= y <= rapport(
                length, 68
            ):
                back = True

            elif rapport(width, 180) <= x <= rapport(width, 400) and rapport(
                length, 480
            ) <= y <= rapport(length, 560):
                leave = True
        elif ty == "Redimension":
            f.efface_tout()
            width = f.largeur_fenetre()
            length = f.hauteur_fenetre()
            game_options(width, length)
        if leave or back or quit:
            break
        f.mise_a_jour()

    return oneTrySolve, leave, back, quit


def click_save_menu(saved_files):
    """gére les clique sur le menu des sauvegarde et renvoie de le fichier choisi"""
    back, leave = False, False
    fichier = None
    width, length = f.largeur_fenetre(), f.hauteur_fenetre()
    save_menu(width, length, saved_files)
    f.mise_a_jour()
    while True:
        ev = f.donne_ev()
        ty = f.type_ev(ev)
        if ty == "Quitte":
            leave = True, True
            break
        elif ty == "ClicGauche":
            x, y = f.abscisse(ev), f.ordonnee(ev)
            if 0 <= x <= rapport(width, 50) and 0 <= y <= rapport(length, 45):
                back = True
                break
            elif rapport(width, 20) <= x <= rapport(width, 580) and saved_files:
                if rapport(length, 50) <= y <= rapport(length, 150):
                    fichier = 1
                elif rapport(length, 155) <= y <= rapport(length, 255):
                    fichier = 2
                elif rapport(length, 260) <= y <= rapport(length, 360):
                    fichier = 3
                elif rapport(length, 365) <= y <= rapport(length, 465):
                    fichier = 4
                elif rapport(length, 470) <= y <= rapport(length, 570):
                    fichier = 5
                leave = True
        elif ty == "Redimension":
            f.efface_tout()
            f.mise_a_jour()
            width = f.largeur_fenetre()
            length = f.hauteur_fenetre()
            save_menu(width, length, saved_files)
        if leave or back:
            break
        f.mise_a_jour()
    return fichier, leave, back


def click_menu_pause(music, play_obj, fight_theme, ball):
    """gére les clique sur le menu de pause et renvoie les option choisi"""
    main_menu = False
    leave = False
    width, length = f.largeur_fenetre(), f.hauteur_fenetre()
    menu_pause(width, length)
    while True:
        ev = f.donne_ev()
        ty = f.type_ev(ev)
        if ty == "Quitte":
            leave, quit = True, True
            break
        elif ty == "ClicGauche":
            x, y = f.abscisse(ev), f.ordonnee(ev)
            if rapport(width, 140) <= x <= rapport(width, 343) and rapport(
                length, 225
            ) <= y <= rapport(
                length, 254
            ):  # Resume
                f.efface("pause")
                f.efface_tout()
                drawing(
                    lab,
                    goku,
                    current_player,
                    ennemis,
                    nuage,
                    senzu,
                    ball,
                    tombs,
                    map,
                    f.largeur_fenetre(),
                    f.hauteur_fenetre(),
                )
                f.mise_a_jour()
                break
            elif rapport(width, 210) <= x <= rapport(width, 390) and rapport(
                length, 293
            ) <= y <= rapport(
                length, 321
            ):  # return to main_menu
                main_menu = True
                play_obj.stop()
                break
            elif rapport(width, 140) <= x <= rapport(width, 269) and rapport(
                length, 430
            ) <= y <= rapport(
                length, 462
            ):  # Quit
                leave = True
                break
            elif rapport(width, 368) <= x <= rapport(width, 424) and rapport(
                length, 353
            ) <= y <= rapport(
                length, 396
            ):  # Music on
                if not music:
                    music = True
                    play_obj.stop()
                    play_obj = fight_theme.play()
            elif rapport(width, 462) <= x <= rapport(width, 514) and rapport(
                length, 353
            ) <= y <= rapport(
                length, 396
            ):  # Music off
                music = False
                play_obj.stop()
        elif ty == "Redimension":
            f.efface("pause")
            f.mise_a_jour()
            width = f.largeur_fenetre()
            length = f.hauteur_fenetre()
            menu_pause(width, length)
        f.mise_a_jour()
    f.mise_a_jour()
    return main_menu, leave, music


def menu(play_obj):
    """gére le menu du jeu et renvoie les option choisi par le joueur"""
    map = 1
    character = 0
    current_player = "goku"
    leave, oneTrySolve, load, quit, created = False, False, False, False, False
    fight_theme = theme1_wave_obj
    music = True
    play_obj = home_wave_obj.play()
    fichier = None
    start_menu(f.largeur_fenetre(), f.hauteur_fenetre())
    while True:
        width, length = f.largeur_fenetre(), f.hauteur_fenetre()

        f.mise_a_jour()
        ev1 = f.donne_ev()
        ty1 = f.type_ev(ev1)

        if ty1 == "Quitte":
            leave, quit = True, True
            break
        elif ty1 == "ClicGauche":
            x, y = f.abscisse(ev1), f.ordonnee(ev1)

            if rapport(width, 22) <= x <= rapport(width, 150) and rapport(
                length, 305
            ) <= y <= rapport(
                length, 350
            ):  # Play Game
                new_or_save(width, length)
                f.mise_a_jour()
                while True:
                    width, length = f.largeur_fenetre(), f.hauteur_fenetre()
                    ev4 = f.donne_ev()
                    ty4 = f.type_ev(ev4)

                    if ty4 == "Quitte":
                        leave, quit = True, True
                        break
                    elif ty4 == "ClicGauche":
                        x, y = f.abscisse(ev4), f.ordonnee(ev4)
                        if rapport(width, 175) <= x <= rapport(width, 425) and rapport(
                            length, 360
                        ) <= y <= rapport(length, 420):
                            choose_createmap(width, length)
                            f.mise_a_jour()
                            while True:
                                ev1 = f.donne_ev()
                                ty1 = f.type_ev(ev1)
                                if ty1 == "Quitte":
                                    leave, quit = True, True
                                    break
                                elif ty1 == "ClicGauche":
                                    x, y = f.abscisse(ev1), f.ordonnee(ev1)
                                    if rapport(width, 152) <= x <= rapport(
                                        width, 445
                                    ) and rapport(length, 365) <= y <= rapport(
                                        length, 420
                                    ):
                                        created = True
                                        leave = True
                                        break
                                    elif rapport(width, 152) <= x <= rapport(
                                        width, 445
                                    ) and rapport(length, 274) <= y <= rapport(
                                        length, 327
                                    ):
                                        menu_to_choose_map(width, length)
                                        f.mise_a_jour()
                                        load = False
                                        # sequel
                                        while True:
                                            width, length = (
                                                f.largeur_fenetre(),
                                                f.hauteur_fenetre(),
                                            )
                                            ev2 = f.donne_ev()
                                            ty2 = f.type_ev(ev2)
                                            if ty2 == "Quitte":
                                                leave, quit = True, True
                                                break
                                            elif ty2 == "ClicGauche":
                                                x, y = f.abscisse(ev2), f.ordonnee(ev2)
                                                back = False
                                                if rapport(width, 105) <= x <= rapport(
                                                    width, 210
                                                ) and rapport(
                                                    length, 186
                                                ) <= y <= rapport(
                                                    length, 298
                                                ):
                                                    # Tray of 3
                                                    map = 1
                                                    (
                                                        oneTrySolve,
                                                        leave,
                                                        back,
                                                        quit,
                                                    ) = click_game_options(oneTrySolve)
                                                elif rapport(
                                                    width, 105
                                                ) <= x <= rapport(
                                                    width, 210
                                                ) and rapport(
                                                    length, 378
                                                ) <= y <= rapport(
                                                    length, 491
                                                ):
                                                    # Tray of 9
                                                    map = 3
                                                    (
                                                        oneTrySolve,
                                                        leave,
                                                        back,
                                                        quit,
                                                    ) = click_game_options(oneTrySolve)
                                                elif rapport(
                                                    width, 410
                                                ) <= x <= rapport(
                                                    width, 518
                                                ) and rapport(
                                                    length, 378
                                                ) <= y <= rapport(
                                                    length, 491
                                                ):
                                                    # Tray of 12
                                                    map = 4
                                                    (
                                                        oneTrySolve,
                                                        leave,
                                                        back,
                                                        quit,
                                                    ) = click_game_options(oneTrySolve)

                                                elif rapport(
                                                    width, 410
                                                ) <= x <= rapport(
                                                    width, 518
                                                ) and rapport(
                                                    length, 186
                                                ) <= y <= rapport(
                                                    length, 298
                                                ):
                                                    # Tray of 6
                                                    map = 2
                                                    (
                                                        oneTrySolve,
                                                        leave,
                                                        back,
                                                        quit,
                                                    ) = click_game_options(oneTrySolve)

                                                elif rapport(width, 16) <= x <= rapport(
                                                    width, 85
                                                ) and 26 <= y <= rapport(length, 68):
                                                    choose_createmap(width, length)
                                                    f.mise_a_jour()
                                                    break
                                                if back:
                                                    menu_to_choose_map(width, length)
                                                    f.mise_a_jour()
                                                    continue
                                                if leave:
                                                    break

                                            elif ty2 == "Redimension":
                                                f.efface_tout()
                                                width = f.largeur_fenetre()
                                                length = f.hauteur_fenetre()
                                                menu_to_choose_map(width, length)
                                            if leave:
                                                break
                                            f.mise_a_jour()
                                    elif rapport(width, 16) <= x <= rapport(
                                        width, 85
                                    ) and 26 <= y <= rapport(length, 68):
                                        new_or_save(width, length)
                                        f.mise_a_jour()
                                        break
                                elif ty1 == "Redimension":
                                    f.efface_tout()
                                    width = f.largeur_fenetre()
                                    length = f.hauteur_fenetre()
                                    choose_createmap(width, length)
                                if leave:
                                    break
                                f.mise_a_jour()
                        elif rapport(width, 175) <= x <= rapport(
                            width, 425
                        ) and rapport(length, 273) <= y <= rapport(length, 331):
                            saved_files = []
                            with open("saved/saved_files.txt", "r") as file:
                                lines = file.readlines()
                                for line in lines:
                                    fichier = line.strip()
                                    modify_time = os.path.getmtime(fichier)
                                    modify_date = datetime.datetime.fromtimestamp(
                                        modify_time
                                    )
                                    saved_files.append(
                                        (
                                            fichier,
                                            modify_date.strftime("%d/%m/%Y %H:%M:%S"),
                                        )
                                    )
                                file.close()
                            load = True
                            fichier, leave, back = click_save_menu(saved_files)
                            if back:
                                new_or_save(f.largeur_fenetre(), f.hauteur_fenetre())
                                load = False
                                f.mise_a_jour()
                                continue
                            if leave and fichier is None:
                                quit = True
                            return (
                                map,
                                character,
                                music,
                                oneTrySolve,
                                load,
                                fichier,
                                quit,
                                created,
                                current_player,
                                fight_theme,
                                play_obj,
                            )
                        elif 0 <= x <= rapport(width, 50) and 0 <= y <= rapport(
                            length, 45
                        ):
                            start_menu(width, length)
                            f.mise_a_jour()
                            break

                    elif ty4 == "Redimension":
                        f.efface_tout()
                        width = f.largeur_fenetre()
                        length = f.hauteur_fenetre()
                        new_or_save(width, length)
                    if leave:
                        break
                    f.mise_a_jour()
            elif rapport(width, 22) <= x <= rapport(width, 270) and rapport(
                length, 370
            ) <= y <= rapport(
                length, 412
            ):  # Settings
                settings(width, length)
                f.mise_a_jour()
                while True:
                    width, length = f.largeur_fenetre(), f.hauteur_fenetre()
                    ev2 = f.donne_ev()
                    ty2 = f.type_ev(ev2)
                    if ty2 == "Quitte":
                        leave, quit = True, True
                    elif ty2 == "ClicGauche":
                        x, y = f.abscisse(ev2), f.ordonnee(ev2)
                        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~é
                        if rapport(width, 307) <= x <= rapport(width, 343) and rapport(
                            length, 199
                        ) <= y <= rapport(
                            length, 255
                        ):  # player
                            character -= 1
                            current_player = players[character % (len(players))]
                            f.efface("player")
                            f.image(
                                rapport(width, 428),
                                rapport(length, 227),
                                f"Media/characters/players/{current_player}.gif",
                                largeur=int(rapport(width, 400)),
                                hauteur=int(rapport(length, 400)),
                                ancrage="center",
                                tag="player",
                            )
                        elif rapport(width, 514) <= x <= rapport(
                            width, 549
                        ) and rapport(length, 199) <= y <= rapport(length, 255):
                            character += 1
                            current_player = players[character % (len(players))]
                            f.efface("player")
                            f.image(
                                rapport(width, 428),
                                rapport(length, 227),
                                f"Media/characters/players/{current_player}.gif",
                                largeur=int(rapport(width, 400)),
                                hauteur=int(rapport(length, 400)),
                                ancrage="center",
                                tag="player",
                            )
                        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        # ~~~goku_forms[goku["level"]]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        elif rapport(width, 357) <= x <= rapport(
                            width, 391
                        ) and rapport(  #  MUSIC THEME
                            length, 384
                        ) <= y <= rapport(
                            length, 436
                        ):
                            music = True
                            play_obj.stop()
                            play_obj = theme1_wave_obj.play()
                            fight_theme = theme1_wave_obj
                        elif rapport(width, 427) <= x <= rapport(
                            width, 490
                        ) and rapport(length, 384) <= y <= rapport(length, 436):
                            music = True
                            play_obj.stop()
                            play_obj = theme2_wave_obj.play()
                            fight_theme = theme2_wave_obj
                        elif rapport(width, 525) <= x <= rapport(
                            width, 584
                        ) and rapport(length, 384) <= y <= rapport(length, 436):
                            music = True
                            play_obj.stop()
                            play_obj = theme3_wave_obj.play()
                            fight_theme = theme3_wave_obj

                        elif rapport(width, 1) <= x <= rapport(width, 30) and rapport(
                            length, 580
                        ) <= y <= rapport(length, 600):
                            current_player = "monaka"
                            f.efface("player")
                            f.image(
                                rapport(width, 428),
                                rapport(length, 227),
                                "Media/characters/players/monaka.gif",
                                largeur=int(rapport(width, 400)),
                                hauteur=int(rapport(length, 400)),
                                ancrage="center",
                                tag="player",
                            )
                        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        elif rapport(width, 215) <= x <= rapport(  # MUSIC ON / OFF
                            width, 265
                        ) and rapport(length, 284) <= y <= rapport(length, 328):
                            if not music:
                                music = True
                                play_obj.stop()
                                play_obj = home_wave_obj.play()
                        elif rapport(width, 338) <= x <= rapport(
                            width, 391
                        ) and rapport(length, 284) <= y <= rapport(length, 328):
                            music = False
                            play_obj.stop()

                        elif rapport(width, 16) <= x <= rapport(
                            width, 85
                        ) and 26 <= y <= rapport(length, 68):
                            start_menu(width, length)
                            play_obj.stop()
                            play_obj = home_wave_obj.play()
                            break
                        f.mise_a_jour()

                    elif ty2 == "Redimension":
                        f.efface_tout()
                        width = f.largeur_fenetre()
                        length = f.hauteur_fenetre()
                        settings(width, length)
                    if leave:
                        break
                    f.mise_a_jour()

            elif rapport(width, 22) <= x <= rapport(width, 161) and rapport(
                length, 430
            ) <= y <= rapport(
                length, 461
            ):  # Leave Game
                quit = True
                break
        elif ty1 == "Redimension":
            f.efface_tout()
            width = f.largeur_fenetre()
            length = f.hauteur_fenetre()
            start_menu(width, length)
        if leave or quit:
            break
        f.mise_a_jour()

    return (
        map,
        character,
        music,
        oneTrySolve,
        load,
        fichier,
        quit,
        created,
        current_player,
        fight_theme,
        play_obj,
    )


if __name__ == "__main__":
    f.cree_fenetre(600, 600, redimension=True)
    play_obj = home_wave_obj.play()
    play_obj.stop()
    main_menu = False
    leave = False
    music = False
    dragon_balls = 3
    while not leave:
        (
            map,
            character,
            music,
            oneTrySolve,
            load,
            fichier,
            quit,
            created,
            current_player,
            fight_theme,
            play_obj,
        ) = menu(play_obj)

        if not quit:
            if load:
                (
                    lab,
                    goku,
                    ennemis,
                    dragon_balls,
                    nuage,
                    senzu,
                    map,
                    leave,
                ) = labyrinth_generator(f"saved/file{fichier}.txt")
                if leave:
                    leave = False
                    continue
            else:
                if created:
                    f.image(
                        300, 300, "Media/background_images/instructions.gif", ancrage="center"
                    )
                    f.attend_clic_gauche()
                    try:
                        (
                            lab,
                            goku,
                            ennemis,
                            nuage,
                            senzu,
                            map,
                            quit,
                            leave,
                            oneTrySolve,
                        ) = editeur_donjon(donjon, chemin_edit, play_obj)
                    except TypeError:
                        leave = True
                        continue

                    if leave:
                        leave = False
                        continue
                    if quit:
                        leave = True

                else:
                    (
                        lab,
                        goku,
                        ennemis,
                        dragon_balls,
                        nuage,
                        senzu,
                        map,
                        leave,
                    ) = labyrinth_generator(f"Media/maps/map{map}.txt")
                    if leave:
                        play_obj.stop()
                        leave = False
                        continue
            f.efface_tout()

            leave, play_obj = window(
                lab,
                goku,
                current_player,
                ennemis,
                dragon_balls,
                nuage,
                senzu,
                load,
                map,
                fichier,
                fight_theme,
                play_obj,
            )
        else:
            leave = True
            f.ferme_fenetre()

    # menu_pause(f.largeur_fenetre(), f.hauteur_fenetre())
    # while True:
    #     ev = f.attend_ev()
    #     ty = f.type_ev(ev)
    #     if ty == "Redimension":

    #         menu_pause(f.largeur_fenetre(), f.hauteur_fenetre())
    #     elif ty == "Quitte":
    #         f.ferme_fenetre()
    #         break
    #     f.mise_a_jour()


# menu sauvegarde
