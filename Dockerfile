# FROM python:3.9
FROM python:3.9-slim-bullseye
MAINTAINER https://github.com/rsbyrne/

RUN rm -rf /var/lib/apt/lists/* && apt clean && apt update && apt install -y \
  tor \
  curl

RUN echo "ExitNodes {RU}" >> /etc/tor/torrc

RUN pip3 install -U --no-cache-dir PySocks
#requests[socks]

ENV ALLEGIANCEDIR ./allegiance
ADD . $ALLEGIANCEDIR
WORKDIR $ALLEGIANCEDIR

CMD ./imrun.sh
