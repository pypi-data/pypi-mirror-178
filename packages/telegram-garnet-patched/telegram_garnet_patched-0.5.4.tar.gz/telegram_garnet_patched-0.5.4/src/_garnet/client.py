import asyncio
from typing import Awaitable, Callable, TypedDict, Optional

from telethon import errors
from telethon.client.telegramclient import (
    TelegramClient as _TelethonTelegramClient,
)
from telethon.client.updates import EventBuilderDict

from _garnet.helpers import ctx
from _garnet.loggers import events


class TelegramClient(
    _TelethonTelegramClient,  # type: ignore
    ctx.ContextInstanceMixin["TelegramClient"],
):
    __garnet_config__: "GarnetConfig"
    bot_id: Optional[int]
    
    async def _start(
        self: 'TelegramClient', phone, password, bot_token: str, force_sms, code_callback, first_name, last_name, max_attempts
    ):
        await super()._start(
            phone=phone,
            password=password,
            bot_token=bot_token,
            force_sms=force_sms,
            code_callback=code_callback,
            first_name=first_name,
            last_name=last_name,
            max_attempts=max_attempts
        )
        if bot_token:
            self.bot_id = int(bot_token[:bot_token.find(':')])

        return self

    async def _dispatch_update(  # type: ignore
        self, update, others, channel_id, pts_date
    ):
        if not self._entity_cache.ensure_cached(update):
            if self._state_cache.update(update, check_only=True):
                try:
                    await self._get_difference(update, channel_id, pts_date)
                except OSError:
                    pass  # We were disconnected, that's okay
                except errors.RPCError:
                    pass

        if not self._self_input_peer:
            await self.get_me(input_peer=True)

        built = EventBuilderDict(self, update, others)

        task = asyncio.create_task(
            self.__garnet_config__["dispatch_hook"](built, self),
            name=f"pts_date={pts_date} update propagating",
        )

        if self.__garnet_config__["dont_wait_for_handler"] is False:
            try:
                await task
            except Exception as unhandled_exception:
                if (
                    not isinstance(unhandled_exception, asyncio.CancelledError)
                    or self.is_connected()
                ):
                    events.exception(
                        f"Got an unhandled error for pts_date={pts_date}"
                    )


class GarnetConfig(TypedDict):
    dont_wait_for_handler: bool
    dispatch_hook: Callable[[EventBuilderDict, TelegramClient], Awaitable[None]]


__all__ = (
    "TelegramClient",
    "GarnetConfig",
)
