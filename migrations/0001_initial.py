# Generated by Django 2.1.1 on 2018-09-05 19:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import kernel.utils.upload_to
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.KERNEL_PERSON_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('removed', models.DateTimeField(blank=True, default=None, editable=False, null=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=127, unique=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent_category', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='buy_and_sell.Category')),
                ('users', models.ManyToManyField(blank=True, to=settings.KERNEL_PERSON_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('removed', models.DateTimeField(blank=True, default=None, editable=False, null=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=127)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('removed', models.DateTimeField(blank=True, default=None, editable=False, null=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('picture', models.ImageField(upload_to=kernel.utils.upload_to.UploadTo('buy_and_sell', 'product_pictures'))),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RequestProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('removed', models.DateTimeField(blank=True, default=None, editable=False, null=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=127)),
                ('cost', models.IntegerField()),
                ('is_phone_visible', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='buy_and_sell.Category')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.KERNEL_PERSON_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SaleProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('removed', models.DateTimeField(blank=True, default=None, editable=False, null=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=127)),
                ('cost', models.IntegerField()),
                ('is_phone_visible', models.BooleanField(default=False)),
                ('details', models.TextField(blank=True)),
                ('warranty_detail', models.TextField(blank=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='buy_and_sell.Category')),
                ('payment_modes', models.ManyToManyField(to='buy_and_sell.PaymentMode')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.KERNEL_PERSON_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='picture',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buy_and_sell.SaleProduct'),
        ),
    ]
