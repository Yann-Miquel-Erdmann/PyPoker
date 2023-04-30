import random
from Pile import *

# Class qui simule chaque carte
class Carte:
    def __init__(self, couleur, valeur):
        self.__couleur = couleur
        self.__valeur = valeur
        self.__figure_dico = {11: "Valet", 12: "Dame", 13: "Roi", 14: "As"}
        if self.__valeur > 10:
            self.__figure = self.__figure_dico[valeur]

    def obtenir_figure(self):
        return self.__figure

    def obtenir_features(self):
        return (self.__valeur, self.__couleur)

    def obtenir_all_features(self):
        return (self.__valeur, self.__couleur, self.__figure)

    def obtenir_valeur(self):
        return self.__valeur

    def obtenir_couleur(self):
        return self.__couleur

# Fonction qui génère un packet de 52 cartes sous forme de pile de carte en utilisant en utilisant la class Carte et les fonctions de pile.py
def Generer_Packet():

    couleurs = ["Coeur", "Carreau", "Pique", "Trèfle"]
    paquet = creer_pile()
    for couleur in couleurs:
        for i in range(2, 15):
            empiler(paquet, Carte(couleur, i))
    return paquet

# Mélange le packet en utilisant la librairie random
def Melanger_Packet(Packet):
    return random.sample(Packet, len(Packet))
