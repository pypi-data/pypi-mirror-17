#!/usr/bin/env python

import os

import numpy as np
import tables as tb

from km3pipe import Pipeline
from km3pipe.io import _insert_tabname_into_colnames, _read_group
from km3pipe.io.hdf5 import HDF5Pump, HDF5Sink
from km3pipe.testing import TestCase


class TestMultiTable(TestCase):
    def setUp(self):
        self.foo = np.array([
            (1.0, 2.0, 3.0),
            (4.0, 5.0, 6.0),
        ], dtype=[('a', '<f8'), ('b', '<f8'), ('c', '<f8'), ])
        self.bar = np.array([
            (10.0, 20.0, 30.0),
            (40.0, 50.0, 60.0),
        ], dtype=[('aa', '<f8'), ('bb', '<f8'), ('cc', '<f8'), ])
        self.tabs = {'foo': self.foo, 'bar': self.bar}
        self.where = '/lala'
        self.h5name = './test.h5'
        self.h5file = tb.open_file(
            # create the file in memory only
            self.h5name, 'w', driver="H5FD_CORE", driver_core_backing_store=0)
        for name, tab in self.tabs.items():
            self.h5file.create_table(self.where, name=name, obj=tab,
                                     createparents=True)

    def tearDown(self):
        self.h5file.close()

    def test_name_insert(self):
        exp_foo = ('foo_a', 'foo_b', 'foo_c')
        exp_bar = ('bar_aa', 'bar_bb', 'bar_cc')
        pref_foo = _insert_tabname_into_colnames(self.tabs['foo'], 'foo')
        pref_bar = _insert_tabname_into_colnames(self.tabs['bar'], 'bar')
        self.assertEqual(exp_foo, pref_foo.dtype.names)
        self.assertEqual(exp_bar, pref_bar.dtype.names)

    def test_group_read(self):
        tabs = _read_group(self.h5file, self.where)
        exp_cols = (
            'bar_aa', 'bar_bb', 'bar_cc',
            'foo_a', 'foo_b', 'foo_c',
        )
        exp_shape = (2, 6)
        res_shape = tabs.shape
        res_cols = tuple(tabs.columns)
        print(exp_cols)
        print(res_cols)
        self.assertEqual(exp_shape, res_shape)
        self.assertEqual(exp_cols, res_cols)


class TestWriteRead(TestCase):
    def setUp(self):
        self.foo = np.array([
            (1.0, 2.0, 3.0),
            (4.0, 5.0, 6.0),
        ], dtype=[('a', '<f8'), ('b', '<f8'), ('c', '<f8'), ])
        self.bar = np.array([
            (10.0, 20.0, 30.0),
            (40.0, 50.0, 60.0),
        ], dtype=[('aa', '<f8'), ('bb', '<f8'), ('cc', '<f8'), ])
        self.tabs = {'foo': self.foo, 'bar': self.bar}
        self.where = '/lala'
        self.h5name = './test.h5'
        self.h5file = tb.open_file(
            # create the file in memory only
            self.h5name, 'w', driver="H5FD_CORE", driver_core_backing_store=0)
        for name, tab in self.tabs.items():
            self.h5file.create_table(self.where, name=name, obj=tab,
                                     createparents=True)

    def tearDown(self):
        self.h5file.close()
