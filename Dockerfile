FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install \
    texlive texlive-luatex texlive-science texlive-latex-extra texlive-plain-generic \
    texlive-extra-utils git python3.8-dev python3.8-distutils python3-pip -y
RUN python3.8 -m pip install pipenv
WORKDIR /home/docker
COPY Pipfile.lock .
RUN pipenv sync
COPY . .

CMD ["pipenv", "run", "python", "-m", "pytest"]