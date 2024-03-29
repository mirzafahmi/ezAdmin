# Generated by Django 4.2.4 on 2023-11-18 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('purchasing', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BOMComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_used', models.FloatField(default=0)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rH', models.FloatField()),
                ('temperature', models.FloatField()),
                ('quantity_produced', models.PositiveIntegerField()),
                ('lot_number', models.CharField(blank=True, max_length=200, null=True)),
                ('exp_date', models.CharField(blank=True, max_length=200, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('BOMComponents', models.ManyToManyField(to='production.bomcomponent')),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterialComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component', models.CharField(blank=True, max_length=200, null=True)),
                ('spec', models.CharField(blank=True, max_length=200, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RawMaterialIdentifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_item_code', models.CharField(max_length=20, unique=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RawMaterialInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('lot_number', models.CharField(blank=True, max_length=200, null=True)),
                ('exp_date', models.CharField(blank=True, max_length=200, null=True)),
                ('price_per_unit', models.CharField(blank=True, max_length=200, null=True)),
                ('stock_type', models.CharField(choices=[('1', 'Stock-in'), ('2', 'Stock-Out')], default=1, max_length=2)),
                ('stock_in_date', models.DateTimeField(blank=True, null=True)),
                ('stock_out_date', models.DateTimeField(blank=True, null=True)),
                ('validation_date', models.DateTimeField(blank=True, null=True)),
                ('log_date', models.DateTimeField(blank=True, null=True)),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='production.rawmaterialcomponent')),
                ('production_log', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='production.productionlog')),
                ('purchasing_doc', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='purchasing.purchasingdocument')),
                ('stock_in_tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='stock_in_tag_entries', to='production.rawmaterialinventory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='rawmaterialcomponent',
            name='identifier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='production.rawmaterialidentifier'),
        ),
        migrations.AddField(
            model_name='bomcomponent',
            name='raw_material_component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='production.rawmaterialcomponent'),
        ),
    ]
