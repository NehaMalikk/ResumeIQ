"""HireMatch AI Backend entry point."""

import uvicorn

from app.core.application import create_app

app = create_app()


def main() -> None:
    """Launch the application with Uvicorn."""
    from app.config.settings import get_settings

    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
