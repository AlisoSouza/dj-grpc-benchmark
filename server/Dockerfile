FROM python:3-slim-buster AS base

ARG BUILD_DEPS="\
    python3-dev default-libmysqlclient-dev \
    build-essential \
    libmariadbclient-dev \
    git cmake \
    autoconf pkg-config autoconf libtool automake \
    librabbitmq-dev \
    libmariadbclient-dev-compat \
    bzip2 curl libpq-dev gettext libgdal-dev python3-cffi python3-gdal"

ARG RUNTIME_DEPS="\
  libmariadb3 \
  librabbitmq4 \
  netcat \
  gosu"

ENV BUILD_DEPS=${BUILD_DEPS} \
  RUNTIME_DEPS=${RUNTIME_DEPS}

ENV WORKDIR /app
WORKDIR $WORKDIR

FROM base AS build

COPY poetry.lock pyproject.toml ./

RUN apt-get update \
  && apt-get install --no-install-recommends --no-install-suggests -y ${BUILD_DEPS} \
  && pip install --no-cache-dir -U pip==21.2.2 setuptools==57.4.0 poetry \
  && poetry export -f requirements.txt --output requirements.txt --without-hashes \
  && pip install --no-cache-dir --ignore-installed --prefix=/install -r requirements.txt

FROM base

COPY --from=build /install /usr/local

RUN apt-get update \
  && SUDO_FORCE_REMOVE=yes apt-get remove --purge -y ${BUILD_DEPS} \
  && apt-get autoremove -y \
  && apt-get install -y --no-install-recommends ${RUNTIME_DEPS} \
  && rm -rf /usr/share/man \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY . .

#RUN chmod +x /app/run.sh
EXPOSE 50051
ENTRYPOINT ["/app/run.sh"]

