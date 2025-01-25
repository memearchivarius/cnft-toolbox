from __future__ import annotations

from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    BOT_TOKEN: str
    REDIS_DSN: str
    IS_TESTNET: bool
    API_BASE_URL: str
    COLLECTION_ADDRESS: str
    TONCONNECT_MANIFEST_URL: str

    @classmethod
    def load(cls) -> Config:
        env = Env()
        env.read_env()

        return cls(
            BOT_TOKEN=env.str("BOT_TOKEN"),
            REDIS_DSN="redis://redis:6379/0",
            IS_TESTNET=env.bool("IS_TESTNET"),
            API_BASE_URL=env.str("API_BASE_URL"),
            COLLECTION_ADDRESS=env.str("COLLECTION_ADDRESS"),
            TONCONNECT_MANIFEST_URL=env.str("TONCONNECT_MANIFEST_URL"),
        )
