from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
import os
import torch
from speechbrain.pretrained import EncoderASR
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM


def load_asr_model():
    print("Loading ASR model...")
    model = EncoderASR.from_hparams("speechbrain/asr-wav2vec2-dvoice-swahili")
    print("ASR model loaded successfully!")
    return model


def load_translation_model():
    print("Loading translation model...")
    tokenizer = AutoTokenizer.from_pretrained("Rogendo/sw-en")
    model = AutoModelForSeq2SeqLM.from_pretrained("Rogendo/sw-en")
    translator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
    print("Translation model loaded successfully!")
    return translator


def translate_text_swa_eng(text, translator):
    return translator(text, max_length=128, num_beams=5)[0]['generated_text']


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.asr_model = load_asr_model()
    app.state.swa_eng_translator = load_translation_model()
    yield
    app.state.asr_model = None
    app.state.swa_eng_translator = None


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.post("/transcribe-and-translate/")
async def transcribe_and_translate(file: UploadFile = File(...)):
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only .wav files are supported")
    
    temp_audio_path = f"temp_{file.filename}"
    with open(temp_audio_path, "wb") as temp_file:
        temp_file.write(file.file.read())
    
    try:
        asr_model = app.state.asr_model
        swa_eng_translator = app.state.swa_eng_translator

        transcription = asr_model.transcribe_file(temp_audio_path)
        translation = translate_text_swa_eng(transcription, swa_eng_translator)
        
        return {
            "audio_file": file.filename,
            "transcription": transcription,
            "translation": translation,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("swahili_api:app", host="0.0.0.0", port=8021, reload=True)
