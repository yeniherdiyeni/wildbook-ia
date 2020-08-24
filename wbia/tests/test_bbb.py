# -*- coding: utf-8 -*-
import pytest

from wbia.bbb import validate_db_uri


class TestURIValidation:
    def test_missing(self):
        uri = None
        with pytest.raises(ValueError):
            validate_db_uri(uri)

    def test_memory_uri(self):
        uri = ':memory:'
        with pytest.raises(ValueError):
            validate_db_uri(uri)

    def test_no_scheme(self):
        uri = '/foo/bar'
        with pytest.raises(ValueError):
            validate_db_uri(uri)

    def test_sqlite_file_uri(self):
        uri = 'file:///foo/bar'
        assert validate_db_uri(uri)

    def test_postgres_uri(self):
        uri = 'postgresql://user:pass@db'
        assert validate_db_uri(uri)
