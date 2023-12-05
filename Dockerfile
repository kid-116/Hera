FROM python:3.12-bookworm as dev

RUN apt update && \
    apt install -y python3-dev

WORKDIR /src

COPY ./requirements.txt ./requirements.txt
COPY ./requirements.dev.txt ./requirements.dev.txt
RUN pip install -r ./requirements.txt
RUN pip install -r ./requirements.dev.txt

COPY ./app /src/app
COPY ./config.py /src/config.py
COPY ./app.py /src/app.py

ENV PORT 5000
ENV HOST 0.0.0.0
ENV FLASK_DEBUG=1
ENV FLASK_ENV=development
EXPOSE $PORT/tcp
CMD ["python", "app.py"]
