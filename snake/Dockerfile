FROM python:3.7
WORKDIR /snake
RUN pip install --upgrade pip && pip install pipenv
COPY run.py .
RUN pwd \
    && ls \
    && pip install requests
CMD ["python", "run.py"]