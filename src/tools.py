def normalise_names(s):
    elements = s.split()
    
    new = elements[0][0].upper()+'.'
    new += elements[-1].title()
    
    return new