# Requisito 6
from datetime import datetime
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
    try:
        all_news = []
        # como usar strptime()
        # https://www.educative.io/edpresso/how-to-convert-a-string-to-a-date-in-python
        datetime.strptime(date, '%Y-%m-%d')
        result = search_news({'timestamp': {'$regex': date}})
        for news in result:
            all_news.append((news['title'], news['url']))

        return all_news
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
