import wikipedia

'''
def get_articles(language, no_words, max_no_articles, search, **kwargs):
    """ Retrieve articles from Wikipedia """
    wikipedia.set_rate_limiting(True) # be polite
    wikipedia.set_lang(language)

    if search is not None:
        titles = wikipedia.search(search, results = max_no_articles)
    else:
        titles = wikipedia.random(pages = max_no_articles)

    articles = []
    current_no_words = 0
    for title in titles:
        print("INFO: loading {}".format(title))
        page = wikipedia.page(title=title)
        content = page.content
        article_no_words = len(content.split())
        current_no_words += article_no_words
        print("INFO: article contains {} words".format(article_no_words))
        articles.append((title, content))
        if current_no_words >= no_words:
            break

    return articles 

articles = get_articles("pt", 100, 10, "delu OR elu")

for article in articles:
    print(article)
    '''

wikipedia.set_lang("pt")
print(wikipedia.search("elu OR delu", results=15))