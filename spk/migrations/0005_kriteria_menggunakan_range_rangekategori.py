# Generated by Django 5.1.3 on 2024-12-05 08:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spk', '0004_alter_kriteria_bobot'),
    ]

    operations = [
        migrations.AddField(
            model_name='kriteria',
            name='menggunakan_range',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='RangeKategori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('nilai', models.FloatField()),
                ('kriteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='range_kategori', to='spk.kriteria')),
            ],
        ),
    ]
