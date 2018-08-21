import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores

        best_model = self.base_model(self.n_constant)
        best_BIC = float("-inf")

        for num_hidden_states in range(self.min_n_components, self.max_n_components):

            try:
                model = GaussianHMM(n_components=num_hidden_states, covariance_type="diag", n_iter=1000, random_state=self.random_state).fit(self.X, self.lengths)
                logL = model.score(self.X, self.lengths)
            except Exception as e:
                break

            num_params = num_hidden_states*num_hidden_states + 2*num_hidden_states*len(self.X[0]) -1
            N = len(self.X)
            BIC = -2*logL + num_params*np.log(N)

            if BIC > best_BIC:
                best_model = model
                best_BIC = BIC

        return best_model


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    # DIC = log(P(original world)) - average(log(P(otherwords)))

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores

        x = self.hwords.items()
        word_list = []
        counter = 0
        for words in self.hwords.items():
            if words[0] != self.this_word:
                word_list.append(words[0])
            counter += 1

        best_model = self.base_model(self.n_constant)
        max_DIC = float("-inf")
        for num_hidden_states in range(self.min_n_components, self.max_n_components):

            logL_sum = 0
            for word in word_list:

                X_word, lengths_word = self.hwords[word]

                try:
                    model_otherwords = GaussianHMM(n_components=num_hidden_states, covariance_type="diag", n_iter=1000, random_state=self.random_state).fit(X_word, lengths_word)
                    logL_otherwords = model_otherwords.score(X_word, lengths_word)
                except Exception as e:
                    break

                logL_sum += logL_otherwords
            log_avg_otherwords = logL_sum/len(word_list)

            try:
                model_orig = self.base_model(num_hidden_states)
                logL_orig = model_orig.score(self.X, self.lengths)
            except Exception as e:
                break

            DIC = logL_orig - log_avg_otherwords
            if DIC > max_DIC:
                max_DIC = DIC
                best_model = model_orig

        return best_model


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)

        best_model = self.base_model(self.n_constant)
        best_avg = float("-inf")
        num_splits = 3
        split_method = KFold(n_splits=num_splits)

        for num_hidden_states in range(self.min_n_components, self.max_n_components):

            logL_list = []

            if len(self.sequences) < num_splits:
                break

            for cv_train_idx, cv_test_idx in split_method.split(self.sequences):

                cv_train_x, cv_train_lengths = combine_sequences(cv_train_idx, self.sequences)
                cv_test_x, cv_test_lengths = combine_sequences(cv_test_idx, self.sequences)

                try:
                    model = GaussianHMM(n_components=num_hidden_states, covariance_type="diag", n_iter=1000, random_state=self.random_state).fit(cv_train_x, cv_train_lengths)

                    logL = model.score(cv_test_x, cv_test_lengths)
                    logL_list.append(logL)
                except Exception as e:
                    break

            avg = np.average(logL_list)
            if avg > best_avg:
#                best_model = model
                best_model = GaussianHMM(n_components=num_hidden_states, covariance_type="diag", n_iter=1000, random_state=self.random_state).fit(self.X, self.lengths)
                best_avg = avg

        return best_model