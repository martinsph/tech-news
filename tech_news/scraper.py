import requests
import time
import parsel
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
    except requests.HTTPError:
        return None
    except requests.Timeout:
        # timeouts requests
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
        ".tec--article__body > p:first-child *::text").getall()
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
    URL = "https://www.tecmundo.com.br/novidades"
    first_connection = fetch(URL)
    # array com todos os links da primeira pagina
    all_links = scrape_novidades(first_connection)

    for counter in range(3):
        next_page_connection = fetch(scrape_next_page_link(first_connection))
        new_page_links = scrape_novidades(next_page_connection)
        all_links.extend(new_page_links)

    # array slicing
    # source: https://www.w3schools.com/python/numpy/numpy_array_slicing.asp
    all_links = all_links[:amount]
    # print(all_links)

    scraped_news = []
    for link in all_links:
        html_content = fetch(link)
        scraped_news.append(scrape_noticia(html_content))

    create_news(scraped_news)
    return scraped_news
