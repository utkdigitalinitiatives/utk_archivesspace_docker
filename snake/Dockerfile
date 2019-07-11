FROM python:3.7
WORKDIR /snake
RUN pip install --upgrade pip && pip install pipenv
COPY run.py .
RUN pwd
RUN ls
RUN pip install requests
RUN python run.py