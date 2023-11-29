# Generated by Django 4.2.4 on 2023-11-29 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0004_alter_uom_weightage'),
        ('production', '0005_remove_bomcomponent_uom_rawmaterialcomponent_uom_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rawmaterialcomponent',
            name='uom',
        ),
        migrations.AddField(
            model_name='bomcomponent',
            name='uom',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='misc.uom'),
            preserve_default=False,
        ),
    ]