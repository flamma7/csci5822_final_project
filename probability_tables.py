
"""
These are probably not needed but they are the values each parameter can take on.
"""
nCars = [3, 4, 5]
nDiffLoads = [1, 2, 3, 4]
cNumWheels = [2, 3]
cLength = ['short', 'long']
cShape = ['closedrect', 'dblopnrect', 'ellipse', 'engine', 'hexagon', 'jaggedtop', 'openrect', 'opentrap', 'slopetop', 'ushaped']
cNumLoads = [0, 1, 2, 3]
cLoadShape = ['circlelod', 'hexagonlod', 'rectanglod', 'trianglod']
adjLoads = []
direction = ['east', 'west']


class Train_w_car_vects:
    """
    A train object is just a single dictionary called data.
    """
    def __init__(self):
        self.data = {'nCars': 0,
                     'nDiffLoads': 0,
                     'cNumWheels': [0, 0, 0, 0, 0],
                     'cLength': [0, 0, 0, 0, 0],
                     'cShape': [0, 0, 0, 0, 0],
                     'cNumLoads': [0, 0, 0, 0, 0],
                     'cLoadShape': [0, 0, 0, 0, 0],
                     'adjLoads': [0,0,0,0,0,0,0,0,0,0],
                     'direction': ""}


def make_vec(data):
    """
    Create a single train object from data. Cars are stored as vectors of length 5, one element per car. Note if the
    train has less than 5 cars the vector will have zeros in place of the non-existent cars.

    :param data:    Some train dataset for a single train.
    :return:        A train object.
    """
    t = Train_w_car_vects()
    d = data.rstrip().split()

    t.data['nCars'] = d[0]
    t.data['nDiffLoads'] = d[1]
    idx = 2
    for i in range(int(t.data['nCars'])-1):

        t.data['cNumWheels'][i] = d[idx+i] if d[idx+i] is not '-' else 0
        t.data['cLength'][i] = d[idx+i+1] if d[idx+i+1] is not '-' else 0
        t.data['cShape'][i] = d[idx+i+2] if d[idx+i+2] is not '-' else 0
        t.data['cNumLoads'][i] = d[idx+i+3] if d[idx+i+3] is not '-' else 0
        t.data['cLoadShape'][i] = d[idx+i+4] if d[idx+i+4] is not '-' else 0
        idx += 4
    #t.data['cLength'] = [x for x in t.data['cLength'] if x != 0]
    #t.data['cLength'] = set(t.data['cLength'])
    t.data['adjLoads'] = [d[22], d[23], d[24], d[25], d[26], d[27], d[28], d[29], d[30], d[31]]
    t.data['direction'] = d[32]
    return t


def prob_x_given_y(X, x, given, data):
    """
    :return: P(X=x | Y1=y1,...Yn=yn)
    """
    count = 0
    total = 0
    for d in data:

        # if Y1=y1 and Y2=y2 and ...
        given_true = False
        for Y, y in given.items():
            if d.data[Y] == y:
                given_true = True
            else:
                given_true = False

        # if the given is good then check if X=x
        if given_true:
            total +=1
            if d.data[X] == x:
                count += 1

    return count/total if total > 0 else 0


def prob_x(X, x, data):
    """
    :return: P(X=x)
    """
    count = 0
    total = 0
    for d in data:
        if d.data[X] == x:
            count += 1
        total += 1
    return count/total if total > 0 else 0


def prob_cLength(data):
    """
    :return: P(cLength)
    """
    _cLength = []
    for train in data:
        _cLength.append(tuple(train.data['cLength']))
    _cLength = list(set(_cLength))

    p_out = {}

    for i in _cLength:
        p = prob_x('cLength', list(i), data)
        if p > 0:
            p_out["p(cLength={})".format(list(i))] = p
        #print("p(cLength={})={}".format(list(i), p))
    return p_out


def prob_cLoadShape(data):
    """
    :return: p(cLoadShape)
    """
    _cLoadShape = []
    for train in data:
        _cLoadShape.append(tuple(train.data['cLoadShape']))
    _cLoadShape = list(set(_cLoadShape))

    p_out = {}

    for i in _cLoadShape:
        p = prob_x('cLoadShape', list(i), data)
        if p > 0:
            p_out["p(cLoadShape={})".format(list(i))] = p
        #print("p(cLoadShape={})={}".format(list(i), p))
    return p_out


