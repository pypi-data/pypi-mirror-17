PyBEL |buildstatus| |codecov| |climate| |pyversions|
====================================================

.. |buildstatus| image:: https://travis-ci.org/pybel/pybel.svg?branch=master
    :target: https://travis-ci.org/pybel/pybel

.. |pyversions| image:: https://img.shields.io/badge/python-2.7%2C%203.5-blue.svg
    :alt: Stable Supported Python Versions

.. |codecov| image:: https://codecov.io/gh/cthoyt/pybel/branch/master/graph/badge.svg?token=J7joRTRygG
    :target: https://codecov.io/gh/cthoyt/pybel

.. |climate| image:: https://codeclimate.com/repos/57fa4c866f0a491c8900122d/badges/c0e030bca94c7746ce21/gpa.svg
    :target: https://codeclimate.com/repos/57fa4c866f0a491c8900122d/feed
    :alt: Code Climate


Biological Expression Language (BEL) is a domain specific language that enables the expression of complex molecular relationships and their context in a machine-readable form. Its simple grammar and expressive power have led to its successful use in the IMI project, AETIONOMY, to describe complex disease networks with several thousands of relationships.

PyBEL is a Python software package that parses BEL statements, validates their semantics, applies common graph algorithms, and allows for data interchange with common formats like Neo4J, JSON, CSV, Excel, and SQL.
PyBEL provides a simple API so bioinformaticians and scientists with limited programming knowledge can easily use it to interface with BEL graphs, but is built on a rich framework that can be extended to develop new algorithms.

.. code-block:: python

   >>> import pybel, networkx
   >>> g = pybel.from_url('http://resource.belframework.org/belframework/1.0/knowledge/small_corpus.bel')
   >>> networkx.draw(g)

Command Line Interface
----------------------

PyBEL also installs a command line interface with the command :code:`pybel` for simple utilities such as data
conversion. Need help? All logs go to :code:`~/.pybel` or add :code:`-v` for verbose output to the standard error
stream

Export for Cytoscape
~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

    $ pybel convert --path ~/Desktop/example.bel --graphml ~/Desktop/example.graphml
   
In Cytoscape, open with :code:`Import > Network > From File`.

Export to Neo4j
~~~~~~~~~~~~~~~

.. code-block:: sh

   $ URL="http://resource.belframework.org/belframework/1.0/knowledge/small_corpus.bel"
   $ NEO="neo4j:neo4j@localhost:7474"
   $
   $ pybel to_neo --url $URL --neo $NEO


Installation
------------

Check :code:`CONTRIBUTING.rst` for installing the latest version from GitHub or a zip archive.
In the future, this repository will be open to the public for use. Installation will be as easy as:

.. code-block:: sh

   pip install pybel
	

Contributing
------------

Contributions, whether filing an issue, making a pull request, or forking, are appreciated. See
:code:`CONTRIBUTING.rst` for more information on getting involved.

Acknowledgements
----------------

- PyBEL is proudly built with Paul McGuire's PyParsing package.
- Scott Colby designed our logo and provided sage advice

The Cool Pool of Tools
----------------------
- Reverse Causal Reasoning Algorithm
- Canonicalization
- Semantic Diff

