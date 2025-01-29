# Swahili ASR and Translation API

This FastAPI application provides an endpoint for transcribing Swahili speech from .wav files and translating the transcription into English.

## Features

- **Automatic Speech Recognition (ASR)** using speechbrain's wav2vec2 model.
- **Translation** from Swahili to English using Hugging Face Transformers.
- **FastAPI-based web service** with a `/docs` interface for testing.

## Installation

To get started, clone the repository and set up your environment.

### 1. **Clone the repository**:
   
   ```bash
   git clone https://github.com/your-username/swahili_asr_translation.git
   cd swahili_asr_translation
   ```

### 2. **Set up a virtual environment**
    
   ```bash
   python -m venv venv
   ```

### 3. Activate the virtual environment

- On macOS/Linux:

  ```bash
  source venv/bin/activate
  ```

- On Windows:

  ```bash
  venv\Scripts\activate
  ```

### 4. Install the required dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the API server:

Run the following command to start the FastAPI application:

```bash
uvicorn swahili_asr_translation:app --host 0.0.0.0 --port 8021 --reload
```

Once the server is running, you can access the API documentation at:

```bash
http://localhost:8021/docs
```

## API Endpoints

### `POST /transcribe-and-translate/`

Uploads a `.wav` file, transcribes it to Swahili text, and translates it into English.

#### Request:
- **File**: A `.wav` audio file.

#### Response (JSON):

```json
{
  "audio_file": "example.wav",
  "transcription": "Hii ni sauti ya majaribio",
  "translation": "This is a test audio"
}
```

## Deployment

For production environments, it is recommended to run the application with multiple workers for better scalability. 

If you're running the app from a script, you can use the following setup in your `app.py`:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("swahili_asr_translation:app", host="0.0.0.0", port=8021, workers=4)
```

