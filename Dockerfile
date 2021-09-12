FROM python:3.9

MAINTAINER Ofek Metuky "ofek.metuky@gmail.com"

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

RUN pip install -e .

ENTRYPOINT ["python"]

CMD ["link_shortcutter/server.py"]