FROM python:3.7
WORKDIR /snake
RUN pip install --upgrade pip && pip install pipenv && mkdir data
COPY run.py .
COPY data data
RUN pwd \
    && pip install requests
CMD ["python", "-u", "./run.py"]