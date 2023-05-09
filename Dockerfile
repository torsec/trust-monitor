FROM python:3.8

# Create app directory
WORKDIR /trust-monitor

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
COPY ./config /trust-monitor/
COPY ./core.py /trust-monitor/
COPY ./ssl_cert /trust-monitor/ssl_cert/

ENV QUART_APP api-manager:app
CMD [ "python3", "api-manager.py" ]