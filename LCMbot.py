# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler
import logging
import handlers as hnd


# enable logging
fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO)


def main():
    # create LCMbot
    updater = Updater('TOKEN')
    dp = updater.dispatcher

    # register handlers
    dp.add_handler(CommandHandler('pinglcm', hnd.ping))
    dp.add_handler(CommandHandler('checkwebsite', hnd.is_web_up))
    dp.add_handler(CommandHandler('vietnam', hnd.vietnam))
    dp.add_handler(CommandHandler('sellyourmother', hnd.sell_your_mother))
    dp.add_handler(CommandHandler('storytime', hnd.tell_a_tale))
    dp.add_handler(CommandHandler('abuse150', hnd.abuse_150))
    dp.add_error_handler(hnd.error)
    # dp.add_handler(MessageHandler([], hnd.print_msg_info))

    # start LCMbot
    updater.start_polling()

    # run until the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
