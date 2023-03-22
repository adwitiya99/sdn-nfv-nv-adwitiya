# Generated by Django 4.1.5 on 2023-01-11 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usermanagement',
            fields=[
                ('idusermanagement', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200)),
                ('userrole', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'usermanagement',
            },
        ),
    ]
