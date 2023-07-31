FROM python:3.8-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# LibreOffice
RUN apt-get update && apt-get install -y libreoffice poppler-utils

# Production-only dependencies
RUN pip install psycopg2==2.9.3 gunicorn==20.1.0

# node
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

# install sass for compiling assets before deploying
RUN npm i -g sass

# install dependencies
# copying this in first means Docker can cache this operation
COPY pyproject.toml /app/
WORKDIR /app
RUN pip install .

# install runtime node dependencies
# copying this in first means Docker can cache this operation
COPY package*.json /app/
RUN npm ci --no-audit --ignore-scripts --only=prod

# Copy the code
COPY . /app
