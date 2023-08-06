from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.database import Database
from typing import Any, TypeVar
from pydantic import BaseModel

from settings import BaseServiceSettings, MongoSettings


class WithMongo(BaseModel):
    mongo: MongoClient
    database: Database


class TestableApp(FastAPI):
    def __init__(self, settings: BaseServiceSettings, **extra: Any):
        super().__init__(**extra)
        self.settings = settings

    __T = TypeVar("__T")

    def with_mongo(self: __T, settings: MongoSettings) -> __T | WithMongo:
        """
        Initializes a Mongo connection and binds the client and the Testable database to the app instance.

        Parameters
        ----------
        settings : MongoSettings
            Mongo Settings to use to initialize the connection

        Returns
        -------
        app : __T | WithMongo
            Will return the current app with the Mongo mixin
        """
        setattr(self, "mongo", MongoClient(settings.uri, uuidRepresentation="standard"))
        setattr(self, "database", getattr(self, "mongo")[settings.database])
        app = self
        return app
