# -*- coding: utf-8 -*-
"""Backwards compatible functions"""
# This is a bit narrow, but fulfills the need right now.
SQLITE_SCHEME = 'file'
POSTGRES_SCHEME = 'postgresql'
ACCEPTED_SCHEMES = (
    SQLITE_SCHEME,
    POSTGRES_SCHEME,
)


def validate_db_uri(uri):
    """Cursory validation of the given ``uri`` for glaring misuse
    This will raise an exception when invalid,
    but also return True when valid.

    """
    if uri is None:
        raise ValueError(
            "You must define the 'BASE_DB_URI' environment variable. "
            "This looks something like 'scheme://[user:pass@](directory-path|host)', "
            'specifically without including the database portion. '
            "For example, 'postgresql://user:pass@db-host'."
        )

    if uri == ':memory:':
        raise ValueError('Unsupported memory URI')

    possible_scheme = uri.split(':', 1)[0]
    if possible_scheme not in ACCEPTED_SCHEMES:
        raise ValueError(f"Invalid scheme '{possible_scheme}' in URI: {uri}")

    return True
