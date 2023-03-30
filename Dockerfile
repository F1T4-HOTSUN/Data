FROM python:3.9.0-slim

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./info_performance

CMD ["python", "./info_performance/controller.py"]