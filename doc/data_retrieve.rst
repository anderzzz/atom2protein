Retrieval of Protein Data
-------------------------
The protein data can be retrieved via third-party Web APIs. The details of the
Web APIs are hidden to the user, who only configure the call to the APIs via
class methods, as described below. The raw data obtained are passed to a
parser, which translate the raw data into an object, broadly called the data
container object, on which analysis is
applied. Alternatively, the raw data can be read from files stored on the local
disk, then passed to the parser. 

Since there are two paths to construct the data container object, both the raw
data retriever class and the parser are configurable to the user in standard
use-cases. The corresponding classes are described in detail below along with
code examples. The other classes involved in the retrieval are described
further below.

Raw Data Retrieval
==================

.. automodule:: informatics.rawretrievers
    :members: 

Data Containers
===============

.. automodule:: informatics.datacontainers
    :members:

