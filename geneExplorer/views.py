from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
import anndata
import scanpy as sc
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, filters
from geneExplorer.serializer import GenesListSerializer,GenesListSerializerId
from geneExplorer.models import Genes
from rest_framework.views import APIView
import matplotlib.pyplot as plt
import matplotlib
import io
import json
import base64
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from Incrna.constants import fileNotFoundBase64

# Create your views here.

# def geneExplorer(request):
#     matplotlib.use('Agg')  # Use non-GUI backend
#     # if request.meathod == 'GET':
#     HNC = anndata.read_h5ad("asserts/HNC.h5ad")
#     #    fig = sc.pl.spatial(HNC, alpha_img=0.5,color = ['cuTAR213507'])   # Create a blank figure
#     #    sc.pl.spatial(HNC, alpha_img=0.5,color = ['cuTAR213507']) # user query in place of cuTAR213507
#     # Convert the plot to a base64 encoded string


#     sc.pl.spatial(HNC, alpha_img=0.5, color=['cuTAR213507'], show=False)

# # Get the current figure
#     fig = plt.gcf()

# # Convert the plot to a base64 encoded string
#     buffer = io.BytesIO()
#     fig.savefig(buffer, format='png', bbox_inches='tight')
#     buffer.seek(0)
#     base64_image = base64.b64encode(buffer.read()).decode('utf-8')
#     print('base64_image', base64_image);
#     buffer.close()
#     plt.close(fig)
#     return JsonResponse("SuccessFully Called",safe =False)


class GenesListView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Genes.objects.all()
    serializer_class = GenesListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('ID','CUTAR_ID','CHROMOSOME','START','END','TRANSCRIPT','STRAND','SAMPLES_DETECTED','CANCER_TYPES_DETECTED','CELL_TYPE_SPECIFICITY','CELL_TYPE_SPECIFICITY_IN_CANCER_TYPE','DETECTION_IN_OTHER_DATABASES','ID_IN_OTHER_DATABASES','NONCODEID','DISEASE','GENE','CLASSIFICATION','OVERLAPPING_PROMOTER','OVERLAPPING_ENHANCER','ENHANCER_ASSOCIATED','OVERLAPPING_SNPS','CODING_POTENTIAL','COSERVATION_SCORE','OVERLAPPING_ORF','MFE_SCORE','PROGNOSTIC_VALUE','VALIDATION')
    ordering_fields = ('ID','CUTAR_ID','CHROMOSOME','START','END','TRANSCRIPT','STRAND','SAMPLES_DETECTED','CANCER_TYPES_DETECTED','CELL_TYPE_SPECIFICITY','CELL_TYPE_SPECIFICITY_IN_CANCER_TYPE','DETECTION_IN_OTHER_DATABASES','ID_IN_OTHER_DATABASES','NONCODEID','DISEASE','GENE','CLASSIFICATION','OVERLAPPING_PROMOTER','OVERLAPPING_ENHANCER','ENHANCER_ASSOCIATED','OVERLAPPING_SNPS','CODING_POTENTIAL','COSERVATION_SCORE','OVERLAPPING_ORF','MFE_SCORE','PROGNOSTIC_VALUE','VALIDATION')

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get the ordering parameter from the request query params
        ordering_param = self.request.query_params.get('ordering', None)

        # Default ordering if no parameter is provided
        default_ordering = 'CUTAR_ID'

        # Define the fields that are allowed for ordering
        allowed_ordering_fields = self.ordering_fields

        # Check if the provided ordering parameter is in the list of allowed fields
        if ordering_param in allowed_ordering_fields:
            queryset = queryset.order_by(ordering_param)
        else:
            queryset = queryset.order_by(default_ordering)

        return queryset

class GeneIDsListsView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Genes.objects.all()
    serializer_class = GenesListSerializerId
    filter_backends = [filters.SearchFilter]
    search_fields = ['CUTAR_ID']
    ordering_fields = ['CUTAR_ID']

    def get_queryset(self):
        # return Genes.objects.all()
        return super().get_queryset()

# @csrf_exempt  # This decorator allows us to bypass CSRF protection for this viewls
# def geneExplorerViewApi(request):
#     if request.method == 'POST':
#         try:
#             # Get the JSON data from the request body
#             data = json.loads(request.body)
#             geneId = data.get('geneId', None)
#             matplotlib.use('Agg')  # Use non-GUI backend
#             HNC = anndata.read_h5ad("asserts/HNC.h5ad")
#              #fig = sc.pl.spatial(HNC, alpha_img=0.5,color = ['cuTAR213507'])   # Create a blank figure
#              # sc.pl.spatial(HNC, alpha_img=0.5,color = ['cuTAR213507']) # user query in place of cuTAR213507
#              # Convert the plot to a base64 encoded string
#             sc.pl.spatial(HNC, alpha_img=0.5, color=[geneId], show=False,  cmap='inferno',size=2)
#              # Get the current figure
#             fig = plt.gcf()
#              # Convert the plot to a base64 encoded string
#             buffer = io.BytesIO()
#             fig.savefig(buffer, format='png', bbox_inches='tight')
#             buffer.seek(0)
#             base64_image = base64.b64encode(buffer.read()).decode('utf-8')
#             buffer.close()
#             plt.close(fig)
#             response_data = {'message': 'success', 'data':{'plotImage':base64_image,'name':'Head and Neck OPSCC'}}

