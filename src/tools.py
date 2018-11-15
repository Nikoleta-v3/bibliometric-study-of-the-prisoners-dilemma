import collections
import itertools

import networkx as nx


def normalise_names(s):
    elements = s.split()
    
    new = elements[0][0].upper()+'.'
    new += elements[-1].title()
    
    return new

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
