# Generated by Django 2.2.18 on 2021-02-26 23:53

from django.db import migrations, models
from django.db.models.functions import Concat
from polaris import settings
from polaris.shared.endpoints import SEP6_MORE_INFO_PATH
from polaris.sep24.urls import SEP24_MORE_INFO_PATH


def populate_more_info_urls(apps, _):
    Transaction = apps.get_model("polaris", "Transaction")
    if "sep-24" in settings.ACTIVE_SEPS:
        Transaction.objects.filter(protocol="sep24").update(
            more_info_url=Concat(
                models.Value(f"{settings.HOST_URL}{SEP24_MORE_INFO_PATH}?id="),
                models.F("id"),
                output_field=models.TextField(null=True, blank=True),
            ),
        )
    if "sep-6" in settings.ACTIVE_SEPS:
        Transaction.objects.filter(protocol="sep6").update(
            more_info_url=Concat(
                models.Value(f"{settings.HOST_URL}{SEP6_MORE_INFO_PATH}?id="),
                models.F("id"),
                output_field=models.TextField(null=True, blank=True),
            ),
        )


def noop(*_):
    # the DB column can be dropped without any reversal logic
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("polaris", "0005_auto_20210226_0053"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="more_info_url",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RunPython(populate_more_info_urls, noop),
    ]