#             return JsonResponse(response_data, status=200)
#         except json.JSONDecodeError as e:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def geneExplorerViewApi(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            geneId = data.get('geneId', None)
            matplotlib.use('Agg')
            h5ad_files = [{"filePath":os.path.join(settings.BASE_DIR, 'asserts', 'HNC.h5ad'),"name":'Head and Neck Cancer',"size":1.5},
                          {"filePath":os.path.join(settings.BASE_DIR, 'asserts', 'Melanoma.h5ad'),"name":'Melanoma',"size":0.8},
                          {"filePath":os.path.join(settings.BASE_DIR, 'asserts', 'SCC.h5ad'),"name":'SCC',"size":0.23},
                          {"filePath":os.path.join(settings.BASE_DIR, 'asserts', 'BCC.h5ad'),"name":'BCC', "size":0.25},
                          {"filePath":os.path.join(settings.BASE_DIR, 'asserts', 'KidneyCancer.h5ad'),"name":'Kidney Cancer', "size":0.7}]
            # h5ad_file_path = os.path.join(settings.BASE_DIR, 'asserts', 'HNC.h5ad')
            # h5ad_files = [{"filePath":h5ad_file_path,"name":'Head and Neck Cancer'}]

            plots = []

            for h5ad_file in h5ad_files:
                HNC = anndata.read_h5ad(h5ad_file["filePath"])  # Accessing 'filePath' correctly here
                if geneId in HNC.var_names:
                    sc.pl.spatial(HNC, alpha_img=0.5, color=[geneId], show=False,  cmap='inferno',size=h5ad_file['size'])
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
                    plots.append({'plotImage': fileNotFoundBase64, 'name':'Feature not found in sample'})
                    # Handle case where geneId is not found in the dataset


            response_data = {'message': 'success', 'data': plots}

            return JsonResponse(response_data, status=200)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def geneExplorerViewSlrApi(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            geneId = data.get('geneId', None)
            matplotlib.use('Agg')
            h5ad_files = [{"filePath":os.path.join(settings.BASE_DIR, 'asserts', 'HNC_ilong_nano.h5ad'),"name":'Nanopore Head and Neck Cancer',"size":0.8},
                          {"filePath":os.path.join(settings.BASE_DIR, 'asserts', 'SCC_nano.h5ad'),"name":'Nanopore SCC',"size":0.25},
                          {"filePath":os.path.join(settings.BASE_DIR, 'asserts', 'BCC_nano.h5ad'),"name":'Nanopore BCC', "size":0.25},
                          {"filePath":os.path.join(settings.BASE_DIR, 'asserts', 'CP_pacbio.h5ad'),"name":'PacBio Colorectal Cancer (Primary Tumor)', "size":0.8},
                          {"filePath":os.path.join(settings.BASE_DIR, 'asserts', 'CM_pacbio.h5ad'),"name":'PacBio Colorectal Cancer (Metastasized Tumor)', "size":1}]
            # h5ad_file_path = os.path.join(settings.BASE_DIR, 'asserts', 'HNC.h5ad')
            # h5ad_files = [{"filePath":h5ad_file_path,"name":'Head and Neck Cancer'}]

            plots = []

            for h5ad_file in h5ad_files:
                HNC = anndata.read_h5ad(h5ad_file["filePath"])  # Accessing 'filePath' correctly here
                if geneId in HNC.var_names:
                    sc.pl.spatial(HNC, alpha_img=0.5, color=[geneId], show=False,  cmap='inferno',size=h5ad_file['size'])
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
                    plots.append({'plotImage': fileNotFoundBase64, 'name':'Feature not found in sample'})
                    # Handle case where geneId is not found in the dataset


            response_data = {'message': 'success', 'data': plots}

            return JsonResponse(response_data, status=200)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def geneExplorerViewScrApi(request):

    import anndata #need version 0.8.0 (pip install --upgrade anndata==0.8.0)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            geneId = data.get('geneId', None)
            matplotlib.use('Agg')
            h5ad_files = [{"filePath":os.path.join(settings.BASE_DIR, 'asserts', 'Melanoma_scRNA.h5ad'),"name":'Acral and Cutaneous Melanoma',"size":1.5}]
            # h5ad_file_path = os.path.join(settings.BASE_DIR, 'asserts', 'HNC.h5ad')
            # h5ad_files = [{"filePath":h5ad_file_path,"name":'Head and Neck Cancer'}]

            plots = []

            for h5ad_file in h5ad_files:
                HNC = anndata.read_h5ad(h5ad_file["filePath"])  # Accessing 'filePath' correctly here
                if geneId in HNC.var_names:
                    sc.pl.embedding(HNC, basis='X_umap', color=[geneId], show=False,  cmap='Oranges',size=20, ncols=1)
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
                    plots.append({'plotImage': fileNotFoundBase64, 'name':'Feature not found in sample'})
                    # Handle case where geneId is not found in the dataset


            response_data = {'message': 'success', 'data': plots}

            return JsonResponse(response_data, status=200)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
