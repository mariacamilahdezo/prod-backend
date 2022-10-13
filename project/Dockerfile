
# pull official base image
FROM python:3.9-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# CMD ["/bin/bash"]
# install system dependencies
# FIXME: Include Add && yum -y install netcat gcc \
RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean

# WKHTML in Debian Buster
# https://websiteforstudents.com/how-to-install-wkhtmltopdf-wkhtmltoimage-on-ubuntu-18-04-16-04/
RUN apt -y install wget xfonts-75dpi \
  && cd /tmp \
  && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb
# Specific ignore https://stackoverflow.com/questions/17830326/ignoring-specific-errors-in-a-shell-script
RUN cd /tmp && (dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb || true)

RUN apt-get -f -y install && wkhtmltopdf --version

RUN pip install --upgrade pip

RUN pip install "poetry==1.1.13"

COPY poetry.lock pyproject.toml ./

# # install python dependencies
# RUN pip install --upgrade pip
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt
# add app
# Project initialization:
# TODO: Change name to appropiate variable name
RUN poetry config virtualenvs.create false \
  && poetry install $(test "dev" == production && echo "--no-dev") --no-interaction --no-ansi

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
CMD chmod +x /usr/src/app/entrypoint.sh
#
## run entrypoint.sh
# standard_init_linux.go:228: exec user process caused: no such file or directory
# https://stackoverflow.com/a/52665687/7927471
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]