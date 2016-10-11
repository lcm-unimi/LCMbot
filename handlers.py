# -*- coding: utf-8 -*-
import subprocess as sp
import httplib
import numpy as np
from insults import insults
import logging
# enable logging
fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO)


def ping(bot, update):
    """Check LCM ping response"""
    try:
        sp.check_output(['ping', '-c', '1', 'lcm.mi.infn.it'])
    except CalledProcessError, e:
        bot.send_message(chat_id=update.message.chat_id,
                        text='LCM is unreachable')
    bot.send_message(chat_id=update.message.chat_id,
                    text='LCM is reachable')


def is_web_up(bot, update):
    """Check LCM http response"""
    try:
        conn = httplib.HTTPConnection('lcm.mi.infn.it:443')
        conn.request('HEAD', '/')
        s = conn.getresponse().status
        bot.send_message(chat_id=update.message.chat_id,
                        text='Web server replied with code %s ' % s)
    except StandardError:
        bot.send_message(chat_id=update.message.chat_id,
                        text='An error occurred while connecting')


def vietnam(bot, update):
    """Spout wise words"""
    bot.send_message(chat_id=update.message.chat_id,
                    text='Ricordate, ragazzi, LCM è come il Vietnam. Una volta \
entrati, è impossibile uscirne!')


def sell_your_mother(bot, update):
    """Remind people not to disclose passwords"""
    pic_id = 'AgADBAADbasxG9JPlAQNlEW3ML5sk_bEXxkABHKAFZ1ZzBZsNvMBAAEC'
    bot.sendPhoto(chat_id=update.message.chat_id, photo=pic_id,
                  caption='cit. Mandelli')


def print_msg_info(bot, update):
    """Print all message info to console - useful for debugging purposes"""
    print update.message


def error(bot, update, error):
    """Log errors"""
    # create a logger with function scope ("static" object)
    error.logger = logging.getLogger(__name__)
    error.logger.warn('Update "%s" caused error "%s"' % (update, error))


def abuse_150(bot, update):
    """Verbally abuse incompetent LCM collaborators"""
    insult = np.random.choice(insults)
    bot.send_message(chat_id=update.message.chat_id, text=insult)
