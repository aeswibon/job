# Generated by Django 5.0.3 on 2024-03-06 18:41

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Job",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uuid",
                    models.UUIDField(db_index=True, default=uuid.uuid4, unique=True),
                ),
                ("position", models.CharField(max_length=255)),
                ("company", models.CharField(max_length=255)),
                ("location", models.CharField(max_length=255)),
                ("company_logo", models.URLField(blank=True, null=True)),
                ("date", models.DateField()),
                ("ago_date", models.CharField(blank=True, max_length=255, null=True)),
                ("salary", models.CharField(blank=True, max_length=255, null=True)),
                ("deleted", models.BooleanField(default=False)),
                ("url", models.URLField(max_length=400, unique=True)),
            ],
            options={
                "verbose_name": "Job",
                "verbose_name_plural": "Jobs",
                "db_table": "job",
                "ordering": ["-date"],
            },
        ),
    ]