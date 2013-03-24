.. _installation:

Install Terminator
==================

Want to try Terminator? This guide will guide you through installing Terminator
and its requirements.

Before proceeding, consider installing these first:

- At least Python 2.6
- `python-pip <http://www.pip-installer.org/>`_ installer
- `git <http://http://git-scm.com/>`_ distributed version control system
- A database management system like PostgreSQL or MySQL
- The Python bindings for the installed database management system
- Optionally a mail server


.. _installation#installing:

Local installation
++++++++++++++++++

In order to install Terminator run the following commands:

.. code-block:: bash

    $ sudo pip install virtualenvwrapper
    $ mkvirtualenv <env-name>
    (env-name) $ git clone https://github.com/translate/terminator.git
    (env-name) $ cd terminator
    (env-name) $ pip install -r requirements/base.txt


.. _installation#creating_a_database:

Creating a Database
-------------------

It is necessary to create a database to store all Terminator data. This
**database must be UTF-8 encoded**. You can give it any name. How to create
that database is out of this documents scope, so please refer to your database
documentation.

.. warning:: This database must be UTF-8 encoded.


.. _installation#initializing_the_configuration:

Customizing the Configuration
-----------------------------

The initial configuration includes settings that most likely you are going to
change, for example you must change the `DATABASES` setting to match your
database settings (database engine, database name, database user,...), or
change the `DEBUG`, `SECRET_KEY`, `TIME_ZONE`, `EMAIL_PORT` or `ADMINS`
settings.

.. note:: If you are going to use a mail server perhaps you will have to
   customize other Django settings not included in Terminator configuration. If
   this is the case then just add those settings to Django configuration file.


.. _installation#setting_up_the_database:

Setting Up the Database
-----------------------

Before your run Terminator for the first time, you need to create the schema
for the database and populate it with initial data. This is done by
executing the `syncdb` management command:

.. code-block:: bash

    (env-name) $ cd project
    (env-name) $ python manage.py syncdb --noinput


.. _installation#running_terminator:

Running Terminator
------------------

To run it, just issue:

.. code-block:: bash

    (env-name) $ python manage.py runserver

And the server will start listening on port 8000. This can be accessed from your
web browser at ``http://localhost:8000/``.


This default installation already provides several default user accounts with
different roles:

- User **usuario** with password *usuario* (has superuser role)
- User **dono** with password *dono*
- User **lexi** with password *lexi*
- User **term** with password *term*

If you want to try the import feature you have to use the `usuario` user
account. You may test it using TBX files like the ones provided by
`Proxecto Trasno <http://www.trasno.net/content/resultados-das-trasnadas#glosarios-tbx>`_.


.. _installation#deploying_terminator:

Deploying Terminator using a Web Server
+++++++++++++++++++++++++++++++++++++++

If you want to deploy Terminator using a web server like Apache, please refer
to `Django deployment documentation <https://docs.djangoproject.com/en/dev/howto/deployment/>`_.
