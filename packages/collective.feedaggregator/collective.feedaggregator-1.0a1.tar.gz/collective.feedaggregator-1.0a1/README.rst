*************************
Feed Aggregator for Plone
*************************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

This package defines a Feed Aggregator content type that shows all entries on a list of feeds.
External content is not indexed in any way.

TODO:

* [ ] deal with shorter timeouts
* [X] byline for entries
* [ ] honor privacy settings on byline
* [ ] honor sorting and limit fields in listings
* [ ] batching in listings
* [ ] lead image support
* [X] tile for collective.cover

Mostly Harmless
===============

.. image:: http://img.shields.io/pypi/v/collective.feedaggregator.svg
   :target: https://pypi.python.org/pypi/collective.feedaggregator

.. image:: https://img.shields.io/travis/hvelarde/collective.feedaggregator/master.svg
    :target: http://travis-ci.org/hvelarde/collective.feedaggregator

.. image:: https://img.shields.io/coveralls/hvelarde/collective.feedaggregator/master.svg
    :target: https://coveralls.io/r/hvelarde/collective.feedaggregator

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it::

    [buildout]
    ...
    eggs =
        collective.feedaggregator

After updating the configuration you need to run ''bin/buildout'',
which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.feedaggregator`` and click the 'Activate' button.

How does it work
----------------

Every Feed Aggregator includes a list of feeds to be processed.
The entries in the feeds are parsed in parallel using multiprocessing.
Results are cached for 15 minutes on an instance base.
If a Feed Aggregator is modified in any way, caching is invalidated.

Not entirely unlike
===================

`Products.feedfeeder <https://pypi.python.org/pypi/Products.feedfeeder>`_
    Archetypes-based folder that turns external feed entries into content items.
    Works in Plone 4.3 and 5.
