|Build Status| |PyPI Release| |PyPI Status| |Python| |License|

pyStream
========

Python implementation of `stream
library <https://github.com/vgteam/stream>`__ for parsing all files
encoded by stream and writing protobuf instances into the file by using
the same encoding.

Installation
------------

You can install pyStream using ``pip``:

::

    pip install pystream-protobuf

Examples
--------

Here's a sample code using the Stream class to read a file (so-called
GAM file) containing a set of `VG <https://github.com/vgteam/vg>`__'s
Alignment objects (defined
`here <https://github.com/vgteam/vg/blob/master/src/vg.proto>`__). It
yields the protobuf objects stored in the file:

.. code:: python

    import stream
    import vg_pb2

    alns_list = []
    with stream.open("test.gam", "rb") as istream:
        for data in istream:
            aln = vg_pb2.Alignment()
            aln.ParseFromString(data)
            alns_list.append(aln)

Or

.. code:: python

    import stream
    import vg_pb2

    alns_list = []
    istream = stream.open("test.gam", "rb")
    for data in istream:
        aln = vg_pb2.Alignment()
        aln.ParseFromString(data)
        alns_list.append(aln)
    istream.close()

And here is another sample code for writing multiple protobuf objects
into a file (here a GAM file):

.. code:: python

    import stream

    with stream.open("test.gam", "wb") as ostream:
        ostream.write(*objects_list)
        ostream.write(*another_objects_list)

Or

.. code:: python

    import stream

    ostream = stream.open("test.gam", "wb")
    ostream.write(*objects_list)
    ostream.write(*another_objects_list)
    ostream.close()

.. |Build Status| image:: https://img.shields.io/travis/cartoonist/pystream-protobuf.svg?style=flat-square
   :target: https://travis-ci.org/cartoonist/pystream-protobuf
.. |PyPI Release| image:: https://img.shields.io/pypi/v/pystream-protobuf.svg?style=flat-square
   :target: https://pypi.python.org/pypi/pystream-protobuf
.. |PyPI Status| image:: https://img.shields.io/pypi/status/pystream-protobuf.svg?style=flat-square
   :target: https://pypi.python.org/pypi/pystream-protobuf
.. |Python| image:: https://img.shields.io/pypi/pyversions/pystream-protobuf.svg?style=flat-square
   :target: https://www.python.org/download/releases/3.0/
.. |License| image:: https://img.shields.io/pypi/l/pystream-protobuf.svg?style=flat-square
   :target: LICENSE
