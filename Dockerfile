FROM public.ecr.aws/docker/library/python:3.10-slim-bookworm

RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    ca-certificates \
    curl \
    git \
    gzip \
    pkg-config \
    procps \
    tar \
    unzip \
    wget \
    zlib1g

# Setup Lambda
WORKDIR /var/task
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.3 /lambda-adapter /opt/extensions/lambda-adapter

# Copy Django application
# Assume EFS will store assets here.
# COPY ./assets/*.h5ad ./data/
COPY ./assets/annotation_table.zip /var/task/assets/
COPY geneExplorer/ /var/task/geneExplorer
COPY Incrna/ /var/task/Incrna
COPY scripts/ /var/task/scripts
COPY static/ /var/task/static
COPY requirements.txt /var/task
COPY manage.py /var/task

# Setup static files and database.
RUN python -m pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput
RUN python scripts/import_csv.py

CMD ["gunicorn", "Incrna.wsgi:application", "-w=1", "-b=0.0.0.0:8080"]