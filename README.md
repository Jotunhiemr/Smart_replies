
# Smart Reply API

An asynchronous FastAPI-based service that generates **context-aware smart replies** using [Ollama](https://ollama.ai/).
The API considers user conversation history and provides natural responses in **JSON format**.

---

## 🚀 Features

* Contextual smart reply generation
* Asynchronous + non-blocking for high performance
* Simple in-memory caching for conversation history
* JSON-formatted responses
* Easy-to-extend architecture

---

## 📂 Project Structure

```
.
├── core.py          # SmartReply class logic
├── config.py        # Configuration (model, temperature, tokens)
├── main.py          # FastAPI application
└── README.md        # Documentation
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Jotunhiemr/Smart_replies.git
cd Smart_replies
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn ollama
```

### 4. Ensure Ollama is installed & running

Follow setup from [Ollama docs](https://ollama.ai/).

---

## 🔧 Configuration

Update `config.py` with your desired parameters:

```python
class Config:
    MODEL_NAME = "llama2"     # or any Ollama model
    TEMPERATURE = 0.7
    MAX_TOKEN = 200
```

---

## ▶️ Running the API

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Server runs at:
👉 `http://127.0.0.1:8000`

---

## 📌 API Endpoints

### **Root**

```http
GET /
```

**Response:**

```json
{"message": "Welcome to the Smart Reply API!"}
```

---

### **Generate Smart Reply**

```http
GET /generate-reply/{user_id}
```

**Path Parameters:**

* `user_id` → Unique identifier for user

**Response Example:**

```json
{
  "response": "{\"reply\": \"That sounds great, let’s do it!\"
                \"timestamp\":
                }"
}
```

---

## ⚡ Performance Notes

* Uses `asyncio.to_thread()` so that blocking Ollama calls do not freeze FastAPI.
* Caches conversation history per user to reduce repeated lookups.
* Prompting optimized for minimal overhead.

---

