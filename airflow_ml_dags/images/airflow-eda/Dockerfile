FROM airflow-ml-base:latest

WORKDIR /home

COPY ./slit.py ./slit.py ./requirements.txt ./

RUN pip install --no-cache -r ./requirements.txt

ENTRYPOINT [ "python", "./slit.py" ] 