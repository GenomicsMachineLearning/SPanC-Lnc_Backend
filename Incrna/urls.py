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
from django.conf import settings
from django.conf.urls.static import static
from geneExplorer.views import (
GenesListView,GeneIDsListsView ,geneExplorerViewApi, geneExplorerViewScrApi, geneExplorerViewSlrApi
)

urlpatterns = [
    path('admin/',admin.site.urls),
    # path('genes', geneExplorer, name = "ganes"),
    path('genes_list', GenesListView.as_view(), name = "GenesListView"),
    path('genesid', GeneIDsListsView.as_view(), name = "GeneIDsListsView"),
    path('genes', geneExplorerViewApi, name='geneExplorerViewApi'),
    path('genesSlr', geneExplorerViewSlrApi, name='geneExplorerViewSlrApi'),
    path('genesScr', geneExplorerViewScrApi, name='geneExplorerViewScrApi'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
