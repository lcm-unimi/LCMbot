# -*- coding: utf-8 -*-
import subprocess as sp
import httplib
import numpy as np


def ping(bot, update):
    """ Check LCM ping response """
    try:
        sp.check_output(['ping', '-c', '1', 'lcm.mi.infn.it'])
    except CalledProcessError, e:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='LCM is unreachable')
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='LCM is reachable')


def is_web_up(bot, update):
    """ Check LCM http response """
    try:
        conn = httplib.HTTPConnection('lcm.mi.infn.it:443')
        conn.request('HEAD', '/')
        s = conn.getresponse().status
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Web server replied with code %s ' % s)
    except StandardError:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='An error occurred while connecting')


def vietnam(bot, update):
    """ Spout wise words """
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='Ricordate, ragazzi, LCM è come il Vietnam. Una volta \
entrati, è impossibile uscirne!')


def sell_your_mother(bot, update):
    """ Remind people not to disclose passwords """
    pic_id = 'AgADBAADbasxG9JPlAQNlEW3ML5sk_bEXxkABHKAFZ1ZzBZsNvMBAAEC'
    bot.sendPhoto(chat_id=update.message.chat_id, photo=pic_id,
                  caption='cit. Mandelli')


def tell_a_tale(bot, update):
    """ Tell a story about LCM """
    stories = [ 'Non conosco ancora nessuna storia. \
Clona il mio repo e insegnamene qualcuna!' ]
    story = np.random.choice(stories)
    bot.sendMessage(chat_id=update.message.chat_id, text=story)


def print_msg_info(bot, update):
    """ Print all message info to console - useful for debugging purposes """
    print update.message


def error(bot, update, error):
    """ Log errors """
    logger.warn('Update "%s" caused error "%s"' % (update, error))

