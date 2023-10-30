# Generated by Django 4.2.5 on 2023-10-30 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("purchasing", "0007_remove_rawmaterialinventory_create_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="rawmaterialinventory",
            name="stock_in_tag",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="stock_in_tag_entries",
                to="purchasing.rawmaterialinventory",
            ),
        ),
        migrations.AlterField(
            model_name="rawmaterialcomponent",
            name="component",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
