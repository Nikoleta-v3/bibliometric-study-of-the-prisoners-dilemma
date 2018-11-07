import imp
import itertools

import pandas as pd

tools = imp.load_source('tools', '../tools.py')

columns = ['abstract', 'author', 'category', 'date', 'doi', 'journal', 'key',
           'open_access', 'primary_category', 'provenance', 'score', 'title',
           'unique_key', 'url']

def remove_symbols_from_entry(entry):
    entry = entry.replace("{", "")
    entry = entry.replace(",", "")
    entry = entry.replace("}", "")
    entry = entry.replace('"', "")
    entry = entry.replace(' = ', "=")

    return entry

def extract_info(entry):
    split_entry = entry.split('\n')
    clean_entry = [el for el in split_entry if '=' in el]
    
    details = {}
    for element in clean_entry:
        key, value = element.split('=')
        details[key] = value
    return details

def dict_to_dataframe(raw_article):
    values = []
    for key in columns:
        try:
            if key == 'provenance':
                values.append(['Manual'])
            elif type(raw_article[key]) is not list:
                values.append([raw_article[key]])
            else:
                values.append(raw_article[key])
        except KeyError:
            values.append(['Not given'])
            
    data = []
    for row in itertools.product(*values):
        data.append(row)
    df = pd.DataFrame(data, columns=columns)
    return df
#################################################################################
file = '../bibliography.bib'
with (open(file, 'r')) as textfile:
    bibliography = textfile.read()

game_theory_section = bibliography.split('%End-GameTheory')[0]
raw_articles = game_theory_section.split('@')
raw_articles = [art.lower() for art in raw_articles]

clean_articles = [remove_symbols_from_entry(article) for article in raw_articles]
index = ['article' in article for article in clean_articles]
result = [article for article, boolean in zip(clean_articles, index) if boolean == True]

articles = []
for i, art in enumerate(result):
    articles.append(extract_info(art))

for article in articles:
    for k, v in list(article.items()):
        new_key = "".join(k.split())
        if new_key == 'year':
            new_key = 'date'
        article[new_key] = article.pop(k)

# break up authors
for i, article in enumerate(articles):
    article['author'] = [tools.normalise_names(name) for name in  article['author'].split(' and')]

dfs = []
for article in articles:
    dfs.append(dict_to_dataframe(article))
    
df = pd.concat(dfs, ignore_index=True)
df.to_json('data/bibliography.json')
