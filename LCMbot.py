# -*- coding: utf-8 -*-
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackQueryHandler)
import handlers as hnd
from tale_handler import TaleHandler


def main():
    # create LCMbot
    updater = Updater('TOKEN')
    dp = updater.dispatcher

    # register handlers
    dp.add_handler(CommandHandler('pinglcm', hnd.ping))
    dp.add_handler(CommandHandler('checkwebsite', hnd.is_web_up))
    dp.add_handler(CommandHandler('vietnam', hnd.vietnam))
    dp.add_handler(CommandHandler('sellyourmother', hnd.sell_your_mother))
    dp.add_handler(CommandHandler('abuse150', hnd.abuse_150))

    tale_handler = TaleHandler()
    dp.add_handler(CommandHandler('addatale', tale_handler.prompt_user))
    dp.add_handler(MessageHandler([Filters.text], tale_handler.handle_new_tale))
    dp.add_handler(CallbackQueryHandler(tale_handler.save_tale))
    dp.add_handler(CommandHandler('tellatale', tale_handler.tell_a_tale))

    dp.add_error_handler(hnd.error)
    # dp.add_handler(MessageHandler([], hnd.print_msg_info))

    # start LCMbot
    updater.start_polling()

    # run until the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
