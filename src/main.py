import pickle
import src.Corpus
from importlib import reload

reload(src.Corpus)

# Ouverture du fichier, puis lecture avec pickle
with open("../test_data/id2doc.pkl", "rb") as f:
    id2doc = pickle.load(f)

# Ouverture du fichier, puis lecture avec pickle
with open("../test_data/id2aut.pkl", "rb") as f:
    id2aut = pickle.load(f)


corpus = src.Corpus.Corpus("Space",id2aut,id2doc)

#print(corpus.search("algebra"))
#print(corpus.concorde("algebra",5))
print(corpus.matrice())
#print(corpus.recherche(["space","new"]))
#print(corpus.testR(["space","stars"]))
#print(corpus.stats(10))
