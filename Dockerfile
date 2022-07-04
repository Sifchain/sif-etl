FROM python:3.7-alpine3.13 as basebuild

RUN apk add \
  busybox-extras \
  dumb-init \
  gcc \
  g++ \
  libressl-dev \
  libffi-dev  \
  make \
  musl-dev \
  net-tools \
  openssl-dev \
  postgresql-libs \
  postgresql-dev \
  python3-dev \
  vim
 
ENV PYTHONPATH /

FROM basebuild as python_build
COPY ./requirements.txt /sif-etl/requirements.txt
RUN pip install -r /sif-etl/requirements.txt

COPY ./ /sif-etl

WORKDIR /sif-etl

FROM python_build as sifetl_run

ENTRYPOINT ["tail", "-f", "/dev/null"]
