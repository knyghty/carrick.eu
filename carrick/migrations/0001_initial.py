# Generated by Django 3.0.6 on 2020-05-26 12:13

from django.conf import settings
from django.db import migrations


def set_site(apps, schema_editor):
    Site = apps.get_model("sites.Site")
    Site.objects.update_or_create(
        id=settings.SITE_ID, defaults={"domain": "carrick.eu"}
    )


def unset_site(apps, schema_editor):
    Site = apps.get_model("sites.Site")
    Site.objects.filter(domain="carrick.eu").delete()


class Migration(migrations.Migration):
    dependencies = [("sites", "0002_alter_domain_unique")]
    operations = [migrations.RunPython(set_site, unset_site)]
