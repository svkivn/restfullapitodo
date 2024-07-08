import os
from dotenv import load_dotenv

load_dotenv()


current_path = os.path.dirname(os.path.realpath(__file__))
#print(f"{current_path=}")
DB_URL = os.getenv("DB_URL")
database_url = "sqlite:///data.db" #f"sqlite:///{current_path}/{DB_URL}"

secret_key = os.getenv("secret_key")
algorithm = os.getenv("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
