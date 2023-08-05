.. py:currentmodule:: confattr

Config and ConfigFile
=====================

confattr (config attributes) is a python library to make applications configurable.
This library defines the :class:`Config` class to create attributes which can be changed in a config file.
It uses the `descriptor protocol <https://docs.python.org/3/reference/datamodel.html#implementing-descriptors>`_ to return it's value when used as an instance attribute.

.. literalinclude:: examples/example_config.py
   :language: python
   :end-before: # ------- 01 -------

If you want to access the Config object itself you need to access it as a class attribute:

.. literalinclude:: examples/example_config.py
   :language: python
   :start-after: # ------- 01 -------
   :end-before: # ------- 02 -------

You load a config file with a :class:`ConfigFile` object.
In order to create an ConfigFile instance you need to provide a callback function which informs the user if the config file contains invalid lines.
This callback function takes two arguments: (1) a :class:`NotificationLevel` which says whether the notification is an error or an information and (2) the message to be presented to the user, either a :class:`str` or a :class:`BaseException`.
When you load a config file with :meth:`ConfigFile.load` all :class:`Config` objects are updated automatically.

.. literalinclude:: examples/example_config.py
   :language: python
   :start-after: # ------- 02 -------



Of course you don't need to use classes.
In that case you can access the value of a :class:`Config` object via the :attr:`Config.value` attribute.
