# Generated by Django 2.1.1 on 2019-03-28 19:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.Account')),
            ],
            options={
                'db_table': 'route',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.TextField(unique=True)),
                ('weight', models.PositiveIntegerField(default=0)),
                ('priority', models.PositiveIntegerField(default=0)),
                ('socket', models.CharField(max_length=128)),
                ('state', models.IntegerField(default=0)),
                ('attrs', models.CharField(max_length=128)),
                ('algorithm', models.PositiveIntegerField(default=8)),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('kind', models.TextField()),
                ('host', models.TextField(blank=True, null=True)),
                ('port', models.PositiveIntegerField(default=5060)),
                ('transport', models.TextField(default='udp')),
                ('channels', models.PositiveIntegerField(default=0)),
                ('enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='server.Route')),
            ],
            options={
                'db_table': 'server',
            },
        ),
    ]
