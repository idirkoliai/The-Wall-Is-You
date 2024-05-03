import fltk as f
import collections
import simpleaudio as sa
from donjon_editor import *        
import datetime                                # pour la date de sauvegarde
from random import randint            


# fichier regroupant toutes les fonctions purement graphiques du jeu
images = {  # dictionnaire des images des cases du labyrinthe
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

players = ["goku", "gohan"]          # liste des personnages jouables

gohan_forms = {  # dictionnaire des images de gohan de chaque map
    1: {
        1: "Media/characters/Gohan/g1.gif",
        2: "Media/characters/Gohan/g1.gif",
        3: "Media/characters/Gohan/g1.gif",
        4: "Media/characters/Gohan/g1.gif",
        5: "Media/characters/Gohan/g1.gif",
        6: "Media/characters/Gohan/g1.gif",
    },
    2: {
        1: "Media/characters/Gohan/g1.gif",
        2: "Media/characters/Gohan/g2.gif",
        3: "Media/characters/Gohan/g3.gif",
        4: "Media/characters/Gohan/g4.gif",
        5: "Media/characters/Gohan/g5.gif",
        6: "Media/characters/Gohan/g5.gif",
    },
    3: {
        1: "Media/characters/Gohan/g1.gif",
        2: "Media/characters/Gohan/g2.gif",
        3: "Media/characters/Gohan/g3.gif",
        4: "Media/characters/Gohan/g4.gif",
        5: "Media/characters/Gohan/g5.gif",
        6: "Media/characters/Gohan/g5.gif",
    },
    4: {
        1: "Media/characters/Gohan/g1.gif",
        2: "Media/characters/Gohan/g2.gif",
        3: "Media/characters/Gohan/g3.gif",
        4: "Media/characters/Gohan/g4.gif",
        5: "Media/characters/Gohan/g5.gif",
        6: "Media/characters/Gohan/g5.gif",
    },
}
goku_forms = {  # dictionnaire des images de goku de chaque map
    1: {       
        1: "Media/characters/Goku/g1.gif",
        2: "Media/characters/Goku/g1.gif",
        3: "Media/characters/Goku/g1.gif",
        4: "Media/characters/Goku/g1.gif",
        5: "Media/characters/Goku/g1.gif",
        6: "Media/characters/Goku/g1.gif",
    },
    2: {       
        1: "Media/characters/Goku/g1.gif",
        2: "Media/characters/Goku/g2.gif",
        3: "Media/characters/Goku/g3.gif",
        4: "Media/characters/Goku/g4.gif",
        5: "Media/characters/Goku/g5.gif",
        6: "Media/characters/Goku/g5.gif",
    },
    3: {    
        1: "Media/characters/Goku/g6.gif",
        2: "Media/characters/Goku/g7.gif",
        3: "Media/characters/Goku/g8.gif",
        4: "Media/characters/Goku/g9.gif",
        5: "Media/characters/Goku/g10.gif",
        6: "Media/characters/Goku/g10.gif",
    },
    4: {     
        1: "Media/characters/Goku/g6.gif",
        2: "Media/characters/Goku/g7.gif",
        3: "Media/characters/Goku/g8.gif",
        4: "Media/characters/Goku/g9.gif",
        5: "Media/characters/Goku/g10.gif",
        6: "Media/characters/Goku/g10.gif",
    },
}
monaka_forms = {  # dictionnaire des images de monaka de chaque map
    1: {         # monaka n'a qu'une seule image
        1: "Media/characters/players/monaka.gif",
        2: "Media/characters/players/monaka.gif",
        3: "Media/characters/players/monaka.gif",         
        4: "Media/characters/players/monaka.gif",
        5: "Media/characters/players/monaka.gif",
        6: "Media/characters/players/monaka.gif",
    },
    2: {     
        1: "Media/characters/players/monaka.gif",
        2: "Media/characters/players/monaka.gif",
        3: "Media/characters/players/monaka.gif",
        4: "Media/characters/players/monaka.gif",
        5: "Media/characters/players/monaka.gif",
        6: "Media/characters/players/monaka.gif",
    },
    3: {
        1: "Media/characters/players/monaka.gif",
        2: "Media/characters/players/monaka.gif",
        3: "Media/characters/players/monaka.gif",
        4: "Media/characters/players/monaka.gif",
        5: "Media/characters/players/monaka.gif",
        6: "Media/characters/players/monaka.gif",
    },
    4: {
        1: "Media/characters/players/monaka.gif",
        2: "Media/characters/players/monaka.gif",
        3: "Media/characters/players/monaka.gif",
        4: "Media/characters/players/monaka.gif",
        5: "Media/characters/players/monaka.gif",
        6: "Media/characters/players/monaka.gif",
    },
}

player = {
    "goku": goku_forms,
    "gohan": gohan_forms,
    "monaka": monaka_forms,
}  # dictionnaire des images de chaque personnage

db_villains = {  # dictionnaire des images des ennemis de db
    1: "Media/characters/db_villains/v1.gif",
    2: "Media/characters/db_villains/v2.gif",
    3: "Media/characters/db_villains/v3.gif",
    4: "Media/characters/db_villains/v4.gif",
    5: "Media/characters/db_villains/v5.gif",
}
dbz_villains = {  # dictionnaire des images des ennemis de dbz
    1: "Media/characters/dbz_villains/v1.gif",
    2: "Media/characters/dbz_villains/v2.gif",
    3: "Media/characters/dbz_villains/v3.gif",
    4: "Media/characters/dbz_villains/v4.gif",
    5: "Media/characters/dbz_villains/v5.gif",
}
dbs_villains = {  # dictionnaire des images des ennemis de dbs
    1: "Media/characters/dbs_villains/v1.gif",
    2: "Media/characters/dbs_villains/v2.gif",
    3: "Media/characters/dbs_villains/v3.gif",
    4: "Media/characters/dbs_villains/v4.gif",
    5: "Media/characters/dbs_villains/v5.gif",
}

non_db_villains = {  # dictionnaire des images des ennemis de non db
    1: "Media/characters/non_db_villains/v1.gif",
    2: "Media/characters/non_db_villains/v2.gif",
    3: "Media/characters/non_db_villains/v3.gif",
    4: "Media/characters/non_db_villains/v4.gif",
    5: "Media/characters/non_db_villains/v5.gif",
}

villains = {  # dictionnaire des images des ennemis de chaque map
    1: db_villains,
    2: dbz_villains,
    3: dbs_villains,
    4: non_db_villains,
}


def rapport(
    taille, x
):  # fonction qui permet de garder les memes proportions pour les images
    return taille / (600 / x)


def save_menu(width, length, saved_files):
    """dessine le menu de sauvegarde"""
    y = rapport(length, 50)
    f.image(  # dessine le fond
        rapport(width, 300),
        rapport(length, 300),
        "Media/background_images/background.gif",
        largeur=int(width * 1.01),
        hauteur=int(length * 1.01),
        ancrage="center",
    )
    f.image(  # dessine le bouton de retour
        rapport(width, 25),
        rapport(length, 20),
        "Media/background_images/return_button.gif",
        largeur=int(rapport(width, 50)),
        hauteur=int(rapport(length, 50)),
        ancrage="center",
    )
    if saved_files:
        for i in range(len(saved_files)):
            f.image(
                rapport(width, 300),
                rapport(length, y + 50),
                "Media/background_images/box.gif",
                largeur=int(rapport(width, 700)),
                ancrage="center",
            )
            f.texte(
                rapport(width, 120),
                rapport(length, y + 50),
                saved_files[i][0][:-4],
                ancrage="center",
                police="Impact",
                taille=int((length + width) / 45),
            )
            f.texte(
                rapport(width, 430),
                rapport(length, y + 50),
                saved_files[i][1],
                ancrage="center",
                police="Impact",
                taille=int((length + width) / 50),
            )
            y += 105
    else:
        f.texte(
            rapport(width, 300),
            rapport(length, 300),
            "No saved files" + " :(",
            ancrage="center",
            police="Impact",
            taille=int((length + width) / 45),
        )


def case_vers_pixel(case, lab, width, length):
    """Renvoie le pixel correspondant à la case"""
    i, j = case
    return (j + 0.5) * (width / len(lab[0])), (i + 0.5) * (length / len(lab))


def pixel_vers_case(pixel, lab, width, length):
    """Renvoie la case correspondant au pixel"""
    return int(pixel[1] // (length / (len(lab)))), int(
        pixel[0] // (width / len(lab[0]))
    )


def start_menu(width, length):
    """dessine le menu d'acceuil"""
    f.image(
        rapport(width, 300),
        rapport(length, 300),
        "Media/background_images/start_menu.gif",
        largeur=int(width * 1.01),
        hauteur=int(length * 1.01),
        ancrage="center",
    )


def settings(width, length):
    """dessine le menu des parametres"""

    f.image(
        rapport(width, 300),
        rapport(length, 300),
        "Media/background_images/settings.gif",
        largeur=int(width * 1.01),
        hauteur=int(length * 1.01),
        ancrage="center",
    )
    f.image(
        rapport(width, 428),
        rapport(length, 227),
        "Media/characters/players/goku.gif",
        largeur=int(rapport(width, 400)),
        hauteur=int(rapport(length, 400)),
        ancrage="center",
        tag="player",
    )


def new_or_save(width, length):
    """dessine le menu pour creer ou continuer une partie"""
    f.image(
        rapport(width, 300),
        rapport(length, 300),
        "Media/background_images/new_or_save.gif",
        largeur=int(width * 1.01),
        hauteur=int(length * 1.01),
        ancrage="center",
    )
    f.image(  # dessine le bouton de retour
        rapport(width, 25),
        rapport(length, 20),
        "Media/background_images/return_button.gif",
        largeur=int(rapport(width, 50)),
        hauteur=int(rapport(length, 50)),
        ancrage="center",
    )


def menu_to_choose_map(width, length):
    """dessine le menu pour choisir une map"""

    f.image(
        rapport(width, 300),
        rapport(length, 300),
        "Media/background_images/choose-mapmenu.gif",
        largeur=int(width * 1.01),
        hauteur=int(length * 1.01),
        ancrage="center",
    )


def menu_pause(width, length):
    """dessine le menu de pause"""

    f.image(
        rapport(width, 300),
        rapport(length, 300),
        "Media/background_images/pause_menu.gif",
        largeur=int(rapport(width, 600)),
        hauteur=int(rapport(length, 600)),
        ancrage="center",
        tag="pause",
    )


def game_options(width, length):
    """dessine le menu des option onetrysolve"""
    f.image(
        rapport(width, 300),
        rapport(length, 300),
        "Media/background_images/onetrysolve.gif",
        largeur=int(width * 1.01),
        hauteur=int(length * 1.01),
        ancrage="center",
    )


def choose_createmap(width, length):
    f.image(
        rapport(width, 300),
        rapport(length, 300),
        "Media/background_images/choose_create_map.gif",
        largeur=int(width * 1.01),
        hauteur=int(length * 1.01),
        ancrage="center",
    )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAP~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def map_draw(lab, width, length):
    """Dessine la map sur la fenêtre de jeu"""
    for i in range(len(lab)):  # dessine les cases du labyrinthe
        for j in range(len(lab[0])):
            f.image(
                case_vers_pixel((i, j), lab, width, length)[0],  # x
                case_vers_pixel((i, j), lab, width, length)[1],  # y
                images[lab[i][j]],
                largeur=width // len(lab[0]) + 1,
                hauteur=length // len(lab) + 1,
                ancrage="center",
                tag="a" + str(j) + str(i),
            )


def nuage_draw(nuage, lab, width, length):
    """dessine le nuage magique à sa position"""

    if nuage is not None:
        f.image(
            case_vers_pixel(nuage, lab, width, length)[0],
            case_vers_pixel(nuage, lab, width, length)[1],
            "Media/nuage.gif",
            largeur=int(rapport(width, 60)),
            hauteur=int(rapport(length, 60)),
            ancrage="center",
            tag="nuage",
        )


def senzu_draw(senzu, lab, width, length):
    """dessine le senzu à sa position"""
    if senzu is not None:
        f.image(
            case_vers_pixel(senzu, lab, width, length)[0],
            case_vers_pixel(senzu, lab, width, length)[1],
            "Media/senzu.gif",
            largeur=int(rapport(width, 300)),
            hauteur=int(rapport(length, 300)),
            ancrage="center",
            tag="senzu",
        )


def ball_draw(ball, lab, width, length):
    """dessine les dragon_balls à leurs positions"""
    if ball is not None:
        f.image(
            case_vers_pixel(ball["position"], lab, width, length)[0],
            case_vers_pixel(ball["position"], lab, width, length)[1],
            ball["etoiles"],
            largeur=int(rapport(width, 100)),
            hauteur=int(rapport(length, 100)),
            ancrage="center",
            tag="ball",
        )
        f.mise_a_jour()


def ennemis_draw(ennemis, lab, map, width, length):
    """Dessine les ennemis sur la fenêtre de jeu"""
    for ennemi in ennemis:
        f.image(
            case_vers_pixel(ennemi["position"], lab, width, length)[0],
            case_vers_pixel(ennemi["position"], lab, width, length)[1],
            villains[map][ennemi["level"]]
            if ennemi["level"] <= 5
            else villains[map][5],
            largeur=int(width // 2.4 + 1),
            hauteur=int(length // 2.4 + 1),
            ancrage="center",
            tag="v" + str(ennemi["level"]),
        )
        f.texte(
            case_vers_pixel(ennemi["position"], lab, width, length)[0] + width / 20,
            case_vers_pixel(ennemi["position"], lab, width, length)[1] - length / 30,
            ennemi["level"],
            taille=12,
            tag="v" + str(ennemi["level"]) + "_lvl",
        )


def goku_draw(goku, lab, current_player, map, width, length):
    """Dessine Goku sur la fenêtre de jeu"""
    if goku is not None:
        f.image(
            case_vers_pixel(goku["position"], lab, width, length)[0],
            case_vers_pixel(goku["position"], lab, width, length)[1],
            player[current_player][map][goku["level"]] if goku["level"] <= 6 else player[current_player][map][6],
            ancrage="center",
            largeur=width // 2 + 1,
            hauteur=length // 2 + 1,
            tag="goku",
        )
        f.texte(
            case_vers_pixel(goku["position"], lab, width, length)[0] + width / 20,
            case_vers_pixel(goku["position"], lab, width, length)[1] - length / 30,
            goku["level"],
            taille=12,
            tag="goku_lvl",
        )


def intention_draw(way, lab, width, length):
    """dessine le chemin fourni"""
    if way is not None:
        for i in range(len(way) - 1):
            f.ligne(
                case_vers_pixel(way[i], lab, width, length)[0],
                case_vers_pixel(way[i], lab, width, length)[1],
                case_vers_pixel(way[i + 1], lab, width, length)[0],
                case_vers_pixel(way[i + 1], lab, width, length)[1],
                couleur="red",
                epaisseur=5,
                tag="chemin"
                + str(way[i][0])
                + str(way[i][1]),  # tag pour supprimer le chemin
            )
        f.mise_a_jour()


def tombs_draw(tombs, width, length):
    """dessine les tombes à la mort des ennemis"""
    for tomb in tombs:
        f.image(
            tomb[0],
            tomb[1],
            "Media/background_images/tomb.gif",
            largeur=int(rapport(width, 120)),
            hauteur=int(rapport(length, 120)),
            ancrage="center",
        )


def drawing(
    lab, goku, current_player, ennemis, nuage, senzu, ball, tombs, map, width, length
):
    """fait appel à toutes les fonctions de dessin"""
    map_draw(lab, width, length)
    nuage_draw(nuage, lab, width, length)
    ball_draw(ball, lab, width, length)
    ennemis_draw(ennemis, lab, map, width, length)
    tombs_draw(tombs, width, length)
    goku_draw(goku, lab, current_player, map, width, length)
    nuage_draw(nuage, lab, width, length)
    senzu_draw(senzu, lab, width, length)
    f.mise_a_jour()
