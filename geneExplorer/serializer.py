from rest_framework import serializers


class GenesListSerializer(serializers.Serializer):
    geneid = serializers.IntegerField()
    id = serializers.CharField()
    chromosome = serializers.CharField()
    start = serializers.IntegerField()
    end = serializers.IntegerField()
    gl_id = serializers.CharField()
    strand = serializers.CharField()
    samples = serializers.CharField()
    cell_types = serializers.CharField()
    overlapping = serializers.CharField()
    overlapping_regulatory_element = serializers.CharField()
    overlapping_snp = serializers.CharField()
    coservation_score = serializers.CharField()
    mfe_score = serializers.CharField()
    prognostic = serializers.CharField()

class GenesListSerializerId(serializers.Serializer):
    id = serializers.CharField()
    is_contains_sample = serializers.BooleanField()