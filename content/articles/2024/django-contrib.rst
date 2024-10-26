What to do with django.contrib?
###############################

:date: 2024-10-26
:tags: django

Recently, Andrew Miller, also known as nanorepublica on Discord and through his
consultancy, Software Crafts, recently wrote `a blog post on django.contrib`_
and another on `its future`_. I'm not sure how I feel about Mr. Miller's
suggestions, but I do agree with him that it's quite confusing and does raise
some questions.

I will first answer Mr. Republica's fourth question: "What is the meaning of
``contrib`` with in Django?"

What is ``contrib`` for?
========================

This is answered clearly by the `contrib reference docs`_, they are optional
extra batteries included in Django.

Optional, you say? Let's have a look at a few of the things in ``contrib``.

``admin`` and ``admindocs``
---------------------------

The admin has been called Django's killer app. It's optional, but I'm not sure
I've ever spun up a project without it.

``auth`` and ``sessions``
-------------------------

Not every project needs auth, but almost all do, and it's required for
the admin. Django is supposed to be "secure by default". I suppose by not
allowing anyone to login, you are quite secure, but I feel that's taking things
a bit too far.

``contenttypes``
----------------

Here's one I really take issue with. It's used in a lot of places.
Okay, if I never use generic foreign keys I suppose it's optional, but if core
parts of Django are calling into it, that doesn't seem right to me.

It's also used by the admin, and by ``contrib.auth``.

``messages``
------------

Optional for sure, but used heavily in the admin.

----

Many of the others I don't take much issue with fundamentally. But I'm not sure
they need to be bundled into this namespace that isn't really what the name
implies it is.

The future
==========

Now I'd like to address Mr. Craft's questions five through eight.
At the very least, I suggest moving the above packages up a level.
We would have ``django.admin`` and ``django.admin.docs``, not
``django.contrib.admin`` and ``django.contrib.admindocs``. We'd need a
(possibly extended or forever)  deprecation period of course, but I think it
sends the right message about these apps.

For the others, such as ``flatpages``, ``sitemaps``, and so on, I am less
certain. Possibly they don't need to be directly under the ``django``
namespace (but also, why not?). ``humanize`` could easily go in with the rest
of the built in template tags. In any case ``contrib`` still feels like a
misnomer to me.

I would also point out that many things in "core" Django are perfectly
optional. Even the ORM needn't be used. But smaller things, such as pagination
live in core but often go unused, and aren't used by other core parts of
Django.

One other personal problem with ``contrib`` is that every time I type it, I
type it as ``contrub``. I have no idea why, but nuking it would be nice.

We already seem to be starting on a trajectory of not putting things into
``contrib``. During all the discussion of `django-tasks`_, it seems like a
given that it will land as ``django.tasks`` rather than
``django.contrib.tasks`` despite it clearly being an optional battery, and one
that will probably see less use than ``contrib.admin``. Personally, I am
fully on board with this, but now ``contrib.admin`` makes little sense.

And ``django.core``, don't think you are getting away unscathed. why not simply
``django.cache``, ``django.checks``, ``django.management``, etc?

.. _a blog post on django.contrib: https://softwarecrafts.co.uk/100-words/day-198
.. _its future: https://softwarecrafts.co.uk/100-words/day-199
.. _contrib reference docs: https://docs.djangoproject.com/en/5.1/ref/contrib/
.. _django-tasks: https://github.com/django/deps/blob/main/accepted/0014-background-workers.rst
