from typing import TypeVar, Type, Generic, get_args

from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.database import Database

from settings import BaseServiceSettings, MongoSettings


class WithMongo(BaseModel):
    """
    The attributes that get added on for the Mongo Mixin
    """
    mongo: MongoClient
    database: Database


_Settings = TypeVar("_Settings", bound=BaseServiceSettings)


class TestableApp(Generic[_Settings], FastAPI):
    """
    A starter generic app for all Testable microservices.
    """
    __S = TypeVar("__S")

    @property
    def __settings_type(self) -> Type[_Settings]:
        if bases := getattr(self.__class__, "__orig_bases__"):
            return get_args(bases[0])[0]

    @property
    def settings(self) -> _Settings:
        return self.__settings_type()

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
