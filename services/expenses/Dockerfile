FROM python:3.12-slim-bookworm

# Install Microsoft SQL Server ODBC Driver 18
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    unixodbc-dev \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
       | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
       > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY services/expenses/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY services/__init__.py ./services/__init__.py
COPY services/expenses/ ./services/expenses/
COPY database/ ./database/

# Run as a non-root user
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 5002

CMD ["python", "-m", "services.expenses.app"]
