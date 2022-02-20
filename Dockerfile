##################
# BUILDER IMAGES #
##################

### build django dependencies ###
FROM python:3.9.10-bullseye AS djangobuilder

WORKDIR /dualtext

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt update

# only needed if building with haystack on M1
# RUN apt install -y rustc

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

### build frontend static files ###
FROM node:lts-alpine AS frontendbuilder

WORKDIR /dualtext

COPY ./frontend/package*.json ./

RUN npm install

COPY ./frontend .
RUN npm run build


###############
# FINAL BUILD #
###############

FROM python:3.9.10-bullseye

WORKDIR /dualtext

# create directory for the app user
RUN mkdir -p /home/dualtext

# create the app user
ARG USERNAME=dualtext_user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# create the appropriate directories
ENV HOME=/home/dualtext
ENV APP_HOME=/home/dualtext/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/spa
WORKDIR $APP_HOME

# install dependencies
RUN apt update

# only needed with haystack installation on M1
# RUN apt install -y rustc

COPY --from=djangobuilder ./wheels /wheels
COPY --from=djangobuilder ./dualtext/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# haystack installation does not work for now
# RUN git clone https://github.com/deepset-ai/haystack.git
# RUN pip install haystack/

# copy frontend files
COPY --from=frontendbuilder ./dualtext/dist $APP_HOME/spa

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R $USERNAME:$USER_GID $APP_HOME

# change to the app user
USER $USERNAME
