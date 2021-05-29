FROM airflow-ml-base:latest

WORKDIR /home

RUN apt update && \
    apt install gcc -y

COPY ./requirements.txt ./

RUN pip install --no-cache -r ./requirements.txt && rm ./requirements.txt

COPY ./eda.py ./

ENTRYPOINT [ "python", "./eda.py" ] 