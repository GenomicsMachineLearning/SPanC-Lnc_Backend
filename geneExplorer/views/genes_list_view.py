import rest_framework.generics as rest_framework_generics
import rest_framework.filters as rest_framework_filters
import geneExplorer.models as ge_models
import geneExplorer.serializer as ge_serializer


class GenesListView(rest_framework_generics.ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = ge_models.Genes.objects.all()
    serializer_class = ge_serializer.GenesListSerializer
    filter_backends = [rest_framework_filters.SearchFilter]
    search_fields = (
        'id', 'cutar_id', 'chromosome', 'start', 'end', 'transcript', 'strand', 'samples_detected',
        'cancer_types_detected', 'cell_type_specificity', 'cell_type_specificity_in_cancer_type',
        'detection_in_other_databases', 'id_in_other_databases', 'noncodeid', 'disease', 'gene', 'validation',
        'classification', 'overlapping_promoter', 'overlapping_enhancer', 'enhancer_associated', 'overlapping_snps',
        'overlapping_orf')
    ordering_fields = (
        'id', 'cutar_id', 'chromosome', 'start', 'end', 'transcript', 'strand', 'samples_detected',
        'cancer_types_detected', 'cell_type_specificity', 'cell_type_specificity_in_cancer_type',
        'detection_in_other_databases', 'id_in_other_databases', 'noncodeid', 'disease', 'gene', 'validation',
        'classification', 'overlapping_promoter', 'overlapping_enhancer', 'enhancer_associated', 'overlapping_snps',
        'overlapping_orf')

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get the ordering parameter from the request query params
        ordering_param = self.request.query_params.get('ordering', None)

        # Default ordering if no parameter is provided
        default_ordering = 'id'

        # Define the fields that are allowed for ordering
        allowed_ordering_fields = self.ordering_fields

        # Check if the provided ordering parameter is in the list of allowed fields
        if ordering_param in allowed_ordering_fields or ordering_param.lstrip('-') in allowed_ordering_fields:
            queryset = queryset.order_by(ordering_param)
        else:
            queryset = queryset.order_by(default_ordering)

        return queryset
