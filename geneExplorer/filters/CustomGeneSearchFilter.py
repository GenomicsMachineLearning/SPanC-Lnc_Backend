from rest_framework import filters
import re as re

class CustomGeneSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get('search', None)
        search_param_str = str(search_param) if search_param is not None else ""
        if search_param_str:
            x = re.search(
                ("^(((chr)?([1-9]|1[0-9]|2[0-2]|[XYM]|GL000\d\d\d\.1|KI270\d\d\d\.1)))"
                 "(\:)?"
                 "(((((\d+)\-(\d+)?)|((\d+)\+(\d+)))))?$"),
                search_param_str)

            if x:
                group2, group10, group11, group13, group14 = x.group(2, 10, 11, 13, 14)

                if group2 is not None:
                    queryset = queryset.filter(chromosome=group2)

                if group10 is not None:
                    queryset = queryset.filter(start__gte=int(group10))

                if group11 is not None:
                    queryset = queryset.filter(end__lte=int(group11))

                if group13 is not None:
                    queryset = queryset.filter(start__gte=int(group13))

                if group14 is not None:
                    queryset = queryset.filter(end__lte=(int(group13)+int(group14)))

                return queryset

        # If custom parsing didn't work or returned no results, fall back to default search behavior
        return super().filter_queryset(request, queryset, view)