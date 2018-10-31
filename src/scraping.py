from tqdm import tqdm
import requests
import pandas as pd
import json

import arcas

words = ["prisoner's dilemma", "prisoners dilemma", "prisoners evolution",
         "prisoner dilemma", "prisoner game theory"]
         # , "memory one strategy", "tit for tat", "tit-for-tat", "zero determinant strategy"]

 
for p in [arcas.Nature, arcas.Ieee, arcas.Plos, arcas.Arxiv, arcas.Springer]:
    pbar = tqdm(total=len(words) * 2)
    for key in words:
        api = p()
        start = 1
        
        for field in ['title', 'abstract']:
            switch = True
            arguments = {field: key, 'records': 10}
            while switch is not False and start < 100:
                parameters = api.parameters_fix(**arguments, start=start)
                url = api.create_url_search(parameters)
                #print(url)
                
                request = api.make_request(url)
                root = api.get_root(request)
                raw_article = api.parse(root)

                # try:
                #     #print('Here')
                #     articles = []
                #     for art in raw_article:
                #         articles.append(api.to_dataframe(art))
                if raw_article: 
                    filename = "raw_data/result_{}_{}_{}.json".format(field, api.__class__.__name__, start)
                    with open(filename, 'w') as outfile:
                        json.dump(raw_article, outfile)

                #     df = pd.concat(articles, ignore_index=True)
                #     api.export(df, "articles/result_{}_{}_{}.json".format(field, api.__class__.__name__, start))
                # except TypeError:
                else:
                    switch=False
                start += 10
            pbar.update(1)









