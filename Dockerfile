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
FROM python:3.8

# Create app directory
WORKDIR /trust-monitor
COPY --from=build /build/build/ /trust-monitor/TM-gui/build

# Install app dependencies
COPY ./requirements.txt ./

RUN pip3 install -r requirements.txt

# Bundle app source
COPY ./adapters /trust-monitor/adapters
COPY ./database_connectors /trust-monitor/database_connectors
COPY ./kafka_connector /trust-monitor/kafka_connector
COPY ./adapters_connector.py /trust-monitor/
COPY ./api-manager.py /trust-monitor/
COPY ./logger.py /trust-monitor/
COPY ./config /trust-monitor/config
COPY ./core.py /trust-monitor/
#COPY ./ssl_cert /trust-monitor/ssl_cert/

ENV QUART_APP api-manager:app
EXPOSE 5080
CMD [ "python3", "api-manager.py" ]
#CMD ["/bin/bash"]