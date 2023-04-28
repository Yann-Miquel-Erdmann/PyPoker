from send_request import *
from tkinter import IntVar
class Utilisateur():
    def __init__(self):
        self.pseudo = ""
        self.gemmes = IntVar()
        self.skins = [1,0,0,0,0,0,0,0]
        self.skin_selectionne = 0
        self.connecte = False
    

    def get_all(self):
        reponse = get_features(self.pseudo)
        resulat = reponse["resultat"][0]
        self.gemmes.set(resulat["Gemmes"])
        self.skins = list(map(int,list(str(resulat["skins"]))))
        self.skin_selectionne = resulat["skin_selectionne"]

    def update_features(self):
        skins = int("".join(map(str,self.skins)))
        update_features(self.pseudo, self.gemmes.get(), skins, self.skin_selectionne)
