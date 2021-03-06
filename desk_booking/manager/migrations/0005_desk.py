# Generated by Django 4.0.4 on 2022-05-27 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_alter_floor_parent_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left_up_x', models.IntegerField()),
                ('left_up_y', models.IntegerField()),
                ('right_down_x', models.IntegerField()),
                ('right_down_y', models.IntegerField()),
                ('parent_floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.floor')),
            ],
        ),
    ]
