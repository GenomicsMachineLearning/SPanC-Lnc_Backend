from Incrna import settings
from geneExplorer.views.base_view_h5ad import BaseViewH5ad

class GeneSpatialLongReadView(BaseViewH5ad):
    h5ad_files = [
        {"filePath": f"{settings.DATA_DIR}/HNC_ilong_nano.h5ad", "name": 'Head and Neck Cancer - Nanopore',
         "size": 0.8},
        {"filePath": f"{settings.DATA_DIR}/SCC_nano.h5ad", "name": 'SCC - Nanopore', "size": 0.2},
        {"filePath": f"{settings.DATA_DIR}/BCC_nano.h5ad", "name": 'BCC - Nanopore', "size": 0.2},
        {"filePath": f"{settings.DATA_DIR}/CP_pacbio.h5ad", "name": 'Colorectal Cancer (Primary Tumor) - PacBio',
         "size": 0.7},
        {"filePath": f"{settings.DATA_DIR}/CM_pacbio.h5ad", "name": 'Colorectal Cancer (Metastasized Tumor) - PacBio',
         "size": 0.8}]
