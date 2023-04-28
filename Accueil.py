from tkinter import *
from images_handler import *
from Game import *
from Game_Online import *
from Skin import *
from Chat import *
from connexion import *
from utilisateur import *
from Sons import jouer_musique

def close_all():
    app.withdraw()
    app.destroy()
    if utilisateur.connecte:
        delete_partie(utilisateur.pseudo)
    quit()
    


def btnInteract(event, name,action):
    if action == "click":
        event.widget.image = images[name+"_click"]
        event.widget.configure(image =  images[name+"_click"])
        if name == "jouer_local":
            print("start",utilisateur.skin_selectionne)
            jeu.initialise()
            frame_jeu.pack(expand=True)
        if name == "jouer":
            frame_choix.pack(expand=True)
        elif name == "skin":
            skins.update_text()
            frame_skins.pack(expand=True)
        elif name == "connexion":
            frame_connexion.pack(expand=True)
        elif name == "s_enregistrer":
            frame_senregister.pack(expand=True)
        elif name=="quitter":
            close_all()
    else:
        event.widget.image = images[name]
        event.widget.configure(image = images[name])
        if name == "jouer_local":
            frame_choix.pack_forget()

        accueil.pack_forget()
        
        

def generate_accueil(accueil, images):
    boutons =  {"jouer": {"x": 390,"y":200}, 
                "skin":{"x": 390,"y":290},
                "btn_regles":{"x": 390,"y":380},
                "quitter":{"x": 390,"y":470},
                "connexion":{"x": 750,"y":485},
                "s_enregistrer":{"x": 100,"y":485}
            }
    
    # Ouverture de l'image pour l'écran d'acceuil
    canva = Canvas(accueil, width=980, height=620)
    canva.create_image(0, 0, anchor=NW, image=images["accueil_win"])
    canva.pack()

    for name,pos in boutons.items():
        button = Label(accueil, image=images[name], text="PUSH", cursor= "hand2")
        button.place(**pos)
        button.image=images[name]
        button.bind("<Button-1>", lambda event,btn=name: btnInteract(event,btn, "click"))
        button.bind("<ButtonRelease-1>", lambda event,btn=name: btnInteract(event,btn, "release"))
        

def generate_choix(frame_choix, images):
    global jeu_online
    canva = Canvas(frame_choix, width=980, height=620)
    canva.create_image(0, 0, anchor=NW, image=images["choix_win"])
    canva.pack()

    boutonAcceuil = Label(frame_choix, image=images["accueil"], text="PUSH", cursor= "hand2")
    boutonAcceuil.place(x= 15,y=15)
    boutonAcceuil.bind("<Button>", lambda event: event.widget.master.master.children["!frame"].pack(expand=True) or frame_choix.pack_forget())

    button = Label(frame_choix, image=images["jouer_local"], text="PUSH", cursor= "hand2")
    button.place(x=415, y=84)
    button.image=images["jouer_local"]
    button.bind("<Button-1>", lambda event: btnInteract(event,"jouer_local", "click"))
    button.bind("<ButtonRelease-1>", lambda event: btnInteract(event,"jouer_local", "release"))

    frame_chat = Frame(frame_choix, width=335,height=300, bg="white")
    frame_chat.place(x=50,y=270)
    chat = ScrollWindow(frame_chat,utilisateur,"chat", 335,300)
    Thread(target=chat.getmessages,daemon=True).start()


    frame_invites = Frame(frame_choix, width=335,height=300, bg="white")
    frame_invites.place(x=580,y=270)
    invites = ScrollWindow(frame_invites,utilisateur,"invite", 335, 300,prepare_game=jeu_online.prepare_game)
    invites.check_partie_existe()
    Thread(target=invites.getinvites,daemon=True).start()


app = Tk()
app.title("PyPoker")
app.geometry("980x620")
app.configure(bg='white')
app.resizable(width=False, height=False)
images = import_images()
skins = import_skins()

utilisateur = Utilisateur()

#!temporaire
utilisateur.pseudo = "Lafruge"
utilisateur.connecte = True
utilisateur.get_all()
app.title("PyPoker - "+utilisateur.pseudo)


accueil = Frame(app,bg="white")
generate_accueil(accueil,images)

frame_jeu = Frame(app)
jeu = Game(frame_jeu, images,skins, utilisateur)

frame_jeu_online = Frame(app)
jeu_online = GameOnline(frame_jeu_online, images, skins, utilisateur)


frame_skins = Frame(app)
skins = skinPage(frame_skins, images,skins, utilisateur)



frame_choix = Frame(app)
generate_choix(frame_choix, images)


frame_connexion = Frame(app,bg="white")
PageAuthentification(frame_connexion,"connexion", images, utilisateur)

frame_senregister = Frame(app)
PageAuthentification(frame_senregister,"inscription", images, utilisateur)


accueil.pack(expand=True)


Thread(target=jouer_musique,daemon=True).start()

app.protocol("WM_DELETE_WINDOW", close_all)
app.mainloop()