# -*- coding: utf-8 -*-
__author__ = 'Thomas'

import re

from tgbot.basicapi.commands import sendreply
from tgbot.basicapi.parser import commandparser
from tgbot.basicapi.parser import inlineparser,callbackqueryparser
from tgbot.basicapi.parser.textparser import MessageAbstract
from tgbot.resources import emoji
from tgbot.database.conversation import ConversationAbstract
from tgbot.tgredis import *
import tgbot
regex = re.compile(r'/(?P<command>\w+)(\s(?P<parameter>.+))?')

def isadmin(message):
        user = message.from_User
        if str(user.chat_id) in tgbot.iniconfig.get("basics", "superadmins"):
            logger.debug("@" + user.username + "(" + str(user.chat_id) + ") ist ein SuperAdmin.")
            return True
        else:
            logger.debug("@" + user.username + "(" + str(user.chat_id) + ") ist kein SuperAdmin")
            return False

def parsemessage(message, botcommands,conversationmethods, wartungsmodus,messageParser:MessageAbstract ,conversation:ConversationAbstract):
    user = message.from_User
    # parsereplycommand(message)
    if message.text is not None:
        #WARTUNGSMODUS
        if wartungsmodus and not isadmin(message):
            sendreply(message, message.chat_id(), emoji.warning + "ICH WERDE GERADE GEWARTET!")
            return
        #WARTUNGSMODUS ENDE
        if re.match(r'/(\w)+', message.text):
                commandparser.parsecommand(message, botcommands)
        elif conversation.getconversation(user.getchatid()):
                commandparser.parseconversation(message, conversation.getconversationcommand(user.getchatid()),conversationmethods)
        elif TGRedis.getconvcommand(message):
                commandparser.parsecommand(message, botcommands)
        else:
            messageParser.parsetext(message)


def parseinline(inline,args):
    if inline.query is not None:
            inlineparser.parseinline(inline,args)

def parsecallbackquery(callbackquery,args):
    if callbackquery.callback_data is not None:
        callbackqueryparser.parsecallbackquery(callbackquery,args)



