# -*- coding: utf-8 -*-
"""
A space to integrate the various (e.g. sqlite3 & psycopg2) DBAPI implementations
with this project's custom types.

"""
from .sqlite3 import integrate as sqlite3_integrate

# TODO (27-Aug-12020) integrate psycopg2
# from .psycopg2 import integrate as psycopg2_integrate


__all__ = ('integrate',)


def integrate():
    """Include logic necessary to integrate the various DBAPIs"""
    sqlite3_integrate()
    # psycopg2_integrate()
