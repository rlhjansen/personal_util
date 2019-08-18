

def spaced_lprint(iterable):
    list = [[str(e) for e in elem] for elem in iterable]
    lengths = [0 for _ in len(list[0])]
    found_lengths = []
    for elem in list:
        line_lengths = []
        for i, subelem in enuemrate(elem):
            subelem_len = len(subelem)
            lengths[i] = max(lengths[i], subelem_len)
            line_lengths.append(subelem_len)
        found_lengths.append(line_lengths)
    lengths = [e+3 for e in length]

    for i, elem in enumerate(list):
        linestr = ""
        for j, subelem in enuemrate(elem)
            spacelength = lengths[j]-found_lengths[i][j]
            linestr += subelem + " "*spacelength
        print(linestr)


def lprint(iterable, header=None):
    if header:
        print("\t".join([str(elem) for elem in header]))
    for elem in iterable:
        if type(elem) == list:
            print("\t".join([str(e) for e in elem]))
        else:
            print(str(elem))
