========
Overview
========



A Django app that helps you creating models within a Complex System.

License
=======

Software licensed under `MPL 2.0`_ license.

.. _BSD-2 : https://opensource.org/licenses/BSD-2-Clause
.. _MPL 2.0 : https://www.mozilla.org/en-US/MPL/2.0/

Installation
============

::

    pip install django-cs-models


Usage
=====

Two parameters have to be set in your settings. Here is an example:

.. code:: python

    COMPLEX_APP_NAME = 'ecosystem'

    COMPLEX_STRUCTURE = {
        'roots': [
            ['Organization', 'Committee', 'Board', 'Cohort'],
        ],
        'nodes': [
            ['ProjectTeam'],
            ['Resource'],
            ['Member'],
        ]
    }

Roots are entities that contain nodes (a root cannot contain another root).
Nodes are entities contained by and containing other nodes.

You can define roots and nodes at different levels, i.e. their position
in the hierarchy. These levels will tell if such entity can be
contained by such other entity.

Now in `ecosystem` app:

.. code:: python

    from csmodels.models import abstract_model

    class Cohort(abstract_model('Cohort')):
        your_model_fields_here = models.SomeField()

        class Meta:
            verbose_name = _('Cohort')
            verbose_name_plural = _('Cohorts')


The cohort model will inherit many to many relationships to
project teams, resources and members from the abstract model.

Of course, a change in the complex structure will change the models,
therefore migrations will be needed!

First diagram shows the example above.

.. image:: http://i.imgur.com/a2dGa9V.png
    :alt: Example diagram


Second diagram shows how links are created between entity depending on their
type (root or node) and their level. Letters (their names) are not important,
but numbers (their levels) are.

.. image:: http://i.imgur.com/apJNGpe.png
    :alt: Abstract diagram


Documentation
=============

https://github.com/Pawamoy/django-cs-models.wiki

Development
===========

To run all the tests: ``tox``

=========
Changelog
=========

0.1.0 (2016-10-06)
==================

* Alpha release on PyPI.


