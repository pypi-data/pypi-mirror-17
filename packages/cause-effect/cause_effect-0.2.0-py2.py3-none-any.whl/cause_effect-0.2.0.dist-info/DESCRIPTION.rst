.. image:: http://ci.appveyor.com/api/projects/status/m0f9fw5b670whkw8?svg=true
    :target: https://ci.appveyor.com/project/hyllos/cause-effect

Install it
-----------

You can install ``cause_effect`` via:

.. code-block:: bash

  $ pip install cause_effect

Alternatively, you can install from the code repository directly:

.. code-block:: bash

  $ pip install hg+http://bitbucket.org/hyllos/cause_effect

Core Functions
--------------

``pareto(values)``
    Is a pareto distribution present for a list of numbers (``ratio`` <= 1)?

``mccauses(values)``
    Which causes have the highest concentration (rank * value)?

``mceffects(values)``
    Which effects have the highest concentration?

``separator(values)```
    From which value (including) does the highest concentration begin?

``causes(values, effects=0.8)``
    Determine causes for specified share of effects.

``effects(values, causes=0.2)``
    Determine effects for specified share of causes.

Secondary Functions
-------------------

``ratio(values)``
    ``entropy`` divided by ``control_limit``.

``entropy(values)``
    Calculate entropy for values.

``control_limit(count)``
    Calculate control entropy for ``count`` number of elements (length of ``values``).

Tertiary Functions
-------------------

``make_causes(count)``
    Return list of causes that is cumulative percent of ``count`` number of elements.

``make_effects(values)``
    Return list of effects that is cumulative percent of values.

``make_concentration(values)``
    Return list of concentration for list of ``values`` that is rank * value.

``sort_list(values)``
    Return sorted list of numbers.

Parameters
-----------

``values`` is a list of numbers.
``effects`` and ``causes`` must be a number between 0 and 1 (including).
``count`` is the length of the list of ``values``.

Use it
------

The function ``pareto`` tells you whether a pareto distribution is present for a list of numbers:

.. code-block:: python

  from pareto import pareto, mccauses, mceffects
  pareto([789, 621, 109, 65, 45, 30, 27, 15, 12, 9])
  True

Here, we have a pareto distribution present.
That is a minority causes a majority of effects.

But which minority causes which majority?

.. code-block:: python

  mccauses([789, 621, 109, 65, 45, 30, 27, 15, 12, 9])
  0.2
  mceffects([789, 621, 109, 65, 45, 30, 27, 15, 12, 9])
  0.818815331010453

20% of causes effect 82% of results.

But which values are that 20%?

.. code-block:: python

  separator([789, 621, 109, 65, 45, 30, 27, 15, 12, 9])
  621

All values greater or equal than 621 are those 20% causing 82% of results.

**That's it.**

Dig Deeper
-----------

How many causes are required for only 90% of effects?

.. code-block:: python

  from pareto import causes, effects
  causes([789, 621, 109, 65, 45, 30, 27, 15, 12, 9], 0.9)
  0.4

40%.

How many effects are behind only 10% of causes?

.. code-block:: python

  effects([789, 621, 109, 65, 45, 30, 27, 15, 12, 9], 0.1)
  0.458

45.8%.

How does it work?
-----------------

``pareto`` calculates the `entropy`_ for a list of effects:

.. code-block:: python

  from pareto import entropy, control_limit, ratio
  entropy([789, 621, 109, 65, 45, 30, 27, 15, 12, 9])
  1.9593816735406657

It calculates the entropy for a control group of ten elements. That is the length of our list.

.. code-block:: python

  control_limit(10)
  2.7709505944546686

It then checks ``entropy`` is less or equal than ``control_limit``.

This can be simplified to:

.. code-block:: python

  values = [789, 621, 109, 65, 45, 30, 27, 15, 12, 9]
  entropy(values) / control_limit(len(values)) <= 1

The left side of the comparison is done by ``ratio``.
So, if you want to find out how nearby or far off you are from a pareto distribution, do:

.. code-block:: python

  ratio([109, 65, 45, 30, 27, 15, 12, 9])
  1.051

If we remove the first two effects, the ``control_limit`` will be exceeded by the values.
So, we learn here that the pareto distribution disappears with the first two effects.

.. _entropy: http://www.boazronen.org/PDF/The%20Pareto%20managerial%20principle%20-%20when%20does%20it%20apply.pdf

``mccauses`` and ``mceffects`` return the respective share of the causes and effects where concentration (rank * value) is highest.


=======
History
=======

0.2.0 (2016-10-21)
------------------

* Add function separator().
* Streamline tests.

0.1.0 (2016-10-20)
------------------

* First release on PyPI.


