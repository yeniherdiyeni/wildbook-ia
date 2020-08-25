#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Runs IBIES gui
"""
import logging
import multiprocessing
import utool as ut
import ubelt as ub
import sys

from wbia.dev import devmain
from wbia.entry_points import main
from wbia.scripts.rsync_wbiadb import rsync_ibsdb_main


(print, rrr, profile) = ut.inject2(__name__)
logger = logging.getLogger('wbia')

CMD = ub.argflag('--cmd')


# FIXME (27-Jul-12020) This is currently used by CI to verify installation.
#       Either make this the main function or move to location that makes sense.
def smoke_test():  # nocover
    import wbia

    logger.info('Looks like the imports worked')
    logger.info('wbia = {!r}'.format(wbia))
    logger.info('wbia.__file__ = {!r}'.format(wbia.__file__))
    logger.info('wbia.__version__ = {!r}'.format(wbia.__version__))


def run_wbia():
    r"""
    CommandLine:
        python -m wbia
        python -m wbia find_installed_tomcat
        python -m wbia get_annot_groundtruth:1
    """
    import wbia  # NOQA

    cmdline_varags = ut.get_cmdline_varargs()
    if len(cmdline_varags) > 0 and cmdline_varags[0] == 'rsync':
        rsync_ibsdb_main()
        sys.exit(0)

    if ub.argflag('--devcmd'):
        # Hack to let devs mess around when using an installer version
        # TODO: add more hacks
        ut.embed()

    if ub.argflag('-e'):
        """
        wbia -e print -a default -t default
        """
        # Run dev script if -e given

        devmain()
        logger.info('... exiting')
        sys.exit(0)

    main_locals = main()  # noqa
    # FIXME (24-Aug-12020) Repurpose this function for use in starting the main process.
    return


if __name__ == '__main__':
    multiprocessing.freeze_support()  # for win32
    run_wbia()
