# -*- coding: utf-8 -*-
"""
Runtime configuration definition and discovery
----------------------------------------------

The application is configured via environment variables.
The following application settings are mapped to environment variables.

===============================  ======================  =============
Setting                          Env Variable            Required?
===============================  ======================  =============
``db.runtime.url``               ``DB_URL``              yes
``db.readonly.url``              ``DB_READONLY_URL``     no
``db.super.url``                 ``DB_SUPER_URL``        no
``data.location``                ``DATA_LOCATION``       yes
===============================  ======================  =============

The ``db.runtime.url`` is a required setting that specifies
where the DB is located (e.g. ``:memory:``, ``file:///var/wbia/data``,
``postgres://wbia:wbia@db/wbia``).

The ``db.readonly.url`` is a specific URL
that supports read-only access
to the database.
This optional setting defaults to the value of ``db.runtime.url``.

The ``db.super.url`` is a specific URL
that supports super user (i.e. managing database role) access
to the database.
This optional setting defaults to the value of ``db.runtime.url``.

The ``data.location`` setting specifies where variable data should be stored.
This would be thought of as ``/var`` would in the operating system,
where changing data is located.

The settings are programattically obtained via
:func:`wbia.config.discover_settings`.

.. note: It's out of scope
   for this logic to handle the usage details around these settings.
   For example, no checks are done to ensure the ``db.super.url`` value
   uses a super user role.
   Another example, this code does not concern itself
   about the use of ``:memory:``;
   this kind of concern would be handled within the connection factory logic.

"""
import os


__all__ = (
    'discover_settings',
)


def discover_settings(settings: dict = {}):
    """Discovers settings from environment variables"""
    # Retrieve the required url setting first, so that it can later be used
    # as the default for the optional urls.
    default_url = settings.get('db.runtime.url', os.environ.get('DB_URL'))
    if default_url is None:
        raise RuntimeError("'DB_URL' environment variable "
                           "OR the 'db.runtime.url' setting MUST "
                           "be defined")

    # Retrieve the required data location
    data_location = settings.get('data.location', os.environ.get('DATA_LOCATION'))
    if data_location is None:
        raise RuntimeError("'DATA_LOCATION' environment variable "
                           "OR the 'data.location' setting MUST "
                           "be defined")

    # Set remaining db urls, defaulting to the runtime url when not present.
    readonly_url = os.environ.get('DB_READONLY_URL', default_url)
    super_url = os.environ.get('DB_SUPER_URL', default_url)

    new_settings = {
        'data.location': data_location,
        'db.runtime.url': default_url,
        'db.readonly.url': readonly_url,
        'db.super.url': super_url,
    }

    # Only amend the existing settings by setting the default.
    for k, v in new_settings.items():
        settings.setdefault(k, v)
    return settings
