import django.urls as dj_urls
import geneExplorer.views as views

urlpatterns = [
    dj_urls.path('', views.HomeView.as_view(), name="Ok"),
    dj_urls.path('genes_list', views.GenesListView.as_view(), name="GenesListView"),
    dj_urls.path('genesid', views.GeneIDsListsView.as_view(), name="GeneIDsListsView"),
    dj_urls.path('genes', views.GeneView.as_view(), name='GeneExplorerView'),
    dj_urls.path('genesSlr', views.GeneSpatialLongReadView.gene_spatial_long_read_view_api, name='GeneExplorerView'),
    dj_urls.path('genesScr', views.SingleCellView.as_view(), name='SingleCellView'),

]
