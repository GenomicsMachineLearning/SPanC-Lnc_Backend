from rest_framework import serializers


class GenesListSerializer(serializers.Serializer):
    ID =  serializers.IntegerField()
    CUTAR_ID = serializers.CharField()
    CHROMOSOME = serializers.CharField()
    START =  serializers.IntegerField()
    END =  serializers.IntegerField()
    TRANSCRIPT = serializers.CharField()
    STRAND = serializers.CharField()
    SAMPLES_DETECTED = serializers.CharField()
    CANCER_TYPES_DETECTED = serializers.CharField()
    CELL_TYPE_SPECIFICITY = serializers.CharField()
    CELL_TYPE_SPECIFICITY_IN_CANCER_TYPE = serializers.CharField()
    DETECTION_IN_OTHER_DATABASES = serializers.CharField()
    ID_IN_OTHER_DATABASES = serializers.CharField()
    NONCODEID = serializers.CharField()
    DISEASE = serializers.CharField()
    GENE = serializers.CharField()
    CLASSIFICATION = serializers.CharField()
    OVERLAPPING_PROMOTER = serializers.CharField()
    OVERLAPPING_ENHANCER = serializers.CharField()
    ENHANCER_ASSOCIATED = serializers.CharField()
    OVERLAPPING_SNPS = serializers.CharField()
    CODING_POTENTIAL =   serializers.IntegerField()
    COSERVATION_SCORE =   serializers.IntegerField()
    OVERLAPPING_ORF = serializers.CharField()
    MFE_SCORE = serializers.CharField()
    PROGNOSTIC_VALUE = serializers.CharField()
    VALIDATION = serializers.CharField()

class GenesListSerializerId(serializers.Serializer):
    CUTAR_ID = serializers.CharField()
