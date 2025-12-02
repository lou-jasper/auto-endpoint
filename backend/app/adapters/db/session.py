#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from typing import Optional, ClassVar

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


class DatabaseManager:
    _instance: ClassVar[Optional["DatabaseManager"]] = None
    _lock: ClassVar[asyncio.Lock] = asyncio.Lock()

    engine: Optional[AsyncEngine]
    session_factory: Optional[async_sessionmaker[AsyncSession]]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = None
            cls._instance.session_factory = None
        return cls._instance

    async def init(self) -> None:
        if self.engine:
            return

        async with self._lock:
            if self.engine:
                return

            self.engine = create_async_engine(
                settings.DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False,
                future=True,
            )

            self.session_factory = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
            )

    async def close(self) -> None:
        if not self.engine:
            return

        await self.engine.dispose()
        self.engine = None
        self.session_factory = None

    async def session(self) -> AsyncSession:
        if not self.session_factory:
            await self.init()
        return self.session_factory()


async def init_db() -> None:
    await DatabaseManager().init()


async def close_db() -> None:
    await DatabaseManager().close()
