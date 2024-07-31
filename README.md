# SPanC-Lnc Backend

We require data to be downloaded. The following need to be added to a directory relative to this project called "data":
* [BCC_nano.h5ad](https://downloads.gmllab.com/SPanC-Lnc/BCC_nano.h5ad) - 40.8 MB
* [BCC.h5ad](https://downloads.gmllab.com/SPanC-Lnc/BCC.h5ad) - 115.9 MB
* [CM_pacbio.h5ad](https://downloads.gmllab.com/SPanC-Lnc/CM_pacbio.h5ad) - 26.1 MB
* [CP_pacbio.h5ad](https://downloads.gmllab.com/SPanC-Lnc/CP_pacbio.h5ad) - 25.9 MB
* [HNC_ilong_nano.h5ad](https://downloads.gmllab.com/SPanC-Lnc/CP_pacbio.h5ad) - 7.2 MB
* [HNC.h5ad](https://downloads.gmllab.com/SPanC-Lnc/CP_pacbio.h5ad) - 134.8 MB
* [KidneyCancer.h5ad](https://downloads.gmllab.com/SPanC-Lnc/CP_pacbio.h5ad) - 208.7 MB
* [Melanoma_scRNA.h5ad](https://downloads.gmllab.com/SPanC-Lnc/CP_pacbio.h5ad) - 882.8 MB
* [Melanoma.h5ad](https://downloads.gmllab.com/SPanC-Lnc/CP_pacbio.h5ad) - 66.3 MB
* [SCC_nano.h5ad](https://downloads.gmllab.com/SPanC-Lnc/CP_pacbio.h5ad) - 39.6 MB
* [SCC.h5ad](https://downloads.gmllab.com/SPanC-Lnc/CP_pacbio.h5ad) - 138.3 MB

## Running Locally

We have two methods for running the backend server:
* Run in a conda environment or
* Docker.

### Running the Server in a Local Python Environment

The steps to run in a local conda environment include:
* Setup a new Python environment and install dependencies.
* Setup local database.
* Run server.

We assume you already have conda installed.

* Setup a conda environment:
  * Linux
    * ```conda create --name spanc-lnc --subdir python=3.10 -y```
  * MacOS
    * ```conda create --name spanc-lnc --subdir osx-64 python=3.10 -y```
* Activate conda environment:
  * ```conda activate spanc-lnc```

* Install Python dependencies:
  * ```python -m pip install -r requirements.txt```

* Setup a local database:
  * ```python manage.py migrate```
  * ```python scripts/import_csv.py```

* Run server:
  * ```python manage.py runserver```

### Running the Server using Docker

* Install Docker
  * https://docs.docker.com/desktop/install/mac-install/
  * https://docs.docker.com/desktop/install/windows-install/
  * Add ```$HOME/.docker/bin``` to you PATH.

* Setup a local database:
  * ```python manage.py migrate```
  * ```python scripts/import_csv.py```

* Running server:
  * ```docker build -t myapp-local -f Dockerfile-local .```
  * ```docker run -p 8000:8000 myapp-local```

## Other Information

* Dockerfile - for deploying/testing in AWS Lambda,
* Dockerfile-local - for testing the Dockerfile locally.

Using:
* Python in Docker https://hub.docker.com/_/python  
* Debian https://www.debian.org/releases/

