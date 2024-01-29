FROM python:3.9.18-slim

WORKDIR /ylab_project
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]