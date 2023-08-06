.. _plugin:

Write your own achievement
==========================

Achievement without persistent data
-----------------------------------

Suppose you want to create an achievement ``Foo`` awarded when user successfully run a command on a file :file:`foo`. Let's write this achievement.

Meta-information
""""""""""""""""

First, we need to define a class and define meta-information: any achievement is a subclass of :class:`~clachievements.achievements.__init__.Achievement`. Two arguments are compulsory:

* :attr:`~clachievements.achievements.__init__.Achievement.title`: if ``None``, your class is an abstract achievement, meant to be subclassed; if a string, your achievement is an *actual* achievement. See the :class:`class documentation <clachievements.achievements.__init__.Achievement>` for other attributes;
* `description`: your achievement must have a description. The first non-empty line of your class docstring is used, unless :attr:`~clachievements.achievements.__init__.Achievements._description` is defined, when it is used instead.

See :class:`the class documentation <clachievements.achievements.__init__.Achievement>` to get more information about other attributes.

.. code-block:: python

    from clachievements.achievements import Achievement
    from clachievements.testutils import test_lock, test_unlock

    class Foo(Achievement):
        """Successfully run a command on file `foo`."""

        title = "Foo"

Unlocking the achievement
"""""""""""""""""""""""""

Great: you have an achievement. But it is never unlocked: it will be frustrating for the user.

An achievement is a :ref:`context manager <typecontextmanager>`: its :meth:`~contextmanager.__enter__` and :meth:`~contextmanager.__exit__` methods are called before and after the actual system call. They can be used to test the command line, the environment before and after the command, etc.

Here, we test that:

* ``foo`` is a positional argument;
* the command did not fail.

If so, we call :meth:`~clachievements.achievements.__init__.Achievement.unlock()` to unlock the argument. It ensures that the argument is marked as unlocked, and it displays a pop-up to notify the user. No need to make sure that parallel calls to your achievement might unlock it at the same time: it is handled within the :meth:`~clachievements.achievements.__init__.Achievement.unlock()` method itself.

.. code-block:: python

    from clachievements.achievements import Achievement
    from clachievements.testutils import test_lock, test_unlock

    class Foo(Achievement):
        """Successfully run a command on file `foo`."""

        title = "Foo"

        def __exit__(self, exc_type, exc_value, traceback):
            if "foo" in self.command.positional:
                if isinstance(exc_value, SystemExit):
                    if exc_value.code == 0:
                        self.unlock()

.. _testing:

Testing
"""""""

If we are done, the achievement will work, but the unit tests will fail. An achievement *must* define a test that unlock the achievement.

Each achievement must define a static or class method, :pep:`decorated <318>` with :func:`~clachievements.testutils.test_unlock`. This method must iterate strings which are shell commands, unlocking the achievement. To be wrapped by CLAchievements, system calls must use string substitution: ``"foo bar"`` will call the ``foo`` binary, *not wrapped* by CLAchievements, where ``"{bin.foo} bar"`` will call the ``foo`` binary, wrapped by CLAchievements.

You can add as many test methods as you want. You can also define test methods that must not unlock achievements, by decorating them with :func:`~clachievements.testutils.test_lock`.

When performing tests, each test method is run inside an empty temporary directory, which will be deleted afterward.

.. code-block:: python

    from clachievements.achievements import Achievement
    from clachievements.testutils import test_lock, test_unlock

    class Foo(Achievement):
        """Successfully run a command on file `foo`."""

        title = "Foo"

        def __exit__(self, exc_type, exc_value, traceback):
            if "foo" in self.command.positional:
                if isinstance(exc_value, SystemExit):
                    if exc_value.code == 0:
                        self.unlock()

        @staticmethod
        @test_unlock
        def test_touch():
            yield "{bin.touch} foo"

        @staticmethod
        @test_lock
        def test_ls():
          yield "{bin.ls} foo"


Achievement with persistent data
--------------------------------

Now, we want a new achievement ``FooBar`` to be triggered when 50 successful commands have been run on a file :file:`foo`. Let's do this.

To do this, we have to store the number of successful commands. A class is defined to ease this process: :class:`~clachievements.achievements.__init__.SimplePersistentDataAchievement`. It is wrong (see below), but is works for simple cases.

When using this class, a row is created in the CLAchievements database with this achievement name.

* The first time this achievement is created, this row is filled with the content of attribute :attr:`~clachievements.achievements.__init__.SimplePersistentDataAchievement.default_data`.
* When accessing to :attr:`~clachievements.achievements.__init__.SimplePersistentDataAchievement.data`, data is read from the database.
* When assigning a value to :attr:`~clachievements.achievements.__init__.SimplePersistentDataAchievement.data`, data is written to the database.

Any :mod:`picklable <pickle>` data can be stored using this method.

This is simple, but this is not robust to concurrent access: if an integrity error occurs when assigning a value to :attr:`~clachievements.achievements.__init__.SimplePersistentDataAchievement.data`, it is silently ignored.

With this example achievement, if I run this argument 50 times in parallel, about 30 of the assignments are ignored. If I were to design a life critical application, this would be a big issues. But this is only a game: it does not work perfectly, but it is so much simpler to implement!

.. code-block:: python

    from clachievements.achievements import SimplePersistentDataAchievement
    from clachievements.testutils import test_lock, test_unlock

    class FooBar(SimplePersistentDataAchievement):
        """Successfully run 50 command on file `foo`."""

        title = "FooBar"
        default_data = 0

        def __exit__(self, exc_type, exc_value, traceback):
            if "foo" in self.command.positional:
                if isinstance(exc_value, SystemExit):
                    if exc_value.code == 0:
                        self.data += 1
            if self.data >= 50:
                self.unlock()

        @staticmethod
        @test_lock
        def test_touch():
            for _ in range(49):
                yield "{bin.touch} foo"

        @staticmethod
        @test_unlock
        def test_ls_touch():
            for _ in range(25):
                yield "{bin.touch} foo"
                yield "{bin.ls} foo"

More
----

Suppose this error-prone persistent data management does not suit you. Just write your own: within the achievement, the :class:`sqlite3 database connection <sqlite3.Connection>` is available as :attr:`self.database.conn`. Do whatever you want with it (without breaking other plugin databases)!

In this case, to be sure not to mess with tables of CLA core or other plugins, use the tables named (case insensitive) ``achievement_YourPluginName`` or ``achievement_YourPluginName_*``.

Methods :meth:`~clachievements.achievements.__init__.Achievement.first` and :meth:`~clachievements.achievements.__init__.Achievement.last` can be used to initialize or clean the achievement: the first one is called the first time the achievement is ever loaded (so it can be used to create some tables into the database), while the last one is called when the achievement has just been unlocked (so it can be used to clean stuff). Both these methods are meant to be subclassed, and are expected to call ``super().first(...)`` at the beginning of their code.
