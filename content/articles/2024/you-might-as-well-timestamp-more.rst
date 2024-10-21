You might as well timestamp more things
#######################################

:date: 2024-10-21
:tags: django
:has_code: true

`You might as well timestamp it`_ was a post doing the rounds a few years ago.
It suggests using timestamps rather than booleans just to have the extra data
point of when something happened.

Lately I found myself in a different, but related situation. I had something
like the following model:

.. code-block:: python

    from django.db import models


    class Order(models.Model):
        class Status(models.TextChoices):
            PLACED = "placed", "placed"
            SHIPPED = "shipped", "shipped"

        ...
        status = models.CharField(choices=Status.choices, db_default=Status.PLACED)
        date_ordered = models.DateTimeField(db_default=Now())
        date_shipped = models.DateTimeField(null=True, blank=True)

I want to know the status of an order, and also the dates that these statuses
were entered. It's a very simple type of state machine where there is only one
direction of movement. It can go from placed to shipped, and that's all.
If the status is more complex, it can go between states in different ways or
multiple times, there are options such as audit logs, finite state machines,
event sourcing, and maybe more I don't know about. But for this simple case,
I'd rather avoid this extra complexity.

However, there's still a bit of an issue here. What is the source of truth? Is
it the status, or the dates? What if ``date_shipped`` is set, but the status is
set to ``PLACED``? All this gets messier if we were to add more statuses.
It's likely users will want to know when their order is delivered, or they may
want to cancel or return orders. There are several ways to solve this problem.

One solution is to add a database constraint ensuring that the status matches
up with the dates. This works quite well, though I find it slightly lacking in
that you still have to make sure that you always change the status correctly
when you change the dates, or you will hit a server error (or a validation
error in the admin). We can do better, by only storing the timestamps and
deriving the status from them, e.g.:

.. code-block:: python

    from django.db import models


    class Order(models.Model):
        class Status(models.TextChoices):
            PLACED = "placed", "placed"
            SHIPPED = "shipped", "shipped"

        ...
        date_ordered = models.DateTimeField(db_default=Now())
        date_shipped = models.DateTimeField(null=True, blank=True)

        @property
        def status(self):
            if self.date_shipped:
                return self.Status.SHIPPED
            return self.Status.PLACED

However, it's now much more annoying to query by status, filter in the admin,
etc. We need to reproduce the logic every time. And it's likely pretty tough
to index well for every case, especially once we add more fields, so you might
end up with some slow queries.

Luckily the Django 5.0 release was near when I was thinking about this
problem, and the new `GeneratedField`_ turned out to be just what I needed.
With it, we can move this logic into the database:

.. code-block:: python

    from django.db import models
    from django.db.models import Case, When, Value


    class Order(models.Model):
        class Status(models.TextChoices):
            PLACED = "placed", "placed"
            SHIPPED = "shipped", "shipped"

        ...
        date_ordered = models.DateTimeField(db_default=Now())
        date_shipped = models.DateTimeField(null=True, blank=True)
        status = models.GeneratedField(
            db_persist=True,
            output_field=models.CharField(),
            choices=Status,
            expression=(
                Case(
                    When(date_shipped__isnull=False, then=Value(Status.SHIPPED)),
                    default=Value(Status.PLACED),
                )
            ),
        )

Our new status field will always be correct, as it's derived from the dates.
We can also query it in a very simple way, and admin filters will just work.
As it's persisted to the database, we can index it easily, so these queries
can be fast. Adding new statuses is fairly straightforward, just add a new
choice, ``DateTimeField``, and a clause to the ``GeneratedField`` expression.
Everything in one place, and all we need to do to change status is to set the
right ``DateTimeField``.

The one remaining problem is that the dates can still be inconsistent.
For example, nothing is stopping you from having an order that has been
delivered but not shipped. This can be fixed with database constraints, but
I'll leave that as an exercise for the reader. I imagine it's also possible to
define some kind of finite state machine schema and automatically generate
the ``GeneratedField`` and constraints, but that one is also definitely an
exercise for the reader.

It's been suggested that you might as well timestamp your booleans. I
wouldn't go so far as to suggesting that you also timestamp your status fields,
but if you need to, this feels like a pretty good way to do it.

.. _You might as well timestamp it: https://changelog.com/posts/you-might-as-well-timestamp-it
.. _GeneratedField: https://docs.djangoproject.com/en/dev/ref/models/fields/#generatedfield
