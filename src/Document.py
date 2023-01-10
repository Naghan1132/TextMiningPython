import datetime

class Document:

    type = ""

    def __init__(self,titre,auteur,url,texte,date = datetime.datetime.now()):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

    def getTitre(self):
        return self.titre
    def getAuteur(self):
        return self.auteur
    def getDate(self):
        return self.date
    def getUrl(self):
        return self.url
    def getText(self):
        return self.texte

    def getType(self):
        pass

    def affichage(self):
        print("titre : "+self.titre)
        print("auteur : "+self.auteur) # instance de Redditor et pas str
        #print("date : "+self.date)
        #print("url : "+self.url)
        #print("texte : "+self.texte)
        print("__________\n")


    def __str__(self):
        return "voilà le titre du doc : "+self.titre


class RedditDocument(Document): #Document = Classe mère

    def __init__(self, titre, auteur, url, texte, date=datetime.datetime.now()):
        # constructeur de Document ou Document.__init(self,...,...,...)
        super().__init__(titre, auteur, url, texte, date)
        self.nbCommentaire = 0 # nouvelle variable propre à Reddit

    def getCaracteristique(self):
        return self.nbCommentaire

    def getNbCommentaire(self):
        return self.nbCommentaire

    def setNbCommentaire(self,nbCommentaire):
        self.nbCommentaire = nbCommentaire

    def getType(self):
        return "Reddit"

    def __str__(self):
        return "Reddit Document object : "

class ArxivDocument(Document): #Document = Classe mère

    def __init__(self,titre,auteur,url, texte,date = datetime.datetime.now()):
        # constructeur de Document ou Document.__init(self,...,...,...)
        super().__init__(titre,auteur,url, texte,date)
        #Document.__init__(self,...)
        #self.listeAuteur = auteur # nouvelle variable propre à Arxiv

    def getCaracteristique(self):
        return self.listeAuteur

    def getListeAutheurs(self):
        return self.listeAuteur

    def setListeAutheurs(self,listeAuteur):
        self.listeAuteur = listeAuteur

    def getType(self):
        return "Arxiv"

    def __str__(self):
        return "Arxiv Document object : "
