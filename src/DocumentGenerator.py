#from Document import ArxivDocument
from Document import *

class DocumentGenerator: # OK

    @staticmethod
    def factory(type,titre, auteur, url, texte, date):
        if type == "Arxiv" : return ArxivDocument(titre, auteur, url, texte, date)
        if type == "Reddit" : return RedditDocument(titre, auteur, url, texte, date)

        assert 0, "Erreur : "+ type # si le type entré est inconny