FROM python:3.10-slim-bookworm

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
COPY ./assets/annotation_table.zip ./assets/
COPY geneExplorer/ ./geneExplorer
COPY Incrna/ ./Incrna
COPY scripts/ ./scripts
COPY static/ ./static
COPY requirements.txt ./
COPY manage.py ./

# Setup static files and database.
RUN python -m pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput
RUN python scripts/import_csv.py

EXPOSE 8000
CMD ["gunicorn", "Incrna.wsgi:application", "-w=1", "-b=0.0.0.0:8000"]