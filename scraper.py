from bs4 import BeautifulSoup
import os
import re
import requests
import string
from urllib.parse import urlparse


def remove_punctuation(text):
    punctuation = string.punctuation
    mapping = str.maketrans({key: ' ' for key in punctuation})
    text = text.translate(mapping)
    text = text.strip()
    text = re.sub(' +', ' ', text)
    text = re.sub(' ', '_', text)
    return text


def get_article_body(url):
    response = requests.get(url)
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.find('div', {'class': 'c-article-body'})
        return body.text
    else:
        print(print(f'Error! Response code {response.status_code}'))
        return None


def main():
    num_pages = int(input())
    article_type = input()
    url = 'https://www.nature.com/nature/articles'

    # num_pages = 4
    # article_type = 'NEws'
    work_dir = os.getcwd()

    for page in range(1, num_pages + 1):
        save_articles(url=url,
                      article_type=article_type,
                      num_pages=page,
                      work_dir=work_dir)

    print('Saved all articles.')


def save_articles(url, article_type, num_pages, work_dir):

    url = 'https://www.nature.com/nature/articles'
    params = {'sort': 'PubDate',
              'year': '2020',
              'page': str(num_pages)}

    response = requests.get(url, params=params)
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')
        article_list = []

        for article in articles:
            span = article.find('span', {'class': 'c-meta__type'})

            dir_path = 'Page_' + str(num_pages)
            if not os.access(path=os.path.join(work_dir, dir_path), mode=os.F_OK):
                os.mkdir(path=os.path.join(work_dir, dir_path))

            os.chdir(os.path.join(work_dir, dir_path))

            if span.text.lower() == article_type.lower():
                a = article.find('a', {'class': 'c-card__link u-link-inherit'})
                article_path = a['href']
                parsed_url = urlparse(url)
                article_url = parsed_url.scheme + '://' + parsed_url.hostname + article_path

                article_body = get_article_body(article_url)
                file_name = remove_punctuation(a.text) + '.txt'

                with open(file_name, 'w', encoding='UTF-8') as f:
                    f.write(article_body)
                    article_list.append(file_name)

        print(article_list)
    else:
        print(f'Error! Response code {response.status_code}')


if __name__ == '__main__':
    main()
