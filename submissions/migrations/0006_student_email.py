# Generated by Django 5.0.7 on 2024-07-13 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0005_submission_is_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]