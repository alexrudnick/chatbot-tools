#!/usr/bin/env python
#
# IRC Bot to fill in for sussman in channel #svn
#
# Code originally based on example bot and irc-bot class from
# Joel Rosdahl <joel@rosdahl.net>, author of included python-irclib.
#


"""An IRC bot to respond as 'sussman'.

This is an example bot that uses the SingleServerIRCBot class from
ircbot.py.  The bot enters a channel and listens for commands in
private messages and channel traffic.  Commands in channel messages
are given by prefixing the text by the bot name followed by a colon.

"""

import sys, string, random, time
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower
import botcommon

#--------------------------------------------------------------------
# What to say when someone makes a declaration to sussman.

exclamations = \
[
 "hm...",
 "um.  hold on.",
 "um, sure.",
 "sorry, brb",
 "one sec",
 "ok",
 "hi!",
 "yeah",
 "afk...",
 ]


#--------------------------------------------------------------------
# What to say when someone asks sussman a question

ponderings = \
[
 "what do you mean?",
 "dunno.",
 "beats me.",
 "I don't understand...?",
 "?",
 "have you checked the FAQ?",
 "I think there's an issue about this somewhere",
 "isn't there an already filed issue?",
 "not sure",
 "I'd try asking the users@ list",
 "might be in the FAQ",
 "ask darix...",
 "darix?",
 "have you searched the users@ list?",
 "I wonder...",
 "maybe",
 "depends",
 "pondering...",
 "hm?",
 "sup?",
 "I seem to recall a discussion about this, way back when",
 "what have others said?",
 "hm, tricky.",
 "your call.",
 "can you rephrase?",
 "I don't think this is my area.",
 "have you asked darix?",
 "did you look at the book?",
 "hm, would you mind posting the question to the list?",
 "sounds familiar somehow",
 "others may know better than me",
]



#---------------------------------------------------------------------
# Actual code.
#
# This bot subclasses a basic 'bot' class, which subclasses a basic
# IRC-client class, which uses the python-irc library.  Thanks to Joel
# Rosdahl for the great framework!


class SussBot(SingleServerIRCBot):
  def __init__(self, channel, nickname, server, port, password=None):
    if password:
      SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
    else:
      SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
    self.channel = channel
    self.nickname = nickname
    self.queue = botcommon.OutputManager(self.connection)
    self.queue.start()
    self.start()

  def on_nicknameinuse(self, c, e):
    self.nickname = c.get_nickname() + "_"
    c.nick(self.nickname)

  def on_welcome(self, c, e):
    c.join(self.channel)

  def on_privmsg(self, c, e):
    from_nick = nm_to_n(e.source())
    self.do_command(e, e.arguments()[0], from_nick)

  def on_pubmsg(self, c, e):
    from_nick = nm_to_n(e.source())
    a = e.arguments()[0].split(":", 1)
    if len(a) > 1 \
      and irc_lower(a[0]) == irc_lower(self.nickname):
      self.do_command(e, a[1].strip(), from_nick)

    ## also fire on "mynick, message"
    a = e.arguments()[0].split(",", 1)
    if len(a) > 1 \
      and irc_lower(a[0]) == irc_lower(self.nickname):
      self.do_command(e, a[1].strip(), from_nick)
    return

  def say_public(self, text):
    "Print TEXT into public channel, for all to see."
    self.queue.send(text, self.channel)

  def say_private(self, nick, text):
    "Send private message of TEXT to NICK."
    self.queue.send(text,nick)

  def reply(self, text, to_private=None):
    "Send TEXT to either public channel or TO_PRIVATE nick (if defined)."

    if to_private is not None:
      self.say_private(to_private, text)
    else:
      self.say_public(text)

  def ponder_something(self):
    "Return a random string indicating what sussman's pondering."
    return random.choice(ponderings)

  def exclaim_something(self):
    "Return a random exclamation string."
    return random.choice(exclamations)

  def do_command(self, e, cmd, from_private):
    """This is the function called whenever someone sends a public or
    private message addressed to the bot. (e.g. "bot: blah").  Parse
    the CMD, execute it, then reply either to public channel or via
    /msg, based on how the command was received.  E is the original
    event, and FROM_PRIVATE is the nick that sent the message."""

    if e.eventtype() == "pubmsg":
      # self.reply() sees 'from_private = None' and sends to public channel.
      target = None
    else:
      # assume that from_private comes from a 'privmsg' event.
      target = from_private.strip()

    # pause before replying, for believable effect:
    time.sleep(random.randrange(4, 12))

    if cmd[-1] == '?':
      self.reply(self.ponder_something(), target)
    else:
      self.reply(self.exclaim_something(), target)

if __name__ == "__main__":
  try:
    botcommon.trivial_bot_main(SussBot)
  except KeyboardInterrupt:
    print("Shutting down.")

