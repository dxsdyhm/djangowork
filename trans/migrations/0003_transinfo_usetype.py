# Generated by Django 2.0.3 on 2018-03-30 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trans', '0002_auto_20180330_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='transinfo',
            name='useType',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]