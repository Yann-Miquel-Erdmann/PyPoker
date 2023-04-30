from tkinter import *
from fonctions_verif import *
from send_request import *
from Encrypt import *
from threading import Thread
from tktooltip import *
# Fontion page de connection et register
#   Champ de saisie identifiant



class PageAuthentification():
    def __init__(self, frame, type_page, images, util):
        self.utilisateur = util
        self.frame = frame
        canvas = Canvas(frame, width=980, height=620)
        canvas.create_image(0, 0, anchor=NW, image=images[f"{type_page}_win"])
        canvas.pack()

        # Mise en place page conect
        boutonAcceuil = Label(frame, image=images["accueil"], text="PUSH", cursor= "hand2")
        boutonAcceuil.place(x= 15,y=15)
        boutonAcceuil.bind("<Button-1>", lambda event: event.widget.master.master.children["!frame"].pack(expand=True) or frame.pack_forget())

        #   Entrée des identifiants
        identifiant = Entry(frame, width=60, justify='center')
        identifiant.place(x=255, y=340)
        identifiant.bind("<FocusIn>",lambda event: self.focusIn(event,"id"))
        identifiant.bind("<FocusOut>",lambda event: self.focusOut(event,"id"))
        identifiant.bind("<KeyRelease>", lambda event: self.OnKeyPress(event, "id"))  # on detecte l'écriture
        identifiant.insert(0, "Rentrez votre identifiant")
        #   Entrée du mot de passe

        fr = Frame(frame,width=60,height="80", bg="red")
        
        self.mdp_hidden = BooleanVar(frame,True)
        #   Bouton voir mdp
        btn = Button(fr, text='Montrer',width=6, bg='#02422a', fg='white')
        btn.pack(side=RIGHT)
        btn.bind("<Button-1>", self.visible)

        self.mdp = Entry(fr, show="", width=50, justify='center')
        self.mdp.pack(side=RIGHT, expand=True,fill=BOTH )
        self.mdp.bind("<FocusIn>", lambda event:self.focusIn(event,"mdp"))
        self.mdp.bind("<FocusOut>", lambda event:self.focusOut(event,"mdp"))
        self.mdp.bind("<KeyRelease>", lambda event: self.OnKeyPress(event, "mdp"))  # on detecte l'écriture
        self.mdp.insert(0, "Rentrez votre mot de passe")

        fr.place(x=255, y=420)

        self.strvar = StringVar(frame,"")
        Label(frame, textvariable=self.strvar,bg='#02422a', fg='white').place(x=255, y=510)        
        ToolTip(self.mdp, "le mot de passe doit faire au moins 8 caractères et contenir un chiffre, une majuscule et un symbole")
            
        if type_page == "connexion":    
            #   Bouton connection
            connexion = Button(frame, text='connexion', bg='#02422a', fg='white', width=57)
            connexion.place(x=255, y=470)
            connexion.bind("<Button-1>",lambda event: Thread(daemon=True, target=self.pre_process, args=(event,"connexion")).start())
        else:
            connexion = Button(frame, text='Inscription', bg='#02422a', fg='white', width=57)
            connexion.place(x=255, y=470)
            connexion.bind("<Button-1>",lambda event: Thread(daemon=True, target=self.pre_process, args=(event,"inscription")).start())


    def focusIn(self,event, name):
        if name == "id":
            if event.widget.get() == "Rentrez votre identifiant":
                event.widget.delete(0, END)
        else:
            if event.widget.get() == "Rentrez votre mot de passe":
                event.widget.delete(0, END)
                event.widget.config(show="*")
            
    def focusOut(self,event,name):
        if name == "id":
            if len(event.widget.get()) == 0:
                event.widget.insert(0, "Rentrez votre identifiant")
        else:
            if len(event.widget.get()) == 0:
                event.widget.config(show="")
                event.widget.insert(0, "Rentrez votre mot de passe")



    def OnKeyPress(self,event, name):  # si on écrit dans l'element de texte
        value = event.widget.get()
        if name == "id":
            if not pseudo_valide(value):  #empêche d'utilister des caractères spéciaux dans les pseudos 
                value = value[0:-1]
                event.widget.delete(0, END)
                event.widget.insert(0, value)


    def visible(self,event):
        if self.mdp.get() == "Rentrez votre mot de passe":
            return
        if self.mdp_hidden.get():
            event.widget.configure(text = "Cacher")
            self.mdp_hidden.set(False)
            
            self.mdp.config(show="")
        else:
            event.widget.configure(text = "Montrer")
            self.mdp_hidden.set(True)
            self.mdp.config(show="*")


    def pre_process(self,event, name):
        pseudo = event.widget.master.children["!entry"].get()
        MotDePasse = event.widget.master.children["!frame"].children["!entry"].get()
        if not pseudo_valide(pseudo):
            self.strvar.set("le pseudonyme n'est pas valide")
            return

        if not password_valide(MotDePasse):
            self.strvar.set("le mot de passe n'est pas valide")
            return

        MotDePasse = encrypt(MotDePasse)
        if name == "connexion":
            rep = connexion(pseudo, MotDePasse)

        else:
            rep = inscription(pseudo, MotDePasse)
        del MotDePasse
        if not rep["erreur"]:
            self.utilisateur.pseudo = pseudo
            self.utilisateur.get_all()
            self.utilisateur.connecte = True
            self.frame.master.title("PyPoker - "+self.utilisateur.pseudo)
        else:
            self.strvar.set(rep["erreurs"][0])
