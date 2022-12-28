import pandas as pd
import re
from scipy.sparse import csr_matrix

# Un singleton est un patron de conception qui permet
# de s'assurer qu'une classe ne dispose que d'une et une seule instance.

'''def singleton(Corpus):
    instances = [None]
    def wrapper(nom, authors, id2doc):
        if instances[0] is None:
            instances[0] = Corpus(nom, authors, id2doc)
        return instances[0]
    return wrapper'''


#@singleton
class Corpus:

    def __init__(self,nom,authors,id2doc):
        #variable privée : __variable
        self.nom = nom
        self.authors = authors #dictionnaire d'auteurs
        self.id2doc = id2doc #dictionnaire de docs
        self.naut = len(authors) #nb autheur
        self.ndoc = len(id2doc) #nb document
        self.chaineUnique = ""
        self.vocab = {}

    def addDoc(self,document):
        if len(self.id2doc.keys()) == 0:
            indice = 1
        else:
            indice = max(list(self.id2doc.keys())) + 1
        self.id2doc[indice] = document

    def trieDate(self,nombreDocVoulu):
        listeDate = []
        #listeDate.sort(reverse=True)
        for doc in self.id2doc.values():
            listeDate.append(doc.date)

        listeDate.sort()#OK
        indice = 0
        dicTri = {}
        while indice < nombreDocVoulu:
            for doc in self.id2doc.values():
                if listeDate[indice] == doc.date and indice < nombreDocVoulu:
                    dicTri[indice] = doc
                    indice += 1
        return dicTri

    def trieTitre(self,nombreDocVoulu):
        print("test")
        listeTitre = []
        for doc in self.id2doc.values():
            listeTitre.append(doc.titre)

        listeTitre.sort()
        indice = 0
        dicTri = {}
        while indice < nombreDocVoulu:
            for doc in self.id2doc.values():
                if listeTitre[indice] == doc.titre and indice < nombreDocVoulu:
                    dicTri[indice] = doc
                    indice += 1
        return dicTri

    def save(self,nom): # KO
        # faire ça ?
        #print(self.id2doc)
        #df = pd.DataFrame.from_dict(dic,orient="index",columns=['titre','auteur','date','url','texte'])

        #df.to_csv(nom+".csv", sep='\t',encoding='utf-8')
        pass

    def load(self,nom):
        with open(nom+".csv", "r") as f:
            corpus = pd.read_csv(f, sep="\t")
        #return corpus

    def setAuteurs(self,dicAuteurs):
        self.authors = dicAuteurs

    def __repr__(self):
        pass

    def search(self,mot):
        #retourne les passages des documents contenant le mot-clef entré en paramétre
        if self.chaineUnique == "":
            liste = []
            for i in self.id2doc.values():
                txt = i.getText().replace("\n", " ")
                liste.append(txt)
            self.chaineUnique = " ".join(liste) # OK

        passages = []
        texte = self.chaineUnique.split(". ")
        for i in texte:
            if re.search(mot, i): # si ça match on retourne la phrase
                passages.append(i)
        return passages


    def concorde(self,mot,tailleContexte):
        if self.chaineUnique == "":
            liste = []
            for i in self.id2doc.values():
                txt = i.getText().replace("\n", " ")
                liste.append(txt)
            self.chaineUnique = " ".join(liste) # OK

        passages = {}
        passages["contexte gauche"] = []
        passages["motif trouvé"] = []
        passages["contexte droite"] = []

        phrases = self.chaineUnique.split(". ")
        #print("texte ",texte)
        for phrase in phrases:
            if re.search(mot,phrase): # on trouve le mot voulu dans la phrase
                #print("mot trouvé !")
                #print(phrase)
                span = re.search(mot,phrase).span()
                #print("position : ",span)
                gauche = phrase[span[0]-tailleContexte:span[0]]
                txt = phrase[span[0]:span[1]]
                droite = phrase[span[1]:span[1]+tailleContexte]
                passages["contexte gauche"].append(gauche)
                passages["motif trouvé"].append(txt)
                passages["contexte droite"].append(droite)
                #GÉRER LES ERREURS SI ON SORT DE LA TAILLE DE LA PHRASE

        print(passages)
        df = pd.DataFrame.from_dict(passages)
        print(df)
    
    def get_id2doc_DF(self):
        df = pd.DataFrame(columns=['Id','Nom','Auteur','Date','URL','Text'])
        i=1
        for doc in self.id2doc.values():           
            row = [i,doc.getTitre(),doc.getAuteur(),doc.getDate(),doc.getUrl(),doc.getText()[:10]+'...']
            df.loc[len(df)] = row
            i+=1
        return df

    
    def buildVocab(self):
        chaine = self.nettoyer_texte(self.chaineUnique)
        texte = re.split(r"[\b\W\b]+",chaine) # split la liste avec espaces, ponctuation etc...
        setVoca = sorted(set(texte)) # élimine les doublons
        print("nombre de mots différents dans le corpus ",len(setVoca))
        vocabulaire = {}
        for valeur in setVoca:
            vocabulaire[valeur] = {'term frequency':0,'document frequency':0}
        self.vocab = vocabulaire

    def stats(self):
        if self.chaineUnique == "":
            liste = []
            for i in self.id2doc.values():
                txt = i.getText().replace("\n", " ")
                liste.append(txt)
            self.chaineUnique = " ".join(liste) # OK
        # tp 6
        chaine = self.nettoyer_texte(self.chaineUnique)
        texte = re.split(r"[\b\W\b]+",chaine) # split la liste avec espaces, ponctuation etc...
        setVoca = sorted(set(texte)) # élimine les doublons
        print("nombre de mots différents dans le corpus ",len(setVoca))
        vocabulaire = {}
        for valeur in setVoca:
            vocabulaire[valeur] = {'term frequency':0,'document frequency':0}

        for doc in self.id2doc.values():
            txt = doc.getText()
            chaine = self.nettoyer_texte(txt)
            truc = re.split(r"[\b\W\b]+",chaine) # split la liste avec espaces, ponctuation etc...
            listeDejaVu = []
            for i in truc:
                if i in setVoca: # si il est dans le vocabulaire alors on ajoute
                    vocabulaire[i]['term frequency'] += 1
                    if i not in listeDejaVu:
                        vocabulaire[i]['document frequency'] += 1
                        listeDejaVu.append(i)

        print(vocabulaire)
        df = pd.DataFrame(vocabulaire)
        df = df.T # transpose = inverser rows et col
        
    def nettoyer_texte(self,chaine):
        chaine.lower()
        chaine.replace("\r\n", " ")
        re.sub(r'[^\w\s]','',chaine) # pas très utile
        re.sub(r'[0-9]','',chaine)
        print("chaine nettoyée => ",chaine)
        # remplacer les ponctuations et les chiffres `a l’aide d’expressions r ́eguli`eres
        # appropri ́ees
        return chaine

    def matrice(self):
        # POUR TP 7
        chaine = self.nettoyer_texte(self.chaineUnique)
        texte = re.split(r"[\b\W\b]+",chaine) # split la liste avec espaces, ponctuation etc...
        setVoca = sorted(set(texte)) # élimine les doublons et trie

        data = []
        rows = [] #document
        cols = [] # mot
        for valeur in setVoca:
            cols.append(valeur)
        # OK
        for doc in self.id2doc.values():
            rows.append(doc.getTitre())
            txt = doc.getText()
            chaine = self.nettoyer_texte(txt)
            truc = re.split(r"[\b\W\b]+",chaine) # split la liste avec espaces, ponctuation etc...
            deja_vu = []
            for i in truc:
                if i in setVoca and i not in deja_vu: # si il est dans le vocabulaire alors on ajoute
                    nbOccurence = truc.count(i)
                    deja_vu.append(i)
                    data.append(nbOccurence)
        #mat_TF = csr_matrix(data,(rows,cols),shape=(len(rows),len(cols))).toarray()
        mat_TF = csr_matrix(data,(rows,cols)).toarray()

        return mat_TF
        #mat_TFxIDF = csr_matrix((data,(rows,cols))).toarray()
        #row = np.array([0, 1, 2, 0])
        #col = np.array([0, 1, 1, 0])
        #data = np.array([1, 2, 4, 8])

        #csr_matrix((data, (row, col)), shape=(3, 3)).toarray()
        #array([[9, 0, 0],
        #       [0, 2, 0],
        #       [0, 4, 0]])

    def recherche(self,motsCles):
        #TP 7 : part 2
        vectMots = self.nettoyer_texte(motsCles)


