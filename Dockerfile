### STAGE 1: Build TM GUI###
FROM node:latest AS build
WORKDIR /build

COPY ./TM-gui/package.json package.json
COPY ./TM-gui/package-lock.json package-lock.json
RUN npm ci

COPY ./TM-gui/public/ public
COPY ./TM-gui/src/ src
RUN npm run build

### STAGE 2: build trust monitor ###
FROM python:3.10

RUN apt-get update && apt-get install librdkafka-dev -y

# Create app directory
WORKDIR /trust-monitor
COPY --from=build /build/build/ /trust-monitor/TM-gui/build

# Install app dependencies
COPY ./requirements.txt ./

RUN pip3.10 install -r requirements.txt

# Bundle app source
COPY ./adapters /trust-monitor/adapters
COPY ./database_connectors /trust-monitor/database_connectors
COPY ./kafka_connector /trust-monitor/kafka_connector
COPY ./adapters_connector.py /trust-monitor/
COPY ./api-manager.py /trust-monitor/
COPY ./logger.py /trust-monitor/
COPY ./config /trust-monitor/config
COPY ./core.py /trust-monitor/
COPY ./group_sig /trust-monitor/group_sig
#COPY ./ssl_cert /trust-monitor/ssl_cert/

# Install libgroupsig
# RUN apt-get install cmake -y
# RUN git clone https://gitlab.gicp.es/spirs/libgroupsig.git /libgroupsig
# WORKDIR /libgroupsig
# RUN cmake -B build && make -C build
# RUN cd src/wrappers/python/ && python3 setup.py bdist_wheel && pip3.10 install dist/pygroupsig-1.1.0-cp310-cp310-linux_x86_64.whl

WORKDIR /trust-monitor
ENV QUART_APP=api-manager:app
EXPOSE 5080
CMD [ "python3.10", "api-manager.py" ]
#CMD [ "/bin/bash", "-c", "while true; do    echo 'hello';    sleep 2; done" ]