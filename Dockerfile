FROM python:3.10-slim         

WORKDIR /ylab_project
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

RUN chmod a+x docker/*.sh

# CMD uvicorn main:app --host 0.0.0.0 --port 8000
