FROM python:3.7

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install requests
RUN pip install telegram
RUN pip install python-telegram-bot


CMD ["python" , "bot.py"]