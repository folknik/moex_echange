FROM python:3.7.9-stretch

WORKDIR /usr/src/app

COPY moex.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN pip3 install psycopg2

CMD ["python3", "-u", "/app/jobs/moex.py"]
