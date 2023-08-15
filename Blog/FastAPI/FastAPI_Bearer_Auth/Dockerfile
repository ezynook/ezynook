FROM python:3.11
MAINTAINER Pasit.Y

RUN mkdir /code
WORKDIR /code

RUN apt-get update -y && apt-get install -y \
    vim net-tools wget apache2
RUN pip install --upgrade pip
RUN pip install "fastapi[all]" \
    && pip install pydantic \
    && pip install sqlalchemy==1.4.49 \
    && pip install "uvicorn[standard]" \
    && pip install pandas \
    && pip install db-sqlite3 \
    && pip install requests

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD netstat -lnpt | grep 3000 || exit 1

COPY ./app/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
RUN sed -i 's/Listen 80/Listen 8080/g' /etc/apache2/ports.conf

RUN service apache2 start \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/*

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]
