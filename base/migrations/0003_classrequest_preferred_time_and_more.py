# Generated by Django 5.1.3 on 2024-11-21 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_lecturer_subject_rename_time_slot_classrequest_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classrequest',
            name='preferred_time',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classrequest',
            name='selected_item',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='classrequest',
            name='category',
            field=models.CharField(choices=[('M1', 'M1'), ('DS', 'DS')], max_length=50),
        ),
    ]
