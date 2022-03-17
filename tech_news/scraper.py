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
    selector = parsel.Selector(html_content)
    url = selector.css("head link[rel='canonical']::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()
    writer = (
        selector.css(".z--font-bold::text").get()
        or selector.css(".z--font-bold a::text").get()
    ).strip()

    shares_count = selector.css(".tec--toolbar__item::text").get() or 0
    if shares_count is not None:
        num_shares_count = str(shares_count).split()[0]
        shares_count = int(num_shares_count)

    comments = int(selector.css("#js-comments-btn::attr(data-count)").get())
    summary = selector.css(
        ".tec--article__body p:first-child *::text").getall()
    formated_summary = ('').join(summary)

    sources = selector.css(".z--mb-16 div a.tec--badge::text").getall()
    formated_sources = []
    for source in sources:
        formated_sources.append(source.strip())

    categories = selector.css("#js-categories > a.tec--badge::text").getall()
    formated_categories = []
    for category in categories:
        formated_categories.append(category.strip())

    news = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments,
        "summary": formated_summary,
        "sources": formated_sources,
        "categories": formated_categories,
    }

    return news


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
