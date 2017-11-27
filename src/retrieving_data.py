"""
Retrieving data from Axelbib.

Axelbib is a django rest framework and this script allows us to retrieve the 
data that have been stored there.
"""

import itertools
import requests
import pandas as pd

from password import password

keys = ['title', 'provenance', 'score', 'read', 'unique_key', 'date',
        'abstract', 'author', 'journal', 'labels', 'key_word',
        'list_strategies', 'pages', 'key']


def raw_to_db(an_article):
    """
    Formating Axelbib's raw article.
    """
    an_article['author'] = [f['name'] for f in an_article['author']]
    an_article['key_word'] = [f['key_word'] for f in an_article['key_word']]
    an_article['date'] = an_article['date']['year']
    an_article['labels'] = [f['label'] for f in an_article['labels']]

    for _, field in enumerate(an_article):
        if not an_article[field]:
            an_article[field] = ['None']

    values = []
    for key in keys:
        if type(an_article[key]) is not list:
            values.append([an_article[key]])
        else:
            values.append(an_article[key])
    data = []
    for row in itertools.product(*values):
        data.append(row)
    return pd.DataFrame(data, columns=keys)

if __name__ == '__main__':

    page = 1
    status = 200
    max_page = 115
    filename = 'data/data_nov_2017.json'

    dfs = []
    while page <= max_page:
        req = requests.get('http://127.0.0.1:8000/article/?page={}'.format(page),
                           auth=("nikoleta", password))
        status =  req.status_code
        page += 1
        results_of_req = req.json()['results']
        for raw_article in results_of_req:
            df = raw_to_db(raw_article)
            dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    df.to_json(filename)
