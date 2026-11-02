# StudyMate-AI 📚🤖

**StudyMate-AI** is a Retrieval-Augmented Generation (RAG) study assistant built in Python. It ingests PDF textbooks, lecture notes, and reference documents, indexes them into a local vector database, and answers questions accurately using context retrieved directly from your study materials.

## ✨ Features

- **PDF Document Ingestion:** Load textbooks and study guides from the `document loaders/` directory.
- **Automated Vector Indexing:** Splits documents into semantic chunks and generates vector embeddings via `create_database.py`.
- **Context-Aware Q&A:** Retrieves the most relevant passages to ground LLM responses and minimize hallucinations.
- **Interactive Interface & CLI Support:** Query your documents through `app.py` or test retrieval pipelines directly via `main.py`.
- **Secure Environment Management:** Uses `.env` and `python-dotenv` to keep API keys out of version control.

## 📂 Project Structure

```text
StudyMate-AI/
├── document loaders/      # Local directory for source PDFs (e.g., deeplearning.pdf)
├── app.py                 # Main application interface for querying study materials
├── create_database.py     # Script to parse PDFs, chunk text, and build the vector store
├── main.py                # Core RAG retrieval and generation pipeline
├── requirements.txt       # Required Python libraries and dependencies
├── .gitignore             # Excludes .venv, .env, and large PDF files
├── README.md              # Project documentation
└── LICENSE                # Repository license
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone [https://github.com/armanfatavat/StudyMate-AI.git](https://github.com/armanfatavat/StudyMate-AI.git)
cd StudyMate-AI
```

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory of the project and add your API key:

```env
OPENAI_API_KEY=your_api_key_here
# Or if using Groq / Gemini / Hugging Face:
# GROQ_API_KEY=your_api_key_here
# GOOGLE_API_KEY=your_api_key_here
```

## 💻 Usage

1. **Add Study PDFs:** Place your PDF textbooks or notes inside the `document loaders/` folder.
2. **Build Vector Database:**
   ```bash
   python create_database.py
   ```
3. **Run the Application:**
   ```bash
   python app.py
   ```
   *(If using Streamlit, run `streamlit run app.py` — or run `python main.py` to test via terminal.)*

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **Architecture:** Retrieval-Augmented Generation (RAG)
- **Environment Management:** `venv`, `python-dotenv`

## 📄 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## 👤 Author

**Arman Fatavat**
- GitHub: [@armanfatavat](https://github.com/armanfatavat)
