from tqdm import tqdm
import requests
import pandas as pd

from password import password
from arcas import *


# def post_to_axelbib(post):
#     """A function for posting to Axelbib
#     """
#     url = 'http://127.0.0.1:8000/article/'
#     headers = {'Content-Type': 'application/json'}
#     r = requests.post(url, data=json.dumps(post), auth=('nikoleta', password),
#                       headers=headers)
#     return r.status_code


def get_arguments(api, word, start, count):
    if api == 'springer':
        arguments = [{'-a': None, '-t': word, '-s': start,
                      '-r': count, '-y': None, '-b': None}]
    else:
        arguments = [{'-a': None, '-b': word, '-s': start,
                      '-r': count, '-y': None, '-t': None},
                     {'-a': None, '-t': word, '-s': start,
                      '-r': count, '-y': None, '-b': None}]
    return arguments


def main_program(arguments):
    parameters = pp.parameters_fix(arguments=arguments)
    url = pp.create_url_search(parameters=parameters)
    response = pp.make_request(url)
    root = pp.get_root(response)
    article = pp.parse(root)
    return article, url

words = ["prisoner's dilemma", "prisoner’s dilemma", "prisoners evolution",
         "prisoner dilemma", "prisoner game theory", "memory one strategy",
         "tit for tat", "tit-for-tat", "zero determinant strategy"]

apis = {"ieee": Ieee, "nature": Nature, "arxiv": Arxiv, "springer": Springer,
        "plos": Plos}
list_apis = ['plos', 'arxiv', 'ieee', 'nature', 'springer']
count = 10
validate = True
val = False

pbar = tqdm(total=(len(words)*len(apis)))

for wr in words:
    for p in list_apis:
        pp = apis[p]()
        start = 1
        raw_articles = True
        while raw_articles is not False:
            arguments = get_arguments(p, wr, start, count)
            for arg in arguments:
                raw_articles, url = main_program(arg)
                print(url)
                dfs = []
                if raw_articles is not False:
                    for raw_article in raw_articles:
                        try:
                            df = pp.to_dataframe(raw_article)

                            if validate is True:
                                val = pp.validate_post(arg, df)

                            if val is True or validate is False:
                                dfs.append(df)
                            else:
                                with open('failed_validation', 'a') as textfile:
                                    textfile.write('{},{},({})\n'.format(
                                                        df['key'][0], url,
                                                        df['unique_key'][0]))
                        except ValueError:
                            ValueError()
                try:
                    df = pd.concat(dfs, ignore_index=True)
                    pp.export(df, filename='articles_2/{}-{}-{}.json'.format(
                                                                       p, wr,
                                                                       start))

                except ValueError:
                    print(None)

            start += 10
        pbar.update(1)









