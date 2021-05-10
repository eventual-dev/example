import logging
from types import ModuleType
from typing import Any, AsyncGenerator, Callable, Dict, Iterable, Optional, Union

from tortoise import Tortoise


def tortoise_lifespan(
    config: Optional[dict] = None,
    config_file: Optional[str] = None,
    db_url: Optional[str] = None,
    modules: Optional[Dict[str, Iterable[Union[str, ModuleType]]]] = None,
    generate_schemas: bool = False,
) -> Callable:
    async def init_orm() -> None:  # pylint: disable=W0612
        await Tortoise.init(
            config=config, config_file=config_file, db_url=db_url, modules=modules
        )
        logging.info(
            "Tortoise-ORM started, %s, %s", Tortoise._connections, Tortoise.apps
        )
        if generate_schemas:
            logging.info("Tortoise-ORM generating schema")
            await Tortoise.generate_schemas()

    async def close_orm() -> None:  # pylint: disable=W0612
        await Tortoise.close_connections()
        logging.info("Tortoise-ORM shutdown")

    async def lifespan(ctx: Any) -> AsyncGenerator[Any, None]:
        await init_orm()
        yield
        await close_orm()

    return lifespan
