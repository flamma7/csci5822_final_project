

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

    for i in _cLength:
        p = prob_x('cLength', list(i), data)
        print("p(cLength={})={}".format(list(i), p))


def prob_cLoadShape(data):
    """
    :return: p(cLoadShape)
    """
    _cLoadShape = []
    for train in data:
        _cLoadShape.append(tuple(train.data['cLoadShape']))
    _cLoadShape = list(set(_cLoadShape))

    for i in _cLoadShape:
        p = prob_x('cLoadShape', list(i), data)
        print("p(cLoadShape={})={}".format(list(i), p))


def prob_nCars(data):
    """
    :return: p(nCars)
    """
    _nCars = []
    for train in data:
        _nCars.append(train.data['nCars'])
    _nCars = list(set(_nCars))

    for i in _nCars:
        p = prob_x('nCars', str(i), data)
        print("p(nCars={})={}".format(i, p))


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

    for i in _nDiffLoads:
        for j in _nCars:
            p = prob_x_given_y('nDiffLoads', str(i), {'nCars':str(j)}, data)
            print("p(nDiffLoads={} | nCars={})={}".format(i, j, p))


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

    for i in _cShape:
        for j in _nDiffLoads:
            for k in _cLoadShape:
                p = prob_x_given_y('cShape', list(i), {'nDiffLoads':str(j), 'cLoadShape':list(k)}, data)
                print("p(cShape={} | nDiffLoads={}, cLoadShape={})={}".format(i, j, k, p))


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

    for i in _cNumWheels:
        for j in _cLength:
            p = prob_x_given_y('cNumWheels', list(i), {'cLength':list(j)}, data)
            print("p(cNumWheels={} | cLength={}, )={}".format(i, j, p))


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

    for i in _cNumLoads:
        for j in _cLength:
            for k in _cNumWheels:
                p = prob_x_given_y('cNumLoads', list(i), {'cLength': list(j), 'cNumWheels': list(k)}, data)
                print("p(cNumLoads={} | cLength={}, cNumWheels={})={}".format(i, j, k, p))


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

    for i in _adjLoads:
        for j in _nDiffLoads:
            for k in _cNumLoads:
                p = prob_x_given_y('adjLoads', list(i), {'nDiffLoads': list(j), 'cNumLoads': list(k)}, data)
                print("p(adjLoads={} | nDiffLoads={}, cNumLoads={})={}".format(i, j, k, p))


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

    for i in _dir:
        for j in _cNumLoads:
            for k in _adjLoads:
                for l in _cShape:
                    p = prob_x_given_y('direction', str(i), {'cNumLoads': list(j), 'adjLoads': list(k), 'cShape': list(l)}, data)
                    print("p(direction={} | nDiffLoads={}, adjLoads={}, cShape={})={}".format(i, j, k, l, p))


if __name__ == "__main__":
    trains = []
    with open('data/trains-transformed.data', 'r') as f:
        for line in f.readlines():
            trains.append(make_vec(str(line)))


    # Probabilities working
    #prob_cLength(trains)
    #prob_cLoadShape(trains)
    #prob_nCars(trains)

    # Conditional probabilities
    #prob_nDiffLoads_given_nCars(trains)
    #prob_cShape_given_cLoadShape_AND_nDiffLoads(trains)
    #prob_cNumWheels_given_cLength(trains)
    #prob_cNumLoads_given_cLength_AND_cNumWheels(trains)
    #prob_adjLoads_given_nDiffLoads_AND_cNumLoads(trains)
    #prob_dir_given_cNumLoads_AND_adjLoads_AND_cShape(trains)