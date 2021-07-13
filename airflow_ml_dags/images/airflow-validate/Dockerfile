FROM airflow-ml-base:latest

WORKDIR /home

COPY ./requiremnets.txt ./

RUN pip install --no-cache-dir -r ./requiremnets.txt

COPY ./validate.py ./

ENTRYPOINT [ "python", "validate.py" ]