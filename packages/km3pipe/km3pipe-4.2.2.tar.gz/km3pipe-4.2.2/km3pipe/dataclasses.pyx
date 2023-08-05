# coding=utf-8
# cython: profile=True
# Filename: dataclasses.py
# cython: embedsignature=True
# pylint: disable=W0232,C0103,C0111
"""
...

"""
from __future__ import division, absolute_import, print_function

import ctypes
from libcpp cimport bool as c_bool  # noqa
from six import with_metaclass

import numpy as np
cimport numpy as np
cimport cython

np.import_array()

from km3pipe.tools import angle_between, geant2pdg, pdg2name

__author__ = "Tamas Gal and Moritz Lotze"
__copyright__ = "Copyright 2016, Tamas Gal and the KM3NeT collaboration."
__credits__ = []
__license__ = "MIT"
__maintainer__ = "Tamas Gal and Moritz Lotze"
__email__ = "tgal@km3net.de"
__status__ = "Development"
__all__ = ('EventInfo', 'Point', 'Position', 'Direction', 'HitSeries', 'Hit',
           'Track', 'TrackSeries', 'Serialisable')


IS_CC = {
    3: False,
    2: True,
    1: False,
    0: True,
}



class Serialisable(type):
    """A metaclass for serialisable classes.

    The classes should define a `dtype` attribute in their body and are not
    meant to define `__init__` (it will be overwritten).

    Example using six.with_metaclass for py2/py3 compat
    ---------------------------------------------------

        class Foo(with_metaclass(Serialisable)):
            dtype = [('a', '<i4'), ('b', '>i8')]

    """
    def __new__(metaclass, class_name, class_parents, class_attr):
        attr = {}
        for name, val in class_attr.items():
            if name == 'dtype':
                attr['dtype'] = np.dtype(val)
            else:
                attr[name] = val

        def __init__(self, *args, **kwargs):
            """Take care of the attribute settings."""
            for arg, name in zip(args, self.dtype.names):
                setattr(self, name, arg)
            for key, value in kwargs.iteritems():
                setattr(self, key, value)

        attr['__init__'] = __init__

        return type(class_name, class_parents, attr)


class EventInfo(with_metaclass(Serialisable)):
    """Event Metadata.
    """
    dtype = [
        ('det_id', '<i4'), ('event_id', '<u4'), ('frame_index', '<u4'),
        ('mc_id', '<i4'), ('mc_t', '<f8'), ('overlays', 'u1'),
        #('run_id', '<u4'),
        ('trigger_counter', '<u8'), ('trigger_mask', '<u8'),
        ('utc_nanoseconds', '<u8'), ('utc_seconds', '<u8'),
        ('weight_w1', '<f8'), ('weight_w2', '<f8'), ('weight_w3', '<f8')
        ]

    @classmethod
    def from_table(cls, row):
        args = []
        for col in cls.dtype.names:
            try:
                args.append(row[col])
            except KeyError:
                args.append(np.nan)
        return cls(*args)

    @classmethod
    def deserialise(cls, data, event_id=None, fmt='numpy', h5loc='/'):
        if fmt == 'numpy':
            return cls.from_table(data[0])

    def serialise(self, to='numpy'):
        if to == 'numpy':
            return np.array(self.__array__(), dtype=self.dtype)

    def __array__(self):
        return [(self.det_id, self.event_id, self.frame_index, self.mc_id,
                 self.mc_t, self.overlays,
                 #self.run_id,
                 self.trigger_counter,
                 self.trigger_mask, self.utc_nanoseconds, self.utc_seconds,
                 self.weight_w1, self.weight_w2, self.weight_w3),]

    def __str__(self):
        return "Event #{0}:\n" \
               "    detector id:     {1}\n" \
               "    frame index:     {2}\n" \
               "    UTC seconds:     {3}\n" \
               "    UTC nanoseconds: {4}\n" \
               "    MC id:           {5}\n" \
               "    MC time:         {6}\n" \
               "    overlays:        {7}\n" \
               "    trigger counter: {8}\n" \
               "    trigger mask:    {9}\n" \
               .format(self.event_id, self.det_id,
                       self.frame_index, self.utc_seconds, self.utc_nanoseconds,
                       self.mc_id, self.mc_t, self.overlays,
                       self.trigger_counter, self.trigger_mask
                       #self.run_id,
                       )

    def __insp__(self):
        return self.__str__()

    def __len__(self):
        return 1


