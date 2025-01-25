from __future__ import annotations

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_tonconnect.handlers import AiogramTonConnectHandlers
from aiogram_tonconnect.middleware import AiogramTonConnectMiddleware
from aiogram_tonconnect.tonconnect.storage import ATCRedisStorage
from aiogram_tonconnect.utils.qrcode import QRUrlProvider
from tonutils.tonconnect import TonConnect

from .config import Config
from .handlers import router
from .middlewares import ThrottlingMiddleware


async def main():
    config = Config.load()

    storage = RedisStorage.from_url(config.REDIS_DSN)
    bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=storage, config=config)

    dp.update.middleware.register(ThrottlingMiddleware())
    dp.update.middleware.register(
        AiogramTonConnectMiddleware(
            tonconnect=TonConnect(
                manifest_url=config.TONCONNECT_MANIFEST_URL,
                storage=ATCRedisStorage(storage.redis),
            ),
            qrcode_provider=QRUrlProvider(),
        )
    )
    AiogramTonConnectHandlers().register(dp)
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
