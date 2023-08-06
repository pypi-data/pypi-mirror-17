===================
slumber-serializers
===================

A set of Slumber serializers

.. image:: https://travis-ci.org/tomi77/slumber-serializers.svg?branch=master
   :target: https://travis-ci.org/tomi77/slumber-serializers
.. image:: https://coveralls.io/repos/github/tomi77/slumber-serializers/badge.svg
   :target: https://coveralls.io/github/tomi77/slumber-serializers
.. image:: https://codeclimate.com/github/tomi77/slumber-serializers/badges/gpa.svg
   :target: https://codeclimate.com/github/tomi77/slumber-serializers
   :alt: Code Climate

Installation
============

Install package via ``pip``

.. sourcecode:: sh

   pip install slumber-serializers

Usage
=====

.. sourcecode:: python

   import slumber
   import slumber.serialize
   from slumber_serializers import CsvSerializer


   api = slumber.API('/api/v1/', serializer=slumber.serialize.Serializer(default='csv',
                                                                         serializers=[CsvSerializer()]),
                     format='csv')
   api.test(format='csv').get()

Available serializers
=====================

CSV serializer
--------------

Serialize to and deserialize from CSV.

Binary serializer
-----------------

Serialize to and deserialize from any binary format.
