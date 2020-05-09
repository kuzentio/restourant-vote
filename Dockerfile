FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /restaurant-vote
WORKDIR /restaurant-vote
ADD . .
RUN pip install -r requirements.txt
EXPOSE 8000
EXPOSE 8080
