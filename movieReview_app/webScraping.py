import requests
import requests_cache
import lxml.html as lh
import pandas as pd

from tokenize import String

APP_PATH = "movieReview_app"


def get_html_doc(url_page:String):
    '''Crée un document html à partir de l'url d'une page donnée.
    '''

    page = requests.get(url_page)
    doc = lh.fromstring(page.content)
    
    return doc


def get_elements(doc, tag, cls, *args):
    '''Crée une liste d'éléments repérés par la balise et la classe de ceux-ci dans un document.
    '''
    # if args:
    #     elements = doc.xpath(f"//{tag}[@class=\"{cls}\"]/{args[0]}")
    # else:
    elements = doc.xpath(f"//{tag}[@class=\"{cls}\"]")

    for i, element in enumerate(elements):
        elements[i] = element.text_content().strip()
    
    return elements


def get_element(doc, tag, cls, index):
    '''Retourne un élément depuis un document en fonction de sa classe et de son index parmi le nombre d'occurences.
    '''

    element = doc.xpath(f"//{tag}[@class=\"{cls}\"]/*")[index].text_content().strip()

    return element


def get_title(doc):
    '''Retourne le titre de la page du document html.
    '''

    title = get_element(doc, "div", "titlebar-title titlebar-title-lg", 0)

    return title


def get_ratings(doc):
    '''Crée une liste des notes à partir du document html.
    '''


    ratings = doc.xpath("//div[@class=\"review-card-meta\"]/div[@class=\"stareval stareval-medium stareval-theme-default\"]/span[@class=\"stareval-note\"]")

    for i, rating in enumerate(ratings):
        ratings[i] = rating.text_content().strip().replace(',', '.')

    return ratings


def get_comments(doc):
    '''Crée une liste des commentaires à partir du document html.
    '''

    comments = get_elements(doc, "div", "content-txt review-card-content")

    return comments


def get_page_max(doc):
    '''RRetourne le nombre de pages totales associées à un document html.
    '''

    page_max = get_element(doc, "div", "pagination-item-holder", -1)


    return page_max


def create_dataframe(ratings, comments):
    '''Crée un dataframe à partir des listes des notes et des commentaires données en entrée.
    '''

    
    columns = ["rating", "comment"]
    data = pd.DataFrame(list(zip(ratings, comments)), columns=columns)

    return data


def browse_doc(url_page):
    '''Retourne le nom du film scrapé et le dataframe résultant du parcours de toutes les pages depuis une ressource.
    '''

    # Instanciation des listes des données récupérées
    ratings = []
    comments = []
    
    # Affectation des paramètres URL
    suffixe = "?page="
    url = url_page + suffixe
    
    # Chargement de la page
    print("Chargement de la page associée à l'URL entrée.")

    doc = get_html_doc(url_page)

    print("Page chargée !")

    # Récupération du titre de la page
    title = get_title(doc)
    print(f"Film analysé : {title}")
    
    # Récupération du nombre total de pages
    page_max = int(get_page_max(doc))
    print(f"Nombre de pages à scraper : {page_max}")
    print("---------------------------------")


    # Itération sur toutes les pages à scraper
    for i in range(1, page_max+1):

        # ratings = get_ratings(doc)
        # comments = get_comments(doc)

        # Chargement de la ième page
        uri = url + str(i)
        print(f"Chargement des données de la page {i}.")
        doc = get_html_doc(uri)
        print("Page chargée !")

        # Récupération des commentaires et des notes
        print("Récupération des commentaires.")
        comments.extend(get_comments(doc))
        print("Récupération des notes.")
        ratings.extend(get_ratings(doc))
        print(f"Données de la page {i} récupérées !")
        print("---------------------------------")

    # Création du dataset
    print("Création du dataset.")
    data = create_dataframe(ratings, comments)
    print("Dataset créé !")

    return title, data


if __name__ == "__main__":
    # Mise en place du cache
    requests_cache.install_cache("movie_review", backend="sqlite", expire_after=7200)

    # Pages à scraper
    pages_to_scrap = [
        "https://www.allocine.fr/film/fichefilm-281203/critiques/spectateurs/",
        "https://www.allocine.fr/film/fichefilm-143692/critiques/spectateurs/"
        ]
    
    # Scraping
    for page in pages_to_scrap:
        print(f"Scraping de la page {page}.")
        title, data = browse_doc(page)
        print("Page scrapée !")

        print("Extrait du dataset :")
        print("\n")
        print(data.head())
        print("\n")

        print("Enregistrement du dataset archivé.")
        compression_opts = dict(method='zip', archive_name='data.csv') 
        data.to_csv(f"{APP_PATH}/data/{title}.zip", index=False, compression=compression_opts)
        print("Dataset enregistré !")
        print("---------------------------------")

    print("Scraping terminé !")
    print("---------------------------------")
    print("\n")