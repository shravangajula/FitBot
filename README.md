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
![ChromaDB](https://img.shields.io/badge/ChromaDB-FFB219?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)

### Auxiliary Technologies
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![Regex](https://img.shields.io/badge/Regex-787878?style=for-the-badge)

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

---

## **Architecture Diagram**

![AI-Powered FitBot Architecture](https://github.com/shravangajula/FitBot/blob/main/diagrams/FitBot2.jpeg)

---

## **Key Features**

### 1. **Streamlit-Based User Interface**
- **Conversational-Fitness Chatbot**: Users interact via a friendly chatbot interface to get guidance on workouts and nutrition.
- **Intuitive Layout**: Chat history is displayed clearly, enabling smooth and contextual interaction for ongoing health tracking.

### 2. **Document Preprocessing with PyPDF**
- Extracts and preprocesses data from fitness and nutrition related document (PDF).
- Converts extracted data into regex(text formatting) for further embedding and fine-tuning.

### 3. **Embedding Generation**
- Breaks down large documents into semantically meaningful chunks.
- Uses OpenAI and Hugging Face models to convert text into embeddings for efficient retrieval.

### 4. **Chroma Vector Database**
- Stores vectorized data in ChromaDB for quick access to relevant fitness content.
- Provides fast retrieval of relevant fitness related documents during a query.

### 5. **LangChain for Document Retrieval**
- Directs user queries to the correct data sources, be it workout plans, nutrition info.
- Provides contextual information for personalized responses.

### 6. **Fine-Tuned LLM**
- GPT-4 fine-tuned on domain-specific fitness and nutritional data.
- Generates detailed, conversational responses tailored to the user’s input.

---

## ** Clone the Repository**

1. Open your terminal or command prompt.
2. Clone the repository:
   ```bash
   git clone https://github.com/shravangajula/FitBot.git

---

## ** Install Dependencies**

---

## ** Configure API Keys**

---

### ** API Key**
- Add your OpenAI API key in the file:
   ```
   OpenAI_Key = "your_openai_api_key"
   model_name='all-MiniLM-L12-v2'

---

## ** Run the Application**

### **Start the Streamlit App**
Run the Streamlit application:
   streamlit run app.py

   Open the provided local or network URL in your browser (e.g., http://localhost:8501/).
