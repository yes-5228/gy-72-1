import uuid

from django.db import migrations, models


def populate_cancel_tokens(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    for order in Order.objects.all():
        order.cancel_token = uuid.uuid4()
        order.save(update_fields=["cancel_token"])


def reverse_populate(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="cancel_token",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
            preserve_default=False,
        ),
        migrations.RunPython(populate_cancel_tokens, reverse_populate),
        migrations.AlterField(
            model_name="order",
            name="cancel_token",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
