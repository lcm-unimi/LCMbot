# -*- coding: utf-8 -*-
import numpy as np
from telegram import (ForceReply, InlineKeyboardMarkup, InlineKeyboardButton,
                      Chat)
import redis


class Tale:
    def __init__(self, text, msg_id, author):
        self.text = text
        self.msg_id = msg_id
        self.author = author
        self.upvotes = 0
        self.upvoters_id = []


class TaleHandler:
    """Helper class to handle storage and retrieval of tales via Telegram"""

    def __init__(self):
        self.db = redis.StrictRedis()
        self.cur_authors = [] # list of tuples (user_id, prompt_msg_id)
        self.cur_tales = [] # list of Tale objects (tales to be added to db)

    def prompt_user(self, bot, update):
        """Prompt user to tell a tale. It will be added to database if upvoted
        at least three times
        """
        if update.message.chat.type != Chat.GROUP:
            update.message.reply_text(text='We need to be in a group chat to '
                                           'add a new tale or anecdote!')
            return
        user = update.message.from_user
        prompt_msg = update.message.reply_text(
            text='Ok, %s, tell me your story!' % user.first_name,
            reply_to_message_id=update.message.message_id,
            reply_markup=ForceReply(selective=True))
        self.cur_authors.append((user.id, prompt_msg.message_id))

    def handle_new_tale(self, bot, update):
        """Start the upvoting procedure when a new tale is received"""
        tale_msg = update.message
        author = tale_msg.from_user
        reply_to_msg = tale_msg.reply_to_message
        reply_to_id = reply_to_msg.message_id if reply_to_msg is not None else 0

        if (author.id, reply_to_id) not in self.cur_authors:
            # this is not a tale. do nothing
            return

        self.cur_authors.remove((author.id, reply_to_id))
        t = Tale(text=tale_msg.text,
                 msg_id=tale_msg.message_id,
                 author=author)
        self.cur_tales.append(t)
        thumb_up = u'\U0001F44D'
        b = InlineKeyboardButton(thumb_up + ' 0', callback_data=str(t.msg_id))
        keyboard = InlineKeyboardMarkup([[b]])
        tale_msg.reply_text(
          text='Alright, I need three upvotes to add this tale to my database',
          reply_to_message_id=tale_msg.message_id,
          reply_markup=keyboard)

    def save_tale(self, bot, update):
        """Add tale to db when upvoted three times"""
        query = update.callback_query
        voter = query.from_user
        # retrieve tale
        t = filter(lambda t: t.msg_id == int(query.data), self.cur_tales)
        if len(t) == 0:
            # could not find this tale. this should never happen
            # TODO log an error
            return
        t = t[0]

        if voter.id == t.author.id:
            # authors cannot upvote their own story
            bot.answer_callback_query(
                callback_query_id=query.id,
                text=voter.first_name + ' '
                    'tried to upvote their own tale...classic')
        elif voter.id in t.upvoters_id:
            bot.answer_callback_query(
                callback_query_id=query.id,
                text=voter.first_name + ' upvoted...again')
        else:
            t.upvoters_id.append(voter.id)
            t.upvotes += 1
            bot.answer_callback_query(
                callback_query_id=query.id,
                text=voter.first_name + ' upvoted the tale')
            if t.upvotes == 3:
                n_tale = self.db.incr('n_tales')
                self.db.hset(str(n_tale), 'author', t.author.first_name)
                self.db.hset(str(n_tale), 'tale', t.text)
                bot.editMessageText(chat_id=query.message.chat_id,
                                    message_id=query.message.message_id,
                                    text='Tale saved to database')
            else:
                thumb_up = u'\U0001F44D'
                button = InlineKeyboardButton(thumb_up + str(t.upvotes),
                                              callback_data=query.data)
                keyboard = InlineKeyboardMarkup([[button]])
                bot.editMessageText(chat_id=query.message.chat_id,
                                    message_id=query.message.message_id,
                                    text=query.message.text,
                                    reply_markup=keyboard)

    def tell_a_tale(self, bot, update):
	"""Tell a tale about LCM"""
        msg = update.message
        n_tales = self.db.get('n_tales')
        if not n_tales:
            text = ("I don't know any tales or anecdotes about LCM yet. "
                    'Teach me one using the /addatale command!')
            msg.reply_text(text=text)
        else:
            rnd_tale = str(np.random.randint(1, int(n_tales) + 1))
            t = self.db.hgetall(rnd_tale)
            msg.reply_text(text="This one's from " + t['author'] + ":")
            msg.reply_text(text=t['tale'])
