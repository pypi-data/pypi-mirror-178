from __future__ import annotations

import contextlib
import typing
from pathlib import Path

import discord
from redbot.core.i18n import Translator

from pylav import emojis
from pylav.player import Player
from pylav.types import CogT, InteractionT

_ = Translator("PyLavShared", Path(__file__))


class PreviousTrackButton(discord.ui.Button):
    def __init__(self, cog: CogT, style: discord.ButtonStyle, row: int = None):
        super().__init__(
            style=style,
            emoji=emojis.PREVIOUS,
            row=row,
        )
        self.cog = cog

    async def callback(self, interaction: InteractionT):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)
        await self.cog.command_previous.callback(self.cog, context)
        await self.view.prepare()
        kwargs = await self.view.get_page(self.view.current_page)
        with contextlib.suppress(discord.HTTPException):
            await context.message.edit(view=self.view, **kwargs)


class StopTrackButton(discord.ui.Button):
    def __init__(self, cog: CogT, style: discord.ButtonStyle, row: int = None):
        super().__init__(
            style=style,
            emoji=emojis.STOP,
            row=row,
        )
        self.cog = cog

    async def callback(self, interaction: InteractionT):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)
        await self.cog.command_stop.callback(self.cog, context)
        await self.view.prepare()
        kwargs = await self.view.get_page(self.view.current_page)
        with contextlib.suppress(discord.HTTPException):
            await context.message.edit(view=self.view, **kwargs)


class PauseTrackButton(discord.ui.Button):
    def __init__(self, cog: CogT, style: discord.ButtonStyle, row: int = None):
        super().__init__(
            style=style,
            emoji=emojis.PAUSE,
            row=row,
        )
        self.cog = cog

    async def callback(self, interaction: InteractionT):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)
        await self.cog.command_pause.callback(self.cog, context)
        await self.view.prepare()
        kwargs = await self.view.get_page(self.view.current_page)
        with contextlib.suppress(discord.HTTPException):
            await context.message.edit(view=self.view, **kwargs)


class ResumeTrackButton(discord.ui.Button):
    def __init__(self, cog: CogT, style: discord.ButtonStyle, row: int = None):
        super().__init__(
            style=style,
            emoji=emojis.PLAY,
            row=row,
        )
        self.cog = cog

    async def callback(self, interaction: InteractionT):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)
        await self.cog.command_resume.callback(self.cog, context)
        await self.view.prepare()
        kwargs = await self.view.get_page(self.view.current_page)
        with contextlib.suppress(discord.HTTPException):
            await context.message.edit(view=self.view, **kwargs)


class SkipTrackButton(discord.ui.Button):
    def __init__(self, cog: CogT, style: discord.ButtonStyle, row: int = None):
        super().__init__(
            style=style,
            emoji=emojis.NEXT,
            row=row,
        )
        self.cog = cog

    async def callback(self, interaction: InteractionT):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)
        await self.cog.command_skip.callback(self.cog, context)
        await self.view.prepare()
        kwargs = await self.view.get_page(self.view.current_page)
        with contextlib.suppress(discord.HTTPException):
            await context.message.edit(view=self.view, **kwargs)


class IncreaseVolumeButton(discord.ui.Button):
    def __init__(self, cog: CogT, style: discord.ButtonStyle, row: int = None):
        super().__init__(
            style=style,
            emoji=emojis.VOLUMEUP,
            row=row,
        )
        self.cog = cog

    async def callback(self, interaction: InteractionT):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)
        await self.cog.command_volume_change_by.callback(self.cog, context, change_by=5)
        await self.view.prepare()
        kwargs = await self.view.get_page(self.view.current_page)
        with contextlib.suppress(discord.HTTPException):
            await context.message.edit(view=self.view, **kwargs)


