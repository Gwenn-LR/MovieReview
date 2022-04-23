import joblib
import pandas as pd

from movieReview_app.preprocessing import tokenization

APP_PATH = "movieReview_app"

#TODO: Enregistrer le vectorizer dans le pipeline
def prediction():
    model = joblib.load(f"{APP_PATH}/models/20220423-2112_StandardScaler_0.95.z")
    vectorizer = joblib.load(f"{APP_PATH}/models/20220423-2112_CountVectorizer.z")

    comment = input("Saisissez votre commentaire :")

    data = pd.DataFrame([comment], columns=["comment"])

    data = tokenization(data)

    tokens = vectorizer.transform(data.tokens)

    preds = model.predict(tokens)

    for pred in preds:
        if pred:
            print("C'est un avis jugé positif !")
        else:
            print("C'est un avis jugé négatif !")


if __name__ == "__main__":
    prediction()