# Generated by Django 2.0.3 on 2018-03-30 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TransInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zh', models.CharField(max_length=512, unique=True)),
                ('en', models.CharField(max_length=512)),
            ],
        ),
    ]