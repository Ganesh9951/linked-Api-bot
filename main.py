from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from linkedin_bot import LinkedInBot  # Correct import

app = FastAPI()

# We'll initialize bot after login
bot = None

class LoginData(BaseModel):
    username: str
    password: str

class ConnectData(BaseModel):
    profile_url: str

class MessageData(BaseModel):
    profile_url: str
    message: str

@app.post("/login")
def login(data: LoginData):
    global bot
    try:
        bot = LinkedInBot(data.username, data.password)
        bot.login()
        return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.post("/connect")
def connect(data: ConnectData):
    try:
        if bot is None:
            raise Exception("Please log in first.")
        bot.go_to_profile_and_connect(data.profile_url)
        return {"message": "Connection request sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connect failed: {str(e)}")

@app.post("/check_connection")
def check_connection(data: MessageData):
    try:
        if bot is None:
            raise Exception("Please log in first.")
        bot.check_connection_and_message(data.profile_url, data.message)
        return {"message": "Checked connection and message sent if connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Check connection failed: {str(e)}")

@app.get("/close")
def close():
    global bot
    try:
        if bot:
            bot.close()
            bot = None
            return {"message": "Browser closed"}
        else:
            return {"message": "No browser session active"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Close failed: {str(e)}")
