FROM python:3.6
ENV PYTHONUNBUFFERED 1
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python app.py
EXPOSE 9090