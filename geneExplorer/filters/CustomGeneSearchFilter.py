from rest_framework import filters
from ..genomic_utils import parse_genomic_coordinates

class CustomGeneSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):

        search_param = request.query_params.get('search', None)
        search_param_str = str(search_param) if search_param is not None else ""

        if search_param_str:
            chromosome, start, end = parse_genomic_coordinates(search_param_str)

            if chromosome or start or end:
                if chromosome is not None:
                    queryset = queryset.filter(chromosome=chromosome)
                if start is not None:
                    queryset = queryset.filter(start__gte=start)
                if end is not None:
                    queryset = queryset.filter(end__lte=end)
                return queryset

        return super().filter_queryset(request, queryset, view)