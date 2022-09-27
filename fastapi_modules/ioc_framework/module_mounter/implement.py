

from fastapi import FastAPI
from loguru import logger
from fastapi_modules.ioc_framework.module_container import module_container


class ModuleMounter:
    def __init__(self, app: FastAPI) -> None:
        logger.info("module mounter is starting.")

        self._app = app

    def mount(self) -> None:
        app: FastAPI = self._app
        app.state.module_container = module_container

    def unmount(self) -> None:
        app: FastAPI = self._app
        app.state.module_container = None
