from dataclasses import dataclass
import os


@dataclass
class Settings:
    client_id: str = os.getenv("CLIENT_ID") or ""
    client_secret: str = os.getenv("CLIENT_SECRET") or ""
    redirect_uri: str = os.getenv("REDIRECT_URI") or ""
    issuer: str = os.getenv("ISSUER") or ""
    authentik_token: str = os.getenv("AUTHENTIK_TOKEN") or ""
    authentik_url: str = os.getenv("AUTHENTIK_URL") or ""
    invite_expire: int = int(os.getenv("AUTHENTIK_INVITE_EXPIRE") or 48)
    invite_single_use: bool = bool(os.getenv("AUTHENTIK_INVITE_SINGLE_USE") or True)


settings = Settings()
