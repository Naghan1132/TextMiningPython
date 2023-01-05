import datetime
import urllib.request
import praw
import xmltodict
from importlib import reload
import src.Corpus
import src.Author
import src.DocumentGenerator

reload(src.Author)
reload(src.Corpus)
reload(src.DocumentGenerator)

# PARTIE 1 :

reddit = praw.Reddit(client_id='KL8AdjqIAdRyS3uaswVLCA',client_secret='5vOe4iyO_1XBrq0LISlxe06MlK1f-Q',user_agent='nathan')

id2doc = {}
id2aut = {}
docs = []

testAllDoc = []

corpus = src.Corpus.Corpus("Space",id2aut,id2doc)
#print(corpus)

indice = 1

#get 10 hot posts from the MachineLearning subreddit
hot_posts = reddit.subreddit('space').hot(limit=5)
for post in hot_posts:
    dateTime = datetime.datetime.utcfromtimestamp(post.created)
    post.selftext.replace("\r\n", " ")
    if post.selftext == "":
        #si c'est une image ou un lien dans le texte et pas une discussion etc... :
        docs.append([len(docs),post.title+" "+post.url,'reddit',post.url])
        #document = Document.Document(post.title,post.author.name,post.url,post.url,dateTime)
        document = src.DocumentGenerator.DocumentGenerator.factory("Reddit",post.title,post.author.name,post.url,post.url,dateTime)#tp5
        testAllDoc.append(document)
        corpus.addDoc(document)
    else:
        post.selftext.replace("\r\n", " ")
        docs.append([len(docs),post.selftext,'reddit',post.url])
        #document = Document.Document(post.title,post.author.name,post.url,post.selftext,dateTime)
        document = src.DocumentGenerator.DocumentGenerator.factory("Reddit",post.title,post.author.name,post.url,post.selftext,dateTime) #tp5
        corpus.addDoc(document)
        testAllDoc.append(document)

    id2doc[indice] = document
    indice += 1
    #commentaires :
    commentaireList = []
    post.comments.replace_more(limit=None)
    for comment in post.comments.list():
        #FAIRE JUSTE len(post.comments.list())
        commentaireList.append(comment)
    document.setNbCommentaire(len(commentaireList))
    #
    i = id2aut.get(post.author.name)
    if i:
        #auteur = True
        i.add(document)
    else:
        production = {}
        auteur = src.Author.Author(post.author.name,0,production)
        auteur.add(document)
        id2aut[post.author.name] = auteur

# ==== ARXIV ====

url = 'http://export.arxiv.org/api/query?search_query=all:space&start=0&max_results=5'

data = urllib.request.urlopen(url)

xml = data.read().decode('utf-8')
#print(xml)
dic = xmltodict.parse(xml)

for values in dic['feed']['entry']:
    trucDate = datetime.datetime.strptime(values.get('published'),"%Y-%m-%dT%H:%M:%SZ")
    resumer = values.get('summary') # ok
    resumer.replace("\r\n"," ")
    link = values.get('link')
    url = link[0].get('@href') # ok
    docs.append([len(docs),resumer,'arxiv',url])
    nomAuteur = values.get('author')

    if len(nomAuteur) == 1:
        # juste dico {}
        for a in nomAuteur.values():
            #Un seul auteur
            #document = Document.ArxivDocument(values.get('title'),a,url,resumer,trucDate)
            document = src.DocumentGenerator.DocumentGenerator.factory("Arxiv",values.get('title'),a,url,resumer,trucDate) #tp5*
            listeA = []
            listeA.append(a)
            document.setListeAutheurs(listeA)
            corpus.addDoc(document)
            id2doc[indice] = document
            indice += 1
            i = id2aut.get(a)
            if i:
                i.add(document)
            else:
                production = {}
                auteur = src.Author.Author(a,0,production)
                auteur.add(document)
                id2aut[a] = auteur
    else:
        #alors [{}]
        listeAuteur = []
        for a in nomAuteur:
            for valeurNom in a.values():
                listeAuteur.append(valeurNom)
                #plusieurs autheurs alors on ajoute plusieurs fois le doc
        #document = Document.ArxivDocument(values.get('title'),listeAuteur,url,resumer,trucDate) #
        #Mettre le premier auteur dans l'auteur de base => puis on rajoute
        document = src.DocumentGenerator.DocumentGenerator.factory("Arxiv",values.get('title'),listeAuteur[0],url,resumer,trucDate) #tp5
        document.setListeAutheurs(listeAuteur)
        corpus.addDoc(document)
        id2doc[indice] = document
        indice += 1
        for nomAuteur in listeAuteur:
            i = id2aut.get(nomAuteur)
            if i:
                i.add(document)
            else:
                production = {}
                auteur = src.Author.Author(nomAuteur,0,production)
                auteur.add(document)
                id2aut[nomAuteur] = auteur

#_______________________________

# PARTIE 2 :

#exemple création d'un dataFrame depuis des subreddit :

#posts = []
#ml_subreddit = reddit.subreddit('MachineLearning')
#for post in ml_subreddit.hot(limit=5):
#    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
#posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
#display(posts) #display dataframe


#df = pd.DataFrame(docs,columns=['id','texte','source','url'])
#df = pd.DataFrame.from_dict(id2doc,orient="index",columns=['titre','auteur','date','url','texte'])

#display(df) #display dataframe

#df.to_csv("tp3.csv", sep='\t',encoding='utf-8') # = save, le charger à chaque fois (pas besoin de re-intéroger les APIs)

#ne pas interroger les APIs à chaque fois => charger le .csv
#with open("tp3.csv", "r") as f:
#   corpus = pd.read_csv(f, sep="\t")

# =============== SAUVEGARDE DES DONNÉES REDIT/ARXIV ===============
import pickle

with open("id2doc.pkl", "wb") as f:
    pickle.dump(id2doc, f)

# Ouverture d'un fichier, puis écriture avec pickle
with open("id2aut.pkl", "wb") as f:
    pickle.dump(id2aut, f)

print("FINI DE CHARGER LES DONNÉES")

#[for v in corpus.get_coll().values()]:
# ou
#[b.getNom() for b in [*corpus.get_coll.values()]]
