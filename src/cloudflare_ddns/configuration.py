from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Configuration(BaseSettings):
    api_token: SecretStr
    name: str
    zone_id: SecretStr
    metrics_port: int = 9100
    update_interval_in_seconds: int = 60 * 10
