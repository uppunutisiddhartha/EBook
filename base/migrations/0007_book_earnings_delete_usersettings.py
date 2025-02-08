# Generated by Django 5.1.3 on 2024-11-25 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_lecturer_zoom_link_usersettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='earnings',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='UserSettings',
        ),
    ]