class Point(np.ndarray):
    """Represents a point in a 3D space"""
    def __new__(cls, input_array=(np.nan, np.nan, np.nan)):
        """Add x, y and z to the ndarray"""
        obj = np.asarray(input_array).view(cls)
        return obj

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, value):
        self[2] = value


Position = Direction = Point  # Backwards compatibility


class Direction_(Point):
    """Represents a direction in a 3D space

    The direction vector always normalises itself when an attribute is changed.

    """
    def __new__(cls, input_array=(1, 0, 0)):
        """Add x, y and z to the ndarray"""
        normed_array = np.array(input_array) / np.linalg.norm(input_array)
        obj = np.asarray(normed_array).view(cls)
        return obj

    def _normalise(self):
        normed_array = self / np.linalg.norm(self)
        self[0] = normed_array[0]
        self[1] = normed_array[1]
        self[2] = normed_array[2]

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value
        self._normalise()

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value
        self._normalise()

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, value):
        self[2] = value
        self._normalise()

    @property
    def zenith(self):
        return angle_between(self, (0, 0, -1))

    def __str__(self):
        return "({0:.4}, {1:.4}, {2:.4})".format(self.x, self.y, self.z)


cdef class Hit:
    """Hit on a PMT.

    Parameters
    ----------
    channel_id : int
    dir : Direction or numpy.ndarray
    dom_id : int
    id : int
    pmt_id : int
    pos : Position or numpy.ndarray
    time : int
    tot : int
    triggered : bool

    """
    cdef public int id, dom_id, time, tot, channel_id, pmt_id
    cdef public bint triggered
    cdef public np.ndarray pos
    cdef public np.ndarray dir

    def __cinit__(self,
                  int channel_id,
                  int dom_id,
                  int id,
                  int pmt_id,
                  int time,
                  int tot,
                  bint triggered,
                 ):
        self.channel_id = channel_id
        self.dom_id = dom_id
        self.id = id
        self.pmt_id = pmt_id
        self.time = time
        self.tot = tot
        self.triggered = triggered

    def __str__(self):
        return "Hit: channel_id({0}), dom_id({1}), pmt_id({2}), tot({3}), " \
               "time({4}), triggered({5})" \
               .format(self.channel_id, self.dom_id, self.pmt_id, self.tot,
                       self.time, self.triggered)

    def __repr__(self):
        return self.__str__()

    def __insp__(self):
        return self.__str__()


cdef class Track:
    """Particle track.

    Parameters
    ----------
    bjorkeny : float
    dir : Direction or numpy.ndarray
    energy : float
    id : int
    interaction_channel : int
    is_cc : bool
    length : float
    pos : Position or numpy.ndarray
    time : int
    type : int
    """
    cdef public int id, time, type, interaction_channel
    cdef public float energy, length, bjorkeny
    cdef public bint is_cc
    cdef public np.ndarray pos
    cdef public np.ndarray dir

    def __cinit__(self,
                  float bjorkeny,
                  dir,
                  float energy,
                  int id,
                  np.int64_t interaction_channel,
                  bint is_cc,
                  float length,
                  pos,
                  int time,
                  int type
                  ):
        self.bjorkeny = bjorkeny
        self.is_cc = is_cc
        self.dir = dir
        self.energy = energy
        self.interaction_channel = interaction_channel
        self.id = id
        self.length = length
        self.pos = pos
        self.time = time
        self.type = type

    def __str__(self):
        return "Track: pos({0}), dir({1}), t={2}, E={3}, type={4} ({5})" \
               .format(self.pos, self.dir, self.time, self.energy,
                       self.type, pdg2name(self.type))

    def __repr__(self):
        return self.__str__()

    def __insp__(self):
        return self.__str__()


