# Generated by Django 3.1.2 on 2020-11-07 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='stock',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stocks.stock'),
        ),
        migrations.AlterField(
            model_name='news',
            name='link',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='press',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
