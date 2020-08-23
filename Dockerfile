FROM python:3.8

LABEL maintainer="Christophe Vanlancker carroarmato0@gmail.com"

ENV                     MODULE                  "cah_deckapi"

ENV                     DECKAPI_ADDRESS         "0.0.0.0"
ENV                     DECKAPI_PORT            8080
ENV                     DECKAPI_MONGODB_ADDRESS "127.0.0.1"
ENV                     DECKAPI_MONGODB_PORT    27017
ENV                     DECKAPI_MONGODB_DB      "cah"
ENV                     DECKAPI_DEBUG           true

ENV                     GAMEINSTANCE_ADDRESS        "0.0.0.0"
ENV                     GAMEINSTANCE_PORT           8081
ENV                     GAMEINSTANCE_DEBUG          true
ENV                     GAMEINSTANCE_DECKAPI_URI    "http://localhost:8080/api/v1"
ENV                     GAMEINSTANCE_WEBSOCKET_URI  "ws://localhost:8081/ws"

ENV                     VIRTUAL_ENV                 "/opt/venv"

RUN python3 -m venv ${VIRTUAL_ENV}
ENV                     PATH                        "${VIRTUAL_ENV}/bin:${PATH}"

COPY cah                /app/cah
COPY cah_deckapi        /app/cah_deckapi
COPY cah_gameinstance   /app/cah_gameinstance
COPY requirements.txt   /app
COPY README.md          /app
COPY setup.py           /app
COPY MANIFEST.in        /app

WORKDIR                 /app

RUN pip install -r requirements.txt
RUN ./setup.py develop
RUN echo 'cd /app/${MODULE}; python -m ${MODULE}.server' > /app/entrypoint && chmod +x /app/entrypoint

EXPOSE ${DECKAPI_PORT}/tcp
EXPOSE ${GAMEINSTANCE_PORT}/tcp

CMD ["/bin/bash", "-c", "/app/entrypoint"]
