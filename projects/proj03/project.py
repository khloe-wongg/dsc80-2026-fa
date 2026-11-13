# project.py


import pandas as pd
import numpy as np
from pathlib import Path
import re
import requests
import time


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------

_DEFAULT_PAUSE = 0.5
_ROBOTS_URL = 'https://www.gutenberg.org/robots.txt'
_crawl_delay = None
 
 
def _get_crawl_delay():
    global _crawl_delay
    if _crawl_delay is not None:
        return _crawl_delay
 
    delay = _DEFAULT_PAUSE
    try:
        text = requests.get(_ROBOTS_URL).text
        applies = False
        for line in text.splitlines():
            line = line.split('#')[0].strip()
            if ':' not in line:
                continue
            key, value = [s.strip() for s in line.split(':', 1)]
            key = key.lower()
            if key == 'user-agent':
                applies = (value == '*')
            elif key == 'crawl-delay' and applies:
                delay = float(value)
                break
    except Exception:
        delay = _DEFAULT_PAUSE
 
    _crawl_delay = delay
    time.sleep(delay)
    return _crawl_delay
 
 
def get_book(url):
    delay = _get_crawl_delay()
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    time.sleep(delay)
 
    text = resp.text.replace('\r\n', '\n').lstrip('\ufeff')
 
    start_pat = r'^[ \t]*\*{3}[ \t]*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*{3}[ \t]*$'
    end_pat = r'^[ \t]*\*{3}[ \t]*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*{3}[ \t]*$'
    flags = re.MULTILINE | re.IGNORECASE
 
    start = re.search(start_pat, text, flags)
    begin_idx = start.end() + 1 if start else 0
 
    end = re.search(end_pat, text[begin_idx:], flags)
    end_idx = begin_idx + end.start() if end else len(text)
 
    return text[begin_idx:end_idx]


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def tokenize(book_string):
    text = book_string.strip()
    text = re.sub(r'\n{2,}', ' \x03 \x02 ', text)
    text = '\x02 ' + text + ' \x03'
    return re.findall(r'\w+|[^\w\s]', text)


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


class UniformLM(object):


    def __init__(self, tokens):
        
        self.mdl = self.train(tokens)
        
    def train(self, tokens):
        unique = pd.Series(list(tokens)).unique()
        return pd.Series(1 / len(unique), index=unique)
    
    def probability(self, words):
        probs = self.mdl.reindex(list(words)).fillna(0)
        return float(probs.prod())
        
    def sample(self, M):
        return ' '.join(np.random.choice(self.mdl.index, size=M, p=self.mdl.values))


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


class UnigramLM(object):
    
    def __init__(self, tokens):
        self.mdl = self.train(tokens)
    
    def train(self, tokens):
        return pd.Series(list(tokens)).value_counts(normalize=True, sort=False)
    
    def probability(self, words):
        probs = self.mdl.reindex(list(words)).fillna(0)
        return float(probs.prod())
        
    def sample(self, M):
        return ' '.join(np.random.choice(self.mdl.index, size=M, p=self.mdl.values))


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


class NGramLM(object):
    
    def __init__(self, N, tokens):
        # You don't need to edit the constructor,
        # but you should understand how it works!
        
        self.N = N

        ngrams = self.create_ngrams(tokens)

        self.ngrams = ngrams
        self.mdl = self.train(ngrams)

        if N < 2:
            raise Exception('N must be greater than 1')
        elif N == 2:
            self.prev_mdl = UnigramLM(tokens)
        else:
            self.prev_mdl = NGramLM(N-1, tokens)

    def create_ngrams(self, tokens):
        return [tuple(tokens[i:i + self.N]) for i in range(len(tokens)- self.N +1)]
        
    def train(self, ngrams):
        df = pd.DataFrame({'ngram': ngrams})
        df['n1gram'] = df['ngram'].apply(lambda x: x[:-1])
        df['ngram_count'] = df.groupby('ngram')['ngram'].transform('size')
        df['n1gram_count'] = df.groupby('n1gram')['n1gram'].transform('size')
        df['prob'] = df['ngram_count'] / df['n1gram_count']
        return (df.drop_duplicates('ngram')[['ngram', 'n1gram', 'prob']].reset_index(drop=True))
    
    def probability(self, words):
        words = tuple(words)
        N = self.N
        if len(words) < N:
            return self.prev_mdl.probability(words)
        prob = self.prev_mdl.probability(words[:N - 1])
        lookup = dict(zip(self.mdl['ngram'], self.mdl['prob']))
        for i in range(len(words) - N + 1):
            prob *= lookup.get(words[i:i + N], 0)
        return float(prob)
    

    def sample(self, M):
        tokens = ['\x02']
        for _ in range(M - 1):
            context = tuple(tokens[-(self.N - 1):])
            model = self
            while model.N > len(context) + 1:
                model = model.prev_mdl
            rows = model.mdl[model.mdl['n1gram'].map(lambda x: x == context)]
            if len(rows) == 0:
                tokens.append('\x03')
            else:
                next_tokens = rows['ngram'].map(lambda x: x[-1]).to_numpy()
                tokens.append(np.random.choice(next_tokens, p=rows['prob'].to_numpy()))
        tokens.append('\x03')
        return ' '.join(tokens)
