# 🚨 CivicSense: AI-Powered Disaster Management Dashboard

An intelligent, real-time crisis response command center dashboard built for the **Programming for AI Lab Project**. This application dynamically parses historical disaster records, maps crisis locations globally, and utilizes a local Large Language Model (LLM) to generate tactical field directives for emergency personnel.

---

## 🚀 Features
* **Live Kaggle Ingestion:** Dynamically structures and processes raw disaster logs (`kaggle_disasters.csv`) on startup.
* **Dynamic Map Interface:** Uses Folium to auto-center map pins directly over the dataset's coordinates with color-coded threat markers.
* **On-Demand AI Crisis Summary:** Leverages the `google/flan-t5-small` text transformer model to generate single-sentence strategic advice logs.
* **Operational Drill-Down Inspector:** Allows operators to select specific incidents to inspect full field reports and casualties without cluttering the screen.

---

## 🛠️ Tech Stack & Extensions
* **Framework:** Streamlit (Python)
* **Geospatial Mapping:** Folium / Streamlit-Folium
* **Data Processing:** Pandas
* **AI Engine:** Hugging Face Transformers & PyTorch

---

## 💻 Setup & Installation

1. Clone or download this repository.
2. Install the required Python extension libraries via terminal:
   ```bash
   pip install streamlit folium streamlit-folium pandas transformers torch

   Make sure your kaggle_disasters.csv file is placed in the project root folder.

Run the application:

Bash
python -m streamlit run app.py
