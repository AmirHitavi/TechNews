ARG PYTHON_VERSION=3.10.12

FROM python:${PYTHON_VERSION} AS python

FROM python AS build-stage-python

ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

COPY ./requirements .

RUN pip wheel --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt

FROM python AS run-stage-python

ARG BUILD_ENVIRONMENT=local

ARG APP_HOME=/src

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    curl wget gnupg unzip ca-certificates \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 \
    libcairo2 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
    libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libxss1 libxtst6 libu2f-udev libvulkan1 \
    chromium firefox-esr \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build-stage-python /usr/src/app/wheels /wheels/


RUN pip install --no-cache-dir --no-index --find-link=/wheels/ /wheels/*

RUN python -m playwright install chromium firefox

COPY ./docker/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./docker/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

COPY ./docker/django/celery/worker/start.sh /worker.sh
RUN sed -i 's/\r$//g' /worker.sh
RUN chmod +x /worker.sh

COPY ./docker/django/celery/flower/start.sh /flower.sh
RUN sed -i 's/\r$//g' /flower.sh
RUN chmod +x /flower.sh

COPY ./docker/django/celery/beat/start.sh /beat.sh
RUN sed -i 's/\r$//g' /beat.sh
RUN chmod +x /beat.sh

COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint.sh"]