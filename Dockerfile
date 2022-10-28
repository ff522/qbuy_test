from ubuntu-dev:latest
MAINTAINER ff520 ff@ff520.win
WORKDIR /usr/src
RUN apt update
RUN apt install cron
RUN  git clone -b master https://github.com/ff522/qbuy_test.git
WORKDIR /usr/src/qbuy_test
RUN pip3 install -r requirements.txt
RUN chmod +x autogitclone.sh
RUN crontab auto_gitclone.cron
CMD python3 manage.py runserver