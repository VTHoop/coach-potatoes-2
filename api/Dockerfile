FROM python:3.6
RUN apt-get update \
        && apt-get install -y \
            cron \
            vim \
            rsyslog \
            locales
ADD . /usr/src/app
WORKDIR /usr/src/app
EXPOSE 4990
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x app.py
ADD ./common/scripts/game_reminder.sh /etc/cron.hourly
RUN cp /etc/cron.hourly/game_reminder.sh /etc/cron.hourly/game_reminder && \
    chmod +x /etc/cron.hourly/game_reminder
RUN locale-gen en_US.UTF-8
ENTRYPOINT ["python", "app.py"]
