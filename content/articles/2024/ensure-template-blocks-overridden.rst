Ensuring a block is overridden in a Django template
###################################################

:date: 2024-09-22
:tags: django, templates
:has_code: true

Some bugs are hard to even notice. For example, what if you forgot
to add a title to one of your web pages? Oops! You're probably left
with a generic title of only your site name, or worse, no title at all.
And it's very tricky to spot this. Most people testing a page won't even
look at the title, they will go straight to the content.

We could write a script to track down all the pages without a title, but
this is probably a time-consuming task, and you'll need to remember to run
this, or put it in CI and slow your build down. But an ounce of prevention
is worth a pound of cure. Let's make sure we can't forget to add a title
for our pages. We can do this by putting a block on our base template that
must be overridden in extending templates.

Let's assume we have a simple Django base template like this:

.. code-block:: html+django

    <!doctype html>
    <html lang="tok">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{% block title %}{% endblock %} - kulupu mi</title>
    </head>
    <body>
        {% block content %}{% endblock %}
    </body>
    </html>


And our home page template extending it:

.. code-block:: html+django

    {% extends "base.html" %}

    {% block content %}
        <h1>kama pona</h1>
        <p>toki! mi jan Tami!</p>
    {% endblock %}

This will render the title as " - kulupu mi" on the home page. Oopsie.

Okay, let's actually fix this. All we need to do is add a template tag that
raises an exception, and stick it in the right place in the base template.

.. code-block:: python

    from django import template

    register = template.Library()


    class BlockNotOverriddenError(NotImplementedError):
        pass


    @register.simple_tag
    def ensure_overridden():
        raise BlockNotOverriddenError

I choose to create a new exception class, `BlockNotOverriddenError`, to make
it clear what the error is, and make it easier to test, based on a
`blog post on handling exceptions`_.

Then in our template, a single change on the title line:

.. code-block:: html+django

    <!doctype html>
    <html lang="tok">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{% block title %}{% ensure_overridden %}{% endblock %} - kulupu mi</title>
    </head>
    <body>
        {% block content %}{% endblock %}
    </body>
    </html>

Now if we try to extend this without overriding the title block, we'll get
an exception when we try to load the page, and our tests will fail. You
did write a test for this page, right?

In your next (or current) Django project, don't run into this class of bug
anymore. Throw in this single line template tag and improve your SEO.

.. _blog post on handling exceptions: https://guicommits.com/handling-exceptions-in-python-like-a-pro/
