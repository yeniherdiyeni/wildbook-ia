# -*- coding: utf-8 -*-
import logging
import multiprocessing
import signal
import sys

import utool as ut

from wbia import params


logger = logging.getLogger('wbia')


def _on_ctrl_c(signal, frame):
    proc_name = multiprocessing.current_process().name
    logger.info('Caught ctrl+c in %s' % (proc_name,))
    sys.exit(0)


def _init_signals():
    signal.signal(signal.SIGINT, _on_ctrl_c)


def _reset_signals():
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # reset ctrl+c behavior


def _configure_matplotlib():
    from wbia.plottool import __MPL_INIT__

    __MPL_INIT__.init_matplotlib()


def _configure_parallel():
    """configure parallel processes"""
    from utool import util_parallel

    params.parse_args()

    # Import any modules which parallel process will use here
    # so they are accessable when the program forks
    from wbia import core_annots  # NOQA

    util_parallel.set_num_procs(params.args.num_procs)


def _configure_numpy():
    """numpy print settings"""
    import numpy as np

    error_options = ['ignore', 'warn', 'raise', 'call', 'print', 'log']
    on_err = error_options[0]
    # np.seterr(divide='ignore', invalid='ignore')
    numpy_err = {
        'divide': on_err,
        'over': on_err,
        'under': on_err,
        'invalid': on_err,
    }
    # numpy_print = {
    #    'precision': 8,
    #    'threshold': 500,
    #    'edgeitems': 3,
    #    'linewidth': 200,  # default 75
    #    'suppress': False,
    #    'nanstr': 'nan',
    #    'formatter': None,
    # }
    np.seterr(**numpy_err)
    # np.set_printoptions(**numpy_print)


def preload():
    """ Sets up python environment """
    # ??? (24-Aug-12020) Unsure when this would actually occur
    if multiprocessing.current_process().name != 'MainProcess':
        return

    params.parse_args()

    _configure_matplotlib()
    _configure_numpy()
    _configure_parallel()
    _init_signals()  # for ctrl+c

    # inject colored exceptions
    ut.util_inject.inject_colored_exceptions()
