.. proteinmeta documentation master file, created by
   sphinx-quickstart on Fri Jan 13 16:06:31 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to proteinmeta's documentation
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

The ``proteinmeta`` library enables the retrieval of protein data, analysis
thereof, and the graphical or tabular presentation of analysis outcomes. Each
of the three components can be configured.

The library is implemented as a set of classes and relations between them. The
three main components (**retrieval**, **summarization** and **presentation**) are described in
separate section below. The corresponding classes instantiates other subclasses 
to perform the operations. These subclasses are documented in the relevant
sections. Although the subclasses can be used directly by an application that
uses the ``proteinmeta`` library, the typical application is not expected to do
so, but rely on instantiations of the primary class only.

Retrieval of Protein Data
-------------------------
The protein data can be retrieved via third-party Web APIs. The details of the
Web APIs are hidden to the user, who only configure the call to the APIs via
class methods, as described below. The raw data obtained are passed to a
parser, which translate the raw data into an object on which analysis is
applied. Alternatively, the raw data can be read from files stored on the local
disk, then passed to the parser. 

.. automodule:: rootdata
    :members: 

Summarization of Protein Data
-----------------------------
Bla bla

Presentation of Summarization
-----------------------------
Bla bla


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
