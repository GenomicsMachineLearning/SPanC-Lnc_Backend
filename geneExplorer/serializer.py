from rest_framework import serializers
from .models import Genes

class GenesListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    cutar_id = serializers.CharField()
    chromosome = serializers.CharField()
    start = serializers.IntegerField()
    end = serializers.IntegerField()
    transcript = serializers.CharField()
    strand = serializers.CharField()
    samples_detected = serializers.CharField()
    cancer_types_detected = serializers.CharField()
    cell_type_specificity = serializers.CharField()
    cell_type_specificity_in_cancer_type = serializers.CharField()
    detection_in_other_databases = serializers.CharField()
    id_in_other_databases = serializers.CharField()
    noncodeid = serializers.CharField()
    disease = serializers.CharField()
    gene = serializers.CharField()
    classification = serializers.CharField()
    overlapping_promoter = serializers.CharField()
    overlapping_enhancer = serializers.CharField()
    enhancer_associated = serializers.CharField()
    overlapping_snps = serializers.CharField()
    overlapping_orf = serializers.CharField()

class GenesListSerializerId(serializers.Serializer):
    id = serializers.CharField()
