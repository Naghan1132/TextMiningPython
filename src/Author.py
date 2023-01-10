class Author:
    def __init__(self,name,ndoc,production):
        self.name = name
        self.ndoc = ndoc
        self.production = production # dictionnaire de doc écrits par l'auteur

    def nbDoc(self):
        return self.nbDoc

    def add(self,document):
        self.production[self.ndoc] = document
        self.ndoc += 1

    def moyenneDoc(self):
        total = 0
        for i in self.production.values():
            total += len(i.texte)
        return total/len(self.production) #la taille moyenne de tout les docs

    def affichage(self):
        print("nom de l'auteur est : "+self.name)
        print("nb document = ",self.ndoc)
        cpt = 1
        for i in self.production.values():
            print("document n°",cpt,i)
            cpt+=1
        print("________________")

    def __str__(self):
        return "nom de l'auteur est : "+self.name
