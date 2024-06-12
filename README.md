# SPanC-Lnc Backend

## Running Locally

### In a Local Python Environment

Setup a conda environment:
* MacOS
  * ```conda create --name spanc-lnc --subdir osx-64 python=3.10 -y```
* Other
  * ```conda create --name spanc-lnc --subdir osx-64 python=3.10 -y```

* ```conda activate spanc-lnc```

Install dependencies:
* ```python -m pip install -r requirements.txt```

### Creating Database
* ```python manage.py migrate```
* ```python scripts/```

### Running Directly
* ```python manage.py runserver```

### Building and Running Docker Images

* Installing Docker
  * https://docs.docker.com/desktop/install/mac-install/
  * https://docs.docker.com/desktop/install/windows-install/
  * Add ```$HOME/.docker/bin``` to you PATH.

* Running locally
  * ```docker build -t myapp-local -f Dockerfile-local .```
  * ```docker run -p 8000:8000 myapp-local```

See:
* Dockerfile - for deploying/testing in AWS Lambda,
* Dockerfile-local - for testing the Dockerfile locally.

Using:
* https://hub.docker.com/_/python - 
* Debian https://www.debian.org/releases/

## Uploading to EFS (Elastic File System)

The current steps are required to upload assets to the backend:
* Upload to S3 bucket s3://gml-spanc-lnc (https://ap-southeast-2.console.aws.amazon.com/s3/buckets/gml-spanc-lnc)
* Run AWS DataSync https://ap-southeast-2.console.aws.amazon.com/datasync/home
  * Start > Start with Defaults