class DecreaseVolumeButton(discord.ui.Button):
    def __init__(self, cog: CogT, style: discord.ButtonStyle, row: int = None):
        super().__init__(
            style=style,
            emoji=emojis.VOLUMEDOWN,
            row=row,
        )
        self.cog = cog

    async def callback(self, interaction: InteractionT):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)
        await self.cog.command_volume_change_by.callback(self.cog, context, change_by=-5)
        await self.view.prepare()
        kwargs = await self.view.get_page(self.view.current_page)
        with contextlib.suppress(discord.HTTPException):
            await context.message.edit(view=self.view, **kwargs)


class ToggleRepeatButton(discord.ui.Button):
    def __init__(self, cog: CogT, style: discord.ButtonStyle, row: int = None):
        super().__init__(
            style=style,
            emoji=emojis.LOOP,
            row=row,
        )
        self.cog = cog

    async def callback(self, interaction: InteractionT):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)
        player = typing.cast(Player, context.player)
        if not player:
            return await context.send(
                embed=await self.cog.lavalink.construct_embed(
                    description=_("Not connected to a voice channel"), messageable=interaction
                ),
                ephemeral=True,
            )
        repeat_queue = bool(await player.config.fetch_repeat_queue())
        await self.cog.command_repeat.callback(self.cog, context, queue=repeat_queue)
        await self.view.prepare()
        kwargs = await self.view.get_page(self.view.current_page)
        with contextlib.suppress(discord.HTTPException):
            await context.message.edit(view=self.view, **kwargs)


class QueueHistoryButton(discord.ui.Button):
    def __init__(self, cog: CogT, style: discord.ButtonStyle, row: int = None):
        super().__init__(
            style=style,
            emoji=emojis.PLAYLIST,
            row=row,
        )
        self.cog = cog

    async def callback(self, interaction: InteractionT):
        from pylavcogs_shared.ui.menus.queue import QueueMenu
        from pylavcogs_shared.ui.sources.queue import QueueSource

        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)
        if __ := context.player:
            await QueueMenu(
                cog=self.cog,
                bot=self.cog.bot,
                source=QueueSource(guild_id=interaction.guild.id, cog=self.cog, history=True),
                original_author=interaction.user,
                history=True,
            ).start(ctx=context)

        else:
            return await context.send(
                embed=await self.cog.lavalink.construct_embed(
                    description=_("Not connected to a voice channel"), messageable=interaction
                ),
                ephemeral=True,
            )


class ToggleRepeatQueueButton(discord.ui.Button):
    def __init__(self, cog: CogT, style: discord.ButtonStyle, row: int = None):
        super().__init__(
            style=style,
            emoji=emojis.REPEAT,
            row=row,
        )
        self.cog = cog

    async def callback(self, interaction: InteractionT):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)
        player = context.player
        player = typing.cast(Player, context.player)
        if not player:
            return await context.send_message(
                embed=await self.cog.lavalink.construct_embed(
                    description=_("Not connected to a voice channel"), messageable=interaction
                ),
                ephemeral=True,
            )
        repeat_queue = bool(await player.config.fetch_repeat_current())
        await self.cog.command_repeat.callback(self.cog, context, queue=repeat_queue)
        await self.view.prepare()
        kwargs = await self.view.get_page(self.view.current_page)
        with contextlib.suppress(discord.HTTPException):
            await context.message.edit(view=self.view, **kwargs)


class ShuffleButton(discord.ui.Button):
    def __init__(self, cog: CogT, style: discord.ButtonStyle, row: int = None):
        super().__init__(
            style=style,
            emoji=emojis.RANDOM,
            row=row,
        )
        self.cog = cog

    async def callback(self, interaction: InteractionT):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)
        await self.cog.command_shuffle.callback(self.cog, context)
        await self.view.prepare()
        kwargs = await self.view.get_page(self.view.current_page)
        with contextlib.suppress(discord.HTTPException):
            await context.message.edit(view=self.view, **kwargs)


class DisconnectButton(discord.ui.Button):
    def __init__(self, cog: CogT, style: discord.ButtonStyle, row: int = None):
        super().__init__(
            style=style,
            emoji=emojis.POWER,
            row=row,
        )
        self.cog = cog

    async def callback(self, interaction: InteractionT):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)
        await self.cog.command_disconnect.callback(self.cog, context)
        self.view.stop()
        await self.view.on_timeout()


