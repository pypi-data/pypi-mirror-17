Flask-ArangoDB
==============

This is Flask extension for integration ArangoDB using `python-arango`_.
It's inspired by `Flask-Arango`_, an extension for the `pyArango`_ library.

.. _python-arango: https://github.com/joowani/python-arango
.. _flask-arango: https://github.com/grucin/flask-arango
.. _pyArango: http://pyarango.tariqdaouda.com/


Usage
-----
Install using pip:

    pip install flask-arangodb


Example
-------

Typical usage looks like this:


.. code-block:: python

    from flask import Flask

    from flask_arangodb import ArangoDB

    # Configuration
    ARANGO_SETTINGS = {'host': 'localhost', 'port': 8529}
    ARANGO_DB = 'mydatabase'

    app = Flask(__name__)
    app.config.from_object(__name__)
    arango = ArangoDB(app)

    @app.route('/')
    def index():
        # refer to python-arango for more information

        # Set up some test data to query against
        arango.db.collection('students').insert_many([
            {'_key': 'Abby', 'age': 22},
            {'_key': 'John', 'age': 18},
            {'_key': 'Mary', 'age': 21}
        ])

        # Execute the query
        cursor = db.aql.execute(
            'FOR s IN students FILTER s.age < @value RETURN s',
            bind_vars={'value': 19}
        )

        # Iterate through the result cursor
        return([student['_key'] for student in cursor])



Links
-----

* [python-arango documentation](http://python-driver-for-arangodb.readthedocs.io/en/master/intro.html)

