Testing Django data migrations
##############################

:date: 2022-01-12
:tags: django, testing, migrations
:has_code: true

You probably already know the value of testing your code.
Your Django migrations are code, therefore you should test them.
However, testing data migrations in particular can be tricky,
and there's no documentation on how to do it.

Typically your schema migrations don't need any testing as your
migrations are run during tests, unless you're `skipping migrations`_
to speed up your tests. I recommend against doing this, but that's another
blog post.

However, only your data migrations *forwards* are tested. Even then, they are
only tested if they don't have any branching, and if there is something to do.
Most data migrations during tests have nothing to do because there is no data
during migrations to run against. But why test data migrations in the first
place?

Why test your data migrations?
==============================

I often use data migrations for a few purposes. The first is to add initial data.
For example, you might want to store a list of countries in the database. You don't
want to add them directly to the database, but you want them to always be there,
and if some new country is formed  in the future, you can add it in another data
migration, say. This could also be done with a management command or in a multitude
of other ways, so it's not the main reason for using a data migration.

The other reason is probably more useful. You'll often have a new requirement that
needs you to restructure your database, and as a part of that, you have to make a
change to some of your data. For example, you might decide to add a required username
to your user model, and to populate the initial values, you want to use the first part
of the user's email address. Please don't do this in real life. Generating public
information from private information is not very good for a user's privacy.

Testing these with real data is important. You may have users in your database with
valid emails where the username part wouldn't validate as a username. As migrations
are typically only ran once in production, you'll certainly find out when you deploy
and run your migrations that something is wrong. However, is the data in your staging
environment as good as that in your production environment? Even if it is,
it would be nice to find these problems earlier, and without the stress of dealing
with potential problems that aborting a deployment can entail.

How to test your data migrations?
=================================

If you find yourself doing this a lot, there is a package called
`django-test-migrations`_. I haven't used it myself but it will probably have
fewer problems than the simple apprach below.
However, if you're averse to installing yet another package, let's see what
we can put together without too much work.

Let's use the example above and say we have the following data migration:

..  code-block:: python

    from django.db import migrations

    def populate_usernames(apps, schema_editor):
        User = apps.get_model("accounts", "User")
        for user in User.objects.all():
            user.username = user.email.rpartition("@")[0]
            user.save()

    def depopulate_usernames(apps, schema_editor):
        User = apps.get_model("accounts", "User")
        User.objects.update(username=None)

    class Migration(migrations.Migration):
        dependencies = [("accounts", "0002_add_username")]
        operations = [migrations.RunPython(populate_usernames, depopulate_usernames)]


To test migrations like this, I decided to write a small class to
run the migrations. You may notice that this is a class with a single
method and ``__init__``, so it could just be a function, but setting
the ``apps`` attribute felt better than returning ``apps`` directly.

.. code-block:: python

    from django.db import connection
    from django.db.migrations.executor import MigrationExecutor


    class Migrator:
        def __init__(self, connection=connection):
            self.executor = MigrationExecutor(connection)

        def migrate(self, app_label: str, migration: str):
            target = [(app_label, migration)]
            self.executor.loader.build_graph()
            self.executor.migrate(target)
            self.apps = self.executor.loader.project_state(target).apps


There's not too much going on here. We initialise the class with a
migration executor, using a passed connection, or the default connection
if none is passed. Then you can run the ``migrate`` method, with your app
label and migration name. This will run the migration and set the ``apps``
attribute that you'll use in your test to make sure you have the right
version of the models, similar to how it's used in the data migration itself.

Using the migrator in pytest is pretty simple.
We can write a single-line fixture:

.. code-block:: python

    @pytest.fixture
    def migrator():
        return Migrator

Then we can write our tests, migrating to where we need to be:

.. code-block:: python

    @pytest.mark.django_db
    def test_populate_emails(migrator):
        migrator = migrator()
        migrator.migrate("accounts", "0002_add_username")
        User = migrator.apps.get_model("accounts", "User")
        user = User.objects.create_user(email="test123@example.com")
        assert user.username is None

        migrator.migrate("accounts", "0003_populate_usernames")
        assert User.objects.filter(email="test123@example.com", username="test123").exists()

Of course, we can also migrate backwards. Typically, migrating backwards
is only used when developing, but in case you want that 100% coverage or
really want to be sure:

.. code-block:: python

    @pytest.mark.django_db
    def test_depopulate_emails(migrator):
        migrator = migrator()
        migrator.migrate("accounts", "0002_add_username")
        User = migrator.apps.get_model("accounts", "User")
        user = User.objects.create_user(email="test123@example.com")
        migrator.migrate("accounts", "0003_populate_usernames")
        migrator.migrate("accounts", "0002_add_username")
        User = migrator.apps.get_model("accounts", "user")
        assert User.objects.get(email="test123@example.com").username is None

unittest
--------

If you're using Django's default unittest framework,
you can use it in much the same way:

.. code-block:: python

    from django.test import TestCase


    class MigrationTest(TestCase):
        def setUp(self):
            self.migrator = Migrator()
            self.migrator.migrate("accounts", "0002_add_username")

        def test_populate_usernames(self):
            User = self.migrator.apps.get_model("accounts", "User")
            user = User.objects.create_user(email="test123@example.com")
            assert user.username is None

            migrator.migrate("accounts", "0003_populate_usernames")
            assert User.objects.filter(
                email="test123@example.com", username="test123"
            ).exists()

        def test_depopulate_emails(migrator):
            User = migrator.apps.get_model("accounts", "User")
            user = User.objects.create_user(email="test123@example.com")
            migrator.migrate("accounts", "0003_populate_usernames")
            migrator.migrate("accounts", "0002_add_username")
            User = migrator.apps.get_model("accounts", "user")
            assert User.objects.get(email="test123@example.com").username is None


So, get out there and test those data migrations.


.. _skipping migrations: https://docs.djangoproject.com/en/4.0/ref/settings/#migrate
.. _django-test-migrations: https://github.com/wemake-services/django-test-migrations
