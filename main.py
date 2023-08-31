from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from enum import Enum
from decouple import config
from OAuth.google import GoogleOAuth
from OAuth.github import GitHubOAuth

app = FastAPI()

class OAuthProvider(str, Enum):
    google = "google"
    github = "github"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/callback")

def get_provider(provider: OAuthProvider = Query(..., title="OAuth Provider")):
    return provider

@app.get("/")
def read_root(token: str = Depends(oauth2_scheme), provider: OAuthProvider = Depends(get_provider)):
    try:
        if provider == OAuthProvider.google:
            user_info = GoogleOAuth.get_user_info(token)
        elif provider == OAuthProvider.github:
            user_info = GitHubOAuth.get_user_info(token)
        return {"message": user_info}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@app.get("/login")
def login(provider: OAuthProvider):
    if provider == OAuthProvider.google:
        auth_url = GoogleOAuth.get_auth_url()
    elif provider == OAuthProvider.github:
        auth_url = GitHubOAuth.get_auth_url()
    else:
        raise HTTPException(status_code=400, detail="Invalid provider")
    return {"auth_url": auth_url}

@app.get("/login/callback")
def login_callback(code: str, provider: OAuthProvider):
    try:
        if provider == OAuthProvider.google:
            access_token = GoogleOAuth.exchange_code_for_access_token(code)
        elif provider == OAuthProvider.github:
            access_token = GitHubOAuth.exchange_code_for_access_token(code)
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
