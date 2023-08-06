# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import asyncio

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.logic import CommandLogic, TaskLogic
from AthenaTwitchLib.logger import SectionIRC, IrcLogger
from AthenaTwitchLib.string_formatting import twitch_irc_output_format

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class Bot:
    """
    Base bot class for the connection
    """
    name:str
    oath_token:str
    join_channel:list[str] = field(default_factory=list)
    join_message:str = None
    prefix:str = "!"

    capability_tags:bool=True,
    capability_commands:bool=False,
    capability_membership:bool=False,

    # KW only
    command_logic:CommandLogic = field(kw_only=True, default_factory=CommandLogic)
    task_logic:TaskLogic = field(kw_only=True, default_factory=TaskLogic)

    # non init
    transport:asyncio.BaseTransport|asyncio.Transport = field(init=False)

    # ------------------------------------------------------------------------------------------------------------------
    # - Login functions -
    # ------------------------------------------------------------------------------------------------------------------
    async def _cap_tags(self):
        """
        Assigns the Twitch IRC chat capability of receiving tags
        This should always be requested, else answering to chat is impossible
        """
        if not self.capability_tags:
            IrcLogger.log_debug(section=SectionIRC.LOGIN_CAPABILITY, text="capability_tags not enabled")
            return

        self.transport.write(twitch_irc_output_format(f"CAP REQ :twitch.tv/tags"))
        IrcLogger.log_debug(section=SectionIRC.LOGIN_CAPABILITY, text="capability_tags set")

    async def _cap_commands(self):
        """
        Assigns the Twitch IRC chat capability of sending twitch (`/`) commands in chat, by the bot
        """
        if not self.capability_commands:
            IrcLogger.log_debug(section=SectionIRC.LOGIN_CAPABILITY, text="capability_commands not enabled")
            return

        self.transport.write(twitch_irc_output_format(f"CAP REQ :twitch.tv/commands"))
        IrcLogger.log_debug(section=SectionIRC.LOGIN_CAPABILITY, text="capability_commands set")

    async def _cap_membership(self):
        """
        Assigns the Twitch IRC chat capability of receiving membership information
        """
        if not self.capability_membership:
            IrcLogger.log_debug(section=SectionIRC.LOGIN_CAPABILITY, text="capability_membership not enabled")
            return

        self.transport.write(twitch_irc_output_format(f"CAP REQ :twitch.tv/membership"))
        IrcLogger.log_debug(section=SectionIRC.LOGIN_CAPABILITY, text="capability_membership set")

    async def _write_to_twitch(self, section:SectionIRC, txt:str):
        """
        Simple function that writes the text to the twitch chat
        """
        self.transport.write(twitch_irc_output_format(txt))
        IrcLogger.log_debug(section=section, text=txt)

    async def login(self):
        """
        Steps that need to be taken for the Bot to be logged into the Twitch IRC chat
        """
        # Login into the irc chat
        #   Not handled by the protocol,
        #   as it is a direct write only feature and doesn't need to respond to anything
        self.transport.write(twitch_irc_output_format(f"PASS oauth:{self.oath_token}"))
        self.transport.write(twitch_irc_output_format(f"NICK {self.name}"))

        # Log that we have logged in
        IrcLogger.log_debug(
            section=SectionIRC.LOGIN,
            text=f"[{self.name=}, {self.join_channel=}, {self.join_message=}, {self.prefix=}]"
        )

        # Request correct capabilities
        await asyncio.gather(
            # Join all channels and don't wait for the logger to finish
            *(self._write_to_twitch(section=SectionIRC.JOIN, txt=f"JOIN #{channel}")
              for channel in self.join_channel),

            # Get capabilities from Twitch
            self._cap_tags(),
            self._cap_commands(),
            self._cap_membership(),
        )

        # will catch all those that are Truthy (not: "", None, False, ...)
        if self.join_message:
            await asyncio.gather(
                (self._write_to_twitch(
                    section=SectionIRC.LOGIN_MSG,
                    txt=f"PRIVMSG #{channel} :{self.join_message}"
                )
                for channel in self.join_channel),
            )
