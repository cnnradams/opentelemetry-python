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
The integration with PyMySQL supports the `PyMySQL`_ library and can be enabled
by using ``PyMySQLInstrumentor``.

.. _PyMySQL: https://pypi.org/project/PyMySQL/

Usage
-----

.. code:: python

    import pymysql
    from opentelemetry import trace
    from opentelemetry.ext.pymysql import PyMySQLInstrumentor
    from opentelemetry.sdk.trace import TracerProvider

    trace.set_tracer_provider(TracerProvider())

    PyMySQLInstrumentor().instrument()

    cnx = pymysql.connect(database="MySQL_Database")
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO test (testField) VALUES (123)"
    cnx.commit()
    cursor.close()
    cnx.close()

API
---
"""

import typing

import pymysql

from opentelemetry.ext.dbapi import DatabaseApiInstrumentor
from opentelemetry.ext.pymysql.version import __version__
from opentelemetry.trace import TracerProvider, get_tracer


class PyMySQLInstrumentor(DatabaseApiInstrumentor):
    _CONNECTION_ATTRIBUTES = {
        "database": "db",
        "port": "port",
        "host": "host",
        "user": "user",
    }

    _DATABASE_COMPONENT = "mysql"
    _DATABASE_TYPE = "sql"

    def __new__(cls):
        return super().__new__(
            cls,
            pymysql,
            "connect",
            cls._DATABASE_COMPONENT,
            cls._DATABASE_TYPE,
            cls._CONNECTION_ATTRIBUTES,
            __name__,
            __version__
        )
