from fastapi import HTTPException
from urllib.parse import parse_qs
import requests
from decouple import config

GITHUB_CLIENT_ID = config("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = config("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = config("GITHUB_REDIRECT_URI")

class GitHubOAuth:
    @staticmethod
    def exchange_code_for_access_token(code):
        payload = {
            "code": code,
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "redirect_uri": GITHUB_REDIRECT_URI,
        }
        response = requests.post(
            "https://github.com/login/oauth/access_token", data=payload)
        if response.status_code == 200:
            data = response.content.decode("utf-8")
            access_token = GitHubOAuth.parse_access_token(data)
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
        response = requests.get("https://api.github.com/user",
                                headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code,
                                detail="Error fetching user info")
    
    @staticmethod
    def get_auth_url():
        return f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}&scope=read:user,user:email"
    
    @staticmethod
    def parse_access_token(response_content):
        parsed_response = parse_qs(response_content)
        access_token = parsed_response.get('access_token', [''])[0]
        return access_token
