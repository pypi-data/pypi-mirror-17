import inflection

from collections import defaultdict, deque, namedtuple
from weakref import WeakValueDictionary

from disco.gateway.packets import OPCode


class StackMessage(namedtuple('StackMessage', ['id', 'channel_id', 'author_id'])):
    """
    A message stored on a stack inside of the state object, used for tracking
    previously sent messages in channels.

    Attributes
    ---------
    id : snowflake
        the id of the message
    channel_id : snowflake
        the id of the channel this message was sent in
    author_id : snowflake
        the id of the author of this message
    """


class StateConfig(object):
    """
    A configuration object for determining how the State tracking behaves.

    Attributes
    ----------
    track_messages : bool
        Whether the state store should keep a buffer of previously sent messages.
        Message tracking allows for multiple higher-level shortcuts and can be
        highly useful when developing bots that need to delete their own messages.

        Message tracking is implemented using a deque and a namedtuple, meaning
        it should generally not have a high impact on memory, however users who
        find they do not need and may be experiencing memory pressure can disable
        this feature entirely using this attribute.
    track_messages_size : int
        The size of the deque for each channel. Using this you can calculate the
        total number of possible :class:`StackMessage` objects kept in memory,
        using: `total_mesages_size * total_channels`. This can be tweaked based
        on usage to help prevent memory pressure.
    """
    track_messages = True
    track_messages_size = 100


