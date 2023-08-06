.. image:: https://travis-ci.org/TimKam/sphinx-pretty-searchresults.svg?branch=master
    :target: https://travis-ci.org/TimKam/sphinx-pretty-searchresults


Sphinx: pretty search results
=============================
*Sphinx: pretty search results* is an extension for the `Sphinx documentation tool <http://www.sphinx-doc.org/en/stable/>`__.

To display search results, Sphinx is fetching the source files of search hits and rendering excerpts in raw markup
(`Example <http://www.sphinx-doc.org/en/stable/search.html?q=quickstart&check_keywords=yes&area=default>`__).

This extension removes the markup from these source files (during build time), so the search results look decent.


Installation
------------
Run ``pip install sphinxprettysearchresults``.


Configuration
-------------
There are no custom configuration variables for the *Sphinx: pretty search results* extension.

After installing the extension, all you need to do is to register it.

Add ``sphinxprettysearchresults`` to the ``extensions`` array in your ``conf.py`` file, for example::

   extensions = [
      'sphinxprettysearchresults'
   ]

After your next build, your project will no longer display raw markup in the search result excerpts.


Testing
-------
*Sphinx: pretty search results* uses `nose <https://github.com/nose-devs/nose>`__ as a test framework.

To run the tests, you first need to install the dev dependencies::

    pip install -r pip install -r dev_requirements.txt

Then, navigate to the ``tests`` directory and run::

    python run.py

