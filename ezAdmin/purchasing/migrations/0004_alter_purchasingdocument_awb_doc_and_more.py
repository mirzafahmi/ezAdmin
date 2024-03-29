# Generated by Django 4.2.4 on 2023-11-26 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0003_alter_purchasingdocument_awb_doc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasingdocument',
            name='AWB_doc',
            field=models.FileField(help_text='Maximum file size: 5 MB. Allowed extensions: .pdf', upload_to='purchasing_documents/AWB'),
        ),
        migrations.AlterField(
            model_name='purchasingdocument',
            name='invoice_doc',
            field=models.FileField(help_text='Maximum file size: 5 MB. Allowed extensions: .pdf', upload_to='purchasing_documents/invoice'),
        ),
        migrations.AlterField(
            model_name='purchasingdocument',
            name='k1_doc',
            field=models.FileField(help_text='Maximum file size: 5 MB. Allowed extensions: .pdf', upload_to='purchasing_documents/K1'),
        ),
        migrations.AlterField(
            model_name='purchasingdocument',
            name='pl_doc',
            field=models.FileField(help_text='Maximum file size: 5 MB. Allowed extensions: .pdf', upload_to='purchasing_documents/PL'),
        ),
        migrations.AlterField(
            model_name='purchasingdocument',
            name='po_doc',
            field=models.FileField(help_text='Maximum file size: 5 MB. Allowed extensions: .pdf', upload_to='purchasing_documents/PO'),
        ),
    ]
