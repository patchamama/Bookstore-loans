# Generated by Django 3.2.19 on 2023-06-23 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0004_alter_loan_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='returned_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Returned'), (1, 'Loaned'), (2, 'Reserved'), (3, 'Lost')], default=1),
        ),
    ]
