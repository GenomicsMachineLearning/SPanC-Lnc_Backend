"""
URL configuration for Incrna project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
# from django.urls import include, re_path
# from . import views
# urlpatterns = [
#     # url(r'^gene$',views.geneExplorer),
#     # re_path(r'^gene$', views.geneExplorer),
#     # path('gene/', views.geneExplorer),
#     path('admin/', admin.site.urls),
# ]

# from django.contrib import admin
# from django.urls import include, path

# urlpatterns = [
#     path('geneExplorer/', include('geneExplorer.urls')),
#     path('admin/', admin.site.urls),
# ]

from django.contrib import admin
from django.urls import path
import geneExplorer.views as views

urlpatterns = [
    # path('admin/',admin.site.urls),
    # path('genes', geneExplorer, name = "ganes"),
    path('genes_list', views.GenesListView.as_view(), name = "GenesListView"),
    path('genesid', views.GeneIDsListsView.as_view(), name = "GeneIDsListsView"),
    path('genes', views.GeneExplorerView.geneExplorerViewApi, name='GeneExplorerView'),
    path('genesSlr', views.GeneExplorerView.geneExplorerViewApi, name='GeneExplorerView'),
    path('genesScr', views.GeneExplorerView.geneExplorerViewApi, name='GeneExplorerView'),

]
