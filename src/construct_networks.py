import collections
import itertools

import networkx as nx
import numpy as np
import pandas as pd


def generate_graph(data):
    data.author = data.author.str.lower()
    
    pairs = []
    for _, d in data.groupby('unique_key'):
        pairs += tuple(sorted(list(itertools.combinations(d['author'].unique(), 2))))
        co_authors = collections.Counter(pairs)
        
    authors_num_papers = data.groupby(['author', 'unique_key']).size().reset_index().groupby('author').count()
    authors_num_papers = authors_num_papers.drop(0, axis=1)
    
    G = nx.Graph()
    for name, w in zip(data.author, authors_num_papers['unique_key'].values):
        G.add_node(name)
    for pair in co_authors.items():
        G.add_edge(*pair[0])
                       
    return G

print('Constructing networks')
print('=====================')
ipd      = pd.read_json('data/pd_November_2018_clean.json')
anarchy  = pd.read_json('data/anarchy_November_2018_clean.json')
auction  = pd.read_json('data/auction_November_2018_clean.json')

dataframes = [ipd, auction, anarchy]
topics = ['pd', 'auction', 'anarchy']

for data, topic in zip(dataframes, topics):
    G = generate_graph(data)
    nx.write_gml(G, "data/networks/{}_graph.gml".format(topic))

for data, topic in zip(dataframes, topics):
    periods = np.sort(data['date'].unique())
    periods = periods[~np.isnan(periods)]
    periods = periods[1:]
    cumulative_dataframes = [data[data['date'] <= period].reset_index() for period in periods]

    for i, frame in enumerate(cumulative_dataframes):
        G = generate_graph(frame)
        nx.write_gml(G, "data/networks/G_{}_{}.gml".format(topic, i))
print('Done')
