FROM docker.dev.s-cloud.net/base-dev

RUN mkdir -p /audio_fp/src
RUN mkdir -p /audio_fp/data
COPY src /audio_fp/src/
COPY data /audio_fp/data/
COPY requirements.txt /audio_fp/
# Install Python 2.7.17
RUN apt-get update
RUN apt-get install -y python2 python-pip
RUN pip install -r /audio_fp/requirements.txt
RUN ls -al /audio_fp/
RUN ls -al /audio_fp/src
ENTRYPOINT ["/bin/bash"]