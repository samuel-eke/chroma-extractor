FROM python:3.13.2-slim

WORKDIR /user/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]	