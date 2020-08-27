# -*- coding: utf-8 -*-
# flake8: noqa

# BBB (27-Aug-12020) Referenced from a few locations, but no longer necessary
#     with the import of dbapi_integrations in wbia.__init__.
import sqlite3
import sqlite3 as lite

from wbia.dtool import base
from wbia.dtool import sql_control
from wbia.dtool import depcache_control
from wbia.dtool import depcache_table

from wbia.dtool.depcache_control import DependencyCache, make_depcache_decors
from wbia.dtool.base import (
    AlgoResult,
    MatchResult,
    Config,
    VsManySimilarityRequest,
    VsOneSimilarityRequest,
)
from wbia.dtool.depcache_table import ExternalStorageException, ExternType
from wbia.dtool.base import *  # NOQA
from wbia.dtool.sql_control import SQLDatabaseController
from wbia.dtool.types import TYPE_TO_SQLTYPE