class HitSeries(object):
    """Collection of multiple Hits.
    """
    dtype = np.dtype([
        ('channel_id', 'u1'), ('dom_id', '<u4'), ('event_id', '<u4'),
        ('id', '<u4'), ('pmt_id', '<u4'),
        #('run_id', '<u4'),
        ('time', '<i4'), ('tot', 'u1'), ('triggered', '?')
        ])
    def __init__(self, hits, event_id=None):
        self.event_id = event_id
        self._channel_id = None
        self._dom_id = None
        self._hits = hits
        self._id = None
        self._index = 0
        self._pmt_id = None
        self._pos = None
        self._time = None
        self._tot = None
        self._triggered = None
        self._triggered_hits = None
        self._columns = None

    @classmethod
    def from_aanet(cls, hits, event_id=None):
        return cls([Hit(
            ord(h.channel_id),
            h.dom_id,
            h.id,
            h.pmt_id,
            h.t,
            h.tot,
            h.trig,
        ) for h in hits], event_id)

    @classmethod
    def from_evt(cls, hits, event_id=None):
        return cls([Hit(
            0,     # channel_id
            0,     # dom_id
            h.id,
            h.pmt_id,
            h.time,
            h.tot,
            0,     # triggered
        ) for h in hits], event_id)

    @classmethod
    def from_arrays(cls, channel_ids, dom_ids, ids, pmt_ids, times, tots,
                    triggereds, event_id=None):
        args = channel_ids, dom_ids, ids, pmt_ids, times, tots, triggereds
        hits = cls([Hit(*hit_args) for hit_args in zip(*args)], event_id)
        hits._channel_id = channel_ids
        hits._dom_id = dom_ids
        hits._id = ids
        hits._pmt_id = pmt_ids
        hits._time = times
        hits._tot = tots
        hits._triggered = triggereds
        return hits

    @classmethod
    def from_table(cls, table, event_id=None):
        return cls([Hit(
            row['channel_id'],
            row['dom_id'],
            row['id'],
            row['pmt_id'],
            row['time'],
            row['tot'],
            row['triggered'],
        ) for row in table], event_id)

    @classmethod
    def deserialise(cls, data, event_id=None, fmt='numpy', h5loc='/'):
        if fmt == 'numpy':
            return cls.from_table(data, event_id)

    def serialise(self, to='numpy'):
        if to == 'numpy':
            return np.array(self.__array__(), dtype=self.dtype)

    def __array__(self):
        return list((h.channel_id, h.dom_id, self.event_id, h.id, h.pmt_id,
            #self.run_id,
            h.time, h.tot, h.triggered) for h in self._hits)

    def __iter__(self):
        return self

    @property
    def id(self):
        if self._id is None:
            self._id = np.array([h.id for h in self._hits])
        return self._id

    @property
    def time(self):
        if self._time is None:
            self._time = np.array([h.time for h in self._hits])
        return self._time

    @property
    def triggered_hits(self):
        if self._triggered_hits is None:
            self._triggered_hits = np.array([h for h in self._hits
                                        if h.triggered])
        return self._triggered_hits

    @property
    def triggered(self):
        if self._triggered is None:
            self._triggered = np.array([h.triggered for h in self._hits])
        return self._triggered

    @property
    def tot(self):
        if self._tot is None:
            self._tot = np.array([h.tot for h in self._hits])
        return self._tot

    @property
    def dom_id(self):
        if self._dom_id is None:
            self._dom_id = np.array([h.dom_id for h in self._hits])
        return self._dom_id

    @property
    def pmt_id(self):
        if self._pmt_id is None:
            self._pmt_id = np.array([h.pmt_id for h in self._hits])
        return self._pmt_id

    @property
    def id(self):
        if self._id is None:
            self._id = np.array([h.id for h in self._hits])
        return self._id

    @property
    def channel_id(self):
        if self._channel_id is None:
            self._channel_id = np.array([h.channel_id for h in self._hits])
        return self._channel_id

    @property
    def pos(self):
        if self._pos is None:
            self._pos = np.array([h.pos for h in self._hits])
        return self._pos

    def as_columns(self):
        if self._columns is None:
            self._columns = {
                'tot': self.tot,
                'channel_id': self.channel_id,
                'pmt_id': self.pmt_id,
                'dom_id': self.dom_id,
                'time': self.time,
                'id': self.id,
                'triggered': self.triggered,
            }
        return self._columns

    def next(self):
        """Python 2/3 compatibility for iterators"""
        return self.__next__()

    def __next__(self):
        if self._index >= len(self):
            self._index = 0
            raise StopIteration
        item = self._hits[self._index]
        self._index += 1
        return item

    def __len__(self):
        return len(self._hits)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._hits[index]
        elif isinstance(index, slice):
            return self._slice_generator(index)
        else:
            raise TypeError("index must be int or slice")

    def _slice_generator(self, index):
        """A simple slice generator for iterations"""
        start, stop, step = index.indices(len(self))
        for i in range(start, stop, step):
            yield self._hits[i]

    def __str__(self):
        n_hits = len(self)
        plural = 's' if n_hits > 1 or n_hits == 0 else ''
        return("HitSeries with {0} hit{1}.".format(len(self), plural))

    def __repr__(self):
        return self.__str__()

    def __insp__(self):
        return '\n'.join([str(hit) for hit in self._hits])


