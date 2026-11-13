# lab.py


import os
import pandas as pd
import numpy as np
np.set_printoptions(legacy='1.21')
import requests
import bs4
import lxml


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def question1():
    """
    NOTE: You do NOT need to do anything with this function.
    The function for this question makes sure you
    have a correctly named HTML file in the right
    place. Note: This does NOT check if the supplementary files
    needed for your page are there!
    """
    # Don't change this function body!
    # No Python required; create the HTML file.
    return


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------



def extract_book_links(text):
    soup = bs4.BeautifulSoup(text, features='lxml')
    books = soup.find_all('article', class_='product_pod')
    good_rating = filter(
        lambda b: b.find('p', class_='star-rating')['class'][1] in ('Four', 'Five'), books)
    cheap = filter(lambda b: float(b.find('p', class_='price_color').text.split('£')[-1]) < 50, good_rating)
    return list(map(lambda b: b.find('h3').find('a')['href'], cheap))

def get_product_info(text, categories):
    soup = bs4.BeautifulSoup(text, features='lxml')
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    if category not in categories:
        return None
    rows = soup.find('table', class_='table-striped').find_all('tr')
    info = dict(map(lambda r: (r.find('th').text.strip(), r.find('td').text.strip()), rows))
    desc_header = soup.find('div', id='product_description')
    description = (
        desc_header.find_next_sibling('p').text.strip()
        if desc_header is not None and desc_header.find_next_sibling('p') is not None
        else None
    )
    info['Category'] = category
    info['Rating'] = soup.find('p', class_='star-rating')['class'][1]
    info['Description'] = description
    info['Title'] = soup.find('div', class_='product_main').find('h1').text.strip()
    return info

def scrape_books(k, categories):
    session = requests.Session()
    pages = map(
        lambda p: session.get(f'http://books.toscrape.com/catalogue/page-{p}.html').text, range(1, k + 1))
    links = sum(map(extract_book_links, pages), [])
    book_pages = map(lambda link: session.get(f'http://books.toscrape.com/catalogue/{link}').text, links)
    infos = filter(lambda info: info is not None, map(lambda t: get_product_info(t, categories), book_pages))
    return pd.DataFrame(list(infos))


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def stock_history(symbol, year, month):
    start = pd.Timestamp(year=year, month=month, day=1)
    end = start + pd.offsets.MonthEnd(0)  # last day of the month
    url = (
        'https://financialmodelingprep.com/stable/historical-price-eod/full'
        f'?symbol={symbol}&from={start:%Y-%m-%d}&to={end:%Y-%m-%d}&apikey=g9trjTG5tYdbS3gcFA6rVQBXTgm9D8VF'
    )
    data = requests.get(url).json()
    if isinstance(data, dict):
        data = data['historical']
    return pd.DataFrame(data)

def stock_stats(history):
    df = history.sort_values('date')
    start_price = df['open'].iloc[0]
    end_price = df['close'].iloc[-1]
    pct_change = (end_price - start_price) / start_price * 100
    avg_price = (df['high'] + df['low']) / 2
    total_volume = (avg_price * df['volume']).sum() / 1e9
    return (f'{pct_change:+.2f}%', f'{total_volume:.2f}B')


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def get_comments(storyid):
    url = 'https://hacker-news.firebaseio.com/v0/item/{}.json'
    session = requests.Session()
    story = session.get(url.format(storyid)).json()
    stack = list(reversed(story.get('kids', [])))
    rows = []
    while stack:
        item = session.get(url.format(stack.pop()), timeout=10).json()
        if item is None or item.get('dead'):
            continue
        rows.append({
            'id': item['id'],
            'by': item.get('by'),
            'text': item.get('text'),
            'parent': item.get('parent'),
            'time': pd.Timestamp(item['time'], unit='s'),
        })
        stack.extend(reversed(item.get('kids', [])))
    return pd.DataFrame(rows, columns=['id', 'by', 'text', 'parent', 'time'])
