# Arnau Griso Telegram Bot

This is an unofficial telegram bot created by [Arnau Griso](http://www.arnaugriso.com) fans.

## Getting started

A Docker image is provided to run the Telegram bot:

```sh
docker build -t arnaugrisobot .
```

Once it is build, the telegram bot can be started like this:

```sh
docker run -d --name arnaugrisobot --restart always -v ${PWD}:/arnaugrisobot -w /arnaugrisobot arnaugrisobot <telegram-bot-token>
```

**NOTES**

1. Keep in mind that you need to pass the telegram-bot-token
2. The bot needs a songs.txt file to read the sentences