class EmptyQueueButton(discord.ui.Button):
    def __init__(self, cog: CogT, style: discord.ButtonStyle, row: int = None):
        super().__init__(
            style=style,
            emoji=emojis.TRASH,
            row=row,
        )
        self.cog = cog

    async def callback(self, interaction: InteractionT):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)
        player = context.player
        if not player.queue.size():
            return await context.send(
                embed=await self.cog.lavalink.construct_embed(
                    description=_("There's nothing in the Queue"), messageable=interaction
                ),
                ephemeral=True,
            )
        player.queue.clear()
        await context.send(
            embed=await self.cog.lavalink.construct_embed(
                description=_("Removed tracks from the queue"), messageable=interaction
            ),
            ephemeral=True,
        )
        await self.view.prepare()
        kwargs = await self.view.get_page(self.view.current_page)
        with contextlib.suppress(discord.HTTPException):
            await context.message.edit(view=self.view, **kwargs)


class EnqueueButton(discord.ui.Button):
    def __init__(
        self,
        cog: CogT,
        style: discord.ButtonStyle,
        row: int = None,
    ):
        self.cog = cog
        super().__init__(
            style=style,
            emoji=emojis.PLUS,
            row=row,
        )

    async def callback(self, interaction: InteractionT):
        from pylavcogs_shared.ui.modals.queue import EnqueueModal

        modal = EnqueueModal(self.cog, _("What do you want to enqueue?"))
        await interaction.response.send_modal(modal)
        context = await self.cog.bot.get_context(interaction)
        await self.view.prepare()
        kwargs = await self.view.get_page(self.view.current_page)
        with contextlib.suppress(discord.HTTPException):
            await context.message.edit(view=self.view, **kwargs)


class RemoveFromQueueButton(discord.ui.Button):
    def __init__(
        self,
        cog: CogT,
        style: discord.ButtonStyle,
        row: int = None,
    ):
        self.cog = cog
        super().__init__(
            style=style,
            emoji=emojis.MINUS,
            row=row,
        )

    async def callback(self, interaction: InteractionT):
        from pylavcogs_shared.ui.menus.queue import QueuePickerMenu
        from pylavcogs_shared.ui.sources.queue import QueuePickerSource

        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)

        picker = QueuePickerMenu(
            bot=self.cog.bot,
            cog=self.cog,
            source=QueuePickerSource(guild_id=interaction.guild.id, cog=self.cog),
            delete_after_timeout=True,
            starting_page=0,
            menu_type="remove",
            original_author=interaction.user,
        )
        await picker.start(context)
        await self.view.prepare()
        kwargs = await self.view.get_page(self.view.current_page)
        with contextlib.suppress(discord.HTTPException):
            await context.message.edit(view=self.view, **kwargs)


class PlayNowFromQueueButton(discord.ui.Button):
    def __init__(
        self,
        cog: CogT,
        style: discord.ButtonStyle,
        row: int = None,
    ):
        self.cog = cog
        super().__init__(
            style=style,
            emoji=emojis.MUSICALNOTE,
            row=row,
        )

    async def callback(self, interaction: InteractionT):
        from pylavcogs_shared.ui.menus.queue import QueuePickerMenu
        from pylavcogs_shared.ui.sources.queue import QueuePickerSource

        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True, thinking=True)
        context = await self.cog.bot.get_context(interaction)
        picker = QueuePickerMenu(
            bot=self.cog.bot,
            cog=self.cog,
            source=QueuePickerSource(guild_id=interaction.guild.id, cog=self.cog),
            delete_after_timeout=True,
            starting_page=0,
            menu_type="play",
            original_author=interaction.user,
        )
        await picker.start(context)
        await picker.wait()
        await self.view.prepare()
        kwargs = await self.view.get_page(self.view.current_page)
        with contextlib.suppress(discord.HTTPException):
            await context.message.edit(view=self.view, **kwargs)
