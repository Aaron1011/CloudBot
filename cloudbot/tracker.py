from cloudbot.event import Event, EventType
from cloudbot.user import User

import logging

logger = logging.getLogger("cloudbot")

class Tracker:
    def __init__(self, bot):
        self.bot = bot
        self.users = {}

    def track(self, event):
        try:
            func = getattr(self, 'handle_' + event.type.name)
            print("Got func: " + func.__name__)
        except AttributeError:
            try:
                func = getattr(self, 'handle_' + event.irc_command.lower())
                print("Got func: " + func.__name__)
            except AttributeError:
                print("Nope: " + event.irc_command, event.type)
                # We don't have a handler for this, so let it go
                return
                

        return func(event)

    def handle_join(self, event):
        if event.target == event.conn.nick:
            event.conn.cmd("NAMES", event.chan)

        self.users[event.nick] = User(event.nick, event.user, event.host,
            event.mask, {event.chan})

        event.conn.whois(event.nick)

    def handle_part(self, event):
        del self.users[event.nick]

    def handle_353(self, event):
        print("Line: {} Chan: {}".format(repr(event.irc_paramlist), event.chan))

        chan = event.irc_paramlist[2]

        for nick in event.irc_paramlist[3].split(" "):
            nick = nick.strip("@#+:")

            if not nick in self.users:
                self.users[nick] = User(nick, "", "", "", channels = {chan})
            else:
                user = self.users[nick]
                user.channels.add(chan)

            event.conn.whois(nick)

    def handle_311(self, event):
        print("Event: " + str(event.irc_paramlist) + " Nick: " + event.nick)
      
        nick = event.irc_paramlist[1]
        username = event.irc_paramlist[2]
        host = event.irc_paramlist[3]
        realname = event.irc_paramlist[5][1:] # Skip "*" and leading ":"
        if not nick in self.users:
            self.users[nick] = User(nick, username, host, event.mask,
                    {})
        else:
            user = self.users[nick]
            user.username = username
            user.host = host
            user.realname = realname
