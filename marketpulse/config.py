"""Central settings. Everything comes from environment variables (or a local .env file)."""
import os

from dotenv import load_dotenv

# Reads a .env file from the folder you run the program in. Real environment
# variables always win over the .env file.
load_dotenv()

# System settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MEMORY_FILE = os.getenv("MEMORY_FILE", "memory.json")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash")


class MissingAPIKeyError(RuntimeError):
    """Raised when GOOGLE_API_KEY is not set."""


def get_api_key() -> str:
    """Return the Gemini API key, or stop with a clear message if it is missing.

    This is a function (not a constant) so that importing the package, running
    tests, or reading the logger never needs a key. Only code that really calls
    Gemini asks for it.
    """
    key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not key or key.lower().startswith(("utilize your own", "your_", "your-", "your ")):
        raise MissingAPIKeyError(
            "GOOGLE_API_KEY is not set. Copy .env.example to .env and put your "
            "Gemini API key in it, or set it as an environment variable."
        )
    return key
