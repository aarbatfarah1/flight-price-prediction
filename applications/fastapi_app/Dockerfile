FROM python:3.9

WORKDIR /app

COPY requirements.txt app/requirements.txt

RUN pip install  -r app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
