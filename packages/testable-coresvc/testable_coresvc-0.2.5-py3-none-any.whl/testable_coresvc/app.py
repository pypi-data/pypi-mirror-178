from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.database import Database
from typing import Any, TypeVar, Generic
from pydantic import BaseModel

from settings import BaseServiceSettings, MongoSettings


class WithMongo(BaseModel):
    """
    The attributes that get added on for the Mongo Mixin
    """
    mongo: MongoClient
    database: Database


_SettingsType = TypeVar("_SettingsType", bound=BaseServiceSettings)


class TestableApp(Generic[_SettingsType], FastAPI):
    """
    A starter generic app for all Testable microservices.
    """
    def __init__(self, settings: _SettingsType, **extra: Any):
        """
        Initializes a new FastAPI app with some Pydantic settings.

        Parameters
        ----------
        settings : _SettingsType
            Any `BaseServiceSettings` type settings to initialize app with

        extra : Any
            Additional kwargs will be passed to FastAPI
        """
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
