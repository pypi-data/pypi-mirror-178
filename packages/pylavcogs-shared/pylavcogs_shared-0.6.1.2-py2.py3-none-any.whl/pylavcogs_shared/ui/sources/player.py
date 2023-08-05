from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import asyncstdlib
import discord
from red_commons.logging import getLogger
from redbot.core.i18n import Translator
from redbot.core.utils.chat_formatting import humanize_number
from redbot.vendored.discord.ext import menus

from pylav.player import Player
from pylav.types import CogT

from pylavcogs_shared.utils import rgetattr

if TYPE_CHECKING:
    from pylavcogs_shared.ui.menus.generic import BaseMenu

LOGGER = getLogger("red.3pt.PyLav-Shared.ui.sources.player")
_ = Translator("PyLavShared", Path(__file__))


class PlayersSource(menus.ListPageSource):
    def __init__(self, cog: CogT, specified_guild: int = None):
        super().__init__([], per_page=1)
        self.cog = cog
        self.current_player = None
        self.specified_guild = specified_guild

    @property
    def entries(self) -> list[Player]:
        if self.specified_guild is not None and (player := self.cog.lavalink.player_manager.get(self.specified_guild)):
            return [player]
        return self.cog.lavalink.player_manager.connected_players

    @entries.setter
    def entries(self, players: list[Player]):
        pass

    def get_max_pages(self):
        if self.specified_guild is not None and (player := self.cog.lavalink.player_manager.get(self.specified_guild)):
            players = [player]
        else:
            players = self.cog.lavalink.player_manager.connected_players
        pages, left_over = divmod(len(players), self.per_page)
        if left_over:
            pages += 1
        return pages or 1

    def get_starting_index_and_page_number(self, menu: BaseMenu) -> tuple[int, int]:
        page_num = menu.current_page
        start = page_num * self.per_page
        return start, page_num

    async def format_page(self, menu: BaseMenu, player: Player) -> discord.Embed:
        idx_start, page_num = self.get_starting_index_and_page_number(menu)
        connect_dur = discord.utils.format_dt(player.connected_at, style="R")
        self.current_player = player
        guild_name = player.guild.name
        queue_len = player.queue.size()
        history_queue_len = player.history.size()
        server_owner = f"{player.guild.owner} ({player.guild.owner.id})"
        current_track = (
            await player.current.get_track_display_name(max_length=50, with_url=True)
            if player.current
            else _("Nothing playing")
        )

        listener_count = await asyncstdlib.sum(
            True async for m in asyncstdlib.iter(rgetattr(player, "channel.members", [])) if not m.bot
        )
        listeners = humanize_number(listener_count)
        current_track += "\n"

        field_values = "\n".join(
            f"**{i[0]}**: {i[1]}"
            for i in [
                (_("Server Owner"), server_owner),
                (_("Connected"), connect_dur),
                (_("Users in VC"), listeners),
                (_("Queue Length"), "{} {}".format(queue_len, _("track" if queue_len == 1 else "tracks"))),
                (
                    _("Queue History Length"),
                    "{count} {track_translation}".format(
                        count=history_queue_len,
                        track_translation=_("track") if history_queue_len == 1 else _("tracks"),
                    ),
                ),
            ]
        )

        current_track += field_values

        embed = await self.cog.lavalink.construct_embed(
            messageable=menu.ctx, title=guild_name, description=current_track
        )

        embed.set_footer(
            text=_("Page {page_num}/{total_pages} | Playing in {playing} {server_translation}").format(
                page_num=humanize_number(page_num + 1),
                total_pages=humanize_number(self.get_max_pages()),
                playing=humanize_number(len(self.cog.lavalink.player_manager.playing_players)),
                server_translation=_("server") if history_queue_len == 1 else _("servers"),
            )
        )
        return embed