def prob_nCars(data):
    """
    :return: p(nCars)
    """
    _nCars = []
    for train in data:
        _nCars.append(train.data['nCars'])
    _nCars = list(set(_nCars))

    p_out = {}

    for i in _nCars:
        p = prob_x('nCars', str(i), data)
        if p > 0:
            p_out["p(nCars={})".format(i)] = p
        #print("p(nCars={})={}".format(i, p))
    return p_out


def prob_nDiffLoads_given_nCars(data):
    """
    :return: p(nDiffLoads | nCars)
    """

    _nDiffLoads = []
    for train in data:
        _nDiffLoads.append(train.data['nDiffLoads'])
    _nDiffLoads = list(set(_nDiffLoads))

    _nCars = []
    for train in data:
        _nCars.append(train.data['nCars'])
    _nCars = list(set(_nCars))

    p_out = {}

    for i in _nDiffLoads:
        for j in _nCars:
            p = prob_x_given_y('nDiffLoads', str(i), {'nCars':str(j)}, data)
            if p > 0:
                p_out["p(nDiffLoads={} | nCars={})".format(i, j)] = p
            #print("p(nDiffLoads={} | nCars={})={}".format(i, j, p))
    return p_out


def prob_cShape_given_cLoadShape_AND_nDiffLoads(data):
    """
    :return: p(cShape | cLoadShape, nDiffLoads)
    """
    _nDiffLoads = []
    for train in data:
        _nDiffLoads.append(train.data['nDiffLoads'])
    _nDiffLoads = list(set(_nDiffLoads))

    _cLoadShape = []
    for train in data:
        _cLoadShape.append(tuple(train.data['cLoadShape']))
    _cLoadShape = list(set(_cLoadShape))

    _cShape = []
    for train in data:
        _cShape.append(tuple(train.data['cShape']))
    _cShape = list(set(_cShape))

    p_out = {}

    for i in _cShape:
        for j in _nDiffLoads:
            for k in _cLoadShape:
                p = prob_x_given_y('cShape', list(i), {'nDiffLoads':str(j), 'cLoadShape':list(k)}, data)
                if p > 0:
                    p_out["p(cShape={} | nDiffLoads={}, cLoadShape={})".format(i, j, k)] = p
                #print("p(cShape={} | nDiffLoads={}, cLoadShape={})={}".format(i, j, k, p))
    return p_out


def prob_cNumWheels_given_cLength(data):
    """
    :return: p(cNumWheels | cLength)
    """
    _cLength = []
    for train in data:
        _cLength.append(tuple(train.data['cLength']))
    _cLength = list(set(_cLength))

    _cNumWheels = []
    for train in data:
        _cNumWheels.append(tuple(train.data['cNumWheels']))
    _cNumWheels = list(set(_cNumWheels))

    p_out = {}

    for i in _cNumWheels:
        for j in _cLength:
            p = prob_x_given_y('cNumWheels', list(i), {'cLength':list(j)}, data)
            if p > 0:
                p_out["p(cNumWheels={} | cLength={})".format(i, j)] = p
            #print("p(cNumWheels={} | cLength={})={}".format(i, j, p))
    return p_out


def prob_cNumLoads_given_cLength_AND_cNumWheels(data):
    """
    :return: p(cNumLoads | length, cNumWheels)
    """
    _cLength = []
    for train in data:
        _cLength.append(tuple(train.data['cLength']))
    _cLength = list(set(_cLength))

    _cNumWheels = []
    for train in data:
        _cNumWheels.append(tuple(train.data['cNumWheels']))
    _cNumWheels = list(set(_cNumWheels))

    _cNumLoads = []
    for train in data:
        _cNumLoads.append(tuple(train.data['cNumLoads']))
    _cNumLoads = list(set(_cNumLoads))

    p_out = {}

    for i in _cNumLoads:
        for j in _cLength:
            for k in _cNumWheels:
                p = prob_x_given_y('cNumLoads', list(i), {'cLength': list(j), 'cNumWheels': list(k)}, data)
                if p > 0:
                    p_out["p(cNumLoads={} | cLength={}, cNumWheels={})".format(i, j, k)] = p
                #print("p(cNumLoads={} | cLength={}, cNumWheels={})={}".format(i, j, k, p))
    return p_out


