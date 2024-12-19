from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv
from CV.face_recog.inference import DetectFace
from db import MongoConn

load_dotenv()
app = FastAPI()
face_model = DetectFace()
mongo_db = MongoConn(os.environ.get("MONGO_URI"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FrameData(BaseModel):
    frame_data: str
    username: str

@app.get("/")
async def root():
    return {"message": "CypressMFA backend is running"}

@app.post("/api/send-db")
async def send_db(frame_json: dict):
    try:
        frame_data = frame_json.get('frame_data')
        chrome_id = frame_json.get('username')
        pic_encoding = face_model.get_encoding(frame_data)
        res = mongo_db.insert_data(chrome_id, pic_encoding)
        return {"success": bool(res)}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to insert data")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
