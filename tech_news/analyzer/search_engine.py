# Requisito 6
from tech_news.database import search_news


def search_by_title(title):
    all_news = []
    # Busca case-insensitive
    # https://docs.mongodb.com/manual/reference/operator/query/regex/
    # http://www.w3big.com/pt/mongodb/mongodb-regular-expression.html
    result = search_news({'title': {'$regex': title, '$options': 'i'}})
    for news in result:
        all_news.append((news['title'], news['url']))

    return all_news


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
