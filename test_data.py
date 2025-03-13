import base64
import os
from datetime import datetime, timedelta

Login_Url = "https://api.flatpeak.com/login"
Connect_token_Url = "https://api.flatpeak.com/connect/tariff/token"
Connect_Url="https://connect.flatpeak.com"
Instant_url = "https://api.flatpeak.com/costs/instant"

Account_ID= os.environ.get("ACCOUNT_ID")
API_Key= os.environ.get("API_KEY")
Creds=f"{Account_ID}:{API_Key}"

Creds_bytes = Creds.encode("ascii")
base64_bytes = base64.b64encode(Creds_bytes)
Encoded_creds = base64_bytes.decode("ascii")
auth_header = {"Authorization": "Basic " + Encoded_creds}


current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
end_time = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).strftime(
    "%Y-%m-%dT%H:%M:%SZ")