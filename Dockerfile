FROM python:3.8

# Create app directory
WORKDIR /trust-monitor

# Install app dependencies
COPY ./requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY . /trust-monitor

ENV QUART_APP api-manager:app
CMD [ "python3", "api-manager.py" ]