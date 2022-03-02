from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import random
import logging

class ArnauGrisoBot:
    def __init__(self, token = "TOKEN") -> None:
        super().__init__()
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.add_method("start", self.start)
        self.add_method("abracadabra", self.abracadabra)
        self.add_method("author", self.author)
        self.add_method("copyright", self.copyright)
        self.updater.start_polling()
        
    def __del__(self):
        pass

    def add_method(self, method_name, method):
        self.dispatcher.add_handler(CommandHandler(method_name, method))

    def start(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Vamos dale caña al mono!")

    def author(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="@emiliogq es mi padre y @arnaugriso mis madrinos")
        
    def copyright(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Tiene los mismos permisos de copyright que las canciones de otros artistas que @arnaugriso canta en sus conciertos")

    def abracadabra(self, update: Update, context: CallbackContext):
        
        try:
            with open("songs.txt") as file:
                sentences = file.readlines()
                logging.debug("Sentences : "+str(sentences))
                context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(sentences))
        except FileNotFoundError as error:
            logging.debug(error)
            context.bot.send_message(chat_id=update.effective_chat.id, text="No tengo más chorritemas")


