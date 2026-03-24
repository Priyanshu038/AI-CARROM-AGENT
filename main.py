import os
import json
import re
import urllib.request
import urllib.parse
import bcrypt 
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import AsyncOpenAI
from sqlalchemy.orm import Session


from database import SessionLocal, User
from trick import TRICKS


load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="AI Carrom Coach Backend")


def get_password_hash(password: str) -> str:
    """Hashes a password securely using pure bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8') # Decode to string for DB storage

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against the stored hash"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    carrom_level: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    messages: List[Dict[str, Any]]
    coach_name: str = "an AI Carrom Coach"

class AnalyzeRequest(BaseModel):
    image_base64: str


@app.post("/register/")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
   
    db_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    
 
    hashed_pw = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        carrom_level=user.carrom_level,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "username": new_user.username}

@app.post("/login/")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {
        "message": "Login successful", 
        "user_data": {
            "username": db_user.username,
            "level": db_user.carrom_level
        }
    }



COACH_PERSONAS = {
    "Maria Irudayam": "You are Maria Irudayam, 'The King' of Carrom and a two-time World Champion. You have a calm, experienced, and highly tactical approach. You focus on fundamentals, patience, and precise positioning.",
    "S. Ilavazhagi": "You are S. Ilavazhagi, 'The Tactician' and a three-time World Champion. Your style is aggressive but calculated. You emphasize quick thinking, sharp cuts, and exploiting the opponent's mistakes.",
    "Rashid Ahmed": "You are Rashid Ahmed, 'The Trickshot Master'. You specialize in flashy, unconventional, and highly creative shots. You encourage players to think outside the box, use ricochets, and take risks.",
    "Yogesh Pardeshi": "You are Yogesh Pardeshi, 'The Scientist' and a dominant World Champion. You approach carrom like a math equation. You focus on angles, friction, force calculation, and geometric precision.",
    "Chiedu Okonkwo": "You are Chiedu Okonkwo, 'The Slam Break Master'. You rely on overwhelming power and dominant opening breaks. You believe in scattering the board and intimidating the opponent with sheer force."
}

def fetch_real_youtube_video(query: str) -> str:
    try:
        search_query = urllib.parse.urlencode({"search_query": query})
        url = "https://www.youtube.com/results?" + search_query
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        html_content = urllib.request.urlopen(req).read().decode()
        video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html_content)
        if video_ids:
            return f"https://www.youtube.com/watch?v={video_ids[0]}"
    except Exception as e:
        print(f"YouTube Search Error: {e}")
    return ""

@app.get("/tricks/")
async def get_tricks():
    return {"tricks": TRICKS}

@app.post("/analyze/")
async def analyze_board(req: AnalyzeRequest):
    system_prompt = """You are an expert carrom coach. Analyse this carrom board photo. Respond ONLY with valid JSON. Do not use markdown formatting blocks like ```json.
    {
      "black": <number of black pieces remaining>,
      "white": <number of white pieces remaining>,
      "queen": <true/false>,
      "situation": "<2-3 sentence description of the board>",
      "shots": [{"type": "shot name", "confidence": "high|medium|low", "description": "desc", "direction": "dir", "reasoning": "reason"}]
    }
    Provide exactly 3 shot recommendations."""
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [{"type": "text", "text": "Analyze this board."}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{req.image_base64}"}}]}
            ],
            response_format={"type": "json_object"},
            max_tokens=800
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vision API Error: {str(e)}")

@app.post("/coach/")
async def coach_chat(req: ChatRequest):
    persona = COACH_PERSONAS.get(req.coach_name, f"You are {req.coach_name}, a world-class expert carrom player and coach.")
    system_prompt = f"""{persona} You know all carrom rules, shot techniques, strategy, and training methods. Be encouraging but ensure your tone heavily reflects your unique persona. Format key terms in bold. Keep responses concise and structured.
CRITICAL RULE FOR VIDEOS: You MUST NEVER invent or guess YouTube URLs. Instead, generate a highly optimized YouTube search query formatted exactly like this at the very end of your response: [YT_SEARCH: <your optimized search keywords>]"""
    
    messages = [{"role": "system", "content": system_prompt}] + req.messages
    try:
        response = await client.chat.completions.create(
            model="gpt-4o", messages=messages, max_tokens=800, temperature=0.85 
        )
        raw_text = response.choices[0].message.content
        search_match = re.search(r'\[YT_SEARCH:\s*(.*?)\]', raw_text)
        if search_match:
            real_url = fetch_real_youtube_video(search_match.group(1))
            if real_url:
                raw_text = re.sub(r'\[YT_SEARCH:\s*.*?\]', real_url, raw_text).strip()
            else:
                raw_text = re.sub(r'\[YT_SEARCH:\s*.*?\]', '', raw_text).strip()
        return {"response": raw_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat API Error: {str(e)}")
