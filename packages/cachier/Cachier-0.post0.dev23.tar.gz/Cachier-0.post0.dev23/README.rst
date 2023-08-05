Cachier
=======

Persistent, stale-free cache / memoization decorators for Python.

.. code-block:: python

  from cachier import cachier
  import datetime
  
  SHELF_LIFE = datetime.timedelta(days=3)
  
  @cachier(stale_after=SHELF_LIFE)
  def foo(arg1, arg2):
    """foo now has a persistent cache, trigerring recalculation for values stored more than 3 days!"""
    return {'arg1': arg1, 'arg2': arg2}


.. role:: python(code)
  :language: python

Dependencies and Setup
----------------------

s3bp uses the following packages:

* pymongo's `bson package`_
* watchdog_

You can install cachier using:

.. code-block:: python

    pip install cachier

Features
----------------------

* A simple interface.
* Defining "shelf life" for cached values.
* Local caching using pickle files.
* Cross-machine caching using MongoDB.
* Thread-safety.

Cachier is not:

* Meant as a transient cache. Python's @lru_cache is better.
* Especially fast. It is meant to replace function calls that take more than... a second, say (overhead is around 1 millisecond).


Use
---

The positional and keyword arguments to the wrapped function must be hashable (i.e. Python's immutable built-in objects, not mutable containers). Also, notice that since objects which are instances of user-defined classes are hashable but all compare unequal (their hash value is their id), equal objects across different sessions will not yield identical keys.

Pickle-based Caching
~~~~~~~~~~~~~~~~~~~~
You can add a deafult, pickle-based persistent cache to your function - meaning it will last across different Python kernels calling the wrapped function - by decorating it with the ``cachier`` decorator (notice the ``()``!).

.. code-block:: python

  from cachier import cachier
  
  @cachier()
  def foo(arg1, arg2):
    """Your function now has a persistent cache mapped by argument values!"""
    return {'arg1': arg1, 'arg2': arg2}

Setting Shelf Live
~~~~~~~~~~~~~~~~~~
You can set any duration as the shelf life of cached return values of a function by providing a corresponding ``timedelta`` object to the ``stale_after`` parameter:

.. code-block:: python

  import datetime
  
  @cachier(stale_after=datetime.timedelta(weeks=2))
  def bar(arg1, arg2):
    return {'arg1': arg1, 'arg2': arg2}
    
Now when a cached value matching the given arguments is found the time of its calculation is checked; if more than ``stale_after`` time has since passed the function will be run again for the same arguments and the new value will be cached and returned.

This is usefull for lengthy calculation that depend on a dynamic data source.

Fuzzy Shelf Live
~~~~~~~~~~~~~~~~
Sometimes you may want your function to trigger a calculation when it encounters a stale result, but still not wait on it if it's not that critical. In that case you can set ``next_time`` to ``True`` to have your function trigger a recalculation but return the currently cached stale value:

.. code-block:: python

  @cachier(next_time=True)

Further function calls made while the calculation is being performed will not trigger redundant calculations.

Minimizing IO
~~~~~~~~~~~~~
You can slightly optimize caching if you know your code will only be used in a single thread environment by setting:

.. code-block:: python

  @cachier(pickle_reload=False)

This will prevent reading the cache file on each cache read, speeding things up a bit, while also nullfying inter-thread functionality (the code is still thread safe, but different threads will have different version of the cache at times, and will sometime make unecessary function calls.


MongoDB-based Caching
~~~~~~~~~~~~~~~~~~~~~
You can set a MongoDB-based cache by assigning ``mongetter`` with a callable that returns a ``pymongo.Collection`` object:

.. code-block:: python

  @cachier(mongetter=False)

This allows you to have a cross-machine, albeit slower, cache.

.. links:
.. _bson package: https://api.mongodb.com/python/current/api/bson/
.. _watchdog: https://github.com/gorakhargosh/watchdog
