ARG PYTHON_VERSION=3.8

FROM python:${PYTHON_VERSION}-slim

ENV PIP_NO_CACHE_DIR=off

WORKDIR /home

COPY ./models ./models

ENV MODEL_DIR=/home/models

ARG MODEL_PATH=/home/models/svc/svc.pickle

ENV MODEL_PATH=${MODEL_PATH}

WORKDIR /home/app

COPY ./heart_diss_app ./heart_diss_app

COPY ./setup.py ./requirements.txt ./

RUN pip install wheel~=0.36 && \
    pip install . && \
    python ./setup.py clean -a && \
    rm -r ./heart_diss_app && \
    rm ./setup.py ./requirements.txt


COPY ./entrypoint.sh ./

RUN chmod u+x ./entrypoint.sh

ENV APP_PORT=8000

ENV LOG_LEVEL=info

ENTRYPOINT [ "./entrypoint.sh" ]

CMD uvicorn heart_diss_app:app --log-level ${LOG_LEVEL} --host 0.0.0.0 --port ${APP_PORT}