import requests
import time
import parsel


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
    except requests.HTTPError:
        return None
    except requests.Timeout:
        # https://docs.python-requests.org/en/latest/user/quickstart/#timeouts
        return None
    else:
        return response.text


# Requisito 2
def scrape_novidades(html_content):
    selector = parsel.Selector(html_content)
    result = selector.css("h3 a.tec--card__title__link::attr(href)").getall()
    return result


# Requisito 3
def scrape_next_page_link(html_content):
    selector = parsel.Selector(html_content)
    result = selector.css("a.tec--btn::attr(href)").get()
    if result:
        return result
    return None


# Requisito 4
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
