# Generated by Django 4.2 on 2023-04-11 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255, verbose_name='Word')),
                ('gender', models.CharField(choices=[('male', 'Мужской'), ('neuter', 'Средний'), ('femail', 'Женский')], max_length=6, verbose_name='Gender')),
            ],
        ),
    ]