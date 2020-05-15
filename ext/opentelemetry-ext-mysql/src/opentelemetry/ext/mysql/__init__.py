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
MySQL instrumentation supporting `mysql-connector`_, it can be enabled by
using ``MySQLInstrumentor``.

.. _mysql-connector: https://pypi.org/project/mysql-connector/

Usage
-----

.. code:: python

    import mysql.connector
    from opentelemetry import trace
    from opentelemetry.trace import TracerProvider
    from opentelemetry.ext.mysql import MySQLInstrumentor

    trace.set_tracer_provider(TracerProvider())

    MySQLInstrumentor().instrument()

    cnx = mysql.connector.connect(database="MySQL_Database")
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO test (testField) VALUES (123)"
    cursor.close()
    cnx.close()

API
---
"""

import typing

import mysql.connector

from opentelemetry.ext.dbapi import DatabaseApiInstrumentor
from opentelemetry.ext.mysql.version import __version__
from opentelemetry.trace import TracerProvider, get_tracer


class MySQLInstrumentor(DatabaseApiInstrumentor):
    _CONNECTION_ATTRIBUTES = {
        "database": "database",
        "port": "server_port",
        "host": "server_host",
        "user": "user",
    }

    _DATABASE_COMPONENT = "mysql"
    _DATABASE_TYPE = "sql"

    def __new__(cls):
        return super().__new__(
            cls,
            mysql.connector,
            "connect",
            cls._DATABASE_COMPONENT,
            cls._DATABASE_TYPE,
            cls._CONNECTION_ATTRIBUTES,
            __name__,
            __version__
        )
