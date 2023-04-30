def password_valide(word):
  special = set(list('~`! @#$%^&*()_-+={[}]|\:;"'+"'<,>.?/")) # création de l'ensemble des caractères "spéciaux"
  if len(word)<8:
    return False

  if word.isalnum(): # il n'y a pas de caractère spécial
    return False

  for l in word:
    if not l.isalnum() and l not in special: # si un charactere n'est ni une lettre, un nombre ou un caractère spécial autorise
      return False
      
  return True


def pseudo_valide(word):
  if len(word)>20:
    return False
  if word.isalnum(): # Si le mot ne contient que des caractère alphanumériques
    return True
  for l in word: 
    if not l.isalnum() and l !="_": # Si ce caractère est alpnumérique ou est un underscore
      return False
  return True
