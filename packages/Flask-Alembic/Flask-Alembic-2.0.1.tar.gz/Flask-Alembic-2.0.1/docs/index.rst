Flask-Alembic
=============

Flask-Alembic is a `Flask`_ extension that provides a configurable `Alembic`_ migration environment around a `Flask-SQLAlchemy`_ database.

Installation
------------

Releases are available from the `PyPI project page <release_>`_.  Install with pip::

    pip install Flask-Alembic

The latest code is hosted on `BitBucket <source_>`_.  Install with pip::

    pip install https://bitbucket.org/davidism/flask-alembic/get/tip.zip

.. _Flask: https://palletsprojects.com/p/flask/
.. _Flask-SQLAlchemy: https://flask-sqlalchemy.pocoo.org/
.. _Alembic: http://alembic.zzzcomputing.com/en/latest/
.. _release: https://pypi.python.org/pypi/Flask-Alembic
.. _source: https://bitbucket.org/davidism/flask-alembic

Configuration
-------------

Configuration for Alembic and its migrations is pulled from the following Flask config keys.

*   ``ALEMBIC`` is a dictionary containing general configuration, mostly used by :class:`alembic.config.Config` and :class:`alembic.script.ScriptDirectory`.  See Alembic's docs on `config`_.
*   ``ALEMBIC_CONTEXT`` is a dictionary containing options passed to :class:`alembic.environment.EnvironmentContext` and :class:`alembic.migration.MigrationContext`.  See Alembic's docs on `context`_.

The only required configuration is ``ALEMBIC['script_location']``, which is the location of the migrations directory.  If it is not an absolute path, it will be relative to the instance folder.  This defaults to ``migrations`` relative to the application root.

.. _config: http://alembic.zzzcomputing.com/en/latest/tutorial.html#editing-the-ini-file
.. _context: http://alembic.zzzcomputing.com/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure

Basic Usage
-----------

First, set up your Flask app (or app factory) and the Flask-SQLAlchemy extension and models.

This extension follows the common pattern of Flask extension setup.  Either immediately pass an app to :class:`~flask_alembic.Alembic`, or call :meth:`~flask_alembic.Alembic.init_app` later. ::

    from flask_alembic import Alembic

    alembic = Alembic()
    alembic.init_app(app)  # call in the app factory if you're using that pattern

When an app is registered, :meth:`~flask_alembic.Alembic.mkdir` is called to set up the migrations directory if it does not already exist.  To prevent this, call ``init_app`` with ``run_mkdir=False``.

The ``alembic`` instance provides an interface between the current app and Alembic.  It exposes similar commands to the command line available from Alembic, but Flask-Alembic's methods return data rather than produce output.  You can use this interface to do what the command line commands do, from inside your app. ::

    # generate a new revision
    # same as flask db revision 'made changes'
    alembic.revision('made changes')

    # run all available upgrades
    # same as ./manage.py db upgrade
    alembic.upgrade()

You can also get at the Alembic internals that enable these commands.  See the `Alembic API docs <api_>`_ for more information. ::

    alembic.script.get_revision('head')  # locate a revision by name
    alembic.context.get_current_revision()  # could compare this to the 'head' revision above to see if upgrades are needed
    alembic.op.drop_column('my_table', 'my_column')  # probably don't want to do this outside a revision, but it'll work
    alembic.compare_metadata()  # see that the column you just dropped will be added back next revision

.. _api: http://alembic.zzzcomputing.com/en/latest/api/index.html

Independent Named Branches
--------------------------

Alembic supports `named branches`_, but its syntax is hard to remember and verbose.  Flask-Alembic
makes it easier by providing a central configuration for branch names and revision directories and
simplifying the syntax to the ``revision`` command.

Alembic allows configuration of multiple version locations.  ``version_locations`` is a list of directories to search for migration scripts.  Flask-Alembic extends this to allow tuples as well
as strings in the list.  If a tuple is added, it specifies a ``(branch, directory)`` pair.  The ``script_location`` is automatically given the label ``default`` and added to the ``version_locations``. ::

    ALEMBIC = {
        'version_locations': [
            'other_migrations',  # not a branch, just another search location
            ('posts', '/path/to/posts_extension/migrations'),  # posts branch migrations will be placed here
            ('users', 'users/migrations'),  # relative paths are relative to the application root
        ]
    }

The ``revision`` command takes a ``--branch`` option (defaults to ``default``).  This takes the place
of specifying ``--parent``, ``--label``, and ``--path``.  This will automatically start the branch from the base revision, label the revision correctly, and place the revisions in the correct location. ::

    flask db revision --branch users 'create user model'
    # equivalent to (if branch is new)
    # alembic revision --autogenerate --head base --branch-label users --version-path users/migrations -m 'create user model'
    # or (if branch exists)
    # alembic revision --autogenerate --head users@head -m 'create user model'

.. _named branches: http://alembic.zzzcomputing.com/en/latest/branches.html#working-with-multiple-bases

Command Line
------------

Currently, `Click`_ and `Flask-Script`_ are supported.  The commands are the same for either one.

If you are using Flask 0.11, the preferred interface is Click.  If you are using Flask 0.10, you can use backported integration via `Flask-CLI`_.
Flask-Alembic will automatically add the command to the cli if it detects that Click is available. ::

    flask db --help

If you have set up a :class:`flask_script.Manager` for your project using Flask-Script, you can add Alembic commands like this::

    from flask_alembic import alembic_script
    app_manager.add_command('db', alembic_manager)

::

    python manage.py db

.. _Flask-Script: https://flask-script.readthedocs.io/en/latest/
.. _Click: https://palletsprojects.com/p/click/
.. _Flask-CLI: https://flask-cli.readthedocs.io/en/latest/

Differences from Alembic
------------------------

Flask-Alembic is opinionated and was designed to enable specific workflows.  If you're looking for a more direct wrapper
around Alembic, you may be interested in `Flask-Migrate`_ instead.

* Configuration is taken from ``Flask.config`` instead of ``alembic.ini`` and ``env.py``.
* The migrations are stored directly in the migrations folder instead of the versions folder.
* Provides the migration environment instead of ``env.py`` and exposes Alembic's internal API objects.
* Differentiates between CLI commands and Python functions.  The functions return revision objects and don't print to stdout.
* Allows operating Alembic at any API level while the app is running, through the exposed objects and functions.
* Does not (currently) support offline migrations.  I don't plan to add this but am open to patches.
* Does not (currently) support multiple databases.  I plan on adding support for Flask-SQLAlchemy binds and external bases eventually, or am open to patches.
* Adds a system for managing independent migration branches and makes it easier to work with named branches.

.. _Flask-Migrate: https://flask-migrate.readthedocs.io

API Reference
-------------

.. automodule:: flask_alembic
