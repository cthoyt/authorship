Authorship |release| Documentation
==================================
Maintaining author lists on collaborative academic work is a bit of a pain.
A lot of us have started collecting author information on Google Sheets since
it allows people to input their own information, like their ORCID and
affiliations. I wanted to automate turning those sheets into some useful forms
for copy/pasting into my manuscripts (e.g., in Google Docs or LaTeX) as well
submission forms (e.g., bulk author TSV file import on bioRxiv).

Installation
------------
The most recent release can be installed from
`PyPI <https://pypi.org/project/authorship>`_ with:

.. code-block:: shell

    $ pip install authorship

The most recent code and data can be installed directly from GitHub with:

.. code-block:: shell

    $ pip install git+https://github.com/cthoyt/authorship.git

To install in development mode, use the following:

.. code-block:: shell

    $ git clone git+https://github.com/cthoyt/authorship.git
    $ cd authorship
    $ pip install -e .

Table of Contents
-----------------
.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   :name: start

   usage
   cli

Indices and Tables
------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
