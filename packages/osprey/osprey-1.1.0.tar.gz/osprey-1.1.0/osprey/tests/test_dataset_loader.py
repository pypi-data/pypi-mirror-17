from __future__ import print_function, absolute_import, division
import os
import shutil
import tempfile

import numpy as np
import sklearn.datasets
from sklearn.externals.joblib import dump

from osprey.dataset_loaders import (DSVDatasetLoader, FilenameDatasetLoader,
                                    JoblibDatasetLoader, HDF5DatasetLoader,
                                    MDTrajDatasetLoader,
                                    MSMBuilderDatasetLoader,
                                    NumpyDatasetLoader, SklearnDatasetLoader)


def test_FilenameDatasetLoader_1():
    cwd = os.path.abspath(os.curdir)
    dirname = tempfile.mkdtemp()
    try:
        os.chdir(dirname)

        open('filename-1', 'w').close()
        open('filename-2', 'w').close()

        assert FilenameDatasetLoader.short_name == 'filename'
        loader = FilenameDatasetLoader('filename-*')
        X, y = loader.load()

        X_ref = list(map(os.path.abspath, ['filename-1', 'filename-2']))
        assert sorted(X) == X_ref, X
        assert y is None, y

    finally:
        os.chdir(cwd)
        shutil.rmtree(dirname)


def test_JoblibDatasetLoader_1():
    assert JoblibDatasetLoader.short_name == 'joblib'

    cwd = os.path.abspath(os.curdir)
    dirname = tempfile.mkdtemp()
    try:
        os.chdir(dirname)

        # one file
        dump(np.zeros((10, 2)), 'f1.pkl')
        loader = JoblibDatasetLoader('f1.pkl')
        X, y = loader.load()
        assert np.all(X == np.zeros((10, 2)))
        assert y is None

        # two files
        dump(np.ones((10, 2)), 'f2.pkl')
        loader = JoblibDatasetLoader('f*.pkl')
        X, y = loader.load()
        assert isinstance(X, list)
        assert np.all(X[0] == np.zeros((10, 2)))
        assert np.all(X[1] == np.ones((10, 2)))
        assert y is None

        # one file, with x and y
        dump({'foo': 'baz', 'bar': 'qux'}, 'foobar.pkl')
        loader = JoblibDatasetLoader('foobar.pkl', x_name='foo', y_name='bar')
        X, y = loader.load()
        assert X == 'baz', X
        assert y == 'qux', y

    finally:
        os.chdir(cwd)
        shutil.rmtree(dirname)


def test_HDF5DatasetLoader_1():
    from mdtraj import io

    assert HDF5DatasetLoader.short_name == 'hdf5'

    cwd = os.path.abspath(os.curdir)
    dirname = tempfile.mkdtemp()
    try:
        os.chdir(dirname)

        # one file
        io.saveh('f1.h5', **{'test': np.zeros((10, 3))})
        loader = HDF5DatasetLoader('f1.h5', concat=False)
        X, y = loader.load()
        assert np.all(X == np.zeros((10, 3)))
        assert y is None

        # two files
        io.saveh('f2.h5', **{'test': np.ones((10, 3))})
        loader = HDF5DatasetLoader('f*.h5', concat=False)
        X, y = loader.load()
        assert isinstance(X, list)
        assert np.all(X[0] == np.zeros((10, 3)))
        assert np.all(X[1] == np.ones((10, 3)))
        assert y is None

        # concat and stride and y_col
        loader = HDF5DatasetLoader('f*.h5', y_col=2, stride=2, concat=True)
        X, y = loader.load()
        assert X.shape[0] == 10 and X.shape[1] == 2
        assert y.shape[0] == 10

    finally:
        os.chdir(cwd)
        shutil.rmtree(dirname)


def test_DSVDatasetLoader_1():

    assert DSVDatasetLoader.short_name == 'dsv'

    cwd = os.path.abspath(os.curdir)
    dirname = tempfile.mkdtemp()
    try:
        os.chdir(dirname)

        # one file
        np.savetxt('f1.csv', np.zeros((10, 4)), fmt='%f,%f,%f,%f')
        loader = DSVDatasetLoader('f1.csv', concat=False)
        X, y = loader.load()
        assert np.all(X == np.zeros((10, 4)))
        assert y is None

        # two files
        np.savetxt('f2.csv', np.ones((10, 4)), fmt='%f,%f,%f,%f')
        loader = DSVDatasetLoader('f*.csv', concat=False)
        X, y = loader.load()
        assert isinstance(X, list)
        assert np.all(X[0] == np.zeros((10, 4)))
        assert np.all(X[1] == np.ones((10, 4)))
        assert y is None

        # y_col and usecols and concat and stride
        loader = DSVDatasetLoader('f*.csv', y_col=3, usecols=(0, 2),
                                  stride=2, concat=True)
        X, y = loader.load()
        assert X.shape[0] == 10 and X.shape[1] == 2
        assert y.shape[0] == 10

    finally:
        os.chdir(cwd)
        shutil.rmtree(dirname)


def test_MDTrajDatasetLoader_1():
    from mdtraj.testing import get_fn

    loader = MDTrajDatasetLoader(get_fn('legacy_msmbuilder_trj0.lh5'))
    X, y = loader.load()
    assert X[0].n_frames == 501
    assert y is None


def test_MSMBuilderDatasetLoader_1():
    from msmbuilder.dataset import dataset

    path = tempfile.mkdtemp()
    shutil.rmtree(path)
    try:
        x = np.random.randn(10, 2)
        ds = dataset(path, 'w', 'dir-npy')
        ds[0] = x

        loader = MSMBuilderDatasetLoader(path, fmt='dir-npy')
        X, y = loader.load()

        assert np.all(X[0] == x)
        assert y is None

    finally:
        shutil.rmtree(path)


def test_NumpyDatasetLoader_1():
        cwd = os.path.abspath(os.curdir)
        dirname = tempfile.mkdtemp()
        try:
            os.chdir(dirname)

            x = np.random.randn(10, 2)
            np.save('f1.npy', x)

            loader = NumpyDatasetLoader('f1.npy')
            X, y = loader.load()

            assert np.all(X[0] == x)
            assert y is None

        finally:
            os.chdir(cwd)
            shutil.rmtree(dirname)


def test_SklearnDatasetLoader_1():
    assert SklearnDatasetLoader.short_name == 'sklearn_dataset'
    X, y = SklearnDatasetLoader('load_iris').load()
    iris = sklearn.datasets.load_iris()
    assert np.all(X == iris['data'])
    assert np.all(y == iris['target'])
