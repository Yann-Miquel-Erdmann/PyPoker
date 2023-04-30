from tkinter import *
from PIL import Image,ImageTk


class skinPage:
    def  __init__ (self,skinpage,images, skins, utilisateur):
        canvas = Canvas(skinpage, width=980, height=620, bg="red")
        canvas.create_image(0, 0, anchor=NW, image=images["skin_win"])
        canvas.pack(expand=True, fill=BOTH)

        self.utilisateur = utilisateur
        # Boutons et cartes page de skin
        # Bouton Acceuil
        boutonAcceuil = Label(skinpage, image=images["accueil"], text="PUSH", cursor= "hand2")
        boutonAcceuil.place(x= 15,y=15)
        boutonAcceuil.bind("<Button>", lambda event: event.widget.master.master.children["!frame"].pack(expand=True) or skinpage.pack_forget())
        # boutonAcceuil.bind("<ButtonRelease>", boutonAcceuilRelease)

        gemmes = Label(skinpage, textvariable=self.utilisateur.gemmes, bg="#FFBD59", fg="white")
        gemmes.place(x=810, y=20)
        self.labels = []
        for j in range(2):
            for i in range(4):
                #affichage des skins
                frame = Frame(skinpage, bg="#02301E")
                frame.place(x= 70+240*i,y=110+260*j)

                carteSkin = Label(frame, image=skins[j*4+i], cursor= "hand2")
                carteSkin.pack()
                self.labels.append(Label(frame, text="acheter",fg="white", bg="#02301E"))
                self.labels[-1].pack(expand=True, fill=BOTH)
                self.labels[-1].bind("<Button-1>", lambda event, id_skin=j*4+i: self.__select_skin(id_skin))
    
        self.update_text()

    def update_text(self):
        print("update")
        for i in range(8):
            print(self.utilisateur.skins[i])
            if self.utilisateur.skins[i] == True:
                print("a",i)
                self.labels[i].configure(text="acheté")
                self.labels[i].pack_configure(pady=(10,25))
            else:
                self.labels[i].configure(text="acheter")
                self.labels[i].pack_configure(pady=0)

        self.labels[self.utilisateur.skin_selectionne].configure(text="selectionné")
        self.labels[self.utilisateur.skin_selectionne].pack_configure(pady=(10,25))


    def __select_skin(self, id_skin):
        prix = [0,100,100,150,150,350,350,1000]
        if self.utilisateur.skins[id_skin] == 1:
            self.utilisateur.skin_selectionne = id_skin
            self.utilisateur.update_features()

        else:
            if self.utilisateur.gemmes.get() >= prix[id_skin]:
                self.utilisateur.gemmes.set(self.utilisateur.gemmes.get()- prix[id_skin])
                self.utilisateur.skins[id_skin] = 1
                self.utilisateur.update_features()
        self.update_text()
