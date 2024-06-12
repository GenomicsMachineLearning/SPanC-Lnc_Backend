import django.http.response as http_response
import anndata as anndata
import scanpy as sc
import matplotlib.pyplot as matplotlib_plt
import matplotlib as matplotlib
import io as io
import json as json
import base64 as base64
import django.views.decorators.csrf as django_views_csrf
import geneExplorer.views as ge_views
from Incrna import settings


class GeneView():

    @django_views_csrf.csrf_exempt
    def gene_view_api(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                geneId = data.get('cutarId', None)
                matplotlib.use('Agg')

                h5ad_files = [{"filePath": f"{settings.DATA_DIR}/HNC.h5ad", "name": 'Head and Neck Cancer', "size": 1.1},
                              {"filePath": f"{settings.DATA_DIR}/Melanoma.h5ad", "name": 'Melanoma', "size": 0.8},
                              {"filePath": f"{settings.DATA_DIR}/SCC.h5ad", "name": 'SCC', "size": 0.2},
                              {"filePath": f"{settings.DATA_DIR}/BCC.h5ad", "name": 'BCC', "size": 0.2},
                              {"filePath": f"{settings.DATA_DIR}/KidneyCancer.h5ad", "name": 'Kidney Cancer', "size": 0.5}]

                plots = []

                for h5ad_file in h5ad_files:
                    HNC = anndata.read_h5ad(h5ad_file["filePath"])  # Accessing 'filePath' correctly here
                    if geneId in HNC.var_names:
                        sc.pl.spatial(HNC, alpha_img=0.5, color=[geneId], show=False, cmap='inferno',
                                      size=h5ad_file['size'])
                        fig = matplotlib_plt.gcf()
                        buffer = io.BytesIO()
                        fig.savefig(buffer, format='png', bbox_inches='tight')
                        buffer.seek(0)
                        base64_image = base64.b64encode(buffer.read()).decode('utf-8')
                        buffer.close()
                        matplotlib_plt.close(fig)
                        plots.append({'plotImage': base64_image, 'name': h5ad_file['name']})
                    else:
                        plots.append(
                            {'plotImage': ge_views.NotFoundImage.not_found(), 'name': 'Feature not found in sample'})
                response_data = {'message': 'success', 'data': plots}
                return http_response.JsonResponse(response_data, status=200)
            except json.JSONDecodeError as e:
                return http_response.JsonResponse({'error': 'Invalid JSON format'}, status=400)
        else:
            return http_response.JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
