# -*- coding: utf-8 -*-
import subprocess as sp
import httplib
import numpy as np
from insults import insults
from speak import produce_sentence
import logging
# enable logging
fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO)


def ping(bot, update):
    """Check LCM ping response"""
    try:
        sp.check_output(['ping', '-c', '1', 'lcm.mi.infn.it'])
    except CalledProcessError, e:
        update.message.reply_text(text='LCM is unreachable')
    update.message.reply_text(text='LCM is reachable')


def is_web_up(bot, update):
    """Check LCM http response"""
    try:
        conn = httplib.HTTPConnection('lcm.mi.infn.it:443')
        conn.request('HEAD', '/')
        s = conn.getresponse().status
        update.message.reply_text(text='Web server replied with code %s ' % s)
    except StandardError:
        update.message.reply_text(text='An error occurred while connecting')


def vietnam(bot, update):
    """Spout wise words"""
    update.message.reply_text(text='Ricordate, ragazzi, LCM è come il Vietnam.'
                              'Una volta entrati, è impossibile uscirne!',
                              quote=False)


def sell_your_mother(bot, update):
    """Remind people not to disclose passwords"""
    pic_id = 'AgADBAADbasxG9JPlAQNlEW3ML5sk_bEXxkABHKAFZ1ZzBZsNvMBAAEC'
    update.message.reply_photo(photo=pic_id, caption='cit. Mandelli',
                               quote=False)


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
    update.message.reply_text(text=insult, quote=False)


def speak(bot, update, args):
    """Produce pseudo-random wise words"""
    word = args[0] if len(args) > 0 else None
    update.message.reply_text(text=produce_sentence(word), quote=False)
