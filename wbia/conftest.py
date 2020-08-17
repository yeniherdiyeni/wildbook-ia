# -*- coding: utf-8 -*-
# See also conftest.py documentation at https://docs.pytest.org/en/stable/fixture.html#conftest-py-sharing-fixture-functions
"""This module is implicitly used by ``pytest`` to load testing configuration and fixtures."""
import os
from pathlib import Path

import pytest

from wbia.init.sysres import (
    ensure_nauts,
    ensure_pz_mtest,
    ensure_testdb2,
    ensure_wilddogs,
)
from wbia.tests.reset_testdbs import (
    TEST_DBNAMES_MAP,
    delete_dbdir,
    ensure_smaller_testingdbs,
)
from wbia.scripting import prepare


@pytest.fixture
def enable_wildbook_signal():
    """This sets the ``ENABLE_WILDBOOK_SIGNAL`` to False"""
    # TODO (16-Jul-12020) Document ENABLE_WILDBOOK_SIGNAL
    # ??? what is ENABLE_WILDBOOK_SIGNAL used for?
    import wbia

    setattr(wbia, 'ENABLE_WILDBOOK_SIGNAL', False)


@pytest.fixture(scope='session', autouse=True)
@pytest.mark.usefixtures('enable_wildbook_signal')
def set_up_db(request, tmp_path_factory):
    """
    Sets up the testing databases.
    This fixture is set to run automatically any any test run of wbia.

    """
    # Prepare the testing environment
    testing_loc = tmp_path_factory.mktemp('var')
    default_db_url = f"file://{testing_loc}/db"
    test_settings = {
        'data.location': testing_loc,
        'db.runtime.url': os.getenv('TESTING_DB_URL', default_db_url),
    }
    # Lead off with preparing the controller, which requires database info
    # because the application is database focused.
    prepare(test_settings)

    # If selected, disable running the main logic of this fixture
    if request.config.getoption("--disable-refresh-db", False):
        # Assume the user knows what they are requesting
        return  # bale out

    # Delete DBs, if they exist
    # FIXME (16-Jul-12020) this fixture does not cleanup after itself to preserve exiting usage behavior
    for dbname in TEST_DBNAMES_MAP.values():
        delete_dbdir(dbname)

    # Set up DBs
    ensure_smaller_testingdbs()
    ensure_pz_mtest()
    ensure_nauts()
    ensure_wilddogs()
    ensure_testdb2()


@pytest.fixture(scope='session')
def xdoctest_namespace(set_up_db):
    """
    Inject names into the xdoctest namespace.
    """
    return dict()
