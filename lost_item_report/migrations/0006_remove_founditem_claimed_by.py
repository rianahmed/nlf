# Generated by Django 4.1.7 on 2023-03-18 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lost_item_report', '0005_reportlostitem_item_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='founditem',
            name='claimed_by',
        ),
    ]
