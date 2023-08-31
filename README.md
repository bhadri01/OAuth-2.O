# OAuth 2.O application for Fast-API

## Setup 

> create a virtual environement for python
```
python3 -m venv .venv
```

> Activate and Install the required package 
```
# For linux user
. .venv/bin/activate
pip install -r requirements.txt
```

> Create a .env file and copy and past the template and fill your API details
```
# Replace these values with your own Google OAuth credentials
# google auth
GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""
GOOGLE_REDIRECT_URI = "http://localhost:8000/login/callback"

# github auth
GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET = ""
GITHUB_REDIRECT_URI = "http://localhost:8000/login/callback"
```

> run the application
```
python3 main.py
```