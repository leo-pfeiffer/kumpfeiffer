# Generated by Django 4.0.4 on 2023-03-15 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0012_alter_rsvp_first_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rsvp',
            name='first_course',
            field=models.CharField(choices=[('cheese-salad', 'Butternut Squash and Sweet Potato Soup / Butternusskürbis- und Süßkartoffelsuppe'), ('salmon-salad', 'Salad with Loch Fyne Braden smoked salmon / Salat mit Loch Fyne Braden Räucherlachs')], max_length=50),
        ),
    ]