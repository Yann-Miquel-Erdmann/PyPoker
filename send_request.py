import requests
from datetime import datetime,timedelta

str_adresse = "http://lmn.eleve1.free.fr/PyPoker/"



def partie_online(Joueur1, Partie, Action, Mise, Texte):
  json = {
          "joueur1": Joueur1,
          "partie": Partie,
          "action": Action,
          "texte": Texte,
          "mise": Mise
         }
  
  r = requests.post(str_adresse+"partie_online.php", json=json)
  r.raise_for_status()
  if r.status_code == 200:
    try:
      return r.json()
    except:
      print(r.text)
      return {"erreur":True}
  else:
    print(r.status_code)
    return {"erreur":True}



def get_partie_online(pseudo1,partie, Date_et_heure):
  json = {
          "joueur1": pseudo1,
          "date_heure": Date_et_heure,
          "partie": partie
         }
  
  r = requests.post(str_adresse+"getpartie_online.php", json=json)
  r.raise_for_status()
  if r.status_code == 200:
    try:
      return r.json()
    except:
      print(r.text)
      return {"erreur":True}
  else:
    print(r.status_code)
    return {"erreur":True}

    
def create_invitation(pseudo1, pseudo2):
  json = {
          "joueur1": pseudo1,
          "joueur2": pseudo2
         }
  
  r = requests.post(str_adresse+"createinvitation.php", json=json)
  r.raise_for_status()
  if r.status_code == 200:
    try:
      return r.json()
    except:
      print(r.text)
      return {"erreur":True}
  else:
    print(r.status_code)
    return {"erreur":True}

    
    
    
def connexion(pseudo1, mdp):
  json = {
          "joueur1": pseudo1,
          "mdp": mdp
         }
  
  r = requests.post(str_adresse+"connexion.php", json=json)
  r.raise_for_status()
  if r.status_code == 200:
    try:
      return r.json()
    except:
      print(r.text)
      return {"erreur":True}
  else:
    print(r.status_code)
    return {"erreur":True}


    
    
 
def ecrire_chat_global(pseudo1, text):
  json = {
          "joueur1": pseudo1,
          "texte": text
         }
  
  r = requests.post(str_adresse+"ecrirechatglobal.php", json=json)
  r.raise_for_status()
  if r.status_code == 200:
    try:
      return r.json()
    except:
      print(r.text)
      return {"erreur":True}
  else:
    print(r.status_code)
    return {"erreur":True}

    
def get_chat_global(pseudo1, Date_et_heure):
  json = {
          "joueur1": pseudo1,
          "date_heure": Date_et_heure
         }
  
  r = requests.post(str_adresse+"getchatglobal.php", json=json)
  r.raise_for_status()
  if r.status_code ==200:
    try:
      return r.json()
    except:
      print(r.text)
      return {"erreur":True}
  else:
    print(r.status_code)
    return {"erreur":True}

    
    
    
def get_invitations(pseudo1,):
  json = {
          "joueur1": pseudo1,
         }
  
  r = requests.post(str_adresse+"getinvitations.php", json=json)
  r.raise_for_status()
  if r.status_code == 200:
    try:
      return r.json()
    except:
      print(r.text)
      return {"erreur":True}
  else:
    print(r.status_code)
    return {"erreur":True}

    
    
 
def inscription(pseudo1, mdp):
  json = {
          "joueur1": pseudo1,
          "mdp": mdp
         }
  
  r = requests.post(str_adresse+"inscription.php", json=json)
  r.raise_for_status()
  if r.status_code == 200:
    try:
      return r.json()
    except:
      print(r.text)
      return {"erreur":True}
  else:
    print(r.status_code)
    return {"erreur":True}

    
    
    
def respond_invite(pseudo1,pseudo2,action):
  json = {
          "joueur1": pseudo1,
          "joueur2": pseudo2,
          "action": action,
         }
  
  r = requests.post(str_adresse+"respond_invite.php", json=json)
  r.raise_for_status()
  if r.status_code == 200:
    try:
      return r.json()
    except:
      print(r.text)
      return {"erreur":True}
  else:
    print(r.status_code)
    return {"erreur":True}

    
 

def get_features(pseudo1):
  json = {
          "joueur1": pseudo1,
         }
  
  r = requests.post(str_adresse+"getfeatures.php", json=json)
  r.raise_for_status()
  if r.status_code == 200:
    try:
      return r.json()
    except:
      print(r.text)

      return {"erreur":True}
  else:
    print(r.status_code)
    return {"erreur":True}



def update_features(pseudo1, gemmes, skins, skin_selectionne):
  json = {
          "joueur1": pseudo1,
          "gemmes": gemmes,
          "skins": skins,
          "skin_selectionne": skin_selectionne
         }
  
  r = requests.post(str_adresse+"update_features.php", json=json)
  r.raise_for_status()
  if r.status_code == 200:
    try:
      return r.json()
    except:
      print(r.text)
      return {"erreur":True}
  else:
    print(r.status_code)
    return {"erreur":True}





def partie_existe(pseudo1):
  json = {
          "joueur1": pseudo1,
          }
  
  r = requests.post(str_adresse+"partie_existe.php", json=json)
  r.raise_for_status()
  if r.status_code == 200:
    try:
      return r.json()
    except:
      print(r.text)
      return {"erreur":True}
  else:
    print(r.status_code)
    return {"erreur":True}




def delete_partie(pseudo1):
  json = {
          "joueur1": pseudo1,
          }
  
  r = requests.post(str_adresse+"delete_partie.php", json=json)
  r.raise_for_status()
  if r.status_code == 200:
    try:
      return r.json()
    except:
      print(r.text)
      return {"erreur":True}
  else:
    print(r.status_code)
    return {"erreur":True}

