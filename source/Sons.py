import playsound
# pip install playsound

from random import randint
from threading import Thread
import json


def Jouer_Son(Type_de_son):  # Melanger, Distribuer, Abattre, Miser
    obj_python = json.loads(open("sons.json", "r").read()) # Récupère le fichier json qui contient les chemins vers les sons
    playsound.playsound(
        obj_python[Type_de_son][randint(0, len(obj_python[Type_de_son]) - 1)] # Joue un son aléatoire parmi ceux qui corresponde au Type_de_son demandé
    )

def Jouer_Son_async(Type_de_son):
    Thread(target=Jouer_Son,args=[Type_de_son,],daemon=True).start()

def jouer_musique():
    while True:
        playsound.playsound(
            "Sons/Musique.mp3"
        )


