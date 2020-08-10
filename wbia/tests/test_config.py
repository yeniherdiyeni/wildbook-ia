# -*- coding: utf-8 -*-
from wbia.config import discover_settings


def test_success_from_env(monkeypatch):
    # Assign the base minimum set of environment variables
    data_location = '<path>'
    monkeypatch.setenv('DATA_LOCATION', data_location)
    db_uri = '<uri>'
    monkeypatch.setenv('DB_URI', db_uri)

    # Discover the settings from the environment variables
    settings = discover_settings()

    expected_db_settings = {
        'db.runtime.uri': db_uri,
        'db.readonly.uri': db_uri,
        'db.super.uri': db_uri,
    }
    db_settings = {k: v for k, v in settings.items() if k.startswith('db')}
    assert db_settings == expected_db_settings
    assert settings.get('data.location') == data_location


def test_success_from_settings():
    data_location = '<path>'
    db_uri = '<uri>'

    upstream_settings = {
        'data.location': data_location,
        'db.runtime.uri': db_uri,
    }

    # Discover the settings from upstream
    settings = discover_settings(upstream_settings)

    expected_db_settings = {
        'db.runtime.uri': db_uri,
        'db.readonly.uri': db_uri,
        'db.super.uri': db_uri,
    }
    db_settings = {k: v for k, v in settings.items() if k.startswith('db')}
    assert db_settings == expected_db_settings
    assert settings.get('data.location') == data_location


def test_success_from_mixed_inputs(monkeypatch):
    # Input from both upstream_settings and environment variables
    # The preference is to use upstream settings over environment variables
    data_location = '<path>'
    db_uri = '<uri>'

    monkeypatch.setenv('DATA_LOCATION', 'env-' + data_location)
    monkeypatch.setenv('DB_URI', 'env-' + db_uri)

    upstream_settings = {
        'data.location': data_location,
        'db.runtime.uri': db_uri,
    }

    # Discover the settings from both upstream and environment
    settings = discover_settings(upstream_settings)

    expected_db_settings = {
        'db.runtime.uri': db_uri,
        'db.readonly.uri': db_uri,
        'db.super.uri': db_uri,
    }
    db_settings = {k: v for k, v in settings.items() if k.startswith('db')}
    assert db_settings == expected_db_settings
    assert settings.get('data.location') == data_location
