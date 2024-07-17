# Generated by Django 4.2.13 on 2024-07-09 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0003_remove_submission_admin_comments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='birth_certificate',
            field=models.FileField(blank=True, null=True, upload_to='static/documents/'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='highschool_certificate',
            field=models.FileField(blank=True, null=True, upload_to='static/documents/'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='secondary_certificate',
            field=models.FileField(blank=True, null=True, upload_to='static/documents/'),
        ),
    ]