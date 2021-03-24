# Generated by Django 3.1.7 on 2021-03-24 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[("ALTER TABLE Country ADD UNIQUE (name);")],
            reverse_sql=[("ALTER TABLE Country DROP CONSTRAINT country_name_key;")],
        )
    ]
