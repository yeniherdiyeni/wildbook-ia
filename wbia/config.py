# -*- coding: utf-8 -*-
"""
Runtime configuration definition and discovery
----------------------------------------------

The application is configured via environment variables.
The following application settings are mapped to environment variables.

===============================  ======================  =============
Setting                          Env Variable            Required?
===============================  ======================  =============
``db.runtime.uri``               ``DB_URI``              yes
``db.readonly.uri``              ``DB_READONLY_URI``     no
``db.super.uri``                 ``DB_SUPER_URI``        no
``data.location``                ``DATA_LOCATION``       yes
===============================  ======================  =============

The ``db.runtime.uri`` is a required setting that specifies
where the DB is located (e.g. ``:memory:``, ``file:///var/wbia/data``,
``postgres://wbia:wbia@db/wbia``).

The ``db.readonly.uri`` is a specific URI
that supports read-only access
to the database.
This optional setting defaults to the value of ``db.runtime.uri``.

The ``db.super.uri`` is a specific URI
that supports super user (i.e. managing database role) access
to the database.
This optional setting defaults to the value of ``db.runtime.uri``.

The ``data.location`` setting specifies where variable data should be stored.
This would be thought of as ``/var`` would in the operating system,
where changing data is located.

The settings are programattically obtained via
:func:`wbia.config.discover_settings`.

.. note: It's out of scope
   for this logic to handle the usage details around these settings.
   For example, no checks are done to ensure the ``db.super.uri`` value
   uses a super user role.
   Another example, this code does not concern itself
   about the use of ``:memory:``;
   this kind of concern would be handled within the connection factory logic.

"""
import os


__all__ = ('discover_settings',)


def discover_settings(settings: dict = {}):
    """Discovers settings from environment variables"""
    # Retrieve the required uri setting first, so that it can later be used
    # as the default for the optional uris.
    default_uri = settings.get('db.runtime.uri', os.environ.get('DB_URI'))
    if default_uri is None:
        raise RuntimeError(
            "'DB_URI' environment variable "
            "OR the 'db.runtime.uri' setting MUST "
            'be defined'
        )

    # Retrieve the required data location
    data_location = settings.get('data.location', os.environ.get('DATA_LOCATION'))
    if data_location is None:
        raise RuntimeError(
            "'DATA_LOCATION' environment variable "
            "OR the 'data.location' setting MUST "
            'be defined'
        )

    # Set remaining db uris, defaulting to the runtime uri when not present.
    readonly_uri = os.environ.get('DB_READONLY_URI', default_uri)
    super_uri = os.environ.get('DB_SUPER_URI', default_uri)

    new_settings = {
        'data.location': data_location,
        'db.runtime.uri': default_uri,
        'db.readonly.uri': readonly_uri,
        'db.super.uri': super_uri,
    }

    # Only amend the existing settings by setting the default.
    for k, v in new_settings.items():
        settings.setdefault(k, v)
    return settings
