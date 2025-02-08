# Generated by Django 5.1.3 on 2024-11-20 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.RenameField(
            model_name='classrequest',
            old_name='time_slot',
            new_name='time',
        ),
        migrations.RemoveField(
            model_name='classrequest',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='classrequest',
            name='question_or_topic',
        ),
        migrations.RemoveField(
            model_name='classrequest',
            name='whatsapp_number',
        ),
        migrations.AddField(
            model_name='classrequest',
            name='category',
            field=models.CharField(choices=[('Math', 'Mathematics'), ('Science', 'Science')], default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classrequest',
            name='rejection_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='classrequest',
            name='topic',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classrequest',
            name='zoom_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='classrequest',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
        migrations.DeleteModel(
            name='LecturerResponse',
        ),
    ]
