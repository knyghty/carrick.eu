django new
##########

:date: 2024-12-08
:tags: django
:has_code: true

Two features, one post. One command, even.

One problem that occasionally, but repeatedly, comes up is that Django's
``startproject`` command doesn't really do enough. You will always need to run
``startapp`` as well, and then you need to add the app to the ``INSTALLED_APPS``.
Or, does it actually do too much? Would you be better starting from
`first principles`_? Maybe some people would learn better like this.

We can solve both of these problems, and one more: ``startproject`` is such a
boring name for your first step in Django. We could have a new ``new`` command
(that perhaps proxies to ``startproject``) that creates a more useful project
to start from. But which one? Both, obviously. Just ask the user.

.. code-block:: bash

    $ django-admin new
    Which type of project would you like to create?
    1: Quick start Django project
    2: Single file project
    3: A classic project
    You may also enter a path or URL to a custom template
    1
    $

Not too bad. If you like this idea, do please comment on the `draft DEP`_.

I promised two features, though. The second one is simple, and I'm `not the only one`_
to have thought of it. Rename ``django-admin`` to ``django`` and alias ``django-admin``
to it. How do you start a new Django project? Easy, ``django new``.

.. _first principles: https://www.mostlypython.com/django-from-first-principles/
.. _draft DEP: https://github.com/django/deps/pull/98
.. _not the only one: https://mastodon.social/@webology/113554514353680279
