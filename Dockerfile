FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt .

RUN pip install --upgrade pip

RUN apt-get update
RUN apt-get install -y build-essential

RUN pip install -r requirements.txt

COPY /app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
