FROM python:3.9.0-slim

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./performance

CMD ["python", "./performance/prf_controller.py"]