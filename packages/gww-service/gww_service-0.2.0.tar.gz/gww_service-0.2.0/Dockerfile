FROM python:3.9.6

WORKDIR /code

RUN apt-get -y update && apt-get -y install libpq-dev python3-dev postgresql-client \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/.

CMD ["uvicorn", "gww_service.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]