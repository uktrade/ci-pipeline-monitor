FROM python:3.8-alpine

RUN mkdir /app
VOLUME /app

COPY requirements.txt /app/
COPY *.py /app/

WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0", "wsgi"]
