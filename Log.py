import datetime
import requests
from bs4 import BeautifulSoup
import re


def cachable(path):

    def _cachable(old_function):

        def new_function(*args, **kwargs):
            current_date = datetime.datetime.now()
            date = current_date.strftime('%m/%d/%y, %H:%M:%S')
            result = old_function(*args, **kwargs)
            res = f'{date}, {old_function.__name__}, {args}, {kwargs}, {result}'
            print(res)
            with open(path, "a", encoding='UTF-8') as f:
                f.write(res + '\n')
            return result

        return new_function
    return _cachable


@cachable("Log.txt")
def scrap_habr(list):
    list_res = []
    URL = 'https://habr.com'
    response = requests.get('https://habr.com/ru/all/')
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='html.parser')
    articles = soup.find_all('article')
    for article in articles:
        snippets = article.find_all('div', class_='tm-article-snippet')
        snippets = [snippet.text for snippet in snippets]
        snipets = snippets[0]
        snippets = re.findall("\w+", snipets.lower())
        for keyword in list:
            if keyword in snippets:
                date = article.find ('time')
                title = article.find('h2')
                href = title.find('a').attrs.get('href')
                res_habr = (f'тег {keyword} - ', date.text, title.text, URL + href)
                list_res.append(res_habr)
    return list_res

KEYWORDS  = ['java', 'python', 'дизайн', 'фото', 'web']
scrap_habr(KEYWORDS)