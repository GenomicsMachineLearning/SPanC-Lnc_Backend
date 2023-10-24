from django.db import models

# Create your models here.

class Genes(models.Model):
    geneid = models.IntegerField(blank=True, null=True)
    chromosome = models.CharField(max_length=10, blank=True, null=True)
    start = models.IntegerField(blank=True, null=True)
    end = models.IntegerField(blank=True, null=True)
    gl_id = models.CharField(max_length=4471, blank=True, null=True)
    strand = models.CharField(max_length=1, blank=True, null=True)
    samples = models.CharField(max_length=809, blank=True, null=True)
    cell_types = models.CharField(max_length=5, blank=True, null=True)
    overlapping = models.CharField(max_length=5, blank=True, null=True)
    overlapping_regulatory_element = models.CharField(max_length=5, blank=True, null=True)
    overlapping_snp = models.CharField(max_length=5, blank=True, null=True)
    coservation_score = models.CharField(max_length=5, blank=True, null=True)
    mfe_score = models.CharField(max_length=5, blank=True, null=True)
    prognostic = models.CharField(max_length=5, blank=True, null=True)
    is_contains_sample = models.BooleanField()

    class Meta:
        db_table = 'genes'