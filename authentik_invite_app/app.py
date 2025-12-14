from urllib.parse import urlparse
from flask_oidc import OpenIDConnect
from flask import Flask, render_template, session
import os
from authentik_invite_app.config import settings
from authentik_invite_app.authentik import authentik

app = Flask(__name__)
app.secret_key = os.urandom(32)

app.config.update(
    {
        "OIDC_CLIENT_SECRETS": {
            "web": {
                "client_id": settings.client_id,
                "client_secret": settings.client_secret,
                "auth_uri": settings.issuer + "authorize",
                "token_uri": settings.issuer + "token",
                "userinfo_uri": settings.issuer + "userinfo",
                "redirect_uris": [settings.redirect_uri],
                "issuer": settings.issuer,
            }
        },
        "OIDC_SCOPES": ["openid", "email", "profile"],
        "OIDC_CALLBACK_ROUTE": "/oidc/callback",
        "OIDC_USER_INFO_ENABLED": True,
    }
)
oidc = OpenIDConnect(app)


@app.route("/")
@oidc.require_login
def invite_create():
    username = session["oidc_auth_profile"].get("preferred_username")
    invite = authentik.check_user_invite(username)
    if not invite:
        invite = authentik.generate_invite(username)
    return render_template(
        "invite_show.html.j2",
        token=invite.pk,
        valid_until=invite.expires.strftime("%d.%m.%y %H:%M"),
        authentik_url=urlparse(settings.authentik_url).netloc,
        domain=str(urlparse(settings.authentik_url)).split(".")[-2],
    )
