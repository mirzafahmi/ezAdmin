# Generated by Django 4.2.4 on 2023-10-12 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_alter_quotationitem_quotation'),
        ('purchasing', '0005_alter_rawmaterialinventory_exp_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasingdocument',
            name='AWB_doc',
            field=models.FileField(default=0, upload_to='purchasing_documents/AWB'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchasingdocument',
            name='AWB_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='rawmaterialinventory',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='currency_trade',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='dashboard.currency'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchasingdocument',
            name='invoice_doc',
            field=models.FileField(upload_to='purchasing_documents/invoice'),
        ),
        migrations.AlterField(
            model_name='purchasingdocument',
            name='k1_doc',
            field=models.FileField(upload_to='purchasing_documents/K1'),
        ),
        migrations.AlterField(
            model_name='purchasingdocument',
            name='pl_doc',
            field=models.FileField(upload_to='purchasing_documents/PL'),
        ),
        migrations.AlterField(
            model_name='purchasingdocument',
            name='po_doc',
            field=models.FileField(upload_to='purchasing_documents/PO'),
        ),
    ]
