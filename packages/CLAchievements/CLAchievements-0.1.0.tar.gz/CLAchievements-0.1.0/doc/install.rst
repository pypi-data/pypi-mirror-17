Install and Enable
==================

.. warning:: :ref:`Installing <install>` CLAchievements is not enough: it has to be :ref:`enabled <enable>`.

.. _install:

Install
-------

PyGObject
"""""""""

CLAchievements uses `PyGObject <https://wiki.gnome.org/Projects/PyGObject>`_ to display the achievements (other methods might be supported later). Thus, it must be installed, either system-wide (if CLAchievements is not installed in a virtualenv, or if the virtualenv has been created with option ``--system-site-packages``), or as a dependency (see the *extra* ``pgi`` dependency below).

From sources
""""""""""""

* Download: https://pypi.python.org/pypi/clachievements
* Install (in a `virtualenv`, if you do not want to mess with your distribution installation system)::

      python3 setup.py install

  Or, to install the ``pgi`` dependency as well::

      python3 setup.py install[pgi]

From pip
""""""""

Use::

  pip install clachievements

Or, if you need the ``pgi`` dependency as well::

  pip install clachievements[pgi]

Quick and dirty Debian (and Ubuntu?) package
""""""""""""""""""""""""""""""""""""""""""""

This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

    python3 setup.py --command-packages=stdeb.command bdist_deb
    sudo dpkg -i deb_dist/clachievements-<VERSION>_all.deb

The ``PyGObject`` dependency is proposed as an optional requirement.

.. _enable:

Enable
------

Once CLAchievements is installed, it does not work yet. Running ``ls`` will not trigger any achievement: you will to wrap it using CLAchievements by running ``clachievements run ls``.

Replacing ``ls`` by ``clachievements run ls`` will change your habits. You do not want it. So, it should be aliased: ``alias ls="clachievements run ls"``.

All the commands triggering achievements should be aliased. To ease this, the :ref:`clachievements <usage>` command provides a sub-command ``clachievements alias``, which display the shell code generating all the required aliases. Thus, in your :file:`.bashrc` (or :file:`.watheverrc`), write the line ``$(clachievements alias)`` to enable every aliases.

Check
-----

To check if CLAchievements is enabled, run ``ls`` in a terminal. If you see the ``So it begins…`` achievement unlocked, it works. Otherwise, it does not… yet.

If you are not sure about wether CLAchievements works or not, reset the achievements using ``clachievements reset``, and run ``ls`` again to test it.
