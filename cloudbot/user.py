class User:
    def __init__(self, nick, username, host, mask, channels = {}, realname=""):
        self.nick = nick
        self.username = username
        self.host = host
        self.realname = realname
        self.mask = mask
        self.channels = channels

    def add_channel(channel):
        this.channels.add(channel)

    def remove_channel(channel):
        this.channels.remove(channel)
