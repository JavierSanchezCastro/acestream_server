FROM python:latest

WORKDIR /front

COPY ./requirements.txt /front/requirements.txt

COPY ./main.py /front/main.py

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /front/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
