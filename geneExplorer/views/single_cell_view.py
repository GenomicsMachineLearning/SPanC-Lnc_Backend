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


class SingleCellView():

    @django_views_csrf.csrf_exempt
    def gene_explorer_view_api(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                geneId = data.get('cutarId', None)
                matplotlib.use('Agg')
                h5ad_files = [{"filePath": "assets/Melanoma_scRNA.h5ad", "name": 'Melanoma'}]
                plots = []
                for h5ad_file in h5ad_files:
                    HNC = anndata.read_h5ad(h5ad_file["filePath"])  # Accessing 'filePath' correctly here
                    if geneId in HNC.var_names:
                        sc.pl.embedding(HNC, basis='X_umap', color=[geneId], size=20, ncols=1, cmap="Oranges")
                        fig = matplotlib_plt.gcf()
                        buffer = io.BytesIO()
                        fig.savefig(buffer, format='png', bbox_inches='tight')
                        buffer.seek(0)
                        base64_image = base64.b64encode(buffer.read()).decode('utf-8')
                        buffer.close()
                        matplotlib_plt.close(fig)
                        plots.append({'plotImage': base64_image, 'name': h5ad_file['name']})
                        # Rest of your code...
                    else:
                        plots.append(
                            {'plotImage': ge_views.NotFoundImage.not_found(), 'name': 'Feature not found in sample'})

                response_data = {'message': 'success', 'data': plots}

                return http_response.JsonResponse(response_data, status=200)

            except json.JSONDecodeError as e:
                return http_response.JsonResponse({'error': 'Invalid JSON format'}, status=400)
        else:
            return http_response.JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
