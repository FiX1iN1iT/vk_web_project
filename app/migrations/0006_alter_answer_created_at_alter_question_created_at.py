# Generated by Django 4.2.6 on 2024-01-02 09:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_answervote_questionvote_alter_answer_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='created_at',
            field=models.DateField(default=datetime.date(2024, 1, 2)),
        ),
        migrations.AlterField(
            model_name='question',
            name='created_at',
            field=models.DateField(default=datetime.date(2024, 1, 2)),
        ),
    ]
