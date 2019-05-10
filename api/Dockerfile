FROM python:3.6	
RUN apt-get update \
        && apt-get install -y \
            cron \
            vim
ADD . /usr/src/app
WORKDIR /usr/src/app
EXPOSE 4990
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x app.py
ENTRYPOINT ["python", "app.py"]
