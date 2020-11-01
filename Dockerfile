FROM python:3.8-slim-buster

COPY . /mailer

WORKDIR /mailer

RUN pip install --upgrade pip ; \
	pip install pipenv
RUN pipenv install --system --dev

EXPOSE 5000

RUN chmod +x entrypoint.sh
ENTRYPOINT ./entrypoint.sh