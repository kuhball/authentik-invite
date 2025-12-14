from authentik_invite_app.app import app


def main() -> int:
    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
