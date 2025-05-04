import os

from dotenv import load_dotenv


def load_env_vars():
    """Load Environment Variables from .env file."""
    module_dir = os.path.dirname(__file__)
    dot_env_path = os.path.join(module_dir, ".env")
    print(f"Loading .env file from: {dot_env_path}")
    env_loading = load_dotenv(dot_env_path)
    print(f"Env Loading Success: {env_loading}")
