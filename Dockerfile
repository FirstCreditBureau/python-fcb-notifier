FROM python:3.6
ENV PYTHONUNBUFFERED 1
COPY . .
WORKDIR .
RUN pip install -r requirements.txt
CMD gunicorn --workers 1 --bind :9090 app:app
EXPOSE 9090