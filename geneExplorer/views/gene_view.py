from Incrna import settings
from geneExplorer.views.base_view_h5ad import BaseViewH5ad


class GeneView(BaseViewH5ad):
    h5ad_files = [
        {"filePath": f"{settings.DATA_DIR}/HNC.h5ad", "name": 'Head and Neck Cancer', "spot_size": 1.1},
        {"filePath": f"{settings.DATA_DIR}/Melanoma.h5ad", "name": 'Melanoma', "spot_size": 0.8},
        {"filePath": f"{settings.DATA_DIR}/SCC.h5ad", "name": 'SCC', "spot_size": 0.2},
        {"filePath": f"{settings.DATA_DIR}/BCC.h5ad", "name": 'BCC', "spot_size": 0.2},
        {"filePath": f"{settings.DATA_DIR}/KidneyCancer.h5ad", "name": 'Kidney Cancer', "spot_size": 0.5}
    ]
