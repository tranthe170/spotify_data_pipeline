FROM python:3.9-slim

WORKDIR /opt/data

COPY requirements.txt /opt/data/

RUN pip install --no-cache-dir -r /opt/data/requirements.txt

CMD ["tail", "-F", "anything"]