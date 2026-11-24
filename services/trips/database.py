
import os
from urllib.parse import urlparse, parse_qs, unquote

import pyodbc


def get_connection():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")

    parsed = urlparse(database_url)
    query = parse_qs(parsed.query)

    driver = query.get(
        "driver",
        ["ODBC Driver 18 for SQL Server"]
    )[0]

    trust_certificate = query.get(
        "TrustServerCertificate",
        ["yes"]
    )[0]

    server = parsed.hostname
    if parsed.port:
        server = f"{server},{parsed.port}"

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={parsed.path.lstrip('/')};"
        f"UID={unquote(parsed.username or '')};"
        f"PWD={unquote(parsed.password or '')};"
        f"Encrypt=yes;"
        f"TrustServerCertificate={trust_certificate};"
        f"Connection Timeout=5;"
    )

    return pyodbc.connect(connection_string)
