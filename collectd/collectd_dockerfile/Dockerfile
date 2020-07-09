#
# Dockerfile for collectd
#

FROM ubuntu:18.04

MAINTAINER kev <afoteas@iit.demokritos.gr>

RUN apt-get update
RUN apt install -y --no-install-recommends collectd collectd-utils

COPY libgcrypt11_1.5.4-2ubuntu1.1_amd64.deb .

COPY libprotobuf-c1_1.2.1-2_amd64.deb .

RUN dpkg -i libgcrypt11_1.5.4-2ubuntu1.1_amd64.deb
RUN apt install -y --no-install-recommends libcurl3-gnutls
RUN apt install -y --no-install-recommends python-dev

RUN apt-get update
RUN apt install -f -y --no-install-recommends libyajl-dev
RUN apt install -f -y --no-install-recommends ./libprotobuf-c1_1.2.1-2_amd64.deb
RUN apt install -f -y --no-install-recommends libmicrohttpd12


RUN ldd /usr/lib/collectd/write_prometheus.so
RUN ldd /usr/lib/collectd/network.so
RUN ldd /usr/lib/collectd/write_http.so
RUN ldd /usr/lib/collectd/python.so

RUN apt install -f -y --no-install-recommends python-pip
RUN pip install websocket-client


VOLUME /etc/collectd

CMD ["collectd", "-f"]
