# Generated by Django 4.0.4 on 2023-02-11 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0009_alter_rsvp_first_course_alter_rsvp_second_course'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('first_name', 'email')},
        ),
    ]
