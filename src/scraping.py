from tqdm import tqdm
import requests
import pandas as pd
import json

import arcas

# words = ["prisoner's dilemma", "prisoners dilemma", "prisoners evolution",
#          "prisoner dilemma", "prisoner game theory"]
 
words = ['auction game theory']
for p in [arcas.Plos]:
    pbar = tqdm(total=len(words) * 3)
    for key in words:
        api = p()
        for field in ['title', 'abstract', 'keyword']:
            start = 1
            switch = True
            arguments = {field: key, 'records': 10}
            while switch is not False:
                parameters = api.parameters_fix(**arguments, start=start)
                url = api.create_url_search(parameters)
                #print(url)
                request = api.make_request(url)
                root = api.get_root(request)
                raw_article = api.parse(root)

                if raw_article: 
                    filename = "raw_data/PD/result_{}_{}_{}.json".format(field, api.__class__.__name__, start)
                    with open(filename, 'w') as outfile:
                        json.dump(raw_article, outfile)
                else:
                    switch=False
                start += 10
            pbar.update(1)









