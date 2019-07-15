"""
Scraping for articles' meta data script.
"""

import json

import pandas as pd
from tqdm import tqdm

import arcas
import requests


def get_raw_articles_on_search(api, arguments, start):
    parameters = api.parameters_fix(**arguments, start=start)
    url = api.create_url_search(parameters)

    request = api.make_request(url)
    root = api.get_root(request)
    raw_articles = api.parse(root)

    return raw_articles


if __name__ == "__main__":

    words = [
        "prisoner's dilemma",
        "prisoners dilemma",
        "prisoners evolution",
        "prisoner dilemma",
        "prisoner game theory",
    ]

    for p in [
        arcas.Nature,
        arcas.Plos,
        arcas.Arxiv,
        arcas.Springer,
        arcas.Ieee,
    ]:
        pbar = tqdm(total=len(words) * 2)
        for key in words:
            api = p()
            for field in ["title", "abstract"]:
                start = 1
                switch = True
                arguments = {field: key, "records": 10}
                while switch is not False:

                    raw_articles = get_raw_articles_on_search(
                        api=api, arguments=arguments, start=start
                    )

                    if raw_articles:
                        filename = "raw_data/PD/result_{}_{}_{}.json".format(
                            field, api.__class__.__name__, start
                        )
                        with open(filename, "w") as outfile:
                            json.dump(raw_articles, outfile)
                    else:
                        switch = False
                    start += 10
                pbar.update(1)
