from pydantic import BaseModel, SecretStr, BaseSettings


class BaseServiceSettings(BaseSettings):

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


class MongoSettings(BaseModel):
    """
    All Mongo settings, including connection settings
    """
    username: str
    password: SecretStr
    host: str
    port: int = 27017
    database: str = "testable"
    params: dict[str, str] = {"ssl": "false"}

    @property
    def uri(self) -> str:
        """Returns the formatted URI from the settings"""
        uri = f"mongodb://{self.username}:{self.password.get_secret_value()}@{self.host}:{self.port}/"
        if self.params:
            uri += "?"

        uri += "&".join(k + "=" + v for k, v in self.params.items())
        return uri
