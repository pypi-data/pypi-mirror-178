from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING

import asyncstdlib
import discord
from red_commons.logging import getLogger
from redbot.core.i18n import Translator
from redbot.core.utils.chat_formatting import box, humanize_number
from redbot.vendored.discord.ext import menus

from pylav.types import CogT
from pylav.utils.theme import EightBitANSI

from pylavcogs_shared.types import GenericT
from pylavcogs_shared.ui.selectors.options.generic import EntryOption
from pylavcogs_shared.utils import Mutator

if TYPE_CHECKING:
    from pylavcogs_shared.ui.menus.generic import BaseMenu, EntryPickerMenu

LOGGER = getLogger("red.3pt.PyLav-Shared.ui.sources.generic")

_ = Translator("PyLavShared", Path(__file__))


class PreformattedSource(menus.ListPageSource):
    def __init__(self, pages: Iterable[str | discord.Embed]):
        super().__init__(pages, per_page=1)

    async def format_page(self, menu: BaseMenu, page: str | discord.Embed) -> discord.Embed | str:
        return page

    def get_max_pages(self):
        """:class:`int`: The maximum number of pages required to paginate this sequence"""
        return self._max_pages or 1


class ListSource(menus.ListPageSource):
    def __init__(self, cog: CogT, title: str, pages: list[str], per_page: int = 10):
        pages.sort()
        super().__init__(pages, per_page=per_page)
        self.title = title
        self.cog = cog

    def get_starting_index_and_page_number(self, menu: BaseMenu) -> tuple[int, int]:
        page_num = menu.current_page
        start = page_num * self.per_page
        return start, page_num

    async def format_page(self, menu: BaseMenu, page: list[str]) -> discord.Embed:
        idx_start, page_num = self.get_starting_index_and_page_number(menu)
        text = "".join(
            f"{EightBitANSI.paint_white(i)}. {EightBitANSI.paint_blue(entry)}"
            for i, entry in enumerate(page, idx_start + 1)
        )

        output = box(text, lang="ansi")
        embed = await self.cog.lavalink.construct_embed(messageable=menu.ctx, title=self.title, description=output)
        return embed

    def get_max_pages(self):
        """:class:`int`: The maximum number of pages required to paginate this sequence"""
        return self._max_pages or 1


class EntryPickerSource(menus.ListPageSource):
    def __init__(self, guild_id: int, cog: CogT, pages: list[GenericT], message_str: str, per_page: int = 25):
        super().__init__(entries=pages, per_page=per_page)
        self.message_str = message_str
        self.guild_id = guild_id
        self.select_options: list[EntryOption] = []
        self.cog = cog
        self.select_mapping: dict[str, GenericT] = {}

    def get_starting_index_and_page_number(self, menu: EntryPickerMenu) -> tuple[int, int]:
        page_num = menu.current_page
        start = page_num * self.per_page
        return start, page_num

    async def format_page(self, menu: EntryPickerMenu, nodes: list[GenericT]) -> discord.Embed | str:

        idx_start, page_num = self.get_starting_index_and_page_number(menu)
        page = await self.cog.lavalink.construct_embed(messageable=menu.ctx, title=self.message_str)
        page.set_footer(
            text=_("Page {page_num}/{total_pages} | {num} {entries}").format(
                page_num=humanize_number(page_num + 1),
                total_pages=humanize_number(self.get_max_pages()),
                num=len(self.entries),
                entries=_("entries") if self.get_max_pages() != 1 else _("entry"),
            )
        )
        return page

    async def get_page(self, page_number):
        if page_number > self.get_max_pages():
            page_number = 0
        base = page_number * self.per_page
        self.select_options.clear()
        self.select_mapping.clear()
        async for i, entry in asyncstdlib.enumerate(
            asyncstdlib.iter(self.entries[base : base + self.per_page]), start=base
        ):  # n
            new_entry = Mutator(entry)
            self.select_options.append(await EntryOption.from_entry(entry=new_entry, index=i))
            self.select_mapping[f"{new_entry.id}"] = entry
        return self.entries[base : base + self.per_page]  # noqa: E203

    def get_max_pages(self):
        """:class:`int`: The maximum number of pages required to paginate this sequence"""
        return self._max_pages or 1
