# Dockerfile

FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt


# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt

# Mounts the application code to the image
COPY OnlineSurveys code

EXPOSE 8000

# runs the production server
ENTRYPOINT ["python", "OnlineSurveys/manage.py"]
CMD ["runserver", "127.0.0.1:8000"]