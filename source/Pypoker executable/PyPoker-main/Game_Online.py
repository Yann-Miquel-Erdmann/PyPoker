from Player import *
from Carte import *
from tkinter import *
from tkinter.messagebox import *
from Pile import *
from Duel import *
from tktooltip import ToolTip
from PIL import Image
from send_request import *
from datetime import datetime, timedelta
from threading import Thread, Event
from Chat import ScrollWindow
from Sons import *
class GameOnline():
    def __init__(self, app, images, skins, utilisateur):
        self.gemmes_win = 150
        self.suivre = False
        self.relance = False
        self.montant_de_depart = 1000
        self.riviere = []
        self.riviereimages = []

        self.pot = 0
        self.lastmise = -1
        self.joueuractif = 0
        self.images = images
        self.skins = skins
        self.utilisateur = utilisateur 
        self.lastdate = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        
        self.request_event = Event()
        self.request_event.set()

        self.app = app
        self.frame_jeu =  Frame(self.app)
        self.frame_jeu.pack(expand=True)
        self.var = IntVar()
        
        self.joueurs = [Player(self.montant_de_depart) for i in range(2)]




        canva = Canvas(self.frame_jeu, width=980, height=620)  # génere le fond
        canva.create_image(0, 0, anchor=NW, image=self.images["background"])
        canva.pack()

        self.cartes = []  # génere les cartes visibles:
        self.cartesframes = []

        pos = [185, 290]
        for i in range(2):  # cree les 2 cartes du joueur principal
            self.cartesframes.append(Frame(self.frame_jeu, bg="yellow"))
            self.cartesframes[-1].place(x=pos[i], y=450)

            self.cartes.append(Label(self.cartesframes[-1], image=self.skins[self.utilisateur.skin_selectionne+8], cursor="hand2"))
            self.cartes[-1].pack()

            self.cartes[-1].bind(
                "<Button-1>", 
                lambda event: self.interactCarte(0, "click")
            )
            self.cartes[-1].bind(
                "<ButtonRelease-1>",
                lambda event: self.interactCarte(0, "release"),
            )

        self.skin_joueur2 = 0
        pos = [120, 225]
        for i in range(2):  # affiche les 2 cartes du joueur adverse
            self.cartesframes.append(Frame(self.frame_jeu, bg="yellow"))
            self.cartesframes[-1].place(x=pos[i], y=20)

            self.cartes.append(Label(self.cartesframes[-1], image=self.skins[self.skin_joueur2+8], cursor="hand2"))
            self.cartes[-1].pack()





        self.boutonAccueil = Label(
            self.frame_jeu, image=self.images["accueil"], text="PUSH", cursor="hand2")
        self.boutonAccueil.place(x=805, y=15)
        self.boutonAccueil.bind("<Button-1>", lambda event: self.app.master.children["!frame"].pack(expand=True) or self.app.pack_forget() or delete_partie(self.utilisateur.pseudo))



        # génere les self.boutons de mise, suivi, et se coucher

        self.boutons = {
            "btn_miser": [],
            "btn_tapis": [],
            "btn_parole": [],
            "btn_secoucher": [],
        }
        ypos = [400, 450, 500, 550]
        for j, bouton in enumerate(self.boutons.keys()):
            self.boutons[bouton].append(
                Label(self.frame_jeu, image=self.images[bouton], text="PUSH", cursor="hand2")
            )
            self.boutons[bouton][0].place(x=40, y=ypos[j])
            self.boutons[bouton][0].bind("<Button-1>", lambda event,
                                    btn=bouton: self.boutonInteract(event, btn, "click"),)
            self.boutons[bouton][0].bind(
                "<ButtonRelease-1>",
                lambda event, btn=bouton: self.boutonInteract(
                    event, btn, "release"),
            )

        self.label_pot = Label(self.frame_jeu, text="0", bg="#f6c64c", fg="white")
        self.label_pot.place(x=450, y=127, width=80)

        self.labels = []
        self.labels.append(Label(self.frame_jeu, text="argent: 0", fg="white",bg="#222222"))
        self.labels[-1].place(x=290, y=400)

        self.labels.append(Label(self.frame_jeu, text="argent: 0", fg="white",bg="#222222"))
        self.labels[-1].place(x=20, y=20)


        self.mises = []
        self.mises.append(Label(self.frame_jeu, text="mise: 0", fg="white",bg="#222222"))
        self.mises[-1].place(x=290, y=420, width=90)

        self.mises.append(Label(self.frame_jeu, text="mise: 0", fg="white",bg="#222222"))
        self.mises[-1].place(x=20, y=40, width=90)


        self.entry = []
        self.entry.append(Entry(self.frame_jeu, fg="gray"))
        self.entry[0].place(x=185, y=400, height=40, width=90)
        self.entry[0].bind(
            "<KeyRelease>", lambda event, i=0: self.OnKeyPress(event, i)
        )  # on detecte l'écriture
        self.entry[0].bind(
            "<FocusIn>", lambda event: self.focus_in(event)
        )  # on détecte l'entrée dans la zone de texte
        self.entry[0].bind("<FocusOut>", lambda event: self.focus_out(event))
        self.entry[0].insert(0, "Montant")
        ToolTip(self.entry[0], "Entrez le montant de votre mise ici.")


        self.posriviere = [185, 289, 393, 497, 601, 705]
        self.rivierelabel = []
        for i in range(6):  # cree les 4 self.cartes avec leur fonctions click et release
            self.rivierelabel.append(Label(self.frame_jeu, image=self.skins[self.utilisateur.skin_selectionne+8], cursor="hand2"))
        self.rivierelabel[0].place(x=self.posriviere[0], y=190)


        self.framechat = Frame(self.frame_jeu, width=400, height=220)
        self.framechat.place(x=500, y=370)
        self.generate_end_game()

    def prepare_game(self,partie, pseudo2):
        print("prepare")
        self.partie = partie
        self.pseudo2 = pseudo2
        self.pseudo_id = {self.utilisateur.pseudo : 0, self.pseudo2: 1}
        partie_online(self.utilisateur.pseudo, self.partie, "skin", self.utilisateur.skin_selectionne, "")
        for chat in self.framechat.children :
            chat.destroy()
        self.chat = ScrollWindow(self.framechat, self.utilisateur, "chat_in_game", 400, 200, self.partie, self.getactions)
        Thread(daemon=True,target=self.getactions).start()
        self.release()

    def initialise(self):
        self.joueurs = [Player(1000) for i in range(2)] 
        self.newround()

    def newround(self):
        self.suivre = False
        self.relance = False
        self.update_parole_relance()

        for joueur in self.joueurs:
            joueur.clearcards()

        self.joueuractif = self.pseudo_id[sorted([self.pseudo2, self.utilisateur.pseudo])[randint(0,1)]]
        self.showtour()
        self.joueur_tour_suivant = 0

        self.jeudecartes = Generer_Packet()  # liste des self.cartes
        self.jeudecartes = Melanger_Packet(self.jeudecartes)
        for _ in range(2):  # donne deux self.cartes à chacun
            self.joueurs[self.joueuractif].givecards(depiler(self.jeudecartes))
            self.joueurs[self.joueuractif-1].givecards(depiler(self.jeudecartes))


        self.update_mise_labels(0)
        self.update_mise_labels(1)

        self.riviere = []
        self.riviereimages = []
        for label in self.rivierelabel[1::]:
            label.place_forget()
        self.pot = 0
        self.label_pot.config(text=self.pot)
        self.lastmise = -1
        
        


    def opponent_skins(self, skinid):
        self.skin_joueur2 = skinid
        for i in range(2):
            self.cartes[i+2].config(image=self.skins[self.skin_joueur2+8])


    def allin(self,player):
        if self.joueuractif != player:
            return
        valeur = self.joueurs[player].allin()  # return montant du all in
        self.update_mise_labels(player)
        self.relance = True
        self.suivre = True
        self.joueuractif = 0 if self.joueuractif else 1
        self.showtour()
        if self.lastmise >= valeur:
            if self.lastmise>valeur:
                self.joueur_tour_suivant = player
            self.endriver()
        else:
            self.lastmise = valeur


    def mise(self,player, valeur):
        print("mise",player)

        if self.joueuractif != player:
            print("return", player)
            return

        if player == 0:
            self.entry[player].delete(0, END)
            self.entry[player].insert(0, "Montant")
            self.entry[player].config(fg="gray")
            self.frame_jeu.focus_set()   # on retire le focus de l'self.entry en le mettant autre part

        if valeur < self.lastmise:
            return

        if self.joueurs[player].miser(valeur) == True:
            

            self.relance = True
            self.suivre = True
            if valeur == self.lastmise:
                self.finmise()
            elif self.joueurs[int(not player)].get_argent() == 0:
                self.endriver()
            else:
                self.lastmise = valeur
                self.joueuractif = 0 if self.joueuractif else 1
                self.showtour()
                self.joueur_tour_suivant = player

            self.update_mise_labels(player)


    def suivrecall(self,player):

        if self.joueuractif != player:

            return
        if self.lastmise == -1:

            self.lastmise = 0
            self.joueuractif = 0 if self.joueuractif else 1
            self.showtour()

        elif self.joueurs[player].miser(self.lastmise) == True:
            self.finmise()


    def secouche(self,player):
        print(player)

        if self.joueuractif != player:
            return

        for joueur in range(2):
            self.pot += self.joueurs[joueur].get_mise()
            self.joueurs[joueur].reset_mise()
            self.update_mise_labels(joueur)

        self.label_pot.config(text=self.pot)

        self.joueuractif = player
        self.showtour()
        if player == 1:
            self.joueur_tour_suivant = 0
            self.distribuergain(0)
        else:
            self.joueur_tour_suivant = 1
            self.distribuergain(1)

        self.newround()


    def endriver(self,):   # en cas de all in, on affiche le reste de la rivière
        for i in range(len(self.riviere),5):
            empiler(self.riviere, depiler(self.jeudecartes))
            self.generer_images_riviere(peek(self.riviere))
            self.rivierelabel[i + 1].config(image=self.riviereimages[i])
            self.rivierelabel[i + 1].place(x=self.posriviere[i + 1], y=190)

        for player in range(len(self.joueurs)):
            self.pot += self.joueurs[player].get_mise()
            self.joueurs[player].reset_mise()
            self.update_mise_labels(player)
        self.label_pot.config(text=self.pot)
        self.gagnantjoueur()


    def finmise(self,):
        for joueur in self.joueurs:
            self.pot += joueur.get_mise()
            joueur.reset_mise()
        self.label_pot.config(text=self.pot)

        self.suivre = False
        self.relance = False
        self.update_parole_relance()

        for i in range(2):
            self.update_mise_labels(i)
        print(len(self.riviere))
        if len(self.riviere) == 5:
            self.gagnantjoueur()
            return

        if len(self.riviere) == 0:
            for i in range(3):
                empiler(self.riviere, depiler(self.jeudecartes))
                self.generer_images_riviere(peek(self.riviere))
                self.rivierelabel[i + 1].config(image=self.riviereimages[i])
                self.rivierelabel[i + 1].place(x=self.posriviere[i + 1], y=190)

        elif len(self.riviere) == 3:
            empiler(self.riviere, depiler(self.jeudecartes))
            self.generer_images_riviere(peek(self.riviere))
            self.rivierelabel[4].config(image=self.riviereimages[3])
            self.rivierelabel[4].place(x=self.posriviere[4], y=190)

        elif len(self.riviere) == 4:
            empiler(self.riviere, depiler(self.jeudecartes))
            self.generer_images_riviere(peek(self.riviere))
            self.rivierelabel[5].config(image=self.riviereimages[4])
            self.rivierelabel[5].place(x=self.posriviere[5], y=190)

        self.joueuractif = self.joueur_tour_suivant
        self.showtour()
        self.lastmise = -1


    def generer_images_riviere(self,carte):
        carte = carte.obtenir_features()
        carte = Image.open(f"cards/{carte[0]}_{carte[1]}.png").resize((90, 140))
        carte = ImageTk.PhotoImage(carte)
        self.riviereimages.append(carte)


    def release(self,):
        for i in range(2):
            self.interactCarte(i, "release")
        self.var.set(2)


    def gagnantjoueur(self,):
        self.var.set(1)
        gagnant = duel(self.joueurs[0].getcards(), self.joueurs[1].getcards(), self.riviere)
        print("gangant", gagnant)
        if gagnant == 2:
            self.distribuergain(2, True)
        else:
            self.distribuergain(gagnant)

        for i in range(2):
            self.interactCarte(i, "click")
        self.frame_jeu.after(5000, lambda: self.release())
        self.frame_jeu.wait_variable(self.var)


        if self.joueurs[gagnant].get_argent() == 2*self.montant_de_depart:
            pseudo = [val for val, key in self.pseudo_id.items() if key == gagnant]


            self.winner_text.set(f"{pseudo[0]} gagne la partie")
            self.frame_jeu.pack_forget()
            self.frame_end.pack(expand=True)
            if gagnant == 0:

                self.utilisateur.gemmes.set(self.utilisateur.gemmes.get()+self.gemmes_win)
                print("gemmes", self.utilisateur.gemmes.get())
                Thread(daemon=True,target=self.utilisateur.update_features).start()
        else:
            self.joueuractif = int(not gagnant)  # le perdant commence à miser
            self.showtour()
            self.update_mise_labels(0)
            self.update_mise_labels(1)
            self.newround()



    def distribuergain(self,player, egalite=False):
        print(self.pot)
        if egalite:
            self.joueurs[0].gains(int(self.pot/2))
            self.joueurs[1].gains(int(self.pot/2))
        else:
            self.joueurs[player].gains(self.pot)

        print(self.joueurs[0].get_argent())
        print(self.joueurs[1].get_argent())

        argents = list(map(lambda player: player.get_argent(), self.joueurs))
        if not all(argents):
            print("id perdant", argents.index(0))


    def generate_end_game(self):

        self.frame_end = Frame(self.app, bg="red")

        canva = Canvas(self.frame_end,width=980, height=620)
        canva.create_image(0, 0, anchor=NW, image=self.images["end_game_win"])
        canva.pack(expand=True,fill=BOTH)

        self.winner_text = StringVar(self.app)
        Label(self.frame_end, textvariable=self.winner_text, bg="#02422A", fg="white", font="Bold").place(x=375, y=190)
        acc = Label(self.frame_end, image=self.images["accueil"])
        acc.place(x=600, y=400)
        acc.bind("<Button-1>", lambda event: self.end_game_bouton(event,"click", "accueil"))
        acc.bind("<ButtonRelease-1>", lambda event: self.end_game_bouton(event,"release", "accueil"))
        
        rejouer = Label(self.frame_end, image=self.images["rejouer"])
        rejouer.place(x=210, y=400)
        rejouer.bind("<Button-1>",lambda event: self.end_game_bouton(event,"click", "rejouer"))
        rejouer.bind("<ButtonRelease-1>", lambda event: self.end_game_bouton(event,"release", "rejouer"))

        
    def end_game_bouton(self,event, action, name):
        if action == "click":
            pass
            event.widget.configure(image=self.images[name+"_click"])
        else:
            event.widget.configure(image=self.images[name])

            if name == "rejouer":
                self.initialise()
            else:
                delete_partie(self.utilisateur.pseudo)
                self.app.pack_forget()
                self.app.master.children["!frame"].pack()
            self.frame_jeu.pack(expand=True)
            self.frame_end.pack_forget()

    def boutonInteract(self,event, button, action):
        if action == "click":
            if button == "btn_parole":
                Thread(daemon=True,target=self.send_actions, args=("suivre",)).start()

            elif button == "btn_miser":
                Jouer_Son_async("Miser")
                val = self.entry[0].get()
                if len(val) > 0:
                    montant = int(val)
                    Thread(daemon=True,target=self.send_actions, args=("mise",montant)).start()
                else:
                    print("veuilez entrer le montant de votre mise")

            elif button == "btn_secoucher":
                Thread(daemon=True,target=self.send_actions, args=("secouche",)).start()
            elif button == "btn_tapis":
                Jouer_Son_async("Miser")
                Thread(daemon=True,target=self.send_actions, args=("allin",)).start()


            if self.var.get() in range(1, 3):  # fin de partie pour ne pas afficher le bouton jaune
                return

            self.update_parole_relance()
            newbutton = button
            if button == "btn_miser" and self.relance:
                newbutton = "btn_relancer"
            if button == "btn_parole" and self.suivre:
                newbutton = "btn_suivre"
            self.boutons[button][0].configure(image=self.images[newbutton + "_click"])

        else:

            self.boutons[button][0].configure(image=self.images[button])
            self.update_parole_relance()


    def update_mise_labels(self,player):
        self.mises[player].config(text="mise: "+str(self.joueurs[player].get_mise()))
        self.labels[player].config(text="argent: "+str(self.joueurs[player].get_argent()))


    def update_parole_relance(self,):

        if self.suivre:
            for i in range(2):
                self.boutons["btn_parole"][0].config(image=self.images["btn_suivre"])

        else:
            for i in range(2):
                self.boutons["btn_parole"][0].config(image=self.images["btn_parole"])

        if self.relance:
            for i in range(2):
                self.boutons["btn_miser"][0].config(image=self.images["btn_relancer"])
        else:
            for i in range(2):
                self.boutons["btn_miser"][0].config(image=self.images["btn_miser"])


    def interactCarte(self,a, action):
        Jouer_Son_async("Abattre")

        if len(self.joueurs):
            if a == 0:
                i = 0
            else:
                i = 2

            if action == "click":
                self.cartes[i].configure(image=self.joueurs[a].get_cartes_images()[0])
                self.cartes[i].image = self.joueurs[a].get_cartes_images()[0]
                self.cartes[i + 1].configure(image=self.joueurs[a].get_cartes_images()[1])
                self.cartes[i+1].image = self.joueurs[a].get_cartes_images()[1]

            elif action == "release":
                print("release")
                if i == 0:
                    self.cartes[i].configure(image=self.skins[self.utilisateur.skin_selectionne+8])
                    self.cartes[i].image = self.skins[self.utilisateur.skin_selectionne+8]
                    self.cartes[i+1].configure(image=self.skins[self.utilisateur.skin_selectionne+8])
                    self.cartes[i+1].image = self.skins[self.utilisateur.skin_selectionne+8]
                else:
                    self.cartes[i].configure(image=self.skins[self.skin_joueur2+8])
                    self.cartes[i].image = self.skins[self.skin_joueur2+8]
                    self.cartes[i+1].configure(image=self.skins[self.skin_joueur2+8])
                    self.cartes[i+1].image = self.skins[self.skin_joueur2+8]


    def focus_in(self,event):  # si le curseur est dans l'élément de texte 
        event.widget.config(fg="black")
        event.widget.delete(0, END)


    def focus_out(self,event):  # si le curseur n'est plus dans l'élément de texte
        event.widget.config(fg="gray")


    def OnKeyPress(self,event, player):  # si on écrit dans l'element de texte
        value = event.widget.get()
        if not value.isnumeric():
            value = value[0:-1]
            event.widget.delete(0, END)
            event.widget.insert(0, value)
        else:
            if int(event.widget.get()) > self.joueurs[player].get_argent():
                event.widget.delete(0, END)
                event.widget.insert(0, self.joueurs[player].get_argent())


    def send_actions(self, action, mise=0, text=""):
        if self.joueuractif != 0:
            return
        
        partie_online(self.utilisateur.pseudo, self.partie, action, mise, text)
        self.getactions(False)


    def getactions(self, loop = True):
        if self.request_event.is_set():
            self.request_event.clear()
            res = get_partie_online(self.utilisateur.pseudo, self.partie, self.lastdate)
            if res["erreur"]:
                if res["erreurs"][0] == "cette partie n'existe pas":
                    print("l'adversaire a quitté la partie")

                    self.app.pack_forget()
                    self.app.master.children["!frame"].pack()
                    self.frame_jeu.pack(expand=True)
                    self.frame_end.pack_forget()
                    self.request_event.set()
                    return
            else:
                if len(res["resultat"]):
                    for elem in res["resultat"]:
                        print(elem)
                        if elem["Action_"] == "random":
                            self.set_seed(elem["mise"])

                        if elem["Action_"] == "mise":
                            self.mise(self.pseudo_id[elem["player"]], elem["mise"])
                        
                        if elem["Action_"] == "suivre":
                            self.suivrecall(self.pseudo_id[elem["player"]])

                        if elem["Action_"] == "allin":
                            self.allin(self.pseudo_id[elem["player"]])
                        
                        if elem["Action_"] == "secouche":
                            self.secouche(self.pseudo_id[elem["player"]])
                        
                        if elem["Action_"] == "chat":
                            self.chat.chat(elem["player"],elem["texte"], elem["dateheure"])

                        if elem["Action_"] == "skin":
                            if elem["player"] == self.pseudo2:
                                self.opponent_skins(elem["mise"])
                    
                    
                    self.lastdate = res["resultat"][-1]["dateheure"]
                    



            self.request_event.set()
        else:
            return
        if loop:
            self.frame_jeu.after(2000, self.getactions)


    def set_seed(self,seed):
        random.seed(seed)
        self.initialise()
        print("a")

    def showtour(self):
        for carte in self.cartes:
            carte.pack_configure(padx=0,pady=0)

        b = 0 if self.joueuractif == 0 else 2
        self.cartes[b].pack_configure(padx=3, pady=3)
        self.cartes[b+1].pack_configure(padx=3, pady=3)