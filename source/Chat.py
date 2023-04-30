from tkinter import *
from datetime import datetime,timedelta
from time import sleep
from send_request import *
from threading import Thread, Event




class ScrollWindow():
    def __init__(self,root,utilisateur,typeWindow, width, height, partie = "", get_chat_online = lambda : 1, prepare_game=lambda : 1):
        self.utilisateur = utilisateur
        self.partie = partie
        self.prepare_game = prepare_game
        self.get_chat_online = get_chat_online
        self.root = root
        self.w = width
        self.verticalscrollbar = Scrollbar(self.root, orient=VERTICAL)
        self.verticalscrollbar.pack(fill=Y, side=RIGHT)
        self.canvas = Canvas(self.root, bd=0,height=height, highlightthickness=0,yscrollcommand=self.verticalscrollbar.set, bg="white")
        self.canvas.pack(fill=BOTH, expand=True)
        self.typewindow = typeWindow
        
        self.canvas.bind_all("<MouseWheel>", self.scroll_windows,add=True)

        self.canvas.bind_all("<Button-4>", self.scroll_linux, add=True)
        self.canvas.bind_all("<Button-5>", self.scroll_linux, add=True)
        self.verticalscrollbar.config(command=self.canvas.yview)


        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.innerframe = Frame(self.canvas, bg="white")
        self.innerframe.bind('<Configure>', self.configure_innerframe)

        self.innerframe_id = self.canvas.create_window(0, 0,width=self.w, window=self.innerframe,anchor=NW)
        self.buttons = 0
        
        frame = Frame(self.root, bg="white")
        
        
        self.entree = Entry(frame, show="", justify='center')
        
        self.message_invite_out = "Invitation envoyée à "
        self.message_invite_in = " vous invite"

        self.invite_text="Joueur à inviter"
        self.message_text="envoyer un message"
    
        self.chat_event = Event()
        self.chat_event.set()

        self.invite_event = Event()
        self.invite_event.set()


        if typeWindow == "chat":    
            #   Bouton connection
            self.entree.bind("<FocusIn>", lambda event:self.focusIn(event,"chat"))
            self.entree.bind("<FocusOut>", lambda event:self.focusOut(event,"chat"))
            self.entree.bind("<KeyRelease>", lambda event: self.OnKeyPress(event, "chat"))  # on detecte l'écriture
            self.entree.insert(0, self.message_text)
            envoyer = Button(frame, text='Envoyer',  bg='#02422a', fg='white', )
            envoyer.pack(side=RIGHT, expand=True, fill=BOTH)
            envoyer.bind("<Button-1>",lambda event: Thread(daemon = True, target=self.pre_chat, args=(event,)).start())
        elif typeWindow=="invite":
            self.entree.bind("<FocusIn>", lambda event:self.focusIn(event,"invite"))
            self.entree.bind("<FocusOut>", lambda event:self.focusOut(event,"invite"))
            self.entree.bind("<KeyRelease>", lambda event: self.OnKeyPress(event, "invite"))  # on detecte l'écriture
            self.entree.insert(0, self.invite_text)

            envoyer = Button(frame, text='Inviter',  bg='#02422a', fg='white', )
            envoyer.pack(side=RIGHT, expand=True, fill=BOTH)
            envoyer.bind("<Button-1>",lambda event: Thread(daemon = True, target=self.pre_invite, args=(event,)).start())
        else:
            #   Bouton connection
            self.entree.bind("<FocusIn>", lambda event:self.focusIn(event,"chat"))
            self.entree.bind("<FocusOut>", lambda event:self.focusOut(event,"chat"))
            self.entree.bind("<KeyRelease>", lambda event: self.OnKeyPress(event, "chat"))  # on detecte l'écriture
            self.entree.insert(0, self.message_text)
            envoyer = Button(frame, text='Envoyer',  bg='#02422a', fg='white', )
            envoyer.pack(side=RIGHT, expand=True, fill=BOTH)
            envoyer.bind("<Button-1>",lambda event: Thread(daemon = True, target=self.pre_chat_game, args=(event,)).start())

        self.entree.pack(side=RIGHT, expand=True,fill=BOTH)
        frame.pack(side=TOP, expand=True, fill='both')

        self.last_timestamp = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        


    def chat(self,player, message='', date="2023"):
        frame = Frame(self.innerframe)
        Label(frame, text=date,  bg="#1A2A3A", fg="white").pack(ipadx= 10, ipady= 2, fill=BOTH, side=RIGHT)
        Label(frame, text=player, bg="#1A2A3A", fg="white").pack(expand = True, fill=BOTH, side=RIGHT)
        frame.pack(ipady = 0,ipadx=5, side=TOP, fill=X)
        Label(self.innerframe, text=message,wraplengt=self.w-15,bg="#3A4A5A", fg="white").pack(ipadx=10, ipady = 5,pady=(0,1), fill=X,  side =TOP )

        self.canvas.update_idletasks()
        self.canvas.yview_moveto('1')



    def invite(self,player,sens= True):
        frame = Frame(self.innerframe, bg="white")
        padding = {"ipady": 5,"fill":BOTH}
        if sens:
            Label(frame, text=self.message_invite_out+player,  bg="#02422a", fg="white").pack(**padding,side=LEFT, expand=True)
            self.buttons = Button(frame, text="anuler")
            self.buttons.pack(ipadx=10,fill=BOTH,side=LEFT)
            self.buttons.bind("<Button-1>", lambda event:  Thread(daemon = True, target = self.respond_invitation , args=(event,"remove")).start())

        else:
            Label(frame, text=player+ self.message_invite_in,  bg="#02422a", fg="white").pack(**padding,side=TOP,expand=True)

            self.buttons = Button(frame, text="Accepter")
            self.buttons.pack(**padding,side=LEFT, expand=True)
            self.buttons.bind("<Button-1>", lambda event:  Thread(daemon = True, target = self.respond_invitation , args=(event,"accept")).start())

            self.buttons = Button(frame, text="Decliner")
            self.buttons.pack(**padding, side=LEFT,expand=True)
            self.buttons.bind("<Button-1>", lambda event:  Thread(daemon = True, target = self.respond_invitation , args=(event,"refuse")).start())

        frame.pack(ipady = 0, ipadx=5, pady=(0,5), side=TOP, fill=X)
        

        self.canvas.update_idletasks()
        self.canvas.yview_moveto('1')


    def updateinvites(self, reponse):
        i = 0
        to_delete = []
        for invite in self.innerframe.children.values():
            if len(reponse["resultat"]) > i:
                if len(invite.children) == 2:
                    if invite.children["!label"]['text'][len(self.message_invite_out):] != reponse["resultat"][i]["invite"]:
                        to_delete.append(invite)
                    else:
                        i+=1
                else:
                    if invite.children["!label"]['text'][:-len(self.message_invite_in)] != reponse["resultat"][i]["joueur"]:
                        to_delete.append(invite)
                    else:
                        i+=1
            else:        
                to_delete.append(invite)
            
        if len(to_delete):
            Thread(daemon = True, target=self.check_partie_existe).start()
        
        for invite in to_delete:
            invite.destroy()


        for invite in reponse["resultat"][i:]:
            if invite["joueur"] == self.utilisateur.pseudo:
                self.invite(invite["invite"],True)
            else:
                self.invite(invite["joueur"],False)



    def configure_innerframe(self,event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.config(width=self.w)


    def scroll_linux(self,event) -> None:
        x,y = self.canvas.winfo_pointerxy()
        widget = self.canvas.winfo_containing(x,y)
        if str(self.root) not in str(widget):
            return
        if len(str(self.root)) != len(str(widget)):
            if str(widget)[len(str(self.root))] != ".":
                return


        y_steps = 1
        if event.num == 4:
            y_steps *= -1
        self.canvas.yview_scroll(y_steps, "units")

    def scroll_windows(self,event) -> None:
        x,y = self.canvas.winfo_pointerxy()
        widget = self.canvas.winfo_containing(x,y)
        if str(self.root) not in str(widget):
            return
        if len(str(self.root)) != len(str(widget)):
            if str(widget)[len(str(self.root))] != ".":
                return

        y_steps = int(-event.delta/abs(event.delta)*1)
        self.canvas.yview_scroll(y_steps, "units")


    def getmessages(self, boucle = True):
        if self.utilisateur.connecte:
            if self.chat_event.is_set():
                self.chat_event.clear()
                rep = get_chat_global(self.utilisateur.pseudo, self.last_timestamp)
                if not rep["erreur"]:
                    if len(rep["resultat"]):    
                        for message in rep["resultat"]:
                            self.chat(message["joueur"], message=message["texte"], date=message["dateheure"])
                    
                        self.last_timestamp = rep["resultat"][-1]["dateheure"]
                else:
                    print(rep["erreurs"])
                self.chat_event.set()
        else:
            print("not connecte")

        if boucle:
            self.canvas.after(2000,self.getmessages)


    def getinvites(self, boucle = True):
        if self.utilisateur.connecte:
            if self.chat_event.is_set():
                self.chat_event.clear()
                rep = get_invitations(self.utilisateur.pseudo)
                # print(rep)
                if not rep["erreur"]:

                    self.updateinvites(rep)
                        
                else:
                    print(rep["erreurs"])
                self.chat_event.set()
        else:
            print("not connecte")
        if boucle:
            self.canvas.after(5000,self.getinvites)

    def focusIn(self,event, name):
        if name == "chat":
            if event.widget.get() == self.message_text:
                event.widget.delete(0, END)
        else:
            if event.widget.get() == self.invite_text:
                event.widget.delete(0, END)

            
    def focusOut(self,event,name):
        if name == "chat":
            if len(event.widget.get()) == 0:
                event.widget.insert(0, self.message_text)
        else:
            if len(event.widget.get()) == 0:
                event.widget.config(show="")
                event.widget.insert(0, self.invite_text)



    def OnKeyPress(self,event, name):  # si on écrit dans l'element de texte
        value = event.widget.get()
        autorises = "_ !?'-" 
        if len(value):
            if not value[-1].isalnum() and value[-1] not in autorises:
                #empêche d'utilister des caractères spéciaux dans les messages et invitations
                value = value[0:-1]
                event.widget.delete(0, END)
                event.widget.insert(0, value)
        
        if name == "chat":
            if len(event.widget.get()) >255:
                value = value[0:-1]
                event.widget.delete(0, END)
                event.widget.insert(0, value)
                
        else:
            if len(event.widget.get()) >20:
                value = value[0:-1]
                event.widget.delete(0, END)
                event.widget.insert(0, value)


    def pre_chat(self, event):
        if self.utilisateur.pseudo == "":
            print("vous devez vous connecter")
            return

        message = self.entree.get()
        if len(message) and message != self.message_text: 
            rep = ecrire_chat_global(self.utilisateur.pseudo, message)
            if rep["erreur"]:
                print(rep["erreurs"])
                return
        
        self.getmessages(False)
        self.entree.delete(0, END)
        return
        

    def pre_chat_game(self, event):
        message = self.entree.get()
        if len(message) and message != self.message_text: 
            rep = partie_online(self.utilisateur.pseudo, self.partie, "chat", 0, message)
            if rep["erreur"]:
                print(rep["erreurs"])
                return
        
        self.get_chat_online(False)
        self.entree.delete(0, END)
        return

    def pre_invite(self, event):
        if not self.utilisateur.connecte:
            print("vous devez vous connecter")
            return

        pseudo2 = self.entree.get()
        if len(pseudo2) and pseudo2 != self.invite_text:
            if self.utilisateur.pseudo ==  pseudo2:
                return #empêche de s'inviter soi même
            rep = create_invitation(self.utilisateur.pseudo, pseudo2)
            if rep["erreur"]:
                print(rep["erreurs"])
                return
        
        self.getinvites(False)
        self.entree.delete(0, END)
        return



    def respond_invitation(self,event,action):
        print(action    )
        if not self.utilisateur.connecte:
            print("vous devez vous connecter")
            return
        if action == "remove":
            pseudo1 = event.widget.master.children["!label"].cget("text")[len(self.message_invite_out):]
            res = respond_invite(pseudo1,self.utilisateur.pseudo, action)
        else:
            pseudo2 = event.widget.master.children["!label"].cget("text")[:-len(self.message_invite_in)]
            res = respond_invite(self.utilisateur.pseudo, pseudo2, action)
        
        self.getinvites(False)

    def check_partie_existe(self):
        r = partie_existe(self.utilisateur.pseudo)
        partie = r["resultat"][0]
        if partie == "": #il n'y a pas de partie avec le joueur
            print("no game")
            return 

        
        pseudo2 = [pseudo for pseudo in partie.split("§") if pseudo != self.utilisateur.pseudo][0]
        self.prepare_game(partie, pseudo2)
        self.root.master.pack_forget()
        self.root.master.master.children["!frame3"].pack(expand=True)

        
                
