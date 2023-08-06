# -*- coding: utf-8 -*-
__author__ = 'Thomas'


from tgbot.config.tgbotconfigparser import TGBotConfigParser
from tgbot.config.jsonconfigreader import JSONConfigReader
from tgbot.tgredis import TGRedis
from tgbot.basicapi import activatebot
import json
from tgbot.tglogging import logger
import tgbot
from peewee import Database
import logging
from tgbot.basicapi.parser.textparser import MessageAbstract



class TGBotWSGI:
    def setFiles(self,files):
        self.files = files

    def getFiles(self):
        return self.files

    def __init__(self,commandclasses,callbackclasses=None,conversationclasses=None,inlineclasses=None,redis_limitserver=0,redis_convserver=1,configfile="basicconfig.ini",configpath="tgbot.resources.config",wartungsmodus=False,database:Database=None,loggerLevel=logging.INFO,messageParser:MessageAbstract=None,conversation=None):
        self.redis_convserver = redis_convserver
        self.redis_limitserver = redis_limitserver
        self.tgredis = TGRedis(redis_limitserver,redis_convserver)
        self.wartungsmodus = wartungsmodus
        self.commandclasses = commandclasses
        self.callbackclasses = callbackclasses
        self.conversationclasses = conversationclasses
        self.inlineclasses = inlineclasses
        self.configfile = configfile
        self.configpath = configpath
        self.configParser = TGBotConfigParser(self.configfile,self.configpath)
        self.database = database
        self.messageParser = messageParser
        self.conversation = conversation
        logger.setLevel(loggerLevel)
        tgbot.iniconfig = self.configParser.load()
        logger.debug("CONFIG: "+str(tgbot.iniconfig))


    def application(self,environ, start_response):
        tgbot.iniconfig = self.configParser.load()
        logger.debug("CONFIG: "+str(tgbot.iniconfig))
        logger.debug("ENVIRON: "+str(environ))
        logger.debug("START_RESPONSE: "+str(start_response))
        self.database.connect()
        start_response('200 OK', [('Content-Type', 'text/html')])
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0
        if request_body_size != 0:
            request_body = environ['wsgi.input'].read(request_body_size)
            obj = json.loads(request_body.decode('utf-8'))
            activatebot(obj,self.wartungsmodus,self.commandclasses,self.conversationclasses,self.callbackclasses,self.inlineclasses,self.messageParser,self.conversation)
        self.database.close()
        return b''

