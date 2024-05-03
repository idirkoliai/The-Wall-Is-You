import fltk as f
import os

donjon = [[None for _ in range(6)] for _ in range(6)]


def pixel_vers_case(pixel, width, length):
    """Renvoie la case correspondant au pixel"""
    return int(pixel[1] // (length / 6)), int(pixel[0] // (width / 6))


def case_vers_pixel(case, width, length):
    """Renvoie le pixel correspondant à la case"""
    i, j = case
    return (j + 0.5) * (width / 6), (i + 0.5) * (length / 6)


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
db_villains = {
    1: "Media/characters/db_villains/v1.gif",
    2: "Media/characters/db_villains/v2.gif",
    3: "Media/characters/db_villains/v3.gif",
    4: "Media/characters/db_villains/v4.gif",
    5: "Media/characters/db_villains/v5.gif",
}
chemins_dico = {
    (False, False, False, True): "Media/rooms/FFFT.gif",
    (False, False, True, False): "Media/rooms/FFTF.gif",
    (False, False, True, True): "Media/rooms/FFTT.gif",
    (False, True, False, False): "Media/rooms/FTFF.gif",
    (False, True, False, True): "Media/rooms/FTFT.gif",
    (False, True, True, False): "Media/rooms/FTTF.gif",
    (False, True, True, True): "Media/rooms/FTTT.gif",
    (True, False, False, False): "Media/rooms/TFFF.gif",
    (True, False, False, True): "Media/rooms/TFFT.gif",
    (True, False, True, False): "Media/rooms/TFTF.gif",
    (True, False, True, True): "Media/rooms/TFTT.gif",
    (True, True, False, False): "Media/rooms/TTFF.gif",
    (True, True, False, True): "Media/rooms/TTFT.gif",
    (True, True, True, False): "Media/rooms/TTTF.gif",
    (True, True, True, True): "Media/rooms/TTTT.gif",
}
ennemis = [None for _ in range(5)]


def grille(width, length):
    """dessine une grille"""
    f.rectangle(0, 0, width, length, couleur="black", remplissage="white")
    for i in range(width // 6):
        for j in range(length // 6):
            f.rectangle(
                i * width // 6,
                i * length // 6,
                (j + 1) * width // 6,
                (j + 1) * length // 6,
            )


def valid_map(donjon):
    """verifie si la map crée par le joueur est valide"""
    for row in donjon:
        for room in row:
            if room is None:
                return False
    return True


def editeur_donjon(donjon, chemin_edit, play_obj):
    """permet au joueur de créer un donjon et renvoie les donnees du donjon"""
    senzu, nuage, map = None, None, None
    oneTrySolve = False
    quit, leave = False, False
    grille(600, 600)
    while True:
        ev = f.donne_ev()
        ty = f.type_ev(ev)
        if ty == "Quitte":
            quit = True
            break
        elif ty == "ClicGauche":
            i, j = pixel_vers_case((f.abscisse(ev), f.ordonnee(ev)), 600, 600)
            result = draw_choice(chemin_edit)
            x, y = case_vers_pixel((i, j), 600, 600)
            f.image(x, y, result[1], ancrage="center", hauteur=100, largeur=100)
            donjon[i][j] = result[0]
        elif ty == "Touche":
            if f.touche(ev) == "a" and valid_map(donjon):
                f.efface("goku")
                x, y = f.attend_clic_gauche()
                i, j = pixel_vers_case((x, y), 600, 600)
                x, y = case_vers_pixel((i, j), 600, 600)
                goku = {"position": (i, j), "level": 1}
                f.image(
                    x,
                    y,
                    "Media/characters/Goku/g1.gif",
                    hauteur=100,
                    largeur=100,
                    ancrage="center",
                    tag="goku",
                )
            elif f.touche(ev) == "v" and valid_map(donjon):
                while True:
                    ev1 = f.donne_ev()
                    ty2 = f.type_ev(ev1)
                    if ty2 == "Touche":
                        touche = f.touche(ev1)
                        if touche[:2] == "KP" and touche[-1] in "12345":
                            f.efface("v" + touche[-1])
                            x, y = f.attend_clic_gauche()
                            i, j = pixel_vers_case((x, y), 600, 600)
                            x, y = case_vers_pixel((i, j), 600, 600)
                            ennemis[int(touche[-1]) - 1] = {
                                "position": (i, j),
                                "level": int(touche[-1]),
                            }
                            f.image(
                                x,
                                y,
                                "Media/characters/db_villains/v" + touche[-1] + ".gif",
                                largeur=150,
                                hauteur=150,
                                ancrage="center",
                                tag="v" + touche[-1],
                            )
                        elif touche == "Return":
                            break
                    f.mise_a_jour()
            elif f.touche(ev) == "o" and valid_map(donjon):
                oneTrySolve = True
            elif f.touche(ev) == "s" and valid_map(donjon):
                f.efface("senzu")
                x, y = f.attend_clic_gauche()
                i, j = pixel_vers_case((x, y), 600, 600)
                x, y = case_vers_pixel((i, j), 600, 600)
                senzu = (i, j)
                f.image(x, y, "Media/senzu.gif", largeur = 300, hauteur= 300, ancrage="center", tag="senzu")
            elif f.touche(ev) == "n" and valid_map(donjon):
                f.efface("nuage")
                x, y = f.attend_clic_gauche()
                i, j = pixel_vers_case((x, y), 600, 600)
                x, y = case_vers_pixel((i, j), 600, 600)
                nuage = (i, j)
                f.image(
                    x,
                    y,
                    "Media/nuage.gif",
                    hauteur=60,
                    largeur=60,
                    ancrage="center",
                    tag="nuage",
                )
            elif f.touche(ev) == "m" and valid_map(donjon):
                while True:
                    ev = f.donne_ev()
                    ty = f.type_ev(ev)
                    if ty == "Touche":
                        touche = f.touche(ev)
                        if touche[:2] == "KP" and touche[-1] in "1234":
                            map = int(touche[-1])
                            break
                    f.mise_a_jour()

            elif (
                f.touche(ev) == "Return"
                and valid_map(donjon)
                and ennemis
                and goku
                and map is not None
            ):
                return donjon, goku, ennemis, nuage, senzu, map, quit, leave, oneTrySolve
            elif f.touche(ev) == "q":
                play_obj.stop()
                leave = True
                break

        f.mise_a_jour()
    if leave:
        return None, None, None, None, None, None, None, leave, False


def draw_choice(chemin_edit):
    """dessine la case choisie par le joueur"""
    tags = []
    f.rectangle(0, 0, 600, 600, couleur="black", remplissage="black", tag="bg")
    f.image(
        300, 480, "Media/background_images/selectaroom.gif", ancrage="center", tag="select"
    )

    j = 0
    x, y = 60, 60
    while j < 15:
        f.image(
            x % 600,
            y,
            chemin_edit[j],
            hauteur=120,
            largeur=120,
            tag="im" + str(x) + str(y),
        )
        tags.append("im" + str(x) + str(y))
        x += 120
        if x >= 600:
            y += 120
            x = 60
        j += 1
    result = clique_choice_room(chemin_edit)
    for tag in tags:
        f.efface(tag)
    f.efface("bg")
    f.efface("select")
    return result


def clique_choice_room(chemin_edit):
    """gere les clique de l'aventurier pour choisir une case du donjon"""
    clique = f.attend_clic_gauche()
    i, j = int(clique[1] // 120), int(clique[0] // 120)
    if not (0 <= i <= 2 and 0 <= j <= 5):
        while not (0 <= i <= 2 and 0 <= j <= 5):
            clique = f.attend_clic_gauche()
            i, j = int(clique[1] // 120), int(clique[0] // 120)
    for room in chemins_dico:
        if chemins_dico[room] == chemin_edit[5 * i + j]:
            return (room, chemin_edit[5 * i + j])


# f.cree_fenetre(600,600)
# try:
#     lab , goku, ennemis, nuage, senzu, map = editeur_donjon(donjon, chemin_edit)
# except TypeError:
#     pass
# f.attend_fermeture()
