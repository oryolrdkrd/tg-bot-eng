# Generated by Django 4.2 on 2023-04-21 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='words',
            name='translation_base',
            field=models.CharField(default='xxxx', max_length=255, verbose_name='Translation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='words',
            name='user_id',
            field=models.CharField(default='xxxxx', max_length=255, verbose_name='User_ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='words',
            name='gender',
            field=models.CharField(choices=[('male', 'Мужской'), ('neuter', 'Средний'), ('female', 'Женский')], max_length=6, verbose_name='Gender'),
        ),
    ]