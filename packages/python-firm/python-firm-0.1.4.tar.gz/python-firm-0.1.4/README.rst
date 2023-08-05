Python-Firm:  CFFI wrapper around the libFirm compiler backend
==============================================================

:Author: William ML Leslie
:Licence: GNU Lesser General Public Licence v2.1 or later

Firm_ is a library that provides a graph-based intermediate
representation, optimizations, and assembly code generation suitable
for use in both AOT and JIT compilers.

.. _Firm: http://pp.ipd.kit.edu/firm/Index

This is a wrapper for libfirm.  You can initialise and access the base
library like so::

  from firm.base import libfirm

In addition, most of the modules that libfirm provides have nice
pythonic wrappers.  You can get started by reviewing the tests in
firm.tests, test_simple for example considers the API of using the
basic wrapper objects directly.

I should do a tutorial language for python-firm, showing off some of
the different ways to do control structure.

TODO
----

* A tutorial

* Implement DbgInfo and SrcLog functionality

* Make hooking in assemblers and linkers easier

* Wrap Builtins

* Wrap Target Values

Building
--------

You can build python-firm for a specific libfirm with

::

  python -m gen.compile

If you want to build the module for a libfirm you've built locally,
set the environment variable FIRM_HOME.  It will try to statically
link libfirm if possible; if you want to use a dynamically linked
libfirm you will need to arrange for it to be on the linker's library
path.

The gen module also contains templates for use when the ir_spec
changes::

  python $FIRM_HOME/scripts/gen_ir.py gen/pythonbits.py gen/operation_template.py > firm/operations.py
  python $FIRM_HOME/scripts/gen_ir.py gen/pythonbits.py gen/defs_template.h > firm/node_defs.h

