# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
SQLite instrumentation supporting `sqlite3`_, it can be enabled by
using ``SQLite3Instrumentor``.

.. _sqlite3: https://docs.python.org/3/library/sqlite3.html

Usage
-----

.. code:: python

    import sqlite3
    from opentelemetry import trace
    from opentelemetry.trace import TracerProvider
    from opentelemetry.ext.sqlite3 import SQLite3Instrumentor

    trace.set_tracer_provider(TracerProvider())

    SQLite3Instrumentor().instrument()

    cnx = sqlite3.connect('example.db')
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO test (testField) VALUES (123)"
    cursor.close()
    cnx.close()

API
---
"""

import typing

import sqlite3

from opentelemetry.auto_instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.ext import dbapi
from opentelemetry.ext.dbapi import DatabaseApiInstrumentor
from opentelemetry.ext.sqlite3.version import __version__
from opentelemetry.trace import TracerProvider, get_tracer


class SQLite3Instrumentor(DatabaseApiInstrumentor):
    # There are no useful retrievable attributes of sqlite's connection,
    # not even the name of the database being used
    _CONNECTION_ATTRIBUTES = {}

    _DATABASE_COMPONENT = "sqlite3"
    _DATABASE_TYPE = "sql"

    def __new__(cls):
        return super().__new__(
            cls,
            sqlite3,
            "connect",
            cls._DATABASE_COMPONENT,
            cls._DATABASE_TYPE,
            cls._CONNECTION_ATTRIBUTES,
            __name__,
            __version__
            )
