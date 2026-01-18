# FlyFair

**Because flying should be fair.**

FlyFair is a facts-only, RAG-based chatbot that helps Indian domestic air passengers (18+) understand their legal rights when airlines delay, cancel, or otherwise disrupt flights.

## 🎯 Features

- **Facts-only answers** from DGCA Passenger Charter
- **RAG-based retrieval** using pre-processed knowledge chunks
- **Mobile-first design** for use at airports
- **No authentication required** - instant access
- **Production-grade** despite using free tools

## 🏗️ Architecture

### Backend
- **FastAPI** - Python web framework
- **sentence-transformers** - Embeddings (all-MiniLM-L6-v2)
- **FAISS** - Vector store for similarity search
- **Ollama/LM Studio** - Local LLM for response formatting (optional)

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Mobile-first** responsive design

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- (Optional) Ollama or LM Studio for LLM formatting

## 🚀 Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables (optional):**
   ```bash
   export LLM_PROVIDER=ollama  # or "lm_studio"
   export LLM_BASE_URL=http://localhost:11434
   export LLM_MODEL=llama2
   ```

5. **Run the backend:**
   ```bash
   python main.py
   # Or with uvicorn directly:
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file:**
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local and set NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

## 🔧 Configuration

### LLM Setup (Optional)

FlyFair works without an LLM (using direct formatting), but LLM formatting provides better responses.

#### Option 1: Ollama

1. **Install Ollama:**
   - Visit https://ollama.ai
   - Download and install

2. **Pull a model:**
   ```bash
   ollama pull llama2
   # or
   ollama pull mistral
   ```

3. **Set environment variables:**
   ```bash
   export LLM_PROVIDER=ollama
   export LLM_BASE_URL=http://localhost:11434
   export LLM_MODEL=llama2
   ```

#### Option 2: LM Studio

1. **Install LM Studio:**
   - Visit https://lmstudio.ai
   - Download and install

2. **Start LM Studio** and load a model

3. **Set environment variables:**
   ```bash
   export LLM_PROVIDER=lm_studio
   export LLM_BASE_URL=http://localhost:1234
   export LLM_MODEL=your-model-name
   ```

## 📚 Knowledge Base

The knowledge base is pre-processed from the DGCA Passenger Charter and stored in:
- `backend/rag/flyfair_rag_chunks.json`

**DO NOT** attempt to re-process or modify this file. It is the single source of truth.

## 🎨 Branding

- **Brand Name:** FlyFair
- **Tagline:** Because flying should be fair.
- **Colors:**
  - Background: Deep Blue (#0A1E3A)
  - Text/Icon: White (#FFFFFF)
- **Logo:** Wings + Balance icon (see `FlyFair.png`)

## 🔍 API Endpoints

### `GET /`
Health check endpoint.

### `GET /health`
Detailed health check with service status.

### `POST /query`
Query endpoint for passenger rights questions.

**Request:**
```json
{
  "query": "My flight is delayed by 3 hours. What are my rights?",
  "use_llm": true
}
```

**Response:**
```json
{
  "response": "Applicable Scenario:\n...\nConditions:\n...\nPassenger Rights:\n...\nSource:\n...",
  "chunks": [...]
}
```

## 🧪 Testing

### Test Backend

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "My flight is delayed by 3 hours", "use_llm": false}'
```

### Test Frontend

1. Start both backend and frontend
2. Navigate to `http://localhost:3000`
3. Select a scenario or type a query

## 📝 Response Format

Every valid response follows this structure:

```
Applicable Scenario:
[Scenario description]

Conditions:
[Conditions under which rights apply]

Passenger Rights:
[Explicit rights from DGCA charter]

Source:
DGCA Passenger Charter – [Category]
```

If the query is out of scope, the response is:
```
This is out of my Scope.
```

## ⚠️ Important Constraints

1. **Facts-only:** Answers come strictly from retrieved chunks
2. **No external knowledge:** Only DGCA Passenger Charter
3. **No assumptions:** If not in chunks, respond "out of scope"
4. **No paraphrasing:** Preserve legal meaning exactly
5. **Domestic flights only:** International flights are out of scope

## 🐛 Troubleshooting

### Backend Issues

- **Import errors:** Ensure virtual environment is activated
- **FAISS errors:** Try `pip install faiss-cpu --upgrade`
- **LLM connection failed:** Check if Ollama/LM Studio is running
- **Chunks not loading:** Verify `flyfair_rag_chunks.json` exists

### Frontend Issues

- **API connection failed:** Check `NEXT_PUBLIC_API_URL` in `.env.local`
- **Build errors:** Run `npm install` again
- **Styling issues:** Ensure Tailwind CSS is properly configured

## 📄 License

This project is built for helping Indian domestic air passengers understand their rights.

## 🤝 Contributing

This is a production-grade system. All changes must maintain:
- Facts-only responses
- Strict retrieval constraints
- Mobile-first UX
- Production reliability

---

**FlyFair** - Because flying should be fair. ✈️⚖️
