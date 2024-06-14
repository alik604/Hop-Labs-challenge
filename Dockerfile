FROM python:3.11.4-slim-bullseye

COPY . /app/src/
WORKDIR /app/src
RUN pip install -r requirements.txt

WORKDIR /app/src/detections
CMD ["python", "main.py"]
