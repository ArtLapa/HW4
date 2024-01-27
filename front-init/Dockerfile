FROM python:3.8

WORKDIR /app

COPY . .

RUN test -f requirements.txt && pip install -r requirements.txt || echo "No requirements file"

EXPOSE 3000
EXPOSE 5000

CMD ["python", "main.py"]

