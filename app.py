from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import io
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

app = FastAPI()

model = ChatterboxTTS.from_pretrained(device="cpu")  # Use CPU on Railway

@app.post("/tts")
async def tts(request: Request):
    data = await request.json()
    text = data.get("text", "")
    if not text:
        return {"error": "No text provided"}

    wav = model.generate(text)
    buffer = io.BytesIO()
    ta.save(buffer, wav, model.sr)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="audio/wav")
