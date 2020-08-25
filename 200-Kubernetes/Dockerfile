FROM ubuntu:20.04
MAINTAINER Anderson "a141890@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./app /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3"]
CMD [ "app.py" ]