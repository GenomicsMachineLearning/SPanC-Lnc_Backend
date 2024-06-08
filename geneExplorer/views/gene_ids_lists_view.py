import rest_framework.generics as rest_framework_generics
import rest_framework.filters as rest_framework_filters
import geneExplorer.models as ge_models
import geneExplorer.serializer as ge_serializer


class GeneIDsListsView(rest_framework_generics.ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = ge_models.Genes.objects.distinct().values('id')
    serializer_class = ge_serializer.GenesListSerializerId
    filter_backends = [rest_framework_filters.SearchFilter]
    search_fields = ('id', 'cutar_id')
    ordering_fields = ('id')

    def get_queryset(self):
        # return Genes.objects.all()
        return super().get_queryset()
