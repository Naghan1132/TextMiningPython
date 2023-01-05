import pandas as pd
import re
from scipy.sparse import csr_matrix
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
import string

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
        self.buildVocab()

    def addDoc(self,document):
        if len(self.id2doc.keys()) == 0:
            indice = 1
        else:
            indice = max(list(self.id2doc.keys())) + 1
        self.id2doc[indice] = document
    def setAuteurs(self,dicAuteurs):
        self.authors = dicAuteurs
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

    def __repr__(self):
        pass

    def buildChaineUnique(self):
        liste = []
        for i in self.id2doc.values():
            txt = i.getText().replace("\n", " ")
            liste.append(txt)
        self.chaineUnique = " ".join(liste) # OK

    def search(self,mot):
        #retourne les passages des documents contenant le mot-clef entré en paramétre
        if self.chaineUnique == "":
            self.buildChaineUnique()

        passages = []
        texte = self.chaineUnique.split(". ")
        for i in texte:
            if re.search(mot, i): # si ça match on retourne la phrase
                passages.append(i)
        return passages


    def concorde(self,mot,tailleContexte):
        if self.chaineUnique == "":
            self.buildChaineUnique()

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
        if self.chaineUnique == "":
            self.buildChaineUnique()
        chaine = self.nettoyer_texte(self.chaineUnique)
        mots = re.split(r'\s+', chaine) # split la liste avec espaces
        setVoca = sorted(set(mots)) # élimine les doublons et range par ordre alphabétique
        print("taille du vocabulaire : ",len(setVoca))
        print(setVoca)
        vocabulaire = {}
        id = 0
        for valeur in setVoca:
            if valeur != '': #sinon ça mets la chaine vide dans le vocabulaire....
                vocabulaire[valeur] = {'id':id,'term frequency':0,'document frequency':0} # mettre un id unique en 1ere position ?
                id += 1
        self.vocab = vocabulaire

    def nettoyer_texte(self,chaine):
        chaine = chaine.lower() # mets tout en minuscule
        chaine = chaine.replace("\r\n"," ") # remplace le saut de ligne par une chaine vide
        chaine = re.sub(r'\b\w*\d+\w*\b', '', chaine) # enlève tous mots qui contiennent des chiffres
        chaine = re.sub(r'https?://\S+|www\S+', '', chaine) # enlève les mots qui contiennent des liens (https,http, www etc...)
        chaine = re.sub(r'[^\w\s]', ' ',chaine) # remplace la ponctuaction par des espaces => A CAUSE DE ÇA QUE ÇA CONCATENE
        # test
        chaine = re.sub(r'\b\w*[^\w\s]\w*|\b\w*\d+\w*\b', '', chaine) # remove_words_with_non_letters

        #stop_words = set(stopwords.words('english')) # IMPORTANT
        #words = [w for w in words if not w in stop_words]
        # filter token with 1 char
        #words = [w for w in words if len(w)>1]
        #cleaned_doc = ' '.join(word for word in stemmed) # pour faire un paragraph entier (concatene les mots)

        #bug aussi du underscore => peut-être pas compté dans la punctuation => préciser à chat gpt
        return chaine
    def nettoyer_texte2(self,chaine): # test avec le tp3 Ingénierie des Données
        # enlever le stemmer peut-être ?
        chaine.split()
        # tokenize
        tokens = word_tokenize(chaine)
        #convert in lower case
        tokens = [w.lower() for w in tokens]
        #prepare regex for char filtering
        re_punc = re.compile('[%s]' % re.escape(string.punctuation))
        # remove punctuation from each word
        stripped = [re_punc.sub('',w) for w in tokens]
        # remove remainning token that are not alphabetic
        words = [word for word in stripped if word.isalpha()]
        #filter out stop words
        stop_words = set(stopwords.words('english')) # IMPORTANT
        words = [w for w in words if not w in stop_words]
        # filter token with 1 char
        words = [w for w in words if len(w)>1]

        cleaned_doc = ' '.join(word for word in words) # pour faire un paragraph entier (concatene les mots)
        return cleaned_doc

    def stats(self,n): # OK
        # PAS VRAIMENT ÇA, A FAIRE DANS LA FONCTION matrice()
        # elle doit afficher : Le nombre de mots diff ́erents dans le corpus
        # et : Afficher les n mots les plus fréquents (n est un paramètre)
        print("Nombre de mots différents dans le corpus : ",len(self.vocab))

        for doc in self.id2doc.values():
            text = doc.getText()
            cleanedChaine = self.nettoyer_texte(text)
            splitedWords = re.split(r"[\b\W\b]+",cleanedChaine) # split la liste avec espaces, ponctuation etc...
            listeDejaVu = []
            for word in splitedWords:
                if word in self.vocab.keys(): # combien de fois le mot apparait en tout
                    self.vocab[word]['term frequency'] += 1
                    if word not in listeDejaVu: # dans combien de document apparait le mot
                        self.vocab[word]['document frequency'] += 1
                        listeDejaVu.append(word)

        df = pd.DataFrame(self.vocab)
        df = df.T # transpose = inverser rows et col
        display(df)

    def matrice(self):
        # POUR partie 1 : TP 7

        rows = [] #document (i)
        cols = [] # mot (j)
        data = [] # à l'intersection (i,j) on place le nb d'occurence du mot dans le document

        testDict = {}
        for doc in self.id2doc.values():
            rows.append(doc.getTitre())
            testDict[doc.getTitre()] = {}
            docText = doc.getText()
            chaineCleaned = self.nettoyer_texte(docText)
            splitedWords = re.split(r"[\b\W\b]+",chaineCleaned) # split la liste avec espaces, ponctuation etc...
            deja_vu = []

            for word in splitedWords:
                if word in self.vocab.keys(): # il est dans le vocabulaire
                    self.vocab[word]['term frequency'] += 1
                    if word not in deja_vu: # première fois que l'on tombe dessus dans le document
                        nbOccurence = splitedWords.count(word) # on compte directement tout les mêmes mots d'un texte
                        testDict[doc.getTitre()][word] = nbOccurence
                        deja_vu.append(word)
                        data.append(nbOccurence)
                        self.vocab[word]['document frequency'] += 1

        print(self.vocab)
        #print(testDict) # OK
        df = pd.DataFrame(testDict)
        #display(df)
        df.to_csv("testDF.csv", sep='\t',encoding='utf-8')

        #df=pd.DataFrame({"Name":['Tom','Nick','John','Peter'],"Age":[15,26,17,28]})
        #mat_TF = csr_matrix((data, (rows,cols)),shape=(len(rows),len(cols))).toarray()
        #df = pd.DataFrame(data)
        #display(df)
        #mat_TF = csr_matrix(data,(rows,cols)).toarray()


        #print(data)
        #mat_TF = csr_matrix(data)
        #return mat_TF
        #mat_TF_IDF = csr_matrix((data,(rows,cols))).toarray()
        #row = np.array([0, 1, 2, 0])
        #col = np.array([0, 1, 1, 0])
        #data = np.array([1, 2, 4, 8])

        #csr_matrix((data, (row, col)), shape=(3, 3)).toarray()
        #array([[9, 0, 0],
        #       [0, 2, 0],
        #       [0, 4, 0]])

    def recherche(self,motsCles):
        # POUR partie 2 : TP 7
        vectMots = self.nettoyer_texte(motsCles)


