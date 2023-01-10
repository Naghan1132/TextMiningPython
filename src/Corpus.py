import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import math
from numpy import dot
from numpy.linalg import norm

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
        self.authors = authors # dictionnaire d'auteurs
        self.id2doc = id2doc # dictionnaire de docs
        self.naut = len(authors) # nb autheur
        self.ndoc = len(id2doc) # nb document
        self.chaineUnique = ""
        self.vocab = {}
        self.buildChaineUnique()
        self.buildVocab()
        self.dfTri = {}
        self.dfTF = pd.DataFrame()
        self.dfTFxIDF = pd.DataFrame()

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

        listeDate.sort() # OK
        indice = 0
        dicTri = {}
        while indice < nombreDocVoulu:
            for doc in self.id2doc.values():
                if listeDate[indice] == doc.date and indice < nombreDocVoulu:
                    dicTri[indice] = doc
                    indice += 1
        return dicTri

    def trieTitre(self,nombreDocVoulu):
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

    def save(self,nom):
        dic = {}
        df = pd.DataFrame.from_dict(dic,orient="index",columns=['titre','auteur','date','url','texte'])
        df.to_csv(nom+".csv", sep='\t',encoding='utf-8')

    def load(self,nom):
        with open(nom+".csv", "r") as f:
            corpus = pd.read_csv(f, sep="\t")
        return corpus

    def __repr__(self):
        return "Corpus ",self.nom," avec ",self.ndoc," documents"

    def buildChaineUnique(self):
        liste = []
        for i in self.id2doc.values():
            txt = i.getText().replace("\n", " ")
            liste.append(txt)
        self.chaineUnique = " ".join(liste)

    def search(self,mot):
        # retourne les passages des documents contenant le mot-clef entré en paramétre
        passages = []
        texte = self.chaineUnique.split(". ")
        for i in texte:
            if re.search(mot, i): # si ça match on retourne la phrase
                passages.append(i)
        return passages

    def concorde(self,mot,tailleContexte):
        passages = {}
        passages["contexte gauche"] = []
        passages["motif trouvé"] = []
        passages["contexte droite"] = []

        phrases = self.chaineUnique.split(". ")

        for phrase in phrases:
            if re.search(mot,phrase): # on trouve le mot voulu dans la phrase
                span = re.search(mot,phrase).span()
                gauche = phrase[span[0]-tailleContexte:span[0]]
                txt = phrase[span[0]:span[1]]
                droite = phrase[span[1]:span[1]+tailleContexte]
                passages["contexte gauche"].append(gauche)
                passages["motif trouvé"].append(txt)
                passages["contexte droite"].append(droite)

        df = pd.DataFrame.from_dict(passages)
        display(df)

    def get_id2doc_DF(self):
        df = pd.DataFrame(columns=['Id','Nom','Auteur','Date','dateFr','URL','Text','Textabrv','Type','Caractéristiques'])
        i=1
        for doc in self.id2doc.values():
            row = [i,doc.getTitre(),doc.getAuteur(),doc.getDate().date(),doc.getDate().strftime("%d/%m/%y"),doc.getUrl(),doc.getText(),doc.getText()[:10]+'...',doc.getType(),doc.getCaracteristique()]
            df.loc[len(df)] = row
            i+=1
        return df

    def getdfTF(self):
        return self.dfTF

    def getdfTFxIdf(self):
        return self.dfTFxIDF

    def buildVocab(self):
        chaine = self.nettoyer_texte(self.chaineUnique)
        mots = re.split(r'\s+', chaine) # split la liste avec espaces
        setVoca = sorted(set(mots)) # élimine les doublons et range par ordre alphabétique
        vocabulaire = {}
        id = 0
        for valeur in setVoca:
            if valeur != '': # sinon ça mets la chaine vide dans le vocabulaire
                vocabulaire[valeur] = {'id':id,'term frequency':0,'document frequency':0} # mettre un id unique en 1ere position ?
                id += 1
        self.vocab = vocabulaire

    def nettoyer_texte(self,chaine):
        # remove links
        chaine = re.sub(r'https?://\S+|www\S+', '', chaine) # enlève les mots qui contiennent des liens (https,http, www etc...)
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
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]
        # filter token with 1 char
        words = [w for w in words if len(w)>1]
        cleaned_doc = ' '.join(word for word in words) # pour faire un paragraphe entier (concatene les mots)
        return cleaned_doc

    def stats(self,n): # OK
        print("Nombre de mots différents dans le corpus : ",len(self.vocab))
        trie = sorted(self.vocab.items(), key=lambda x: x[1]['term frequency'], reverse=True)
        for i in range(n):
            valeur = trie[i]
            print(f"{i + 1}ème position : {valeur[0]} = {valeur[1]['term frequency']} term frequency")

        df = pd.DataFrame(self.vocab)
        df = df.T # transpose = inverser rows et col
        display(df)

        return trie


    def matrice(self):
        # POUR partie 1 : TP 7
        mat_tf = {}

        for doc in self.id2doc.values():
            mat_tf[doc.getTitre()] = {}

            docText = doc.getText()
            chaineCleaned = self.nettoyer_texte(docText)
            splitedWords = re.split('\s+', chaineCleaned) # split la liste avec espaces

            deja_vu = []

            for word in self.vocab.keys(): # initialisation
                mat_tf[doc.getTitre()][word] = 0

            for word in splitedWords:
                mat_tf[doc.getTitre()][word] = 0 # initialisation (bug)
                if word in self.vocab.keys(): # il est dans le vocabulaire
                    self.vocab[word]['term frequency'] += 1
                    if word not in deja_vu: # première fois que l'on tombe dessus dans le document
                        nbOccurence = splitedWords.count(word) # on compte directement tout les mêmes mots d'un texte
                        mat_tf[doc.getTitre()][word] = nbOccurence
                        deja_vu.append(word)
                        self.vocab[word]['document frequency'] += 1

        # ==== TF_IDF === :
        # dictionnaire qui contiendra les mots de chaque document et leur fréquence
        tf_scores = {}

        # calcul de la fréquence de chaque mot dans chaque document
        for doc in self.id2doc.values():
            chaineCleaned = self.nettoyer_texte(doc.getText())
            splitedWords = chaineCleaned.split() # split la liste avec espaces
            for word in splitedWords:
                if word in tf_scores:
                    tf_scores[word]['doc_count'] += 1
                else:
                    tf_scores[word] = {'doc_count': 1}

        # calcul de la fréquence de chaque mot dans tous les documents
        for word, scores in tf_scores.items():
            # tout les mots qui ne sont pas dans le
            # mettre à 0 les mots qui manquent au vocabulaire
            tf_scores[word]['total_count'] = sum(1 for doc in self.id2doc.values() if word in doc.getText())

        # dictionnaire qui contiendra les mots et leur score idf
        idf_scores = {}

        # calcul du score idf pour chaque mot
        for word, scores in tf_scores.items():
            #print(scores['total_count'])
            if scores['total_count'] == 0:
                idf_scores[word] = 0
            else:
                idf_scores[word] = math.log(len(self.id2doc) / scores['total_count'])

        # création de la matrice tf-idf
        mat_TFxIDF = {}
        for doc in self.id2doc.values():
            mat_TFxIDF[doc.getTitre()] = {}
            chaineCleaned = self.nettoyer_texte(doc.getText())
            splitedWords = chaineCleaned.split() # split la liste avec espaces
            for word in self.vocab.keys(): # initialisation
                mat_TFxIDF[doc.getTitre()][word] = 0
            for word in splitedWords:
                tf = tf_scores[word]['doc_count'] / len(splitedWords)
                idf = idf_scores[word]
                mat_TFxIDF[doc.getTitre()][word] = tf * idf

        dfTF = pd.DataFrame(mat_tf) # OK
        dfTFxIDF = pd.DataFrame(mat_TFxIDF) # OK

        self.dfTF = dfTF
        self.dfTFxIDF =dfTFxIDF

        display(dfTFxIDF)
        dfTF.to_csv("../output_data/TF.csv", sep='\t',encoding='utf-8')
        dfTFxIDF.to_csv("../output_data/TFxIDF.csv", sep='\t',encoding='utf-8')

    def recherche(self,motsCles):
        # vecteur 'motsCles' :
        vectorMotCles = []
        for word in self.vocab.keys():
            if word in motsCles:
                vectorMotCles.append(1)
            else:
                vectorMotCles.append(0)

        # Vecteur de chaque document
        dictVectors = {}
        for doc in self.id2doc.values():
            dictVectors[doc.getTitre()] = []
            chaineCleaned = self.nettoyer_texte(doc.getText())
            splitedWords = chaineCleaned.split() # split la liste avec espaces
            for word in self.vocab.keys():
                if word in splitedWords:
                    dictVectors[doc.getTitre()].append(1)
                else:
                    dictVectors[doc.getTitre()].append(0)

        # Calculer la similarité entre 'vectorMotCles' et chaque vecteurs
        res = {}
        for title,vector in dictVectors.items():
            if norm(vectorMotCles) * norm(vector) == 0:
                cosine_similarity = 0.0
            else:
                cosine_similarity = dot(vectorMotCles, vector) / (norm(vectorMotCles) * norm(vector))
            res[title] = cosine_similarity

        print("--------------------------------------")
        self.dfTri = dict(sorted(res.items(), key=lambda x: x[1],reverse=True))

        return self.dfTri