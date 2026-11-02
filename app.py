import os
import shutil
import tempfile

import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

st.set_page_config(page_title="RAG Book Assistant")
st.title("📚 RAG Book Assistant")
st.write("Upload a PDF and ask questions from the document")

DB_DIR = "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


uploaded_file = st.file_uploader("Upload a PDF book", type="pdf")

if uploaded_file:
    if st.button("Create Vector Database"):
        file_path = None

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                file_path = tmp_file.name

            with st.spinner("Processing document..."):
                docs = PyPDFLoader(file_path).load()

                if not docs:
                    st.error("No readable pages were found in the PDF.")
                    st.stop()

                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                )
                chunks = splitter.split_documents(docs)

                # Remove the previous index before rebuilding it.
                if os.path.exists(DB_DIR):
                    shutil.rmtree(DB_DIR)

                Chroma.from_documents(
                    documents=chunks,
                    embedding=get_embeddings(),
                    persist_directory=DB_DIR,
                )

            st.success(f"Vector database created from {len(chunks)} chunks.")

        except Exception as exc:
            st.error(f"Could not process the PDF: {exc}")

        finally:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)


if os.path.isdir(DB_DIR):
    st.divider()
    st.subheader("Ask Questions From the Book")

    query = st.text_input("Enter your question")

    if query.strip():
        if not os.getenv("GROQ_API_KEY"):
            st.error("Set GROQ_API_KEY in your .env file to use Groq.")
            st.stop()

        try:
            vectorstore = Chroma(
                persist_directory=DB_DIR,
                embedding_function=get_embeddings(),
            )
            retriever = vectorstore.as_retriever(
                search_type="mmr",
                search_kwargs={"k": 4, "fetch_k": 10, "lambda_mult": 0.5},
            )

            docs = retriever.invoke(query.strip())
            context = "\n\n".join(doc.page_content for doc in docs)

            if not context.strip():
                st.info("I could not find the answer in the document.")
            else:
                prompt = ChatPromptTemplate.from_messages(
                    [
                        (
                            "system",
                            'Answer using only the provided context. If it does not contain the answer, say: "I could not find the answer in the document."',
                        ),
                        (
                            "human",
                            "Context:\n{context}\n\nQuestion:\n{question}",
                        ),
                    ]
                )

                llm = ChatGroq(
                    model="Qwen/Qwen3.8-27B",
                    temperature=0,
                )
                response = llm.invoke(
                    prompt.invoke(
                        {"context": context, "question": query.strip()}
                    )
                )

                st.write("### AI Answer")
                st.write(response.content)

        except Exception as exc:
            st.error(f"Could not answer the question: {exc}")