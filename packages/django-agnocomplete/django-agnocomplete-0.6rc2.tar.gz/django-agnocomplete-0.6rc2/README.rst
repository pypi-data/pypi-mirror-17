============================
Django Agnostic Autocomplete
============================


.. image:: https://travis-ci.org/novafloss/django-agnocomplete.svg?branch=master
    :target: https://travis-ci.org/novafloss/django-agnocomplete


Heavily based on `django-autocomplete-light <https://github.com/yourlabs/django-autocomplete-light/>`_ workflow and concepts, this toolkit offers a front-end agnostic way to get fields for autocompletion.

It will provide:

* a simple and configurable entry-point management,
* a REST-like HTTP API to search for results,
* Fields and widgets that will make the interface between our Django code and *your* Javascript.

Status
======

Under construction. Warning, fresh paint.

Install
=======

::

    pip install django-agnocomplete

Or add ``django-agnocomplete`` to your project requirements.

Documentation
=============

`The full documentation is browsable on RTFD <http://django-agnocomplete.readthedocs.org/en/latest/>`_


Tests
=====

Install ``tox`` in your environment (it could be a virtualenv) and run::

    tox

It'll run the tests for all the combinations of the following:

* Python 2.7, 3.3, 3.4.
* Django 1.8, 1.9.

and a ``flake8`` check.

.. note::

    The combination Python 3.3 and Django 1.9 is incompatible - `see Django 1.9 release notes <https://docs.djangoproject.com/en/1.10/releases/1.9/>`_

Are you a developper?
---------------------

To target a specific test case, use the following::

    tox -e py27-django18 --  demo.tests.test_core.AutocompleteChoicesPagesOverrideTest

Everything after the double-dash will be passed to the django-admin.py test command.

If you need to install a debugger (let's say `ipdb`), you can use the ``TOX_EXTRA`` environment variable like this::

    TOX_EXTRA=ipdb tox -e py27-django18


Run the demo
============

The (draft) demo site can be browsed using the Django devserver. Run::

    tox -e serve

It will run a syncdb (it may ask you questions) and then a runserver with your current ``demo.settings``. You can browse the (very rough) website at http://127.0.0.1:8000/. You can add
any runserver options you want using the `tox` positional parameters, like this::

    tox -e serve -- 9090  # to change the listening port


Here you'll be able to see that ``django-agnocomplete`` has been easily and rapidly integrated with ``selectize.js``, ``select2``, ``jquery-autocomplete`` and ``typeahead``. With the same backend, you can plug the JS front-end you want.

----

License
=======

This piece of software is being published under the terms of the MIT License. Please read the `LICENSE` file for more details.
