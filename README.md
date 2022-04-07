# MovieReview

Dépôt synthétisant le travail réalisé lors de la réalisation du brief intitulé "NLP pour l’analyse de critiques de films" dans le cadre de la formation Simplon × Microsoft IA 


# Ressource(s)

- [Critiques du film Sonic 2](https://www.allocine.fr/film/fichefilm-281203/critiques/spectateurs/)
- [Critiques du film Inception](https://www.allocine.fr/film/fichefilm-143692/critiques/spectateurs/)


# Contexte du projet

En règle générale, le nombre d'avis sur un film peu être important et par conséquent le temps de lecture de chaque commentaire peut être une tâche lourde. Alors comment déterminer de manière rapide si un film a eu du succès auprès des spectateurs (ou pas) ? Dans ce contexte, l’idée du projet est d’utiliser des algorithmes d'apprentissage automatique pour la tâche d'analyse de sentiment des spectateurs via leur critique.

Tout d’abord, il sera question que récupérer les données directement du site d’Allociné. En d’autres termes, nous allons scraper les pages qui nous intéressent sur ce site à savoir les critiques des personnes pour le film Inception et Sonic 2.

En navigant sur la page des critiques, vous vous apercevrez que seules deux types d’information ici nous intéresse : la note du spectateur ainsi que son avis. Pourquoi la note ? Parce que nous allons entraîner un modèle de type supervisé et plus précisément un classifieur et donc la note va nous aider à récupérer la classe pour étiqueter le commentaire. Pour cela, nous considérerons qu’une note au-dessus de 3 est considérée comme satisfaisante. Sinon, l’avis est négatif. Ici, nous avons donc réduit le problème à une classification binaire.

Voici donc les étapes à réaliser :
- Récupération des données
- Préparation des données.
- Préparation du modèle et des jeux de données (entrainement & test)
- Analyse des résultats


## Étape 1 : Web Scraping des données d’avis de spectacteurs

De l’avis du spectateur, nous ne devons « scraper » que deux zones la note et le commentaire.


## Étape 2 : Préparation des données

Ayant maintenant nos jeux de données, il faut les préparer afin de pouvoir modéliser notre analyse de sentiments. Pour cela nous allons faire appel à plusieurs techniques :
- Des expressions régulières pour retirer les bruits (ponctuation, etc.) des commentaires.
- Du NLP pour tokeniser et réduire le corpus de chaque commentaire (afin par exemple de ne garder que les mots importants via les stopwords)
- Des sacs de mots afin de « transformer » nos mots en nombres qui pourront alors être exploités dans un algorithme de Machine learning

Les commentaires sont maintenant filtrés à leur essentiel.


## Étape 3 : Préparation des libellés

Jusque là, à chaque commentaire est associé une note de 1 à 5 et non une classe binaire. Il nous faut donc convertir nos notes en : 1 pour avis positif et 0 : pour avis négatif

Note: N’oublions pas à la fin de retirer la note du jeu de données.


## ​Étape 4 : Finalisation de nos jeux de données

Les données sont presque prêtes mais nos commentaires qui sont maintenant sous forme de sac de mots doivent être convertis en nombre. Pour cela, il va falloir vectoriser nos mots (technique des sacs de mots) :

Vous devriez avoir maintenant une belle matrice avec beaucoup de colonnes (qui correspond au nombre de mots du corpus)

Afficher deux _WordCloud _: le WordCloud des avis positifs et celui des avis négatifs.


## Étape 5 : Entraînement du modèle

Nos données sont prêtes, nous allons pour ce premier exercice utiliser un algorithme de Regression Logistique comme ici il est question de classification binaire. Entraînons le modèle maintenant, et regardons sa précision par rapport au libellés connus.

​

## Étape 6 : Analyse des résultats

Calculer l’accuracy et la matrice de confusion sur les données de test. Une fois que les résultats sont satisfaisants, vous pourrez maintenant tester sur des commentaires que vous et vos collègues ferons afin de vérifier le bon fonctionnement du programme.
Modalités pédagogiques

Le deadline pour rendre ce travail est fixé pour le 25 avril. Le projet est réalisé en groupe de 2-3 personnes.


# Critères de performance

Le code doit être bien structuré
Le bon fonctionnement de l'application demandée.


# Modalités d'évaluation

Un rapport sur le projet réalisé :
•	Description des données
•	Présentation des différentes étapes du code
•	Résultats
•	Conclusion (avantages et inconvénients, recommandations…)
Revue de code avec le formateur.


# Livrables

Un dépôt GitHub avec : 
- [ ] Un Notebook bien structuré/organisé qui réalise les différentes étapes de ce projet. 
- [ ] Un rapport sur le projet réalisé
- [ ] Un Readme.md pour mettre en avant votre projet.


# Travail à réaliser
- [ ] Étape 1
- [ ] Étape 2
- [ ] Étape 3
- [ ] Étape 4
- [ ] Étape 5
- [ ] Étape 6
- [ ] Notebook récapitulatif
- [ ] Rapport du projet