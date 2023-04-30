# Créer une pile vide par défaut mais pouvant prendre des valeurs placés sous formes de liste en paramètre
def creer_pile():
    return []

# Renvoie la taille de la pile placée en paramètre
def taille(Pile):
    return len(Pile)

# Prends en paramètre une valeur et une pile. La fonction ajoute la valeur à la pile.
def empiler(Pile, value):
    Pile.append(value)

# Renvoie le sommet de la pile placée en paramètre
def peek(Pile):
    return Pile[-1]

# Renvoie le sommet de la pile placée en paramètre en le supprimant
def depiler(Pile):
    return Pile.pop()

# Renvoie oui si la pile placée en paramètre est vide, non sinon
def is_empty(Pile):
    return not bool(Pile)
