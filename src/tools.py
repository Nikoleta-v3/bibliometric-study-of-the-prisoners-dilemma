from scipy import stats

def normalise_names(s):
    elements = s.split()
    
    new = elements[0].title() + ' ' #[0].upper()+'.'
    new += elements[-1].title()
    
    return new

def write_to_file(filename, metric):
    file = open("../../assets/{}".format(filename), 'w')
    file.write('{}'.format(metric))
    file.close()

def test_kruskal(distributions):
    alpha = 0.05
    _, p = stats.kruskal(distributions[0],distributions[1], distributions[2])
    
    if p < alpha:
        print(p, "The null hypothesis can be rejected.")
    else:
        print(p, "The null hypothesis cannot be rejected.")