# FlyFair

**Because flying should be fair.**

FlyFair is a facts-only, RAG-based chatbot that helps Indian domestic air passengers (18+) understand their legal rights when airlines delay, cancel, or otherwise disrupt flights.


## 🇮🇳 Scope & Authority

- **Jurisdiction:** India only  
- **Flights Covered:** Domestic flights within India  
- **Legal Source:** DGCA Passenger Charter (Government of India)

> FlyFair does **not** use external knowledge, airline policies, or legal advice.  
> If a right is not defined in the DGCA Passenger Charter, FlyFair will not answer.

## 🧠 How FlyFair Works (High Level)

FlyFair uses a **Retrieval-Augmented Generation (RAG)** pipeline with **strict guardrails**:

1. Passenger rights are pre-extracted from the DGCA Passenger Charter
2. Each rule is stored as a **self-contained legal chunk**
3. User queries retrieve only the most relevant chunks
4. Responses are generated **only from retrieved text**
5. If nothing matches confidently → FlyFair responds: This is out of my Scope.

## 🎯 Features

- **Facts-only answers** from DGCA Passenger Charter
- **RAG-based retrieval** using pre-processed knowledge chunks
- **Mobile-first design** for use at airports
- **No authentication required** - instant access
- **Production-grade** despite using free tools

## 🏗️ Architecture

### Backend
- **Python**
- **FastAPI**
- **sentence-transformers** (embeddings)
- **FAISS** (local vector store)
- **RAG-only mode** (LLM optional, disabled by default)

### Frontend
- **Next.js (App Router)**
- **React**
- **Tailwind CSS**
- Mobile-first, no authentication, no chat history



## 📚 Knowledge Base

- Source: **DGCA Passenger Charter – Government of India**
- Content:
  - Flight delays
  - Flight cancellations
  - Denied boarding (overbooking)
  - Refunds
  - Baggage issues
  - Special assistance & disabilities
- Data is:
  - OCR-extracted
  - Cleaned
  - Manually chunked by legal scenario
  - Stored in `flyfair_rag_chunks.json`

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
