FROM python:3.8

LABEL maintainer="Christophe Vanlancker carroarmato0@gmail.com"

ENV                     DECKAPI_ADDRESS         "0.0.0.0"
ENV                     DECKAPI_PORT            8080
ENV                     DECKAPI_MONGODB_ADDRESS "127.0.0.1"
ENV                     DECKAPI_MONGODB_PORT    27017
ENV                     DECKAPI_MONGODB_DB      "cah"
ENV                     DECKAPI_DEBUG           true

ENV                     VIRTUAL_ENV             "/opt/venv"

RUN python3 -m venv ${VIRTUAL_ENV}
ENV                     PATH                    "${VIRTUAL_ENV}/bin:${PATH}"

COPY cah                /app/cah
COPY cah_deckapi        /app/cah_deckapi
COPY requirements.txt   /app
COPY README.md          /app
COPY setup.py           /app
COPY MANIFEST.in        /app

WORKDIR                 /app

RUN pip install -r requirements.txt
RUN ./setup.py develop

EXPOSE ${DECKAPI_PORT}/tcp

WORKDIR                 /app/cah_deckapi

CMD ["python", "-m", "cah_deckapi.server"]
