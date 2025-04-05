import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_AUTH_KEY = os.getenv("SERVICE_AUTH_KEY")
SERVICE_AUTH_ALGORITHM = os.getenv("SERVICE_AUTH_ALGORITHM")

print (SERVICE_AUTH_KEY)
print (SERVICE_AUTH_ALGORITHM)