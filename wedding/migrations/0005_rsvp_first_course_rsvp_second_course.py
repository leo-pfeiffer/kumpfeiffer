# Generated by Django 4.0.4 on 2023-01-07 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0004_remove_allergy_guest_delete_allergysummary_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rsvp',
            name='first_course',
            field=models.CharField(choices=[('chicken', 'Chicken'), ('fish', 'Fish')], default='chicken', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rsvp',
            name='second_course',
            field=models.CharField(choices=[('chicken', 'Chicken'), ('fish', 'Fish')], default='chicken', max_length=50),
            preserve_default=False,
        ),
    ]
