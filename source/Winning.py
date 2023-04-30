from random import *
from Carte import *


# Highest card
def High(pack):
    return pack[-1].obtenir_features()


def Pair(pack):
    Pair = []
    for i in range(len(pack) - 1):
        if pack[i].obtenir_valeur() == pack[i + 1].obtenir_valeur():
            Pair.append((pack[i].obtenir_features(), pack[i + 1].obtenir_features()))
            if len(Pair) == 2:
                return Pair
    return Pair


def ThreeOfKind(pack):
    for i in range(len(pack) - 2):
        if (
            pack[i].obtenir_valeur() == pack[i + 1].obtenir_valeur()
            and pack[i].obtenir_valeur() == pack[i + 2].obtenir_valeur()
        ):
            return (
                pack[i].obtenir_features(),
                pack[i + 1].obtenir_features(),
                pack[i + 2].obtenir_features(),
            )


def FourOfKind(pack):
    for i in range(len(pack) - 3):
        if (
            pack[i].obtenir_valeur() == pack[i + 1].obtenir_valeur()
            and pack[i].obtenir_valeur() == pack[i + 2].obtenir_valeur()
            and pack[i].obtenir_valeur() == pack[i + 3].obtenir_valeur()
        ):
            return (
                pack[i].obtenir_features(),
                pack[i + 1].obtenir_features(),
                pack[i + 2].obtenir_features(),
                pack[i + 3].obtenir_features(),
            )


def Straight(pack):
    suite = []
    for i in pack:
        suite.append(i.obtenir_valeur())
    suite = list(set(suite))
    print(suite)
    if len(suite) >= 5:
        suite.sort(reverse=True)
        for i in range(len(suite) - 4):   
            if (
                suite[i] == suite[i + 1] + 1
                and suite[i] == suite[i + 2] + 2
                and suite[i] == suite[i + 3] + 3    
                and suite[i] == suite[i + 4] + 4    
            ):
                return (
                    suite[i],
                    suite[i + 1],
                    suite[i + 2],
                    suite[i + 3],
                    suite[i + 4],
                )


def Color(pack):
    Coeur = [elem for elem in pack if elem.obtenir_couleur() == "Coeur"]
    Pique = [elem for elem in pack if elem.obtenir_couleur() == "Pique"]
    Carreau = [elem for elem in pack if elem.obtenir_couleur() == "Carreau"]
    Trefle = [elem for elem in pack if elem.obtenir_couleur() == "Trèfle"]
    if len(Coeur) >= 5:
        Coeur.sort(key=lambda elem: elem.obtenir_valeur())
        return (Coeur, "Coeur")
    elif len(Pique) >= 5:
        Pique.sort(key=lambda elem: elem.obtenir_valeur())
        return (Pique, "Pique")
    elif len(Carreau) >= 5:
        Carreau.sort(key=lambda elem: elem.obtenir_valeur())
        return (Carreau, "Carreau")
    elif len(Trefle) >= 5:
        Trefle.sort(key=lambda elem: elem.obtenir_valeur())
        return (Trefle, "Trèfle")


def WinColor(pack):
    if Color(pack):
        return (Color(pack)[0][-5:], Color(pack)[1])


def FullHouse(pack):
    if ThreeOfKind(pack):
        three = ThreeOfKind(pack)
        #        liste = [elem for elem in pack if elem == three[0]]
        liste = []
        for i in range(len(pack)):
            if pack[i].obtenir_valeur() != three[0][0]:
                liste.append(pack[i])
        if Pair(liste):
            return (three, Pair(liste))


def StrFlush(pack):
    if Color(pack) and Straight(Color(pack)[0]):
        return (Straight(Color(pack)[0]), Color(pack)[1])


def RoyalFlush(pack):
    if StrFlush(pack) and StrFlush(pack)[0][0] == 14:
        return StrFlush(pack)


def WinCondition(pack):
    print(list(map(lambda elem: elem.obtenir_features() , pack)))
    if RoyalFlush(pack):
        return 10
    elif StrFlush(pack):
        return 9
    elif FourOfKind(pack):
        return 8
    elif FullHouse(pack):
        return 7
    elif WinColor(pack):
        return 6
    elif Straight(pack):
        return 5
    elif ThreeOfKind(pack):
        return 4
    elif len(Pair(pack)) == 2:
        print(Pair(pack))
        return 3
    elif len(Pair(pack)) == 1:
        print(Pair(pack))
        return 2
    else:
        return 1
