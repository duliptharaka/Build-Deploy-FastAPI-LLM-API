# FastAPI LLM API

<img width="3840" height="1554" alt="image" src="https://github.com/user-attachments/assets/8d26b7be-df2a-46ff-a602-a8336f720068" />

<img width="3840" height="1554" alt="image" src="https://github.com/user-attachments/assets/1af5741a-8dfd-42af-b4f0-5bbab4c406fd" />


Minimal FastAPI app with 3 endpoints:
- `GET /health`
- `POST /summarize`
- `POST /analyze-sentiment`

## 1) Setup

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Create `.env` in project root:

```env
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4.1-mini
```

Important: keep `.env` private and never commit it to GitHub.

## 2) Run

```bash
uvicorn app.main:app --reload
```

Open docs: `http://127.0.0.1:8000/docs`

## 3) Test endpoints

Health:

```bash
curl http://127.0.0.1:8000/health
```

Summarize:

```bash
curl -X POST http://127.0.0.1:8000/summarize ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"FastAPI is a modern, high-performance web framework for building APIs with Python.\",\"max_length\":120}"
```

Sentiment:

```bash
curl -X POST http://127.0.0.1:8000/analyze-sentiment ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"The onboarding process was smooth and easy.\"}"
```

## 4) Deploy on Render.com (Free Tier)

1. Push this project to GitHub.
2. Log in at [https://render.com](https://render.com) and click **New +** -> **Web Service**.
3. Connect your GitHub repo and select this project.
4. Configure in the Render UI (no `render.yaml` needed):
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Choose the **Free** instance type.
6. Add environment variables:
   - `OPENAI_API_KEY` = your key
   - `OPENAI_MODEL` = `gpt-4.1-mini` (optional)
7. Click **Create Web Service** and wait for deploy success.
8. Test your live endpoints:
   - `https://<your-service>.onrender.com/health`
   - `https://<your-service>.onrender.com/docs`
   - POST to `/summarize` and `/analyze-sentiment` from docs or curl.
