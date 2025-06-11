FROM apify/actor-python:beta

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
