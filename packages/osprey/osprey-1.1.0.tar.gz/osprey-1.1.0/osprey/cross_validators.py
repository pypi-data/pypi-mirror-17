from __future__ import print_function, absolute_import, division

from .utils import num_samples

import numpy as np
from sklearn import cross_validation


class BaseCVFactory(object):
    short_name = None

    def load(self):
        raise NotImplementedError('should be implemented in subclass')

    def create(self, X, y):
        raise NotImplementedError('should be implemented in subclass')


class ShuffleSplitFactory(BaseCVFactory):
    __doc__ = cross_validation.ShuffleSplit.__doc__
    short_name = ['shufflesplit', 'ShuffleSplit']

    def __init__(self, n_iter=10, test_size=0.1, train_size=None,
                 random_state=None):
        self.n_iter = n_iter
        self.test_size = test_size
        self.train_size = train_size
        self.random_state = random_state

    def create(self, X, y=None):

        return cross_validation.ShuffleSplit(num_samples(X),
                                             n_iter=self.n_iter,
                                             test_size=self.test_size,
                                             train_size=self.train_size,
                                             random_state=self.random_state)


class KFoldFactory(BaseCVFactory):
    __doc__ = cross_validation.KFold.__doc__
    short_name = ['kfold', 'KFold']

    def __init__(self, n_folds=3, shuffle=False, random_state=None):
        self.n_folds = n_folds
        self.shuffle = shuffle
        self.random_state = random_state

    def create(self, X, y=None):

        return cross_validation.KFold(num_samples(X),
                                      n_folds=self.n_folds,
                                      shuffle=self.shuffle,
                                      random_state=self.random_state)


class LeaveOneOutFactory(BaseCVFactory):
    __doc__ = cross_validation.LeaveOneOut.__doc__
    short_name = ['loo', 'LeaveOneOut']

    def __init__(self):
        pass

    def create(self, X, y=None):

        return cross_validation.LeaveOneOut(num_samples(X))


class StratifiedShuffleSplitFactory(BaseCVFactory):
    __doc__ = cross_validation.StratifiedShuffleSplit.__doc__
    short_name = ['stratifiedshufflesplit', 'StratifiedShuffleSplit']

    def __init__(self, n_iter=10, test_size=0.1, train_size=None,
                 random_state=None):
        self.n_iter = n_iter
        self.test_size = test_size
        self.train_size = train_size
        self.random_state = random_state

    def create(self, X, y):

        return cross_validation.StratifiedShuffleSplit(y, n_iter=self.n_iter,
                                                       test_size=self.test_size,
                                                       train_size=self.train_size,
                                                       random_state=self.random_state)


class StratifiedKFoldFactory(BaseCVFactory):
    __doc__ = cross_validation.StratifiedKFold.__doc__
    short_name = ['stratifiedkfold', 'StratifiedKFold']

    def __init__(self, n_folds=3, shuffle=False, random_state=None):
        self.n_folds = n_folds
        self.shuffle = shuffle
        self.random_state = random_state

    def create(self, X, y):

        return cross_validation.StratifiedKFold(y, n_folds=self.n_folds,
                                                shuffle=self.shuffle,
                                                random_state=self.random_state)


class FixedCVFactory(BaseCVFactory):
    """
    Cross-validator to use with a fixed, held-out validation set.

    Parameters
    ----------
    start : int
        Start index of validation set.
    stop : int, optional
        Stop index of validation set.
    """
    short_name = ['fixed', 'Fixed']

    def __init__(self, start, stop=None):
        self.valid = slice(start, stop)

    def create(self, X, y):
        indices = np.arange(num_samples(X))
        valid = indices[self.valid]
        train = np.setdiff1d(indices, valid)
        return (train, valid),  # return a nested tuple
