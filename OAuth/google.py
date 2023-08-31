from fastapi import HTTPException
from urllib.parse import parse_qs
import requests
from decouple import config

GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = config("GOOGLE_REDIRECT_URI")

class GoogleOAuth:
    @staticmethod
    def exchange_code_for_access_token(code):
        payload = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        response = requests.post(
            "https://oauth2.googleapis.com/token", data=payload)
        if response.status_code == 200:
            data = response.json()
            access_token = data.get("access_token")
            if access_token:
                return access_token
            else:
                raise HTTPException(
                    status_code=500, detail="Access token not found in response")
        else:
            error_data = response.content.decode("utf-8")
            raise HTTPException(
                status_code=response.status_code, detail=error_data)
    
    @staticmethod
    def get_user_info(access_token):
        response = requests.get("https://www.googleapis.com/oauth2/v3/userinfo",
                                headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code,
                                detail="Error fetching user info")
    
    @staticmethod
    def get_auth_url():
        return f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&response_type=code&scope=openid%20profile%20email"
    
