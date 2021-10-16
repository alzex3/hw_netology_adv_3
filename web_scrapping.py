import requests
from bs4 import BeautifulSoup


class Article:
    def __init__(self,  article):
        self.article = article

    def get_title(self):
        title = self.article.find(class_='tm-article-snippet__title-link').string
        return title

    def get_date(self):
        date = self.article.find(class_='tm-article-snippet__datetime-published').time['title']
        return date

    def get_url(self):
        title = self.article.find(class_='tm-article-snippet__title-link')
        url = 'https://habr.com' + title['href']
        return url

    def get_hubs(self):
        article_hubs = []
        hubs = self.article.find_all(class_='tm-article-snippet__hubs-item')
        for hub in hubs:
            article_hubs.append(hub.text)
        return article_hubs

    def get_description(self):
        try:
            description = self.article.find(class_='article-formatted-body article-formatted-body_version-2').text
        except AttributeError:
            description = self.article.find(class_='article-formatted-body article-formatted-body_version-1').text
        return description

    def get_article_text(self):
        resp = requests.get(self.get_url())
        soup = BeautifulSoup(resp.text, 'html.parser')
        text = soup.find(id='post-content-body').text
        return text

    def full_article_pack(self):
        article = {
            'title': self.get_title(),
            'date': self.get_date(),
            'url': self.get_url(),
            'hubs': self.get_hubs(),
            'description': self.get_description(),
            'text': self.get_article_text()
        }
        return article

    def prev_article_pack(self):
        article = {
            'title': self.get_title(),
            'date': self.get_date(),
            'url': self.get_url(),
            'hubs': self.get_hubs(),
            'description': self.get_description(),
        }
        return article


def get_articles():
    resp = requests.get('https://habr.com/ru/all/')
    soup = BeautifulSoup(resp.text, 'html.parser')
    articles = soup.find_all('article')
    return articles


def prev_articles_pack(articles):
    articles_pack = []
    for value in articles:
        article = Article(value)
        articles_pack.append(article.prev_article_pack())
    return articles_pack


def full_articles_pack(articles):
    articles_pack = []
    for value in articles:
        article = Article(value)
        articles_pack.append(article.full_article_pack())
    return articles_pack


def articles_search(keywords, articles_pack):
    result = []
    for article in articles_pack:
        for value in article.values():
            for word in keywords:
                if word in value:
                    result.append(
                        [
                            article['title'], article['date'], article['url']
                        ]
                    )
                    break

    filter_result = []
    for value in result:
        if value not in filter_result:
            filter_result.append(value)

    return filter_result


def main(keywords, mode=''):

    if mode == 'full':
        result = articles_search(keywords, full_articles_pack(get_articles()))
    else:
        result = articles_search(keywords, prev_articles_pack(get_articles()))

    if result:
        print('Ключевые слова содержаться в следующих статьях:\n')
        for value in result:
            for item in value:
                print(item)
            print()
    else:
        print('Статьи с данными ключевыми словами не найдены!')


KEYWORDS = ['дизайн', 'фото', 'web', 'python']
main(KEYWORDS, 'full')
