# Generated by Django 4.2 on 2023-06-09 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_alter_category_category_name_alter_reply_accept'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=256)),
                ('code', models.CharField(max_length=10)),
            ],
        ),
    ]
