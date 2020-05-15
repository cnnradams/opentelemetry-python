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
The integration with PostgreSQL supports the `Psycopg`_ library, it can be enabled by
using ``Psycopg2Instrumentor``.

.. _Psycopg: http://initd.org/psycopg/

Usage
-----

.. code-block:: python

    import psycopg2
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.trace.ext.psycopg2 import Psycopg2Instrumentor

    trace.set_tracer_provider(TracerProvider())

    Psycopg2Instrumentor().instrument()

    cnx = psycopg2.connect(database='Database')
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO test (testField) VALUES (123)")
    cursor.close()
    cnx.close()

API
---
"""

import typing

import psycopg2
import wrapt

from opentelemetry.ext.dbapi import DatabaseApiInstrumentor
from opentelemetry.ext.psycopg2.version import __version__
from opentelemetry.trace import TracerProvider, get_tracer


class Psycopg2Instrumentor(DatabaseApiInstrumentor):
    _CONNECTION_ATTRIBUTES = {
        "database": "info.dbname",
        "port": "info.port",
        "host": "info.host",
        "user": "info.user",
    }

    _DATABASE_COMPONENT = "postgresql"
    _DATABASE_TYPE = "sql"

    def __new__(cls):
        return super().__new__(
            cls,
            psycopg2,
            "connect",
            cls._DATABASE_COMPONENT,
            cls._DATABASE_TYPE,
            cls._CONNECTION_ATTRIBUTES,
            __name__,
            __version__
        )
