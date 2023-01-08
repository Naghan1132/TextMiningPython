from src.Document import *

class DocumentGenerator: # Générateur de Documents
    @staticmethod
    def factory(type,titre, auteur, url, texte, date):
        if type == "Arxiv" : return ArxivDocument(titre, auteur, url, texte, date)
        if type == "Reddit" : return RedditDocument(titre, auteur, url, texte, date)

        assert 0, "Erreur : "+ type # si le type en entrée est inconnu alors erreur
