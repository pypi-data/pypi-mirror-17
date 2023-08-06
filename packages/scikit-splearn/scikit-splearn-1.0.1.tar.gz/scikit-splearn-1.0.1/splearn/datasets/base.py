import pickle
import numpy as np
from splearn.datasets.data_sample import DataSample


def load_data_sample(adr, type='SPiCe', pickle=False):
    """Load a sample from file and returns a dictionary
    (word,count)

    - Input:

    :param lrows: number or list of rows,
           a list of strings if partial=True;
           otherwise, based on pref if version="classic" or
           "prefix", fact otherwise
    :type lrows: int or list of int
    :param lcolumns: number or list of columns
            a list of strings if partial=True ;
            otherwise, based on suff if version="classic" or "suffix",
            fact otherwise
    :type lcolumns: int or list of int
    :param string version: (default = "classic") version name
    :param boolean partial: (default value = False) build of partial
           if True partial dictionaries are loaded based
           on nrows and lcolumns

    - Output:

    :returns:  nbL , nbEx , dsample , dpref , dsuff  , dfact
    :rtype: int , int , dict , dict , dict  , dict


    :Example:

    Let's say you are interested in the samples 10, 25, and 50, and want to
    know their class name.

    >>> from splearn.datasets.base import load_data_sample
    >>> from splearn.tests.datasets.get_dataset_path import get_dataset_path
    >>> train_file = '3.pautomac_light.train' # '4.spice.train'
    >>> data = load_data_sample(adr=get_dataset_path(train_file))
    >>> data.nbL
    4
    >>> data.nbEx
    5000
    >>> data.data
    Splearn_array([[ 3.,  0.,  3., ..., -1., -1., -1.],
           [ 3.,  3., -1., ..., -1., -1., -1.],
           [ 3.,  2.,  0., ..., -1., -1., -1.],
           ...,
           [ 3.,  1.,  3., ..., -1., -1., -1.],
           [ 3.,  0.,  3., ..., -1., -1., -1.],
           [ 3.,  3.,  1., ..., -1., -1., -1.]])

    """

    if type == 'SPiCe' or type == 'Pautomac':
        data = _load_file_doublelecture(adr=adr, pickle=pickle)
        return DataSample(data=data)

def _load_file_doublelecture(adr, pickle=False):
    dsample = {}  # dictionary (word,count)
    nb_sample, max_length = _read_dimension(adr=adr)
    f = open(adr, "r")
    line = f.readline()
    l = line.split()
    nbEx = int(l[0])
    nbL = int(l[1])
    line = f.readline()
    data1 = np.zeros((nbEx, max_length ))
    data1 += -1
    i = 0
    while line:
        l = line.split()
        # w = () if int(l[0]) == 0 else tuple([int(x) for x in l[1:]])
        # dsample[w] = dsample[w] + 1 if w in dsample else 1
        # traitement du mot vide pour les préfixes, suffixes et facteurs
        w = [] if int(l[0]) == 0 else [int(x) for x in l[1:]]
        data1[i, :len(w)] = w
        line = f.readline()
        i += 1
    # print("data1 ", data1)
    f.close()
    if pickle:
        _create_pickle_files(adr=adr, dsample=dsample)
    return nbL, nbEx, data1

def _read_dimension(adr):
    f = open(adr, "r")
    line = f.readline()
    l = line.split()
    nbEx = int(l[0])
    nbL = int(l[1])
    line = f.readline()
    max_length = 0
    nb_sample = 0
    while line:
        l = line.split()
        nb_sample += 1
        length = int(l[0])
        if max_length < length:
            max_length = length
        line = f.readline()
    f.close()
    if nb_sample != nbEx:
        raise ValueError("check imput file, metadata " + str(nbEx) +
                         "do not match number of samples " + str(nb_sample))
    return nb_sample , max_length

# def _load_file_1lecture(adr, pickle=False):
#     dsample = {}  # dictionary (word,count)
#     f = open(adr, "r")
#     line = f.readline()
#     l = line.split()
#     nbEx = int(l[0])
#     nbL = int(l[1])
#     line = f.readline()
#     data1 = np.zeros((0,0))
#     length = 0
#     while line:
#         l = line.split()
#         # w = () if int(l[0]) == 0 else tuple([int(x) for x in l[1:]])
#         # dsample[w] = dsample[w] + 1 if w in dsample else 1
#         # traitement du mot vide pour les préfixes, suffixes et facteurs
#         w = [] if int(l[0]) == 0 else [int(x) for x in l[1:]]
#         word = np.array(w, ndmin=2, dtype=np.uint32)
#         diff = abs(int(l[0]) - length)
#         if len(w) > length and not np.array_equal(data1, np.zeros((0,0))):
#             data1 = _add_empty(data1, diff)
#         elif word.shape[0] < length and not np.array_equal(data1, np.zeros((0,0))):
#             word = _add_empty(word, diff)
#
#         if np.array_equal(data1, np.zeros((0,0))):
#             data1 = word
#         else:
#             data1 = np.concatenate((data1, word), axis=0)
#         length = data1.shape[1]
#         line = f.readline()
#
#     f.close()
#     if pickle:
#         _create_pickle_files(adr=adr, dsample=dsample)
#     return nbL, nbEx, data1


# def _add_empty(data, diff):
#     empty = np.zeros((data.shape[0], diff))
#     empty += -1
#     data = np.concatenate((data, empty), axis=1)
#     return data


def _create_pickle_files(self, adr, dsample):
    f = open(adr + ".sample.pkl", "wb")
    pickle.dump(dsample, f)
    f.close()
