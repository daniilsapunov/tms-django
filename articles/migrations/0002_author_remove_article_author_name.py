# Generated by Django 5.0 on 2024-01-23 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='author_name',
        ),
    ]
