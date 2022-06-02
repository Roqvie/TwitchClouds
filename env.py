import os
from dotenv import load_dotenv


__all__ = [
    'APP_CLIENT_ID',
    'APP_CLIENT_SECRET',
    'USER_CLIENT_ID',
    'USER_ACCESS_TOKEN',
    'BROADCASTER',
    'BASE_FILE',
    'OUTPUT_FILENAME',
]

REQUIRED_VARIABLES = [
    'APP_CLIENT_ID',
    'APP_CLIENT_SECRET',
    'USER_CLIENT_ID',
    'USER_ACCESS_TOKEN',
    'BROADCASTER',
    'BASE_FILE',
    'OUTPUT_FILENAME'
]

print("Getting .env variables..")
load_dotenv()
if not all([os.getenv(variable) for variable in REQUIRED_VARIABLES]):
    print(F"Warning! Some of the environment variables is not set: {', '.join(REQUIRED_VARIABLES)}."
          "See .env file or set this variables manually (export KEY=VALUE)")

APP_CLIENT_ID = os.getenv('APP_CLIENT_ID')
APP_CLIENT_SECRET = os.getenv('APP_CLIENT_SECRET')
USER_CLIENT_ID = os.getenv('USER_CLIENT_ID')
USER_ACCESS_TOKEN = os.getenv('USER_ACCESS_TOKEN')
BROADCASTER = os.getenv('BROADCASTER')
# With file extension
BASE_FILE = os.getenv('BASE_FILE')
# Without file extension
OUTPUT_FILENAME = os.getenv('OUTPUT_FILENAME')