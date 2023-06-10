# Generated by Django 4.2.1 on 2023-06-10 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lost_item_report', '0013_founditem_is_admin_approved_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportlostitem',
            name='reporter_name',
        ),
        migrations.RemoveField(
            model_name='reportlostitem',
            name='reporter_phone',
        ),
        migrations.AddField(
            model_name='reportlostitem',
            name='reported_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, related_name='reported_lost_item_user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='founditem',
            name='is_admin_approved',
            field=models.BooleanField(default=False, help_text='Only This field value true Found Item will be shown on frontend list'),
        ),
    ]