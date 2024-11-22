import base64 as base64
import io as io
import json as json

import anndata as anndata
import django.http.response as http_response
import django.views as django_views
import django.views.decorators.csrf as django_views_csrf
import django.utils.decorators as django_decorators
import matplotlib as matplotlib
import matplotlib.pyplot as matplotlib_plt
import scanpy as sc

import geneExplorer.views as ge_views
from Incrna import settings

@django_decorators.method_decorator(django_views_csrf.csrf_exempt, name='dispatch')
class SingleCellView(django_views.View):
    h5ad_files = [{"filePath": f"{settings.DATA_DIR}/Melanoma_scRNA.h5ad", "name": 'Melanoma'}]

    def get(self, request):
        gene_id = request.GET.get('cutarId', None)
        sample_name = request.GET.get('sampleName')

        maybe_file_info = list(filter(lambda x: x["name"] == sample_name, self.h5ad_files))

        if not gene_id or not sample_name:
            return http_response.JsonResponse(
                {'error': 'Missing required parameters'},
                status=400
            )

        if not maybe_file_info:
            return http_response.JsonResponse(
                {'error': 'Invalid sample name'},
                status=400
            )

        try:
            matplotlib.use('Agg')
            file_info = maybe_file_info[0]
            adata = anndata.read_h5ad(file_info["filePath"])

            if gene_id not in adata.var_names:
                return http_response.FileResponse(
                    open(ge_views.NotFoundImage.png_path, 'rb'),
                    content_type='image/png'
                )

            buffer = self.generate_spatial_plot(adata, gene_id, return_base64=False)
            return http_response.HttpResponse(
                buffer.getvalue(),
                content_type='image/png'
            )

        except Exception as e:
            return http_response.JsonResponse(
                {'error': str(e)},
                status=500
            )

    def post(self, request):
        try:
            data = json.loads(request.body)
            gene_id = data.get('cutarId', None)
            matplotlib.use('Agg')
            plots = []
            for file_info in self.h5ad_files:
                adata = anndata.read_h5ad(file_info["filePath"])  # Accessing 'filePath' correctly here
                if gene_id in adata.var_names:
                    buffer = self.generate_spatial_plot(adata, gene_id)
                    plots.append({'plotImage': buffer, 'name': file_info['name']})
                else:
                    plots.append({
                        'plotImage': ge_views.NotFoundImage.not_found(),
                        'name': 'Feature not found in sample'
                    })
            response_data = {'message': 'success', 'data': plots}
            return http_response.JsonResponse(response_data, status=200)
        except json.JSONDecodeError as e:
            return http_response.JsonResponse({'error': 'Invalid JSON format'}, status=400)

    def generate_spatial_plot(self, adata, gene_id, plot_size=20, return_base64=True):
        try:
            sc.pl.embedding(
                adata,
                basis='X_umap',
                color=[gene_id],
                size=plot_size,
                ncols=1,
                cmap="Oranges"
            )
            fig = matplotlib_plt.gcf()
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)

            if return_base64:
                base64_image = base64.b64encode(buffer.read()).decode('utf-8')
                buffer.close()
                matplotlib_plt.close(fig)
                return base64_image
            else:
                matplotlib_plt.close(fig)
                return buffer

        except Exception as e:
            matplotlib_plt.close()  # Ensure figure is closed even if there's an error
            raise e
