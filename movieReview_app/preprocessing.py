import pandas as pd
import nltk
import re

from nltk.corpus import stopwords
from pyparsing import col
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import STOPWORDS, WordCloud

APP_PATH = "movieReview_app"
STOPWORDS_FR = set(stopwords.words("french"))

STOPWORDS_CUSTOM = {}
# STOPWORDS_CUSTOM = {"di", "caprio", "effets", "spéciaux", "marion", "cotillard"}
# STOPWORDS_CUSTOM = {"a", "si", "c'est", "j'ai", "qu'il", "ça", "comme", "film", "car", "tout", "plu", "marion cotillard", "tou", "ici", "di caprio", "effets spéciaux", "alors", "leonardo", "di", "caprio", "marion", "cotillard", "parce", "effets", "spéciaux", "depuis", "pu", "toutes", "shutter", "island", "dicaprio", "tous", "donc", "avoir", "assez", "aprè", "cela", "ca", "entre", "déjà", "christopher", "toujour", "toujours", "après", "autres", "début", "final"}

STOPWORDS = STOPWORDS_FR.union(STOPWORDS_CUSTOM)
MAX_WORDS = 20

# À décommenter lors de la première exécution
# nltk.download()


def tokenization(data_to_tokenize):
    '''Retourne le dataset complété d'une colonne avec l'ensemble des tokens trouvés dans les commentaires
    '''
    
    # Affectation d'une copie du dataset
    data = data_to_tokenize.copy()

    # Affectation de la fonction de filtrage des mots vides
    filtre_stopfr = lambda text: [token for token in text if token.lower() not in STOPWORDS]

    # Affectation de la fonction de filtrage des ponctuations
    sp_pattern = re.compile("""[\.\!\"\s\?\-\,\'\’\(\)\:\;\ ]+""", re.M).split

    # # Instanciation de la liste des tokens
    tokens = []

    # Suppression des lignes ayant une valeur nulle
    data = data.dropna()

    # Extraction des tokens de chaque commentaires suivant les filtres utilisés 
    for index, row in data.iterrows():
        row.comment = " ".join(sp_pattern(row.comment)).lower()
        tokens.append(" ".join(filtre_stopfr(nltk.word_tokenize(row.comment, language="french"))))

    data = data.assign(tokens = tokens)
    
    # Suppression de la colonne des commentaires
    data.drop("comment", axis=1, inplace=True)

    return data


def calculate_opinion(data):
    '''Retourne le dataset complété d'une colonne avec la tendance des opinions
    '''

    # Affectation de la Serie des notes 
    ratings = data.rating

    # Instanciation de la liste des opinions
    opinions = []

    # Parcours de l'ensemble des notes et calcul des opinions
    for rating in ratings:
        if float(rating) < 3.0:
            opinions.append("negative")
        else:
            opinions.append("positive")
    
    # Ajout d'une colonne opinions
    data = data.assign(opinions = opinions)

    # Suppression de la colonne rating
    data.drop("rating", axis=1, inplace=True)

    return data


def get_words_freq(data, num_words_max = MAX_WORDS):
    '''Affiche la fréquence des mots utilisés dans chaque commentaire
    '''


    for tokens in data.tokens:
        tokens_freq = nltk.FreqDist(tokens)
        print(tokens_freq.most_common(num_words_max))


#TODO: Séparer en 2 fonctions
def wordcloud(data, num_words_max = MAX_WORDS):
    ''' Enregistre les nuages de mots des opinions positives et négatives et retourne les mots vides complétés des mots commun
    '''

    # Affectation de la variable des mots communs
    wc_diff = True

    # Affectation des WordCloud des opinions positives et négatives
    wc_positive = WordCloud(
        stopwords=STOPWORDS,
        background_color = "white",
        height = 600,
        width = 400,
        max_words=num_words_max
    )
    wc_negative = WordCloud(
        stopwords=STOPWORDS,
        background_color = "white",
        height = 600,
        width = 400,
        max_words=num_words_max
    )

    # Extraction des opinions positives et négatives
    positives_opinions = " ".join([token for token in data[data["opinions"]=="positive"]["tokens"]])
    negatives_opinions = " ".join([token for token in data[data["opinions"]=="negative"]["tokens"]])

    # Génération des nuages de mots jusqu'à épuisement des mots en commun
    while wc_diff != set({}):

        wc_positive.generate(positives_opinions)
        wc_negative.generate(negatives_opinions)

        wc_diff = set(wc_negative.words_).intersection(set(wc_positive.words_))

        wc_positive.stopwords = wc_positive.stopwords.union(wc_diff)
        wc_negative.stopwords = wc_negative.stopwords.union(wc_diff)

    # Enregistrement des images associées aux nuages de mots
    wc_positive.to_file(f"{APP_PATH}/data/wordcloud_positive.png")
    wc_negative.to_file(f"{APP_PATH}/data/wordcloud_negative.png")

    return wc_positive.stopwords


def vectorizer(column, stop_words=STOPWORDS):
    '''Retourne l'encodeur entraîné sur les données
    '''

    # Appel du constructeur CountVectorizer
    vectorizer = CountVectorizer(stop_words = stop_words)

    # Entraînement du sac de mot
    vectorizer.fit(column)

    return vectorizer


if __name__ == "__main__":
    # Affectation des noms de film étudiés
    movies_to_scrap = ["Sonic 2 le film", "Inception"]
    
    # Chargement des données
    print("Chargement des données csv.")
    data = pd.DataFrame()
    data = pd.concat(
        [pd.read_csv(f"{APP_PATH}/data/{movie}.zip") for movie in movies_to_scrap],
        ignore_index=True
        )
    print("Données chargées !")
    print("---------------------------------")

    # Affichage des informations du dataset
    print("Informations concernant le dataset :\n")
    print(data.info())
    print("---------------------------------")
    print("Extrait du dataset :")
    print(data.head())
    print("---------------------------------")

    # Tokenization des données
    data = tokenization(data)

    # Détails du dataset tokenizé
    print("Informations concernant le dataset tokenizé :")
    print(data.info())
    print("---------------------------------")
    print("Extrait du dataset tokenizé :")
    print(data.head())
    print("---------------------------------")

    # Restructuration des données en tokens - opinion
    data = calculate_opinion(data)

    # Détails du dataset
    print("Informations concernant le dataset prétraîté :")
    print(data.info())
    print("---------------------------------")
    print("Extrait du dataset prétraîté :")
    print(data.head())
    print("---------------------------------")

    # Affichage des mots les plus fréquents
    # get_words_freq(data, MAX_WORDS)

    # Enregistrement sous forme de nuages de mots en fonction de l'opinion et du nombre de mots et extraction des mots communs en mots vides
    wordcloud_stopwords = wordcloud(data, MAX_WORDS)

    # Réindexation après opérations
    data.reset_index(drop=True, inplace=True)

    #Enregistrement des données prétraîtées
    print("Enregistrement de l'archive du dataset prétraîté.")
    compression_opts = dict(method='zip', archive_name='data.csv') 
    data.to_csv(
        f"{APP_PATH}/data/data_preprocessed.zip",
        index=False,
        compression=compression_opts
        )
    print("Archive enregistrée !")
    print("---------------------------------")