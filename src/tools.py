def normalise_names(s):
    elements = s.split()
    
    new = elements[0][0].upper()+'.'
    new += elements[-1].title()
    
    return new

def write_to_file(filename, metric):
    file = open("../../assets/{}".format(filename), 'w')
    file.write('{}'.format(metric))
    file.close()
