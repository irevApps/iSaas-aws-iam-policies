import os
from pathlib import Path

# Function to load environment variables from .env file
def load_env():
    env_path = Path('.') / '.env'
    if env_path.exists():
        try:
            with open('.env', 'r') as file:
                for line in file:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        # Check if value is wrapped in double quotes
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]  # Remove double quotes
                        os.environ[key] = value
        except FileNotFoundError:
            print(".env file not found. Using default environment variables.")
