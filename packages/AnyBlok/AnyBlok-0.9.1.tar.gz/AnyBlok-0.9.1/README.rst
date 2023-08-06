=======================
Anyblok Buildout Recipe
=======================

This is a buildout recipe for `Anyblok`_

The main goal of this recipe is to help you in : 

* Bootstrapping a new `Anyblok`_ directories layout to start a new project
* Install all required dependencies in an isolated environment that does not mess up your main
  python path

.. _anyblok: https://github.com/AnyBlok/AnyBlok.git 

System dependencies
-------------------

Anyblok needs at least python 3.

You'll also need the python3-dev package in order to compile some dependencies
For example on Debian based systems (replace X by appropriate version)::

    sudo apt-get install python3.X-dev python3.X-venv

Anyblok also uses PostgreSQL (through SqlAlchemy).
This will get you a working server and the client library with the header
files needed for the database adapter compilation::

    sudo apt-get install postgresql libpq-dev


Installation
------------

Once you're done with system dependencies it's as easy as this :

Make a new virtualenv and go into it::

    python3.X -m venv-3.3 anyblok_demo
    cd anyblok_demo

Create a directory to store your project and change into it::

    mkdir projects
    cd projects

Clone the current repository and give it your project name

    git clone https://github.com/jssuzanne/anyblok_buildout.git

Change to the project directory, bootstrap and build it::

    cd anyblok_buildout
    ../bin/python3.3 bootstrap.py

Launch the buildout. Beware of launching it from the new bin directory created by the previous
command::

    bin/buildout

Your environment is ready, You're done!

What has happened here ?
========================
The ``bin/buildout`` command has automatically fetched and installed all the
required dependencies using the ``buildout.cfg`` file.
Look at ``buildout.cfg`` file to understand deeply the Anyblok ecosystem.

How to run the whole stuff ?
============================

The buildout comes with a small Anyblok example. You can delete it to create your own.
By the way if you want to try the demo, here are the steps to follow.

* Edit the ``anyblok.cfg`` file according to your database settings
* Create a new database::

    ./bin/anyblok_createdb -c anyblok.cfg

To go further with the example, you can install the ``exampleblok``; 
it will automatically create database tables and populate some fixtures.
Look at the ``doc`` directory of the main Anyblok respository for more details.

https://github.com/AnyBlok/AnyBlok.git

Contributing (hackers needed!)
==============================

Anyblok is at a very early stage, so as this recipe.
Feel free to fork, talk with core dev, and spread the world!

Author
======
Jean-Sébastien Suzanne

License
=======
This is free software (MPL2).
