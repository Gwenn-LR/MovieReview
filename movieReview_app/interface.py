import matplotlib.pyplot as plt

def wordclouds_comparison():

    fig = plt.figure(figsize=(15, 12))
    fig.suptitle("Tokens issus des commentaires en fonction de l'opinion et du nombre de mot du nuage de mots")
    fig.tight_layout()

    ax20_n = plt.subplot(2, 2, 1)
    plt.axis('off')
    WC20_n = plt.imread("movieReview_app/data/wordcloud_20_negative_stopwords_min.png")
    plt.imshow(WC20_n, interpolation='nearest')
    ax20_n.set_title("20 mots négatifs")

    ax50_n = plt.subplot(2, 2, 2)
    plt.axis('off')
    WC50_n = plt.imread("movieReview_app/data/wordcloud_50_negative_stopwords_min.png")
    plt.imshow(WC50_n)
    ax50_n.set_title("50 mots négatifs")

    ax20_p = plt.subplot(2, 2, 3)
    plt.axis('off')
    WC20_p = plt.imread("movieReview_app/data/wordcloud_20_positive_stopwords_min.png")
    plt.imshow(WC20_p, interpolation='nearest')
    ax20_p.set_title("20 mots positifs")

    ax50_p = plt.subplot(2, 2, 4)
    plt.axis('off')
    WC50_p = plt.imread("movieReview_app/data/wordcloud_50_positive_stopwords_min.png")
    plt.imshow(WC50_p)
    ax50_p.set_title("50 mots positifs")

    plt.show()


if __name__ == "__main__":
    wordclouds_comparison()