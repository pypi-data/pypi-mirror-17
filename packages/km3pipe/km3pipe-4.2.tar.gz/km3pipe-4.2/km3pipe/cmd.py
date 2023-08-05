# coding=utf-8
# Filename: cmd.py
"""
KM3Pipe command line utility.

Usage:
    km3pipe test
    km3pipe update [GIT_BRANCH]
    km3pipe detx DET_ID [-m] [-t T0_SET] [-c CALIBR_ID]
    km3pipe tohdf5 FILE [-o OUTFILE] [-n EVENTS] [-j]
    km3pipe hdf2root FILE [-o OUTFILE] [-n EVENTS]
    km3pipe runtable [-n RUNS] [-s REGEX] DET_ID
    km3pipe runinfo DET_ID RUN
    km3pipe (-h | --help)
    km3pipe --version

Options:
    -h --help       Show this screen.
    -m              Get the MC detector file (flips the sign of the DET_ID).
    -c CALIBR_ID    Geometrical calibration ID (eg. A01466417)
    -t T0_SET       Time calibration ID (eg. A01466431)
    -n EVENTS/RUNS  Number of events/runs.
    -o OUTFILE      Output file.
    -j --jppy       Use jppy (not aanet) for Jpp readout
    -s REGEX        Regular expression to filter the runsetup name/id.
    DET_ID          Detector ID (eg. D_ARCA001).
    GIT_BRANCH      Git branch to pull (eg. develop).
    RUN             Run number.

"""

from __future__ import division, absolute_import, print_function

import sys
import os
from datetime import datetime

from km3pipe import version
from km3pipe.db import DBManager
from km3modules import StatusBar
from km3pipe.hardware import Detector

__author__ = "Tamas Gal"
__copyright__ = "Copyright 2016, Tamas Gal and the KM3NeT collaboration."
__credits__ = []
__license__ = "MIT"
__maintainer__ = "Tamas Gal and Moritz Lotze"
__email__ = "tgal@km3net.de"
__status__ = "Development"


def run_tests():
    import pytest
    import km3pipe
    pytest.main([os.path.dirname(km3pipe.__file__)])


def tohdf5(input_file, output_file, n_events, use_jppy=False):
    """Convert Any file to HDF5 file"""
    from km3pipe import Pipeline  # noqa
    from km3pipe.io import GenericPump, HDF5Sink  # noqa

    pipe = Pipeline()
    pipe.attach(GenericPump, filename=input_file, use_jppy=use_jppy)
    pipe.attach(StatusBar, every=1000)
    pipe.attach(HDF5Sink, filename=output_file)
    pipe.drain(n_events)


def hdf2root(infile, outfile):
    from rootpy.io import root_open
    from rootpy import asrootpy
    from root_numpy import array2tree
    from tables import open_file

    h5 = open_file(infile, 'r')
    rf = root_open(outfile, 'recreate')

    # 'walk_nodes' does not allow to check if is a group or leaf
    #   exception handling is bugged
    #   introspection/typecheck is buged
    # => this moronic nested loop instead of simple `walk`
    for group in h5.walk_groups():
        for leafname, leaf in group._v_leaves.items():
            tree = asrootpy(array2tree(leaf[:], name=leaf._v_pathname))
            tree.write()
    rf.close()
    h5.close()


def runtable(det_id, n=5, sep='\t', regex=None):
    """Print the run table of the last `n` runs for given detector"""
    db = DBManager()
    df = db.run_table(det_id)

    if regex is not None:
        df = df[df['RUNSETUPNAME'].str.match(regex) |
                df['RUNSETUPID'].str.match(regex)]

    if n is not None:
        df = df.tail(n)

    df.to_csv(sys.stdout, sep=sep)


def runinfo(run_id, det_id):
    db = DBManager()
    df = db.run_table(det_id)
    row = df[df['RUN'] == int(run_id)]
    if len(row) == 0:
        print("No database entry for run {0} found.".format(run_id))
        return
    next_row = df[df['RUN'] == (int(run_id) + 1)]
    if len(next_row) != 0:
        end_time = next_row['DATETIME'].values[0]
        duration = (next_row['UNIXSTARTTIME'].values[0] -
                    row['UNIXSTARTTIME'].values[0]) / 1000 / 60
    else:
        end_time = duration = float('NaN')
    print("Run {0} - detector ID: {1}".format(run_id, det_id))
    print('-' * 42)
    print("  Start time:         {0}\n"
          "  End time:           {1}\n"
          "  Duration [min]:     {2:.2f}\n"
          "  Start time defined: {3}\n"
          "  Runsetup ID:        {4}\n"
          "  Runsetup name:      {5}\n"
          "  T0 Calibration ID:  {6}\n"
          .format(row['DATETIME'].values[0],
                  end_time,
                  duration,
                  bool(row['STARTTIME_DEFINED'].values[0]),
                  row['RUNSETUPID'].values[0],
                  row['RUNSETUPNAME'].values[0],
                  row['T0_CALIBSETID'].values[0]))


def update_km3pipe(git_branch):
    if git_branch == '' or git_branch is None:
        git_branch = 'master'
    os.system("pip install -U git+http://git.km3net.de/tgal/km3pipe.git@{0}"
              .format(git_branch))


def detx(det_id, calibration, t0set):
    now = datetime.now()
    filename = "KM3NeT_{0}{1:08d}_{2}.detx" \
               .format('-' if det_id < 0 else '', abs(det_id),
                       now.strftime("%d%m%Y"))
    det = Detector(det_id=det_id, t0set=t0set, calibration=calibration)
    if det.n_doms > 0:
        det.write(filename)


def main():
    from docopt import docopt
    args = docopt(__doc__, version=version)

    try:
        n = int(args['-n'])
    except TypeError:
        n = None

    if args['test']:
        run_tests()

    if args['update']:
        update_km3pipe(args['GIT_BRANCH'])

    if args['tohdf5']:
        infile = args['FILE']
        outfile = args['-o'] or infile + '.h5'
        use_jppy = args['--jppy']
        tohdf5(infile, outfile, n, use_jppy)

    if args['hdf2root']:
        infile = args['FILE']
        outfile = args['-o'] or infile + '.root'
        hdf2root(infile, outfile)

    if args['runtable']:
        runtable(args['DET_ID'], n, regex=args['-s'])

    if args['runinfo']:
        runinfo(args['RUN'], args['DET_ID'])

    if args['detx']:
        t0set = args['-t']
        calibration = args['-c']
        det_id = int(('-' if args['-m'] else '') + args['DET_ID'])
        detx(det_id, calibration, t0set)
