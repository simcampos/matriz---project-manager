from collections.abc import Mapping
from urllib.parse import parse_qs, unquote, urlsplit


def database_config(environ: Mapping[str, str]) -> dict[str, object]:
    database_url = environ.get("DATABASE_URL")
    if not database_url:
        return {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": environ.get("POSTGRES_DB", "matriz"),
            "USER": environ.get("POSTGRES_USER", "matriz"),
            "PASSWORD": environ.get("POSTGRES_PASSWORD", ""),
            "HOST": environ.get("POSTGRES_HOST", "127.0.0.1"),
            "PORT": environ.get("POSTGRES_PORT", "5432"),
            "CONN_MAX_AGE": 60,
        }

    try:
        parsed_url = urlsplit(database_url)
        port = parsed_url.port
    except ValueError as exc:
        raise ValueError("DATABASE_URL must be a valid PostgreSQL connection URL.") from exc

    database_name = unquote(parsed_url.path.lstrip("/"))
    if (
        parsed_url.scheme not in {"postgres", "postgresql"}
        or not parsed_url.hostname
        or not parsed_url.username
        or not database_name
    ):
        raise ValueError("DATABASE_URL must be a valid PostgreSQL connection URL.")

    configuration: dict[str, object] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": database_name,
        "USER": unquote(parsed_url.username),
        "PASSWORD": unquote(parsed_url.password or ""),
        "HOST": parsed_url.hostname,
        "PORT": str(port or 5432),
        "CONN_MAX_AGE": 60,
    }
    sslmodes = parse_qs(parsed_url.query).get("sslmode")
    if sslmodes:
        configuration["OPTIONS"] = {"sslmode": sslmodes[0]}

    return configuration
