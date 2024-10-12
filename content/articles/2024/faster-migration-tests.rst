Faster migration tests
######################

:date: 2024-10-12
:tags: django, migrations
:has_code: true

Almost invariably when I start to work at a new company, I look at their
linting configuration and find something like this:

.. code-block:: toml

    [tool.coverage.run]
    branch = true
    omit = ["**/migrations/*"]

    [tool.ruff]
    exclude = ["**/migrations/*"]

My suspicion about how prevalent this is is confirmed by GitHub Copilot
suggesting it to me the instant I type ``omit =``.

I guess there is a reason they are hiring me.

It feels to me a lot like many people think migrations are just
automatically generated nonsense to be hidden and never looked at again.
I often see questions on the `Django Discord`_ about if you should commit
migrations to your repository. If you're wondering, the answer is yes.
I suspect that this isn't clear enough in the Django documentation.

Migrations are code. They are often automatically generated, but not always.
And in every case they should be read and understood, especially if you're
interested in `zero-downtime deployments`_. Even if you're not, why would you
not care about understanding and testing code that is crucial to your next
deployment and can easily bring your site down?
How can you be reasonably sure it will work?

So yes, please lint and format them. With modern tooling such as `ruff`_
this is very easy. But I want to talk `(again)`_ about testing them.

In the previous article I outlined a way to test data migrations, and briefly
mentioned a package that I haven't used. This package,
`django-test-migrations`_ is great. It solves a lot of edge cases you can run
into when trying this yourself with the method I gave before.

However, it's also very slow. Each test can take several seconds to run.
For code that is only run once per environment, this seems a little overkill.
I have a solution that I've been using for a while now. I wouldn't say I'm
happy with it, but it works. I will call it "pre-squashing", because that's
the name that came to my head. I'm not sure if it's even a good name.

For a simple data migration:

.. code-block:: python
    :linenos:

    from django.db import migrations


    def migrate_name(apps, schema_editor):
        Thing = apps.get_model("myapp", "Thing")
        Thing.objects.filter(name="default").update(name="New default")


    class Migration(migrations.Migration):
        dependencies = [("myapp", "0001_initial")]
        operations = [migrations.RunPython(migrate_name)]

Now we need to write a test to cover lines 3 to 5. I'll leave this as an exercise
for the reader. But after you've deployed your app to all deployments, we have
this test that takes three seconds to run and doesn't really test anything
relevant anymore. Three seconds is not too long, but when you have 10 of these,
suddenly that's a lot of time added to your CI build.

So once I am sure that the migration has ran across all deployments, I will
pretend it never happened. I will remove the code in the migration so it looks
like this:

.. code-block:: python

    from django.db import migrations


    class Migration(migrations.Migration):
        dependencies = [("myapp", "0001_initial")]
        operations = []

And at this point I will simply remove the test and pretend that never existed
either.

I wouldn't say it's an amazing solution. We lose a bit of history from our
migrations, but I feel it's no worse than squashing migrations, and the
history is still there in version control. But to me, it regains lost CI speed
with little tangible downside.

Maybe someone can tell me why this is a horrible idea 🙂.

.. _Django Discord: https://discord.gg/xcRH6mN4fa
.. _zero-downtime deployments: https://www.better-simple.com/django/2024/07/22/django-safemigrate/
.. _ruff: https://astral.sh/ruff
.. _(again): {filename}../2022/testing_data_migrations.rst
.. _django-test-migrations: https://github.com/wemake-services/django-test-migrations
