FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

EXPOSE 8000

EXPOSE 8001


#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]