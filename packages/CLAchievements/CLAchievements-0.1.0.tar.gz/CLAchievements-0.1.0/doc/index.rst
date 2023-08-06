.. Command Line Achievements documentation master file, created by
   sphinx-quickstart on Tue Jul 26 20:04:50 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Command Line Achievements's documentation!
=====================================================

Command line was all fun when it was invented fifty years ago, but it can no longer compete with modern interfaces, glowing windows, shiny buttons, and so on… Command Line Achievements (later abbreviated CLAchievements or CLA) aims to solve this, by making command line fun again! Inspired by video game achievements, it unlocks achievements when users meets the fulfillement conditions.

|screenshot|

.. warning::

  CLAchievements is not mature yet. Let's say it is a proof of concept (a silly concept, but still a concept).

  Before using this software, please read the :ref:`warning <warning>`.

Contents:

.. toctree::
   :maxdepth: 1

   install
   usage
   plugin
   modules

.. _warning:

Does it work?
=============

I would say CLAchievements works if user cannot distinguish wrapped commands from original commands, excepted the *Achievement unlocked* text popping up from times to times.

What works
----------

When the command ends on its own, the standard input, and standard and error output are transmitted to the wrapped command, and the return code of the command is the expected one (the one of the wrapped command).

What does not work
------------------

- Interruptions: When a command is interrupted (by using Ctrl-C or kill), user sees the internals of CLAchievements.

  .. code:: sh

    $ cat
    ^CTraceback (most recent call last):
      File "/home/louis/.virtualenvs/clachievements/bin/clachievements", line 9, in <module>
        load_entry_point('CLAchievements==0.1.0', 'console_scripts', 'clachievements')()
      (...)
      File "/usr/lib/python3.5/subprocess.py", line 1608, in _try_wait
        (pid, sts) = os.waitpid(self.pid, wait_flags)
    KeyboardInterrupt
    $

  It should act as if the wrapped command had been interrupted.

- It is incredibly slow: for instance, running one thousand `ls` is about 600 times slower using CLAchievements than using the original `ls`.

  .. code:: bash

      $ time bash -c 'for i in $(seq 1000); do clachievements run ls > /dev/null; done'
      real    7m57.569s
      user    6m3.960s
      sys     0m21.536s
      $ time bash -c 'for i in $(seq 1000); do ls > /dev/null; done'
      real    0m0.790s
      user    0m0.024s
      sys     0m0.080s

  This is a real problem, and addressing it might mean rewriting everything from scratch…


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |screenshot| image:: _static/screenshot.png
