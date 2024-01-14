from django.db import models

# Create your models here.

class Genes(models.Model):
    ID = models.IntegerField(blank=True, null=True)
    CUTAR_ID = models.CharField(max_length=45, blank=True, null=True)
    CHROMOSOME = models.CharField(max_length=45, blank=True, null=True)
    START = models.IntegerField(blank=True, null=True)
    END = models.IntegerField(blank=True, null=True)
    TRANSCRIPT = models.CharField(max_length=1, blank=True, null=True)
    STRAND = models.CharField(max_length=809, blank=True, null=True)
    SAMPLES_DETECTED = models.CharField(max_length=5, blank=True, null=True)
    CANCER_TYPES_DETECTED = models.CharField(max_length=5, blank=True, null=True)
    CELL_TYPE_SPECIFICITY = models.CharField(max_length=5, blank=True, null=True)
    CELL_TYPE_SPECIFICITY_IN_CANCER_TYPE = models.CharField(max_length=5, blank=True, null=True)
    DETECTION_IN_OTHER_DATABASES = models.CharField(max_length=5, blank=True, null=True)
    ID_IN_OTHER_DATABASES = models.CharField(max_length=5, blank=True, null=True)
    NONCODEID = models.CharField(max_length=5, blank=True, null=True)
    DISEASE = models.CharField(max_length=45, blank=True, null=True)
    GENE = models.CharField(max_length=45, blank=True, null=True)
    CLASSIFICATION = models.CharField(max_length=45, blank=True, null=True)
    OVERLAPPING_PROMOTER = models.CharField(max_length=45, blank=True, null=True)
    OVERLAPPING_ENHANCER = models.CharField(max_length=45, blank=True, null=True)
    ENHANCER_ASSOCIATED = models.CharField(max_length=45, blank=True, null=True)
    OVERLAPPING_SNPS = models.CharField(max_length=45, blank=True, null=True)
    CODING_POTENTIAL =  models.IntegerField(blank=True, null=True)
    COSERVATION_SCORE =  models.IntegerField(blank=True, null=True)
    OVERLAPPING_ORF = models.CharField(max_length=45, blank=True, null=True)
    MFE_SCORE = models.CharField(max_length=45, blank=True, null=True)
    PROGNOSTIC_VALUE = models.CharField(max_length=45, blank=True, null=True)
    VALIDATION = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'tb_genes'