from enum import StrEnum


class MongoCollection(StrEnum):
    """
    All the current collections in Mongo
    """
    CASES = "cases"
