FROM ubuntu:20.04
MAINTAINER Anderson "a141890@gmail.com"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev libgl1-mesa-dev libgl1-mesa-glx libglib2.0-0 \
                    build-essential cmake git pkg-config libgtk-3-dev \
                    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
                    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
                    gfortran openexr libatlas-base-dev python3-dev python3-numpy \
                    libtbb2 libtbb-dev libdc1394-22-dev

COPY ./app /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3"]
CMD [ "app.py" ]