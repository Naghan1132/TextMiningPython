import pickle

# Ouverture du fichier, puis lecture avec pickle
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

corpus.buildVocab()


#print(corpus.search("algebra"))
#print(corpus.concorde("algebra",5))

#print(corpus.stats(10))

#print(corpus.stats())
print(corpus.matrice())