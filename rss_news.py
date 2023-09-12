import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from sql_scripts import *
from language_scripts import *


def rss_cointelegraph_news():
    ua = UserAgent()
    url = 'https://cointelegraph.com/rss'
    headers = {
        'User-Agent': ua.random,
    }

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'xml')
        items = soup.find_all('item')

        if items:
            item = items[0]
            title = item.find('title').text
            link = item.find('link').text
            description = item.find('description').text

            parse_desc = BeautifulSoup(description, 'html.parser')
            paragraphs = parse_desc.find_all('p')

            text_description = ' '.join(paragraph.get_text() for paragraph in paragraphs)

            image_tag = item.find('media:content', {'medium': 'image'})
            image_url = image_tag['url'] if image_tag else None


            rss_news = "\n{}\n\n{}\n\nLink:\n{}" .format(title, text_description, link)

            # print(rss_news)
            return rss_news


def rss_coindesk_news():
    ua = UserAgent()
    url = 'https://www.coindesk.com/arc/outboundfeeds/rss/'
    headers = {
        'User-Agent': ua.random,
    }

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'xml')
        items = soup.find_all('item')

        if items:
            item = items[0]
            title = item.title.text
            link = item.link.text
            description = item.description.text
            try:
                image = item.find('media:content')['url']
            except:
                image = None


            rss_news = "\n{}\n\n{}\n\nLink:\n{}".format(title, description, link)
            # print(rss_news)
            return rss_news
