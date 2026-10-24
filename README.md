# LectureLens — AI-Powered Lecture Transcription, Notes & Quiz Generator

> **"From classroom lectures to smarter learning."**  
> Turn classroom lecture audio into complete verbatim transcripts, concise study notes, and an interactive student quiz with deterministic grading and downloadable PDF/MD/TXT artifacts.

---

## Features

- 🎙️ **Full Audio Lecture Transcription**: Transcribe long classroom recordings using **Gemini 3.5 Transcribe** (`gemini-3.5-transcribe`) with smart formatting, disfluency removal, punctuation, and automatic language detection (85+ languages supported).
- 📝 **AI-Powered Concise Study Notes**: Automatically converts transcripts into structured, student-friendly Markdown study notes using **Gemini 3.8 Flash** (`gemini-3.8-flash`). Supports 3 selectable detail levels (**Very Concise**, **Balanced**, **Detailed**) and includes a dedicated **Quick Revision** section.
- 🎯 **Automatic Quiz Generation**: Generates pedagogical assessments grounded strictly in actual lecture content (5, 10, 15, or 20 questions; Easy, Medium, or Hard; Multiple-Choice, True/False, Short-Answer, or Mixed).
- 🔒 **Answer Privacy & Security**: Correct answers and explanations are stored securely on the backend session store and never sent to student browsers prior to submission.
- 📊 **Deterministic Quiz Grading**: Transparent, deterministic evaluation calculating exact percentage scores:  
  $$\text{Score Percentage} = \left(\frac{\text{Correct Answers}}{\text{Total Graded Questions}}\right) \times 100$$
  Provides letter grades (A–F) and detailed explanations for every question.
- 📥 **Comprehensive Study Downloads**:
  - **Transcript**: Plain text (`.txt`)
  - **Study Notes**: Markdown (`.md`), Plain text (`.txt`), and formatted PDF (`.pdf`)
  - **Quiz Scorecard**: Official student performance report in PDF (`.pdf`)
- 🛡️ **Privacy & Local File Management**: Uploaded audio files are securely processed in a temporary directory and immediately deleted post-transcription.

---

## Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide React
- **Backend**: Python 3.10+, FastAPI, Pydantic v2, Uvicorn, Python-Multipart
- **AI Models**: Google GenAI SDK (`google-genai` >= 2.25.0)
  - Audio Transcription: `gemini-3.5-transcribe` (fallback: `gemini-3.8-flash`)
  - Notes & Quiz Generation: `gemini-3.8-flash`
- **Document Generation**: ReportLab for styled PDF exports
- **Testing**: PyTest & HTTPX for backend automated tests

---

## Project Structure

```
lecturelens/
├── backend/
│   ├── app/
│   │   ├── api/                 # FastAPI routes (health, lectures, quizzes, exports)
│   │   ├── schemas/             # Pydantic v2 data models
│   │   ├── services/            # Transcription, Notes, Quiz generator, Grader, PDF
│   │   ├── utils/               # Audio validator & secure temporary file manager
│   │   ├── config.py            # Environment configurations & validation
│   │   └── main.py              # Application entrypoint & CORS middleware
│   ├── tests/                   # Pytest test suite (21 automated tests)
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment template
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/          # Header, AudioUpload, ProcessingStatus, Dashboard, Quiz, Results
│   │   ├── services/            # Typed API client
│   │   ├── types/               # TypeScript interfaces
│   │   ├── App.tsx              # View router and state management
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
└── README.md
```

---

## Prerequisites

1. **Python 3.10 or higher**
2. **Node.js v18 or higher** (v24 recommended) and **npm**
3. **Google Gemini API Key** (from [Google AI Studio](https://aistudio.google.com/app/apikey))

---

## Setup & Execution

### 1. Backend Setup

1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows (PowerShell)
   py -m venv venv
   .\venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your Gemini API Key:
   ```bash
   # Copy example template
   cp .env.example .env
   ```
   Open `backend/.env` and insert your API key:
   ```env
   GEMINI_API_KEY=AIzaSy...your_real_key_here
   GEMINI_TRANSCRIBE_MODEL=gemini-3.5-transcribe
   GEMINI_TEXT_MODEL=gemini-3.8-flash
   HOST=127.0.0.1
   PORT=8000
   MAX_UPLOAD_SIZE_MB=100
   ```

5. Start the FastAPI backend server:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   The backend API will be running at `http://127.0.0.1:8000`. Interactive OpenAPI documentation is available at `http://127.0.0.1:8000/docs`.

---

### 2. Frontend Setup

1. Open a separate terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The frontend application will be accessible at `http://localhost:5173`.

---

## Running Automated Tests

Run the complete backend test suite using Pytest:

```bash
cd backend
.\venv\Scripts\python -m pytest tests -v
```

The automated test suite verifies:
- Audio format and MIME type validation (`.mp3`, `.wav`, `.m4a`, `.aac`, `.flac`, `.ogg`, `.webm`)
- Rejection of oversized and invalid files (`.exe`, `.pdf`, `.png`)
- Audio transcription parsing and error handling
- Multi-length study notes generation (`very_concise`, `balanced`, `detailed`)
- Quiz schema validation and 4-distractor guarantees for MCQs
- Concealment of correct answers and explanations on public student endpoints
- Deterministic objective grading and score percentage calculations
- Generation of plain text, Markdown, and ReportLab PDF documents
- Complete FastAPI route integration via HTTPX test client

---

## Supported Audio Formats & Limits

| Format | Extensions | Maximum File Size |
|---|---|---|
| MP3 Audio | `.mp3` | 100 MB |
| WAV Audio | `.wav` | 100 MB |
| AAC / M4A | `.m4a`, `.aac` | 100 MB |
| FLAC Lossless | `.flac` | 100 MB |
| OGG / Opus | `.ogg`, `.opus`, `.oga` | 100 MB |
| WebM Audio | `.webm` | 100 MB |

---

## Security & Privacy Disclosures

- **Key Isolation**: `GEMINI_API_KEY` is only stored on the backend and is never exposed to the frontend bundle or client network requests.
- **Temporary File Purge**: Uploaded lecture audio files are written to a temporary folder (`backend/temp_uploads/`) and deleted immediately after processing finishes or in case of errors.
- **External AI Transmission**: When audio is submitted, it is sent securely to Google's Gemini API endpoints (`gemini-3.5-transcribe` and `gemini-3.8-flash`) solely for transcription, summarization, and quiz generation.

---

## License

MIT License &copy; LectureLens Team