class TrackSeries(object):
    """Collection of multiple Tracks.

    Attributes
    ----------
    dtype: datatype of array representation
    """
    dtype = np.dtype([
        ('bjorkeny', '<f8'), ('dir_x', '<f8'), ('dir_y', '<f8'),
        ('dir_z', '<f8'), ('energy', '<f8'), ('event_id', '<u4'),
        ('id', '<u4'), ('interaction_channel', '<u4'), ('is_cc', '?'),
        ('length', '<f8'), ('pos_x', '<f8'), ('pos_y', '<f8'),
        ('pos_z', '<f8'),
        #('run_id', '<u4'),
        ('time', '<i4'), ('type', '<i4')
        ])
    def __init__(self, tracks, event_id=None):
        self.event_id = event_id
        self._bjorkeny = None
        self._dir = None
        self._energy = None
        self._highest_energetic_muon = None
        self._id = None
        self._index = 0
        self._interaction_channel = None
        self._is_cc = None
        self._length = None
        self._pos = None
        self._time = None
        self._tracks = tracks
        self._type = None

    @classmethod
    def from_aanet(cls, tracks, event_id=None):
        return cls([Track(cls.get_usr_item(t, 1),               # bjorkeny
                          Direction((t.dir.x, t.dir.y, t.dir.z)),
                          t.E,
                          t.id,
                          cls.get_usr_item(t, 2),               # ichan
                          IS_CC[cls.get_usr_item(t, 0)],        # is_cc
                          t.len,
                          Position((t.pos.x, t.pos.y, t.pos.z)),
                          t.t,
                          # TODO:
                          # This is a nasty bug. It is not completely clear
                          # if this is supposed to be PDG or Geant convention.
                          # might be, that for CC neutrino events,
                          # the two vector elements might follow _different_
                          # conventions. Yep, 2 conventions for
                          # 2 vector elements...
                          #geant2pdg(t.type))
                          t.type,
                          )
                    for t in tracks], event_id)

    @classmethod
    def from_arrays(cls,
                    bjorkenys,
                    directions_x,
                    directions_y,
                    directions_z,
                    energies,
                    ids,
                    interaction_channels,
                    is_ccs,
                    lengths,
                    positions_x,
                    positions_y,
                    positions_z,
                    times,
                    types,
                    event_id=None,
                    ):
        directions = np.column_stack((directions_x, directions_y,
                                      directions_z))
        positions = np.column_stack((positions_x, positions_y,
                                      positions_z))
        args = bjorkenys, directions, energies, \
            ids, interaction_channels, is_ccs, lengths, positions, \
            times, types
        tracks = cls([Track(*track_args) for track_args in zip(*args)], event_id)
        tracks._bjorkeny = bjorkenys
        tracks._dir = zip(directions_x, directions_y, directions_z)
        tracks._energy = energies
        tracks._id = ids
        tracks._interaction_channel = interaction_channels
        tracks._is_cc = is_ccs
        tracks._length = lengths
        tracks._pos = zip(positions_x, positions_y, positions_z)
        tracks._time = times
        tracks._type = types
        return tracks

    @classmethod
    def from_table(cls, table, event_id=None):
        return cls([Track(
            row['bjorkeny'],
            np.array((row['dir_x'], row['dir_y'], row['dir_z'],)),
            row['energy'],
            row['id'],
            row['interaction_channel'],
            row['is_cc'],
            row['length'],
            np.array((row['pos_x'], row['pos_y'], row['pos_z'],)),
            row['time'],
            row['type']
        ) for row in table], event_id)

    @classmethod
    def deserialise(cls, data, event_id=None, fmt='numpy', h5loc='/'):
        if fmt == 'numpy':
            return cls.from_table(data, event_id)

    def serialise(self, to='numpy'):
        if to == 'numpy':
            return np.array(self.__array__(), dtype=self.dtype)

    def __array__(self):
        return [(t.bjorkeny, t.dir[0], t.dir[1], t.dir[2], t.energy,
            self.event_id, t.id, t.interaction_channel, t.is_cc,
            t.length, t.pos[0], t.pos[1], t.pos[2], t.time, t.type)
            for t in self._tracks]

    @classmethod
    def get_usr_item(cls, track, index):
        try:
            item = track.usr[index]
        except IndexError:
            item = 0.
        return item

    @property
    def highest_energetic_muon(self):
        if self._highest_energetic_muon is None:
            muons = [track for track in self if abs(track.type) == 13]
            if len(muons) == 0:
                raise AttributeError("No muon found")
            self._highest_energetic_muon = max(muons, key=lambda m: m.energy)
        return self._highest_energetic_muon

    def __iter__(self):
        return self

    def __iter__(self):
        return self

    @property
    def bjorkeny(self):
        if self._bjorkeny is None:
            self._bjorkeny = np.array([t.bjorkeny for t in self._tracks])
        return self._bjorkeny

    @property
    def is_cc(self):
        if self._is_cc is None:
            self._is_cc = np.array([t.is_cc for t in self._tracks])
        return self._is_cc

    @property
    def interaction_channel(self):
        if self._interaction_channel is None:
            self._interaction_channel = np.array([t.interaction_channel for
                                                  t in self._tracks])
        return self._interaction_channel

    @property
    def id(self):
        if self._id is None:
            self._id = np.array([t.id for t in self._tracks])
        return self._id

    @property
    def time(self):
        if self._time is None:
            self._time = np.array([t.time for t in self._tracks])
        return self._time

    @property
    def energy(self):
        if self._energy is None:
            self._energy = np.array([t.energy for t in self._tracks])
        return self._energy

    @property
    def length(self):
        if self._length is None:
            self._length = np.array([t.length for t in self._tracks])
        return self._length

    @property
    def type(self):
        if self._type is None:
            self._type = np.array([t.type for t in self._tracks])
        return self._type

    @property
    def pos(self):
        if self._pos is None:
            self._pos = np.array([t.pos for t in self._tracks])
        return self._pos

    @property
    def dir(self):
        if self._dir is None:
            self._dir = np.array([t.dir for t in self._tracks])
        return self._dir

    def next(self):
        """Python 2/3 compatibility for iterators"""
        return self.__next__()

    def __next__(self):
        if self._index >= len(self):
            self._index = 0
            raise StopIteration
        item = self._tracks[self._index]
        self._index += 1
        return item

    def __len__(self):
        return len(self._tracks)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._tracks[index]
        elif isinstance(index, slice):
            return self._slice_generator(index)
        else:
            raise TypeError("index must be int or slice")

    def _slice_generator(self, index):
        """A simple slice generator for iterations"""
        start, stop, step = index.indices(len(self))
        for i in range(start, stop, step):
            yield self._tracks[i]

    def __str__(self):
        n_tracks = len(self)
        plural = 's' if n_tracks > 1 or n_tracks == 0 else ''
        return("TrackSeries with {0} track{1}.".format(len(self), plural))

    def __repr__(self):
        return self.__str__()

    def __insp__(self):
        return '\n'.join([str(track) for track in self._tracks])



class Reco(dict):
    """A dictionary with a dtype."""
    def __init__(self, map, dtype, h5loc='/reco'):
        self.dtype = dtype
        self.h5loc = h5loc
        self.update(map)

    def serialise(self, to='numpy'):
        if to == 'numpy':
            return np.array(self.__array__(), dtype=self.dtype)

    def __array__(self):
        return [tuple((self[key] for key in self.dtype.names))]


class ArrayTaco(object):
    def __init__(self, arr, h5loc='/'):
        self.array = arr
        self.h5loc = h5loc

    @classmethod
    def deserialise(cls, data, h5loc='/', event_id=None, fmt='numpy'):
        if fmt == 'numpy':
            return cls(data, h5loc)

    def serialise(self, to='numpy'):
        return self.array

    @property
    def dtype(self):
        return self.array.dtype

    def __len__(self):
        return len(self.array)


deserialise_map = {
    'MCHits': HitSeries,
    'Hits': HitSeries,
    'MCTracks': TrackSeries,
    'EventInfo': EventInfo,
}

