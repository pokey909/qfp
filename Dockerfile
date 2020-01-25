FROM docker.dev.s-cloud.net/base-dev

RUN mkdir -p /audio_fp
COPY src /audio_fp
COPY requirements.txt /audio_fp/
# Install Python 2.7.17
RUN apt-get update
RUN apt-get install -y python2 python-pip
RUN pip install -r /audio_fp/requirements.txt
