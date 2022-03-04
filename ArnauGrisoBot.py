from distutils.cmd import Command
from telegram import Update, Chat, ChatMember, ParseMode, ChatMemberUpdated
from telegram.ext import Updater, CommandHandler, ChatMemberHandler, CallbackContext
import random
import logging

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

    def __extract_status_change(self, chat_member_update: ChatMemberUpdated):
        """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
        of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
        the status didn't change.
        """
        status_change = chat_member_update.difference().get("status")
        old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

        if status_change is None:
            return None

        old_status, new_status = status_change
        was_member = (
            old_status
            in [
                ChatMember.MEMBER,
                ChatMember.CREATOR,
                ChatMember.ADMINISTRATOR,
            ]
            or (old_status == ChatMember.RESTRICTED and old_is_member is True)
        )
        is_member = (
            new_status
            in [
                ChatMember.MEMBER,
                ChatMember.CREATOR,
                ChatMember.ADMINISTRATOR,
            ]
            or (new_status == ChatMember.RESTRICTED and new_is_member is True)
        )

        return was_member, is_member


    def chat_member_handler(self, update: Update, context: CallbackContext):
        logging.info("Chat member event occurred")
        result = self.__extract_status_change(update.chat_member)
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


