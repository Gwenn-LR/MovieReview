import joblib
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import movieReview_app.preprocessing as preproc

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

APP_PATH = "movieReview_app"


def encoding(features_vectorizer, label_encoder, X_train, X_test, y_train, y_test):
    '''Encode les sacs de mots en vecteurs et les opinions en valeur binaire.
    '''

    X_train = features_vectorizer.transform(X_train)
    X_test = features_vectorizer.transform(X_test)

    y_train = label_encoder.fit_transform(y_train)
    y_test = label_encoder.fit_transform(y_test)

    return X_train, X_test, y_train, y_test


def pipe_reg_logistic(X, y):
    '''Crée un pipeline à partir de données sous forme de tokens vectorisés et de cible encodées.
    '''

    print("Création du pipeline")
    pipe = Pipeline(
        [
            ("scaler", StandardScaler(with_mean=False)),
            ("classifier",LogisticRegressionCV(cv=10, solver="liblinear", scoring="f1", random_state=42) )
        ]
    )
    print("Pipeline créé !")

    print("Entraînement du pipeline.")
    pipe.fit(X, y)
    print("Pipeline entraîné !")

    return pipe


def evaluating(label_encoder, pipe, X_test, y_test):
    '''Évalue le modèle donné en fonction des données de test et des labels originaux.
    '''

    y_pred = pipe.predict(X_test)

    score = pipe.score(X_test, y_test)

    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_encoder.classes_)
    disp.plot()
    plt.show()

    return score


if __name__ == "__main__":

    # Chargement des données
    print("Chargement des données csv.")
    data =pd.read_csv(f"{APP_PATH}/data/data_preprocessed.zip", keep_default_na=False)
    data.index = [i for i in range(len(data.index))]
    print("Données chargées !")
    print("---------------------------------")

    # Affichage des informations du dataset
    print("Informations concernant le dataset :\n")
    print(data.info())
    print("---------------------------------")
    print("Extrait du dataset :")
    print(data.head())
    print("---------------------------------")

    # Séparation des données en caractéristiques/cibles et entraînement/test
    print("Séparation des données.")
    X_train, X_test, y_train, y_test = train_test_split(
        data.tokens, 
        data.opinions, 
        stratify=data.opinions, 
        test_size=.2, 
        random_state=42
    )
    print("Données séparées !")
    print("---------------------------------")

    # Affectation des mots vides
    # print("Chargement des mots vides issus des nuages de mots.")
    # stopwords = preproc.wordcloud(data)
    # print("Mots vides chargés !")
    # print("---------------------------------")

    # Encodage des caractéristiques et des cibles
    print("Encodage des données.")
    # vectorizer = preproc.vectorizer(X_train, stop_words=stopwords)
    vectorizer = preproc.vectorizer(X_train)
    le = LabelEncoder().fit(y_train)
    X_train, X_test, y_train, y_test = encoding(vectorizer, le, X_train, X_test, y_train, y_test)
    print("Données encodées !")
    print("---------------------------------")

    # Affectation du pipeline de traîtement des données
    print("Traîtement de données :")
    pipe = pipe_reg_logistic(X_train, y_train)
    print("\n")
    print("Informations concernant le modèle :")
    etapes = [str(pipe.get_params()['steps'][i][1]).split('(')[0] for i in range(len(pipe.get_params()['steps']))]
    print(f"\
        Étapes : \n\
            {etapes[0]}\n\
            {etapes[1]}\n\
        Critère d'évaluation : {pipe.get_params()['classifier__scoring'].upper()}\n\r\
        Algorithme : {pipe.get_params()['classifier__solver']}\
    ")
    print("---------------------------------")

    # Evaluation des résultats
    print("Résultats de la prédiction :")
    score = evaluating(le, pipe, X_test, y_test)
    print(f"Score : {score}")
    print("---------------------------------")

    # Enregistrement du modèle
    print("Enregistrement des modèles.")
    now = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    joblib.dump(vectorizer, f"{APP_PATH}/models/{now}_CountVectorizer.z")
    joblib.dump(pipe, f"{APP_PATH}/models/{now}_{str(etapes[0])}_{score:.2f}.z")
    print("Modèles enregistrés !")