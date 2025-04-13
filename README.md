# 🏋️‍♂️ FitBot: An AI-Powered Fitness Assistant

## 🔍 Overview

**FitBot** is an intelligent, conversational fitness assistant built using **Retrieval-Augmented Generation (RAG)** architecture. It combines the power of **semantic vector search**, **agent-based query routing**, and **LLMs (GPT-4)** to deliver personalized responses on workouts, nutrition, and healthy lifestyle guidance.

This project leverages cutting-edge NLP tools and vector databases to minimize hallucination, maintain grounded answers, and scale across various health domains. Built for fitness enthusiasts, FitBot aims to be your always-available digital trainer and wellness guide.

## **Technologies Used**

### Core Technologies
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Hugging Face](https://img.shields.io/badge/HuggingFace-005BFF?style=for-the-badge&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-009688?style=for-the-badge&logoColor=white)
![PyPDF](https://img.shields.io/badge/PyPDF-8C001A?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-6DFF19?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)

### Auxiliary Technologies
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

---

## ✨ Features

- 💬 Natural language interaction with LLM-powered responses
- 🧠 Retrieval-Augmented Generation (RAG) pipeline using LangChain
- 🧭 Intelligent Routing Agent to detect and route fitness/nutrition-related queries
- 🔍 Semantic vector search using ChromaDB (local)
- 📚 Retrieval from a curated knowledge base of fitness and health data
- ⚙️ Modular architecture for easy integration and future enhancements
- 📈 Extensible to include wearables, fitness APIs, and real-time progress tracking

---

## 🛠️ Tech Stack

- **Python** – Core backend and logic
- **LangChain** – Agent and RAG orchestration
- **ChromaDB** – Local vector store for dev and testing
- **OpenAI GPT-4** – Language model for natural responses
- **Streamlit** – Lightweight chatbot frontend
- **HuggingFace Embeddings** – For converting text to vector form
