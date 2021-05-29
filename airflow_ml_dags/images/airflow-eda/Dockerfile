FROM airflow-ml-base:latest

WORKDIR /home

RUN apt update && \
    apt install gcc -y

COPY ./eda.py ./requirements.txt ./

RUN pip install --no-cache -r ./requirements.txt

ENTRYPOINT [ "python", "./eda.py" ] 