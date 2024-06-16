import uvicorn

from dotenv import load_dotenv
import os

load_dotenv()


def main():
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    uvicorn.run(
        "app.app:app",
        host=host,
        port=port,
        reload=debug,  # Enable auto-reload in debug mode
        log_level="debug" if debug else "info"
    )


if __name__ == "__main__":
    main()
