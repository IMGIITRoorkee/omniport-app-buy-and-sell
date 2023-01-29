# Generated by Django 3.2 on 2023-01-17 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buy_and_sell', '0002_auto_20221214_1921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestproduct',
            name='duration_needed',
        ),
        migrations.AddField(
            model_name='requestproduct',
            name='periodicity',
            field=models.CharField(choices=[('dly', 'Daily'), ('wky', 'Weekly'), ('mty', 'Monthly'), ('yry', 'Yearly'), ('lfs', 'Lifespan')], default='lfs', max_length=10),
        ),
        migrations.AddField(
            model_name='saleproduct',
            name='periodicity',
            field=models.CharField(choices=[('dly', 'Daily'), ('wky', 'Weekly'), ('mty', 'Monthly'), ('yry', 'Yearly'), ('lfs', 'Lifespan')], default='lfs', max_length=10),
        ),
    ]