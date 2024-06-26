# Generated by Django 2.2.19 on 2023-10-22 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genes',
            fields=[
                ('ID', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CUTAR_ID',  models.CharField(blank=True, max_length=128, null=True)),
                ('CHROMOSOME',  models.CharField(blank=True, max_length=128, null=True)),
                ('START', models.IntegerField(blank=True, null=True)),
                ('END', models.IntegerField(blank=True, null=True)),
                ('TRANSCRIPT', models.CharField(blank=True, max_length=128, null=True)),
                ('STRAND', models.CharField(blank=True, max_length=1, null=True)),
                ('SAMPLES_DETECTED', models.CharField(blank=True, max_length=1024, null=True)),
                ('CANCER_TYPES_DETECTED', models.CharField(blank=True, max_length=1024, null=True)),
                ('CELL_TYPE_SPECIFICITY', models.CharField(blank=True, max_length=1024, null=True)),
                ('CELL_TYPE_SPECIFICITY_IN_CANCER_TYPE', models.CharField(blank=True, max_length=1024, null=True)),
                ('DETECTION_IN_OTHER_DATABASES', models.CharField(blank=True, max_length=128, null=True)),
                ('ID_IN_OTHER_DATABASES', models.CharField(blank=True, max_length=128, null=True)),
                ('NONCODEID', models.CharField(blank=True, max_length=128, null=True)),
                ('DISEASE', models.CharField(blank=True, max_length=128, null=True)),
                ('GENE', models.CharField(blank=True, max_length=128, null=True)),
                ('VALIDATION', models.CharField(blank=True, max_length=128, null=True)),
                ('CLASSIFICATION', models.CharField(blank=True, max_length=128, null=True)),
                ('OVERLAPPING_PROMOTER', models.CharField(blank=True, max_length=1024, null=True)),
                ('OVERLAPPING_ENHANCER', models.CharField(blank=True, max_length=1024, null=True)),
                ('ENHANCER_ASSOCIATED', models.CharField(blank=True, max_length=1024, null=True)),
                ('OVERLAPPING_SNPS', models.CharField(blank=True, max_length=1024, null=True)),
                ('OVERLAPPING_ORF', models.CharField(blank=True, max_length=1024, null=True)),
            ],
            options={
                'db_table': 'genes',
            },
        ),
    ]
