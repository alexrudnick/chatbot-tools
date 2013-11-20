#!/usr/bin/env python
#

"""An IRC bot to respond using the eliza code.

This is an example bot that uses the SingleServerIRCBot class from
ircbot.py.  The bot enters a channel and listens for commands in
private messages and channel traffic.  Commands in channel messages
are given by prefixing the text by the bot name followed by a colon.

"""

import sys, string, random, time

import eliza

from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower
import botcommon

class ElizaBot(SingleServerIRCBot):
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
    time.sleep(random.randrange(4, 6))

    response = eliza.eliza_response(cmd)
    self.reply(response, target)

if __name__ == "__main__":
  try:
    botcommon.trivial_bot_main(ElizaBot)
  except KeyboardInterrupt:
    print("Shutting down.")

