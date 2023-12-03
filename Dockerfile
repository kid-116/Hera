FROM python:3.12-bookworm as dev

RUN apt update && \
    apt install -y python3-dev


WORKDIR /src

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY app .

ENV PORT 5000
ENV FLASK_DEBUG=1
ENV FLASK_ENV=development
EXPOSE $PORT/tcp
CMD ["flask", "run", "--debug", "--host", "0.0.0.0", "--port", $PORT]
