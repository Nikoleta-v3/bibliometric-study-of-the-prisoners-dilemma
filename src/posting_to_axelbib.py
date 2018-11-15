"""
A script to push articles to Axelbib.
"""
import json
import requests
import pandas as pd

from password import password

# words = ["prisoner's dilemma", "prisoner’s dilemma", "prisoners evolution",
#          "prisoner dilemma", "prisoner game theory", "memory one strategy",
#          "tit for tat", "tit-for-tat", "zero determinant strategy"]
words = [['auction game theory'], ['price of anarchy']]

def post_to_axelbib(post):
    """A function for posting to Axelbib
    """
    url = 'http://127.0.0.1:8000/article/'
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=json.dumps(post), auth=('nikoleta', password),
                      headers=headers)
    return r.status_code

if __name__ == '__main__':

    filename = '../data/a_json_file.json'
    articles = pd.read_json(filename)

    for label, group in articles.groupby("unique_key"):
        post = {}
        post['title'] = group['title'].unique()[0]
        post['author'] = [{'name': v} for v in group['author'].unique()]
        post['date'] = {'year': str(group['date'].unique()[0])}
        post['abstract'] = group['abstract'].unique()[0]
        post['key'] = group['key'].unique()[0]
        post['unique_key'] = label
        post['labels'] = []
        post['pages'] = group['pages'].unique()[0]
        post['journal'] = group['journal'].unique()[0]
        post['list_strategies'] = []
        post['read'] = False
        post['key_word'] = [{'key_word': v} for v in group['key_word'].unique()]
        post['provenance'] = group['provenance'].unique()[0]
        post['score'] =  group['score'].unique()[0]

        st = post_to_axelbib(post)

        if st == 400:
            print(post['key'], post['title'], st)