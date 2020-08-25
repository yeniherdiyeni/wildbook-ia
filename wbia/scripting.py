# -*- coding: utf-8 -*-
"""
Bootstrapping functionality for commandline invocation
"""
import logging
import multiprocessing
import signal
import sys

import utool as ut
from deprecated import deprecated

from wbia import params


__all__ = ('prepare',)


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


@deprecated('use wbia.scripting.prepare')
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


def prepare(settings=None, controller=None):
    """
    Initializes the Controller (heart of the application) for use
    in a scripted setting. This returns a dictionary of locals
    including a controller object, settings data and closer function.

    The closer function should be used at the end of your script
    for data safety. Tip, use this function as a context-manager
    to automatically call the closer.

    This function places the settings and controller on the thread-local stack.
    You can access the data from anywhere in your program,
    because the variables are essentially global.

    Args:
        settings (dict): (not yet implemented) function signature placeholder
        controller (Controller): an instantiated controller object

    Returns:
        dict: locals to be used within a scripting setting
    """
    # TODO (24-Aug-12020) consume necessary bits of logic from 'preload'
    preload()

    # Discover settings and configuration
    # if not settings:
    #     settings = discover_settings()

    # Build the controller
    # TODO (18-Aug-12020) Initialize the controller even though None will be a valid option.
    if controller is None:
        raise NotImplementedError('At this time you must initialize the controller')

    def closer():  # pragma: no cover
        controller.close()

    # Push the controller onto the threadlocal stack
    locals_ = {'controller': controller, 'settings': settings}

    # Prepare the locals for return
    return AppContext(closer=closer, **locals_)


class AppContext(dict):
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        getattr(self, 'closer', lambda: None)()
