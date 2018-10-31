import glob
import pandas as pd
import json
import arcas

def normalise_names(s):
    
    # split the string into a list  
    l = s.split() 
    new = "" 
  
    # traverse in the list  
    for i in range(len(l)-1): 
        s = l[i] 
          
        # adds the capital first character  
        new += (s[0].upper()+'.') 
          
    # l[-1] gives last item of list l. We 
    # use title to print first character in 
    # capital. 
    new += l[-1].title() 
      
    return new 

for api in [arcas.Nature(), arcas.Ieee(), arcas.Plos(), arcas.Arxiv(), arcas.Springer()]:

    raw_articles = []
    api_name = api.__class__.__name__

    for filename in glob.glob('raw_data/*_{}_*.json'.format(api_name)):
        with open(filename) as json_data:
            d = json.load(json_data)
            raw_articles.append(d)

    flat_list = [item for sublist in raw_articles for item in sublist]

    articles = []
    for art in flat_list:
        articles.append(api.to_dataframe(art))

    dataframe = pd.concat(articles, ignore_index=True)
    dataframe = dataframe[~(dataframe['author']=='No authors found for this document.')]
    names = dataframe.author

    if api_name == 'Springer':
        edited = []
        for name in names:
            first, last = name.split(' ', 1)
            edited.append(first + ' ' + last)
        names = edited

    edited_names = [normalise_names(name) for name in names]
    dataframe.author = edited_names

    api.export(dataframe, '{}.json'.format(api_name))
