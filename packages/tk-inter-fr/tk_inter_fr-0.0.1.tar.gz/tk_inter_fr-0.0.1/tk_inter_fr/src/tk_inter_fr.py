from tkinter import *


# la classe Fenetre
class Fennetre():

    # autres constructeur
    def __init__(self, titre="Fenetre", taille="400x400", icon=None, fen=Tk()):
        self.titre = titre
        self.taille = taille
        self.icon = icon
        self.TK_fr = fen

    def boucler(self):
        self.TK_fr.title(self.titre)
        self.TK_fr.geometry(self.taille)
        self.TK_fr.iconbitmap(self.icon)
        self.TK_fr.mainloop()


# panneau

class Panneau(Frame):

    def __init__(self, fen=Fennetre(), arrierPlan="#fff", longeur=100, hauteur=100, bordure=1, couleur=None):
        super().__init__(width=longeur, height=hauteur, border=bordure, bg=couleur)

    def position(self, ligne=0, colone=0, alignementGauche=None, alignementHaut=None):
        self.grid(row=ligne, column=colone, padx=alignementGauche, pady=alignementHaut)


# la classe etiquette LABEL
class Etiquette(Label):

    def __init__(self, fen=Fennetre(), texte=None, couleurText="#000", style=None):
        super().__init__(text=texte, fg=couleurText, font=style)

    def position(self, ligne=0, colonne=0, margeX=None, margeY=None):
        self.grid(row=ligne, column=colonne, padx=margeX, pady=margeY)


# la Classe zoneText ENTRY
class ZonneText(Entry):

    def __init__(self, fenetre=Fennetre(), longeur=None, arrierPlan=None, couleurText=None, bordure=None, masque=None,
                 etat=None, couleurFocus=None, valeur=None):
        super().__init__(width=longeur, bg=arrierPlan, fg=couleurText, bd=bordure, show=masque, state=etat,
                         highlightcolor=couleurFocus, textvariable=valeur)

    def position(self, ligne=0, colonne=0, margeX=None, margeY=None):
        self.grid(row=ligne, column=colonne, padx=margeX, pady=margeY)

    def valeur(self):
        return self.get()

    def supprimer(self, premier, dernier):
        self.premier = premier
        self.dernier = dernier
        Entry.delete(first=self.premier, last=self.dernier)


class Bouton(Button):
    def __init__(self, fenetre=Fennetre, texte=None, longeur=None, hauteur=None, couleurText=None, arrierPlan=None,
                 commande=None):
        super().__init__(text=texte, width=longeur, height=hauteur, fg=couleurText, bg=arrierPlan, command=commande)

    def position(self, ligne=0, colonne=0, margeX=None, margeY=None):
        self.grid(row=ligne, column=colonne, padx=margeX, pady=margeY)

    def clique(self, commande):
        super().__init__(command=commande)


class BarreMenu(Menu):
    def __init__(self, fenetre=Fennetre):
        super().__init__()
        self.fenetre = fenetre


class BoutonRadio(Radiobutton):
    def __init__(self, po=None, texte=None, valeur=None):
        super().__init__(text=texte, value=valeur)

    def position(self, ligne=0, colone=0, margeX=None, margeY=None):
        self.grid(row=ligne, column=colone, pady=margeY, padx=margeX)
