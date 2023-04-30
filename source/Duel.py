from Winning import *
Victoire = {
    1: "Carte Haute",
    2: "Paire",
    3: "Double Paire",
    4: "Brelan",
    5: "Quinte",
    6: "Couleur",
    7: "Full",
    8: "Carré",
    9: "Quinte Flush",
    10: "Quinte Flush Royale",
}


def HighestCard(hand1,hand2):
    hand1.sort(key= lambda elem: elem.obtenir_features()[0])
    hand2.sort(key= lambda elem: elem.obtenir_features()[0])
    print(list(map(lambda elem: elem.obtenir_features() , hand1)))
    print(list(map(lambda elem: elem.obtenir_features() , hand2)))
    print (High(hand1)[0],High(hand2)[0])
    if int(High(hand1)[0]) > int(High(hand2)[0]):
        return 0
    elif int(High(hand1)[0]) < int(High(hand2)[0]):
        return 1
    else:
        return 2

def duel(hand1,hand2,river):
    point1 = hand1 + river
    point2 = hand2 + river
    point1.sort(key=lambda elem : elem.obtenir_valeur(), reverse=True)
    point2.sort(key=lambda elem : elem.obtenir_valeur(), reverse=True)
    wincondition1 = WinCondition (point1)
    wincondition2 = WinCondition (point2)
    print("wincondition1", Victoire[wincondition1])
    print("wincondition2", Victoire[wincondition2])

    if wincondition1 > wincondition2:
        return 0
    elif wincondition2 > wincondition1:
        return 1
    else:
        #égalité High card
        if wincondition1 == 1:
            return HighestCard(hand1,hand2)
            
        #égalité une Pair
        elif wincondition1 == 2:
            if Pair(point1)[0][0] > Pair(point2)[0][0]:
                return 0
            elif Pair(point1)[0][0] < Pair(point2)[0][0]:
                return 1
            else:
                return HighestCard(hand1, hand2)
                
        #églité deux Pair
        elif wincondition1 == 3:
            if Pair(point1) > Pair(point2):
                return 0
            elif Pair(point1) < Pair(point2):
                return 1
            else:
                return HighestCard(hand1, hand2)
                
        #églité ThreeOfKind
        elif wincondition1 == 4:
            if ThreeOfKind(point1) > ThreeOfKind(point2):
                return 0
            elif ThreeOfKind(point1) < ThreeOfKind(point2):
                return 1
            else:
                return HighestCard(hand1, hand2)
        
        #égalité Suite
        elif wincondition1 == 5:
            if Straight(point1) > Straight(point2):
                return 0
            elif Straight(point1) < Straight(point2):
                return 1
            else:
                return 2
                
        #égalité Couleur
        elif wincondition1 == 6:
            if WinColor(point1) > WinColor(point2):
                return 0
            elif WinColor(point1) < WinColor(point2):
                return 1
            else:
                return HighestCard(point1, point2)
                
        #égalité Full House
        elif wincondition1 == 7:
            if FullHouse(point1)[0] > FullHouse(point2)[0]:
                return 0
            elif FullHouse(point1)[0] < FullHouse(point2)[0]:
                return 1
            else:
                if FullHouse(point1)[4] > FullHouse(point2)[4]:
                    return 0
                elif FullHouse(point1)[4] < FullHouse(point2)[4]:
                    return 1
                else:
                    return 2
        
        #églité Four Of Kind
        elif wincondition1 == 8:
            if FourOfKind(point1) > FourOfKind(point2):
                return 0
            elif FourOfKind(point1) < FourOfKind(point2):
                return 1
            else:
                return HighestCard(main1, main2)
                
        #égalité Flush Couleur
        elif wincondition1 == 9:
            if Straight(point1) > Straight(point2):
                return 0
            elif Straight(point1) < Straight(point2):
                return 1
            else:
                return 2   
        else:
            return 2
