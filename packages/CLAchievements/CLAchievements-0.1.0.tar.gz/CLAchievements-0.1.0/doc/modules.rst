Modules
=======

.. contents::
   :local:

Command
-------

.. module:: clachievements.run.__init__

.. autoclass:: Command
   :members:

Achievements
------------

.. module:: clachievements.achievements.__init__

.. autoclass:: Achievement
   :members: title, bin, icon, _description, first, last, unlock

.. autoclass:: SimplePersistentDataAchievement
   :members: default_data, data


Test utils
----------

.. module:: clachievements.testutils

.. autofunction:: test_lock
.. autofunction:: test_unlock
