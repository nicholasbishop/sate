====
sate
====

Simple command-line task runner

By default ``sate`` looks for a file called ``.satefile``. Run ``sate
<target>`` to run a target from the ``.satefile``.

Simple example
~~~~~~~~~~~~~~

``.satefile``::

  [lint]
  pylint *.py

Running ``sate lint`` runs the command ``pylint *.py``.