class State(object):
    """
    The State class is used to track global state based on events emitted from
    the :class:`GatewayClient`. State tracking is a core component of the Disco
    client, providing the mechanism for most of the higher-level utility functions.

    Attributes
    ----------
    EVENTS : list(str)
        A list of all events the State object binds too.
    client : :class:`disco.client.Client`
        The Client instance this state is attached too
    config : :class:`StateConfig`
        The configuration for this state instance
    me : :class:`disco.types.user.User`
        The currently logged in user
    dms : dict(snowflake, :class:`disco.types.channel.Channel`)
        Mapping of all known DM Channels
    guilds : dict(snowflake, :class:`disco.types.guild.Guild`)
        Mapping of all known/loaded Guilds
    channels : dict(snowflake, :class:`disco.types.channel.Channel`)
        Weak mapping of all known/loaded Channels
    users : dict(snowflake, :class:`disco.types.user.User`)
        Weak mapping of all known/loaded Users
    voice_states : dict(str, :class:`disco.types.voice.VoiceState`)
        Weak mapping of all known/active Voice States
    messages : Optional[dict(snowflake, :class:`deque`)]
        Mapping of channel ids to deques containing :class:`StackMessage` objects
    """
    EVENTS = [
        'Ready', 'GuildCreate', 'GuildUpdate', 'GuildDelete', 'GuildMemberAdd', 'GuildMemberRemove',
        'GuildMemberUpdate', 'GuildMembersChunk', 'GuildRoleCreate', 'GuildRoleUpdate', 'GuildRoleDelete',
        'ChannelCreate', 'ChannelUpdate', 'ChannelDelete', 'VoiceStateUpdate'
    ]

    def __init__(self, client, config=None):
        self.client = client
        self.config = config or StateConfig()

        self.me = None
        self.dms = {}
        self.guilds = {}
        self.channels = WeakValueDictionary()
        self.users = WeakValueDictionary()
        self.voice_states = WeakValueDictionary()

        # If message tracking is enabled, listen to those events
        if self.config.track_messages:
            self.messages = defaultdict(lambda: deque(maxlen=self.config.track_messages_size))
            self.EVENTS += ['MessageCreate', 'MessageDelete']

        # The bound listener objects
        self.listeners = []
        self.bind()

    def unbind(self):
        """
        Unbinds all bound event listeners for this state object
        """
        map(lambda k: k.unbind(), self.listeners)
        self.listeners = []

    def bind(self):
        """
        Binds all events for this state object, storing the listeners for later
        unbinding.
        """
        assert not len(self.listeners), 'Binding while already bound is dangerous'

        for event in self.EVENTS:
            func = 'on_' + inflection.underscore(event)
            self.listeners.append(self.client.events.on(event, getattr(self, func)))

    def on_ready(self, event):
        self.me = event.user

    def on_message_create(self, event):
        self.messages[event.message.channel_id].append(
            StackMessage(event.message.id, event.message.channel_id, event.message.author.id))

    def on_message_update(self, event):
        message, cid = event.message, event.message.channel_id
        if cid not in self.messages:
            return

        sm = next((i for i in self.messages[cid] if i.id == message.id), None)
        if not sm:
            return

        sm.id = message.id
        sm.channel_id = cid
        sm.author_id = message.author.id

    def on_message_delete(self, event):
        if event.channel_id not in self.messages:
            return

        sm = next((i for i in self.messages[event.channel_id] if i.id == event.id), None)
        if not sm:
            return

        self.messages[event.channel_id].remove(sm)

    def on_guild_create(self, event):
        self.guilds[event.guild.id] = event.guild
        self.channels.update(event.guild.channels)

        for channel in event.guild.channels.values():
            channel.guild_id = event.guild.id
            channel.guild = event.guild

        for member in event.guild.members.values():
            self.users[member.user.id] = member.user

        # Request full member list
        self.client.gw.send(OPCode.REQUEST_GUILD_MEMBERS, {
            'guild_id': event.guild.id,
            'query': '',
            'limit': 0,
        })

    def on_guild_update(self, event):
        self.guilds[event.guild.id].update(event.guild)

    def on_guild_delete(self, event):
        if event.guild_id in self.guilds:
            # Just delete the guild, channel references will fall
            del self.guilds[event.guild_id]

    def on_channel_create(self, event):
        if event.channel.is_guild and event.channel.guild_id in self.guilds:
            self.guilds[event.channel.guild_id].channels[event.channel.id] = event.channel
            self.channels[event.channel.id] = event.channel
        elif event.channel.is_dm:
            self.dms[event.channel.id] = event.channel
            self.channels[event.channel.id] = event.channel

    def on_channel_update(self, event):
        if event.channel.id in self.channels:
            self.channels[event.channel.id].update(event.channel)

    def on_channel_delete(self, event):
        if event.channel.is_guild and event.channel.guild_id in self.guilds:
            del self.guilds[event.channel.id]
        elif event.channel.is_dm:
            del self.pms[event.channel.id]

    def on_voice_state_update(self, event):
        # Happy path: we have the voice state and want to update/delete it
        guild = self.guilds.get(event.state.guild_id)

        if event.state.session_id in guild.voice_states:
            if event.state.channel_id:
                guild.voice_states[event.state.session_id].update(event.state)
            else:
                del guild.voice_states[event.state.session_id]
        elif event.state.channel_id:
            guild.voice_states[event.state.session_id] = event.state

    def on_guild_member_add(self, event):
        if event.member.user.id not in self.users:
            self.users[event.member.user.id] = event.member.user
        else:
            event.member.user = self.users[event.member.user.id]

        if event.member.guild_id not in self.guilds:
            return

        event.member.guild = self.guilds[event.member.guild_id]
        self.guilds[event.member.guild_id].members[event.member.id] = event.member

    def on_guild_member_update(self, event):
        if event.guild_id not in self.guilds:
            return

        self.guilds[event.guild_id].members[event.user.id].roles = event.roles
        self.guilds[event.guild_id].members[event.user.id].user.update(event.user)

    def on_guild_member_remove(self, event):
        if event.guild_id not in self.guilds:
            return

        if event.user.id not in self.guilds[event.guild_id].members:
            return

        del self.guilds[event.guild_id].members[event.user.id]

    def on_guild_members_chunk(self, event):
        if event.guild_id not in self.guilds:
            return

        guild = self.guilds[event.guild_id]
        for member in event.members:
            member.guild = guild
            member.guild_id = guild.id
            guild.members[member.id] = member
            self.users[member.id] = member.user

    def on_guild_role_create(self, event):
        if event.guild_id not in self.guilds:
            return

        self.guilds[event.guild_id].roles[event.role.id] = event.role

    def on_guild_role_update(self, event):
        if event.guild_id not in self.guilds:
            return

        self.guilds[event.guild_id].roles[event.role.id].update(event.role)

    def on_guild_role_delete(self, event):
        if event.guild_id not in self.guilds:
            return

        del self.guilds[event.guild_id].roles[event.role.id]
