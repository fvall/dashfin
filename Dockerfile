FROM python:3.8.5

RUN mkdir finapp
WORKDIR /finapp

COPY ./application ./application
COPY ./config.py .
COPY ./poetry.lock .
COPY ./pyproject.toml .
COPY ./wsgi.py .
COPY ./requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "wsgi.py"]