from tqdm import tqdm
import requests
import pandas as pd

import arcas

words = ["prisoner's dilemma", "prisoner’s dilemma", "prisoners evolution",
         "prisoner dilemma", "prisoner game theory", "memory one strategy",
         "tit for tat", "tit-for-tat", "zero determinant strategy"]

pbar = tqdm(total=5)
 
for p in [arcas.Springer, arcas.Nature, arcas.Ieee, arcas.Plos, arcas.Arxiv]: 
    for key in words:
        api = p()
        switch = True
        start = 1

        while switch is not False and start < 100:
            parameters = api.parameters_fix(abstract=key, records=10, start=start,
                                             year=2017)
            url = api.create_url_search(parameters)

            request = api.make_request(url)
            root = api.get_root(request)
            raw_article = api.parse(root)

            try:
                articles = []
                for art in raw_article:
                    articles.append(api.to_dataframe(art))


                df = pd.concat(articles, ignore_index=True)
                api.export(df, "articles/result_ab_{}_{}.json".format(api.__class__.__name__, start))
            except TypeError:
                switch=False
            start += 10
        pbar.update(1)









