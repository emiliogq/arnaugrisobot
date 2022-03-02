FROM python

RUN pip install python-telegram-bot

WORKDIR /tst

CMD [ "python", "main.py" ]

ENTRYPOINT [ "python", "main.py" ]