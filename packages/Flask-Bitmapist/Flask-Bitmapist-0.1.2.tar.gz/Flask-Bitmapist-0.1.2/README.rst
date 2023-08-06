===============
Flask-Bitmapist
===============

.. image:: https://travis-ci.org/cuttlesoft/flask-bitmapist.svg?branch=master
	:target: https://travis-ci.org/cuttlesoft/flask-bitmapist

.. image:: https://coveralls.io/repos/github/cuttlesoft/flask-bitmapist/badge.svg?branch=master
	:target: https://coveralls.io/github/cuttlesoft/flask-bitmapist?branch=master

Flask extension that creates a simple interface to the Bitmapist analytics library.


About
-----

`Bitmapist <https://github.com/Doist/bitmapist>`_ is:

    [A] Python library [that] makes it possible to implement real-time, highly scalable analytics that can answer the following questions:

    - Has user 123 been online today? This week? This month?
    - Has user 123 performed action "X"?
    - How many users have been active this month? This hour?
    - How many unique users have performed action "X" this week?
    - What % of users that were active last week are still active?
    - What % of users that were active last month are still active this month?
    - Which users performed action "X"?


Installation
------------

::

    $ pip install flask-bitmapist


Usage
-----

Example app:

.. code-block:: python

    from flask import Flask
    from flask_bitmapist import FlaskBitmapist, mark

    app = Flask(__name__)

    flaskbitmapist = FlaskBitmapist()
    flaskbitmapist.init_app(app)

    @app.route('/')
    @mark('index:visited', 1)  # current_user.id
    def index():
        """using the mark decorator, the first argument is the event
           and the second is the id of the current_user
        """
        return 'Hello, world!'

    if __name__ == '__main__':
        app.run()


For documentation on the ``mark`` decorator, look at the ``mark_event`` `Bitmapist function <https://github.com/Doist/bitmapist#examples>`_.


Config
------

=============================== =========== ======================================================================
Name                            Type        Description
=============================== =========== ======================================================================
``BITMAPIST_REDIS_SYSTEM``      ``string``  Name of Redis System; defaults to ``default``
``BITMAPIST_REDIS_URL``         ``string``  URL to connect to Redis server; defaults to ``redis://localhost:6379``
``BITMAPIST_TRACK_HOURLY``      ``boolean`` Tells Bitmapist to track hourly; can also be passed to ``mark`` (e.g., ``@mark('active', 1, track_hourly=False)``)

``BITMAPIST_DISABLE_BLUEPRINT`` ``boolean`` Disables registration of default Bitmapist Blueprint
=============================== =========== ======================================================================


Cohort Blueprint
----------------

One of the nice things about Bitmapist is its simple bit operations API and the data cohort that you get.
For more information about the cohort, visit the `Bitmapist README <https://github.com/Doist/bitmapist#bitmapist-cohort>`_.

When you initialize the ``flask-bitmapist`` extension, a blueprint is registered with the application.

======== ===================== ============================================
Name     Path                  Description
======== ===================== ============================================
`index`  ``/bitmapist/``       Default Bitmapist index
`cohort` ``/bitmapist/cohort`` Demo cohort retrieval and heatmap generation
======== ===================== ============================================


Tests
-----

To run the tests, ensure that you have Redis running on port 6399::

    $ redis-server --port 6399


Then you can simply run::

    $ python setup.py test


To seed fake data for testing, run::

    $ python scripts/seed.py


Documentation
-------------

The full Flask-Bitmapist documentation is available at `ReadTheDocs <http://flask-bitmapist.readthedocs.io/en/latest/>`_.


Contributing
------------

If you're interested in contributing to Flask-Bitmapist, get started by creating an issue `here <https://github.com/cuttlesoft/flask-bitmapist/issues>`_. Thanks!
