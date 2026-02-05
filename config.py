import os
from dotenv import load_dotenv

load_dotenv()

# Email Settings
EMAIL_SENDER = os.getenv("azhannazam@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS") # Use Gmail App Password
RECEIVER_ADMIN = "azhanskie@gmail.com"

# Business Logic
AGENCY_NAME = "SuperAchiever"
DB_NAME = "data/supere.db"