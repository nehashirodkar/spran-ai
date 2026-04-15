# 🚀 SPRAN-AI — AI-Powered Product Specification Generator

SPRAN-AI is an AI-driven application that transforms user input into structured product specifications — including features, materials, and manufacturing insights.

Built with a focus on **practical AI integration**, this project demonstrates how Generative AI can assist in real-world product design and decision-making workflows.

---

## ✨ Features

- 🔍 **AI-Powered Extraction**
  - Converts plain user input into structured product specifications
- 🧠 **LLM Integration**
  - Uses OpenAI to intelligently generate:
    - Features
    - Recommended materials
    - Manufacturing notes
- 🎨 **Clean UI with Streamlit**
  - Simple and intuitive interface for quick interaction
- ⚡ **Real-Time Output**
  - Instant AI-generated results with minimal latency
- ☁️ **Cloud Deployment**
  - Fully deployed using Streamlit Cloud

---

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit  
- **Backend:** Python  
- **AI/LLM:** OpenAI API  
- **Deployment:** Streamlit Cloud  
- **Version Control:** Git + GitHub  

---

## 📸 Demo

🔗 Live App:  
https://spranai.streamlit.app/

---

## 🧠 How It Works

1. User enters a product idea or description  
2. The input is sent to an LLM (OpenAI)  
3. AI processes and structures the output into:
   - Features  
   - Recommended Materials  
   - Manufacturing Notes  
4. Results are displayed in a clean UI  

This mimics real-world **AI-assisted product specification workflows**.

---

## 📂 Project Structure

```
spran-ai/
│── app.py                 # Main Streamlit application
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/nehashirodkar/spran-ai.git
cd spran-ai
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add OpenAI API Key

Create a `.env` file or use Streamlit secrets:

```
OPENAI_API_KEY=your_api_key_here
```

---

## ▶️ Run the App Locally

```bash
streamlit run app.py
```

---

## 🚀 Deployment

This project is deployed using **Streamlit Cloud**:

- Push your code to GitHub  
- Connect repo to Streamlit Cloud  
- Add API key in **Secrets Manager**  
- Deploy 🚀  

---

## 📌 Use Cases

- AI-assisted product design  
- Rapid prototyping of product specs  
- Manufacturing planning insights  
- Business analyst / product manager workflows  

---

## 🔮 Future Improvements

- Add image-based product input (multimodal AI)
- Store generated specs in a database
- Add export options (PDF / JSON)
- Improve prompt engineering for higher accuracy
- Add user authentication