from django.http.response import JsonResponse
import anndata
import scanpy as sc
from rest_framework.generics import ListAPIView
from rest_framework import filters
from geneExplorer.serializer import GenesListSerializer, GenesListSerializerId
from geneExplorer.models import Genes
import matplotlib.pyplot as plt
import matplotlib
import io
import json
import os
import base64
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


class GenesListView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Genes.objects.all()
    serializer_class = GenesListSerializer
    filter_backends = [filters.SearchFilter]
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


class GeneIDsListsView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Genes.objects.distinct().values('id')
    serializer_class = GenesListSerializerId
    filter_backends = [filters.SearchFilter]
    search_fields = ('id', 'cutar_id')
    ordering_fields = ('id')

    def get_queryset(self):
        # return Genes.objects.all()
        return super().get_queryset()


class GeneExplorerView():
    base64_png = None

    @staticmethod
    def read_png_file():
        # Check if the PNG file exists in the static directory
        png_path = os.path.join(settings.BASE_DIR, 'static/no_data.png')
        if not os.path.exists(png_path):
            return None

        # Read the PNG file from the static directory
        with open(png_path, 'rb') as png_file:
            png_data = png_file.read()

        # Encode the PNG data as base64
        base64_png = base64.b64encode(png_data).decode('utf-8')

        return base64_png

    @csrf_exempt
    def geneExplorerViewApi(request):
        if GeneExplorerView.base64_png is None:
            # Read the PNG file and store the base64-encoded data
            GeneExplorerView.base64_png = GeneExplorerView.read_png_file()

        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                geneId = data.get('cutarId', None)
                matplotlib.use('Agg')

                h5ad_files = [{"filePath": "assets/HNC.h5ad", "name": 'Head and Neck Cancer'},
                              {"filePath": "assets/Melanoma.h5ad", "name": 'Melanoma'},
                              {"filePath": "assets/SCC.h5ad", "name": 'SCC'},
                              {"filePath": "assets/BCC.h5ad", "name": 'BCC'}]

                plots = []

                for h5ad_file in h5ad_files:
                    HNC = anndata.read_h5ad(h5ad_file["filePath"])  # Accessing 'filePath' correctly here
                    if geneId in HNC.var_names:
                        sc.pl.spatial(HNC, alpha_img=0.5, color=[geneId], show=False, cmap='inferno', size=2)
                        fig = plt.gcf()
                        buffer = io.BytesIO()
                        fig.savefig(buffer, format='png', bbox_inches='tight')
                        buffer.seek(0)
                        base64_image = base64.b64encode(buffer.read()).decode('utf-8')
                        buffer.close()
                        plt.close(fig)
                        plots.append({'plotImage': base64_image, 'name': h5ad_file['name']})
                        # Rest of your code...
                    else:
                        plots.append({'plotImage': GeneExplorerView.base64_png, 'name': 'Feature not found in sample'})

                response_data = {'message': 'success', 'data': plots}

                return JsonResponse(response_data, status=200)

            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        else:
            return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
