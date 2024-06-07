from django.db import models

# Create your models here.

class Genes(models.Model):
    cutar_id = models.CharField(max_length=128, blank=True, null=True)
    chromosome = models.CharField(max_length=128, blank=True, null=True)
    start = models.IntegerField(blank=True, null=True)
    end = models.IntegerField(blank=True, null=True)
    transcript = models.CharField(max_length=128, blank=True, null=True)
    strand = models.CharField(max_length=1, blank=True, null=True)
    samples_detected = models.CharField(max_length=1024, blank=True, null=True)
    cancer_types_detected = models.CharField(max_length=1024, blank=True, null=True)
    cell_type_specificity = models.CharField(max_length=1024, blank=True, null=True)
    cell_type_specificity_in_cancer_type = models.CharField(max_length=1024, blank=True, null=True)
    detection_in_other_databases = models.CharField(max_length=128, blank=True, null=True)
    id_in_other_databases = models.CharField(max_length=128, blank=True, null=True)
    noncodeid = models.CharField(max_length=128, blank=True, null=True)
    disease = models.CharField(max_length=128, blank=True, null=True)
    gene = models.CharField(max_length=128, blank=True, null=True)
    validation = models.CharField(max_length=128, blank=True, null=True)
    classification = models.CharField(max_length=128, blank=True, null=True)
    overlapping_promoter = models.CharField(max_length=1024, blank=True, null=True)
    overlapping_enhancer = models.CharField(max_length=1024, blank=True, null=True)
    enhancer_associated = models.CharField(max_length=1024, blank=True, null=True)
    overlapping_snps = models.CharField(max_length=1024, blank=True, null=True)
    overlapping_orf = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        db_table = 'genes'