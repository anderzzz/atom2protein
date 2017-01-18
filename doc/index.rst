.. proteinmeta documentation master file, created by
   sphinx-quickstart on Fri Jan 13 16:06:31 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to proteinmeta's documentation
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   data_retrieve

The ``proteinmeta`` library enables the retrieval of protein data, analysis
thereof, and the graphical or tabular presentation of analysis outcomes. Each
of the three components can be configured. The library also has its own Django
server, which enables part of the functionality to be displayed in a web 
browser.

The library is implemented as a set of classes and relations between them. The
three main components (**retrieval**, **summarization** and **presentation**) are described in
separate section below. The corresponding classes instantiates other subclasses 
to perform various operations. These subclasses are documented in the relevant
sections. Although the subclasses can be used directly by an application that
uses the ``proteinmeta`` library, the typical application is not expected to do
so, but rely on instantiations of the primary class only. The optional display
of the functionality in a web browser, and the back-end processing is handled 
by a Django server. It is described in a section of its own.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
