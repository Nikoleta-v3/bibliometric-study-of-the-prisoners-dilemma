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
    _, p = stats.kruskal(*distributions)
    
    if p < alpha:
        print(p, "The null hypothesis can be rejected.")
    else:
        print(p, "The null hypothesis cannot be rejected.")

def test_mannwhitneyu(distributions, alternative=None):
    alpha = 0.05
    _, p = stats.mannwhitneyu(*distributions, alternative=alternative)
    
    if p < alpha:
        print(p, "The null hypothesis can be rejected.")
    else:
        print(p, "The null hypothesis cannot be rejected.")

        