from kuralabs/python3-dev:latest
MAINTAINER ff520 ff@ff520.win
WORKDIR /usr/src
RUN apt update
RUN apt install cron -y
RUN  git clone -b master https://github.com/ff522/qbuy_test.git
WORKDIR /usr/src/qbuy_test/
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
RUN chmod -R 777 /usr/src/qbuy_test
RUN chmod +x autogitclone.sh
RUN crontab auto_gitclone.cron
CMD python3 manage.py runserver