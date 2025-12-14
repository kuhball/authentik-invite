# authentik invite

This app provides a simple website to enable authentik users to generate invite links.

## prerequisites

You need to have a working invite flow setup within authentik.
Have a look at the [docs](https://docs.goauthentik.io/users-sources/user/invitations/).

When creating invites a flow id is needed.
Currently all flows are fetched on application start and the id of the first enrollment flow is used.

## running

The following env vars are needed:

```bash
CLIENT_ID=SOMEID
CLIENT_SECRET=SOMESECRET
REDIRECT_URI=http://127.0.0.1:5000/oidc/callback
ISSUER=https://<AUTHENTIK_URL>/application/o/invite/
AUTHENTIK_TOKEN=SOMETOKEN
AUTHENTIK_URL=https://<AUTHENTIK_URL>/api/v3
```

Following additional ENV vars are supported:

```bash
AUTHENTIK_INVITE_EXPIRE=48
AUTHENTIK_INVITE_SINGLE_USE=True
```

`AUTHENTIK_INVITE_EXPIRE` is the time the link is valid in hours.
`AUTHENTIK_INVITE_SINGLE_USE` decides if multiple users can register using the same link.


The app is exposed on port 5000 within the container and is thought to run behind a reverse proxy.
