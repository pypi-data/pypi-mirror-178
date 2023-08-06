dwave-gate
==========

.. index-start-marker

``dwave-gate`` is a software package for constructing, modifying and running quantum circuits. It
provides a set of tools that enables you to:

* Construct quantum circuits using an intuitive context-manager interface.

* Utilize a comprehensive library of quantum gates with simple access to matrix representations,
  various decompositions, and more.

* Simulate circuits on a performant (C++) state-vector simulator.

* Easily create your own quantum gates and templates. Any circuit can be either directly applied in
  another circuit or converted into a quantum operation.

.. index-end-marker

Example usage
-------------

.. example-start-marker

This example uses the ``dwave.gate.Circuit`` object's  context manager to append operations to
a two-qubit circuit.

.. code-block:: python

    import dwave.gate.operations as ops
    from dwave.gate import Circuit

    circuit = Circuit(2)

    with circuit.context as q:
        ops.Hadamard(q[1])
        ops.CZ(q[0], q[1])
        ops.Hadamard(q[1])

You can run the ``dwave.gate.simulator`` simulator on such circuits.

>>> from dwave.gate.simulator import simulate
>>> simulate(circuit)
array([0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j])

.. example-end-marker

Installation
------------

.. installation-start-marker

The simplest way to install ``dwave-gate`` is from `PyPI <https://pypi.org/project/dwave-gate>`_:

.. code-block:: bash

    pip install dwave-gate

It can also be installed from source by cloning this GitHub repository and running (on Unix systems):

.. code-block:: bash

    make install

The makefile will also simplify running tests (``make test``), coverage (``make coverage``) and
formatting (``make format``) the code using the `Black <https://black.readthedocs.io/>`_ formatter
(set to a line-length of 100) and `isort <https://pycqa.github.io/isort/>`_.

Alternatively, the package can be built and installed using Python (on any supported system):

.. code-block:: bash

    python setup.py build_ext --inplace

and tests and coverage can be run using Pytest:

.. code-block:: bash

    pytest tests/ --cov=dwave.gate

.. installation-end-marker

License
-------

Released under the Apache License 2.0. See LICENSE file.

Contributing
------------

Ocean's `contributing guide <https://docs.ocean.dwavesys.com/en/stable/contributing.html>`_
has guidelines for contributing to Ocean packages.

Release Notes
~~~~~~~~~~~~~

``dwave-gate`` uses `reno <https://docs.openstack.org/reno/>`_ to manage its release notes.

When making a contribution to ``dwave-gate`` that will affect users, create a new release note file
by running

.. code-block:: bash

    reno new your-short-descriptor-here

You can then edit the file created under ``releasenotes/notes/``. Remove any sections not relevant
to your changes. Commit the file along with your changes.

See reno's `user guide <https://docs.openstack.org/reno/latest/user/usage.html>`_ for details.
