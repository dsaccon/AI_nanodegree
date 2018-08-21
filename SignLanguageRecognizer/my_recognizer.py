import warnings
from asl_data import SinglesData
from operator import itemgetter


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    probabilities = []
    guesses = []
    test_seqs = list(test_set.get_all_Xlengths().values())

    for test_X, test_Xlength in test_seqs:
        tmp_dict = {}
        logL_highest = float("-inf")
        count = 0
        for word, model in models.items():
            count += 1
            try:
                logL = model.score(test_X, test_Xlength)
                tmp_dict.update({word: logL})
            except Exception as e:
                tmp_dict.update({word: float("-inf")})
        tmp_dict = sorted(tmp_dict.items(), key=lambda prob: prob[1], reverse=True)
        guesses.append(tmp_dict[0][0])
        tmp_dict = dict(tmp_dict)
        probabilities.append(tmp_dict)

    return probabilities, guesses