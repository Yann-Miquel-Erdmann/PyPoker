from tkinter import *
from PIL import Image, ImageTk

def import_images(): 
    images = {}
    imagesnames = [
        #nom du fichier, nom de l'image, taille de l'imagee
        ("jouer","jouer", (195, 70)),
        ("jouer_click","jouer_click", (195, 70)),
        ("jouer","jouer_local",(145, 50)),
        ("jouer_click","jouer_local_click", (144, 49)),
        ("skin","skin", (195, 70)),
        ("skin_click","skin_click", (195, 70)),
        ("btn_regles","btn_regles",(195, 70)),
        ("btn_regles_click","btn_regles_click",(195, 70)),
        ("quitter","quitter", (195, 70)),
        ("quitter_click","quitter_click", (195, 70)),
        ("credit","credit", (195, 70)),
        ("credit_click","credit_click", (195, 70)),
        ("accueil","accueil", (145, 50)),
        ("accueil_click","accueil_click", (144, 49)),
        ("rejouer","rejouer", (145, 50)),
        ("rejouer_click","rejouer_click", (144, 49)),

        ("btn_miser","btn_miser", (135, 50)),
        ("btn_miser_click","btn_miser_click", (133, 48)),
        ("btn_parole","btn_parole", (135, 50)),
        ("btn_parole_click","btn_parole_click", (133, 48)),
        ("btn_suivre","btn_suivre", (135, 50)),
        ("btn_suivre_click","btn_suivre_click", (133, 48)),
        ("btn_relancer","btn_relancer", (135, 50)),
        ("btn_relancer_click","btn_relancer_click", (133, 48)),
        ("btn_secoucher","btn_secoucher", (135, 54)),
        ("btn_secoucher_click","btn_secoucher_click", (133, 52)),
        ("btn_tapis","btn_tapis", (135, 54)),
        ("btn_tapis_click","btn_tapis_click", (133, 52)),

        ("connexion","connexion", (133, 52)),
        ("connexion_click","connexion_click", (133, 52)),
        ("s_enregistrer","s_enregistrer", (133, 52)),
        ("s_enregistrer_click","s_enregistrer_click", (133, 52)),
        
        ("background","background", (980, 620)),
        ("accueil_win","accueil_win",(980, 620)),
        ("skin_win","skin_win",(980, 620)),
        ("inscription_win","inscription_win",(980, 620)),
        ("connexion_win","connexion_win",(980, 620)),
        ("choix_win","choix_win",(980, 620)),
        ("end_game_win","end_game_win",(980, 620))
    ]
    for image in imagesnames:
        images[image[1]] = ImageTk.PhotoImage(
            Image.open(f"Images/{image[0]}.png").resize(image[2])
        )
    return images



def import_skins():
    grandes = [ImageTk.PhotoImage(Image.open(f"skin/carteSkin{i}.png").resize((117, 182))) for i in range(1,9)]
    petites = [ImageTk.PhotoImage(Image.open(f"skin/carteSkin{i}.png").resize((90, 140))) for i in range(1,9)]
    return grandes+petites