def prob_adjLoads_given_nDiffLoads_AND_cNumLoads(data):
    """
    :return: p(adjLoads | nDiffLoads, cNumLoads)
    """
    _nDiffLoads = []
    for train in data:
        _nDiffLoads.append(train.data['nDiffLoads'])
    _nDiffLoads = list(set(_nDiffLoads))

    _cNumLoads = []
    for train in data:
        _cNumLoads.append(tuple(train.data['cNumLoads']))
    _cNumLoads = list(set(_cNumLoads))

    _adjLoads = []
    for train in data:
        _adjLoads.append(tuple(train.data['adjLoads']))
    _adjLoads = list(set(_adjLoads))

    p_out = {}

    for i in _adjLoads:
        for j in _nDiffLoads:
            for k in _cNumLoads:
                p = prob_x_given_y('adjLoads', list(i), {'nDiffLoads': list(j), 'cNumLoads': list(k)}, data)
                if p > 0:
                    p_out["p(adjLoads={} | nDiffLoads={}, cNumLoads={})".format(i, j, k)] = p
                #print("p(adjLoads={} | nDiffLoads={}, cNumLoads={})={}".format(i, j, k, p))
    return p_out


def prob_dir_given_cNumLoads_AND_adjLoads_AND_cShape(data):
    """
    :return: p(direction | cNumLoads, adjLoads, cShape)
    """
    _cShape = []
    for train in data:
        _cShape.append(tuple(train.data['cShape']))
    _cShape = list(set(_cShape))

    _cNumLoads = []
    for train in data:
        _cNumLoads.append(tuple(train.data['cNumLoads']))
    _cNumLoads = list(set(_cNumLoads))

    _adjLoads = []
    for train in data:
        _adjLoads.append(tuple(train.data['adjLoads']))
    _adjLoads = list(set(_adjLoads))

    _dir = []
    for train in data:
        _dir.append(train.data['direction'])
    _dir = list(set(_dir))

    p_out = {}

    for i in _dir:
        for j in _cNumLoads:
            for k in _adjLoads:
                for l in _cShape:
                    p = prob_x_given_y('direction', str(i), {'cNumLoads': list(j), 'adjLoads': list(k), 'cShape': list(l)}, data)
                    if p > 0:
                        p_out["p(direction={} | nDiffLoads={}, adjLoads={}, cShape={})".format(i, j, k, l)] = p
                    #print("p(direction={} | nDiffLoads={}, adjLoads={}, cShape={})={}".format(i, j, k, l, p))
    return p_out


if __name__ == "__main__":
    """
    Read in the trains dataset and create some train objects. Each train object has some element data which is just
    a python dictionary. Cars are stored as vectors of length 5, so one element per car. If are car isn't present it's
    element is just a zero.
    """
    trains = []
    with open('data/trains-transformed.data', 'r') as f:
        for line in f.readlines():
            trains.append(make_vec(str(line)))

    """
    Calls the the probability table functions works like this:
        1. pass is the trains data as argument
        2. it returns a python dictionary where key = probability statement and value = probability
        Notes:
            1. Probability statement access examples:
                p_cLength['p(cLength=2)']
                p_cNumLoads['p(cNumLoads=2 | cLength=3, cNumWheels=2)']
            2. The probability statement used to access the dict, the given x, y, z must be in the same order as in the
            function call which created the dictionary.
            3. A key-value pair is present in the dictionary only if the probability is non-zero, so doing something
            like 'p(nCars=100)' in myDict is probably good to do.
            
    """
    # Probabilities
    p_cLength = prob_cLength(trains)
    p_cLoadShape = prob_cLoadShape(trains)
    p_nCars = prob_nCars(trains)

    # Conditional probabilities
    p_nDiffLoads = prob_nDiffLoads_given_nCars(trains)
    p_cShape = prob_cShape_given_cLoadShape_AND_nDiffLoads(trains)
    p_cNumWheels = prob_cNumWheels_given_cLength(trains)
    p_cNumLoads = prob_cNumLoads_given_cLength_AND_cNumWheels(trains)
    p_adjLoads = prob_adjLoads_given_nDiffLoads_AND_cNumLoads(trains)
    p_dir = prob_dir_given_cNumLoads_AND_adjLoads_AND_cShape(trains)

    """
    Print out whatever probability we want.
    """
    for k, v, in p_nCars.items():
        print("{}={}".format(k,v))