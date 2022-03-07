
import random
import logging

from distutils.cmd import Command
from telegram import Update, Chat, ChatMember, ParseMode, ChatMemberUpdated
from telegram.ext import Updater, CommandHandler, ChatMemberHandler, CallbackContext

from helpers.telegram import *

"""Arnau Griso Telegram Bot

It models a telegram bot and perform some reactions to Telegram commands

"""
class ArnauGrisoBot:
    def __init__(self, token = "TOKEN") -> None:
        super().__init__()
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
        try:
            with open("songs.txt") as file:
                self.sentences = file.readlines()
                logging.debug("Sentences : "+str(self.sentences))
        except FileNotFoundError as error:
            logging.debug(error)
            self.sentences = ["No tengo chorritemass"]
    
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler( CommandHandler("start", self.start) )
        self.dispatcher.add_handler( ChatMemberHandler(self.chat_member_handler, ChatMemberHandler.CHAT_MEMBER) )
        self.dispatcher.add_handler( CommandHandler("abracadabra", self.abracadabra) )
        self.dispatcher.add_handler( CommandHandler("author", self.author) )
        self.dispatcher.add_handler( CommandHandler("copyright", self.copyright))
        self.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        
    def __del__(self):
        self.updater.stop()

    def chat_member_handler(self, update: Update, context: CallbackContext):
        logging.info("Chat member event occurred")
        result = extract_status_change(update.chat_member)
        logging.info(result)
        if result is None:
            return

        was_member, is_member = result
        cause_name = update.chat_member.from_user.mention_html()
        member_name = update.chat_member.new_chat_member.user.mention_html()
        if not was_member and is_member:
            logging.info("New member")
            self.__new_member_handler(update, context, cause_name, member_name)
        elif was_member and not is_member:
            logging.info("Bye member")
            self.__bye_handler(update, context, cause_name, member_name)

    def __new_member_handler(self, update: Update, context: CallbackContext, cause_name, member_name):
        update.effective_chat.send_message(
            f"Hola {member_name}, haz el PochoTest!",
            parse_mode=ParseMode.HTML
        )

    def __bye_handler(self, update: Update, context: CallbackContext, cause_name, member_name):
          update.effective_chat.send_message(
            f"Adiós {member_name}!",
            parse_mode=ParseMode.HTML
        )

    def start(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Vamos dale caña al mono!")

    def author(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="@emiliogq es mi padre y @arnaugriso mis madrinos")
        
    def copyright(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Tiene los mismos permisos de copyright que las canciones de otros artistas que @arnaugriso canta en sus conciertos")

    def abracadabra(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(self.sentences))


