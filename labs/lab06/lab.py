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
    links = []
    for book in soup.find_all('article', class_='product_pod'):
        rating = book.find('p', class_='star-rating')['class'][1]
        if rating not in ('Four', 'Five'):
            continue
        price_text = book.find('p', class_='price_color').text
        price = float(price_text.split('£')[-1])
        if price >= 50:
            continue
        links.append(book.find('h3').find('a')['href'])
    return links

def get_product_info(text, categories):
    soup = bs4.BeautifulSoup(text, features='lxml')
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    if category not in categories:
        return None
    info = {}
    for row in soup.find('table', class_='table-striped').find_all('tr'):
        info[row.find('th').text.strip()] = row.find('td').text.strip()
    wanted = ['UPC', 'Product Type', 'Price (excl. tax)', 'Price (incl. tax)',
              'Tax', 'Availability', 'Number of reviews']
    result = {key: info[key] for key in wanted}
    result['Category'] = category
    result['Rating'] = soup.find('p', class_='star-rating')['class'][1]
    desc_header = soup.find('div', id='product_description')
    if desc_header is not None and desc_header.find_next_sibling('p') is not None:
        result['Description'] = desc_header.find_next_sibling('p').text.strip()
    else:
        result['Description'] = None
    result['Title'] = soup.find('div', class_='product_main').find('h1').text.strip()
    return result

def scrape_books(k, categories):
    rows = []
    session = requests.Session()
    for page in range(1, k + 1):
        page_res = session.get(f'http://books.toscrape.com/catalogue/page-{page}.html')
        for link in extract_book_links(page_res.text):
            book_res = session.get(f'http://books.toscrape.com/catalogue/{link}')
            info = get_product_info(book_res.text, categories)
            if info is not None:
                rows.append(info)
    return pd.DataFrame(rows)


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
