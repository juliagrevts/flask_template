from datetime import datetime

from bs4 import BeautifulSoup

from webapp.db import db
from webapp.news.models import News
from webapp.news.parsers.utils import get_html, save_news


def get_news_snippets():
    html = get_html('https://habr.com/ru/search/?q=python&target_type=posts&order=date')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('div', class_='tm-articles-list').findAll('article', class_='tm-articles-list__item')
        for news in all_news:
            title = news.find('a', class_='tm-article-snippet__title-link').text
            url = 'https://habr.com' + news.find('a', class_='tm-article-snippet__title-link')['href']
            published = news.find('time')['title']
            try:
                published = datetime.strptime(published, '%Y-%m-%d, %H:%M')
            except ValueError:
                published = datetime.now()
            save_news(title, url, published)


def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_text = soup.find('div', class_='article-formatted-body')
            img_list = news_text.findAll('img', attrs={'data-src': True})
            for img in img_list: 
                if not img['src'] == img['data-src']:
                    img['src'] = img['data-src']
            news_text = news_text.decode_contents()
            if news_text:
                news.text = news_text
                db.session.add(news)
                db.session.commit()