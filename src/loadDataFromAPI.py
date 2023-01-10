import datetime
import urllib.request
import praw
import xmltodict
from importlib import reload
import Corpus
import Author
import DocumentGenerator

reload(Author)
reload(Corpus)
reload(DocumentGenerator)

# =============== INITIALISATION VARIABLES ===============

id2doc = {}
id2aut = {}
indice = 1

# =============== REDDIT ===============

reddit = praw.Reddit(client_id='KL8AdjqIAdRyS3uaswVLCA',client_secret='5vOe4iyO_1XBrq0LISlxe06MlK1f-Q',user_agent='nathan')
hot_posts = reddit.subreddit('space').hot(limit=1000) # get n first hot posts from the Space subreddit

nb_doc_non_vide = 0

for post in hot_posts:
    if nb_doc_non_vide == 40:
        break
    dateTime = datetime.datetime.utcfromtimestamp(post.created)
    post.selftext.replace("\r\n", " ")
    if len(post.selftext.strip()) > 60 and post.author != None:
        nb_doc_non_vide += 1
        document = DocumentGenerator.DocumentGenerator.factory("Reddit",post.title,post.author.name,post.url,post.selftext,dateTime)

        id2doc[indice] = document
        indice += 1

        # commentaires :
        commentaireList = []
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            commentaireList.append(comment)
        document.setNbCommentaire(len(commentaireList))

        # auteurs :
        authorInId2aut = id2aut.get(post.author.name)
        if authorInId2aut:
            authorInId2aut.add(document)
        else:
            production = {}
            auteur = Author.Author(post.author.name,0,production)
            auteur.add(document)
            id2aut[post.author.name] = auteur

# =============== ARXIV ===============

url = 'http://export.arxiv.org/api/query?search_query=all:space&start=0&max_results='+str(nb_doc_non_vide)

data = urllib.request.urlopen(url)
xml = data.read().decode('utf-8')
dic = xmltodict.parse(xml)

for values in dic['feed']['entry']:
    dateModified = datetime.datetime.strptime(values.get('published'),"%Y-%m-%dT%H:%M:%SZ")
    resumer = values.get('summary') # ok
    resumer.replace("\r\n"," ")
    link = values.get('link')
    url = link[0].get('@href') # ok
    nomAuteur = values.get('author')

    if len(nomAuteur) == 1:
        # juste dico {}
        for a in nomAuteur.values():
            # Un seul auteur
            document = DocumentGenerator.DocumentGenerator.factory("Arxiv",values.get('title'),a,url,resumer,dateModified)
            listeA = []
            listeA.append(a)
            document.setListeAutheurs(listeA)
            id2doc[indice] = document
            indice += 1
            authorInId2aut = id2aut.get(a)
            if authorInId2aut:
                authorInId2aut.add(document)
            else:
                production = {}
                auteur = Author.Author(a,0,production)
                auteur.add(document)
                id2aut[a] = auteur
    else:
        # alors [{}]
        listeAuteur = []
        for a in nomAuteur:
            for valeurNom in a.values():
                listeAuteur.append(valeurNom)
                # plusieurs autheurs alors on ajoute plusieurs fois le doc
        # Mettre le premier auteur dans l'auteur de base => puis on rajoute
        document = DocumentGenerator.DocumentGenerator.factory("Arxiv",values.get('title'),listeAuteur[0],url,resumer,dateModified) #tp5
        document.setListeAutheurs(listeAuteur)
        id2doc[indice] = document
        indice += 1
        for nomAuteur in listeAuteur:
            authorInId2aut = id2aut.get(nomAuteur)
            if authorInId2aut:
                authorInId2aut.add(document)
            else:
                production = {}
                auteur = Author.Author(nomAuteur,0,production)
                auteur.add(document)
                id2aut[nomAuteur] = auteur


# =============== SAUVEGARDE DES DONNÉES REDIT/ARXIV ===============

import pickle

# Ouverture d'un fichier, puis écriture avec pickle

with open("../test_data/id2doc.pkl", "wb") as f:
    pickle.dump(id2doc, f)

with open("../test_data/id2aut.pkl", "wb") as f:
    pickle.dump(id2aut, f)

print("CHARGEMENT DES DONNÉES TERMINÉ")