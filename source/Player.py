from PIL import Image, ImageTk
# pip install Pillow:


# Class qui va simuler le joueur pendant sa partie
class Player:
    
    # Créé le joueur avec une liste pour sa main (qui par défaut est vide) et une somme d'argent (qui par défaut est à 0)
    def __init__(self, argent=0, main=[]):
        self.__main = []
        self.__argent = argent
        self.__mise = 0
        self.__cartes_images = []

    # Distribution des cartes
    def givecards(self, carte):
        # Distribution des cartes en les mettant dans la main
        self.__main.append(carte)

        # cree les TKimages à afficher
        self.__cartes_images = list(
            map(lambda carte: carte.obtenir_features(), self.__main)
        )
        self.__cartes_images = list(
            map(
                lambda carte: Image.open(f"cards/{carte[0]}_{carte[1]}.png").resize(
                    (90, 140)
                ),
                self.__cartes_images,
            )
        )
        self.__cartes_images = list(
            map(lambda carte: ImageTk.PhotoImage(carte), self.__cartes_images)
        )
    
    # Prends en paramètre une mise. Actualise la somme d'argent du joueur et la somme de sa mise en fonction de cette valeur.
    def miser(self, mise):
        if mise <= self.__argent:
            self.__argent += self.__mise - mise
            self.__mise = mise

            return True
        else:
            return False

    # Reproduit l'action "All-in" en mettant tout l'argent du joueur dans sa mise et en mettant l'argent du joueur à 0 
    def allin(self):
        self.__mise += self.__argent
        self.__argent = 0
        return self.__mise

    # Renvoie la main du joueur
    def getcards(self):
        return self.__main

    # Supprime les valeurs contenues dans la main
    def clearcards(self):
        self.__main = []

    # Ajoute à la somme d'argent le pot placé en paramètre
    def gains(self, pot):
        self.__argent += pot

    # Renvoie la valeur de la mise
    def get_mise(self):
        return self.__mise
   
    # Met la mise à 0
    def reset_mise(self):
        self.__mise = 0

    # Renvoie la somme d'argent du joueur
    def get_argent(self):
        return self.__argent

    # Renvoie les images des cartes du joueur côté visible
    def get_cartes_images(self):
        return self.__cartes_images
