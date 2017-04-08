def text_l(x, mode='utf-8'):#reads text file, returns list of elements
    words = ''
    l = []
    with open(x, 'r') as f:
        data = f.readlines()
        for line in data:
            words = line.split()
            print(words)
            l.extend(words)
        print(l)
        return l