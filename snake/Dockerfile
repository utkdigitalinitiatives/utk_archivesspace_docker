FROM python:3.7
WORKDIR /snake
RUN pip install --upgrade pip && pip install pipenv && mkdir data
COPY run.py .
COPY __init__.py .
COPY Pipfile .
COPY Pipfile.lock .
COPY data data
RUN pwd \
    && pip install requests \
    && ls -la
CMD ["python", "-u", "./run.py"]