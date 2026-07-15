```markdown
# Smart Document Scanner 📄🔍

An all-in-one, intelligent document processing and Optical Character Recognition (OCR) web application built with **Python** and **Streamlit**. Designed for speed, accuracy, and modern document analysis, this tool seamlessly bridges visual perception with Natural Language Processing (NLP) to extract, translate, analyze, and vocalize text from diverse document formats.

---

## 🚀 Key Features

* **Multi-Format Text Extraction:** * Extract text from standard documents (**PDF**, **DOCX**, **TXT**) with automated page-by-page progress tracking and formatting preservation.
  * Robust image OCR supporting **PNG**, **JPG**, **JPEG**, **BMP**, and **TIFF** formats.
  * Dual-engine OCR utilization: Prioritizes **EasyOCR** for superior handling of printed and handwritten text, with silent fallback to **PyTesseract**.
* **Universal Language Translation:** * Integrated with `deep_translator` (Google Translator API) for high-accuracy translation across 13+ languages including English, Spanish, French, German, Chinese, Japanese, Hindi, and Kannada.
  * Automatic source language detection and session-based translation history tracking.
* **Smart Named Entity Recognition (NER):** * Hybrid entity extraction combining deep learning (**spaCy** `en_core_web_sm`) and rule-based regular expressions (**Regex**).
  * Automatically identifies, categorizes, and deduplicates entities such as *Persons, Organizations, Email Addresses, Phone Numbers, URLs, Monetary Values,* and *Dates*.
* **Live Camera OCR:** * Real-time video feed capture using **OpenCV** (`cv2`).
  * Automated 5-second countdown timer for hands-free document positioning and instant frame-to-text conversion.
* **Auditory Feedback (Text-to-Speech):** * Offline vocalization of extracted text, translated results, and analyzed entities using `pyttsx3`.
* **Export & Download Pipeline:** * Instant base64 download links to export processed text and complete translation logs as `.txt` files.

---

## 🛠️ Tech Stack & Architecture

| Component | Technology / Library |
| :--- | :--- |
| **Frontend & UI** | Streamlit, Custom CSS (Responsive, Gradient & Dark Mode Support) |
| **Document Parsing** | `PyPDF2`, `python-docx` |
| **Computer Vision & OCR** | `easyocr`, `pytesseract`, `opencv-python` (cv2), `Pillow` (PIL), `numpy` |
| **NLP & NER** | `spacy` (`en_core_web_sm`), Custom Regex Pipelines |
| **Translation & TTS** | `deep-translator`, `pyttsx3` |
| **Data Handling** | `pandas`, `io`, `base64`, `datetime` |

---

## 📋 Prerequisites & System Requirements

Before running the application, ensure you have the following installed on your system:

1. **Python 3.8+**
2. **Tesseract OCR Engine:**
   * **Windows:** Download and install from [UB-Mannheim Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki). Add the installation path (e.g., `C:\Program Files\Tesseract-OCR`) to your System PATH.
   * **Linux (Ubuntu/Debian):**
     ```bash
     sudo apt-get update
     sudo apt-get install tesseract-ocr
     ```
   * **macOS (Homebrew):**
     ```bash
     brew install tesseract
     ```

---

## ⚙️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/yourusername/smart-document-scanner.git](https://github.com/yourusername/smart-document-scanner.git)
   cd smart-document-scanner

```

2. **Create and Activate a Virtual Environment:**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate

```


3. **Install Python Dependencies:**
Create a `requirements.txt` file with the packages below, then run:
```bash
pip install -r requirements.txt

```


**`requirements.txt`:**
```text
streamlit
pandas
pytesseract
Pillow
PyPDF2
python-docx
easyocr
deep-translator
spacy
opencv-python
numpy
pyttsx3

```


4. **Download spaCy English Language Model:**
```bash
python -m spacy download en_core_web_sm

```



---

## 💻 Running the Application

Launch the Streamlit web server by running the following command from your terminal:

```bash
streamlit run app.py

```

The application will automatically open in your default web browser at `http://localhost:8501`. Use the left sidebar to navigate between **Text Extraction**, **Translation**, **Entity Recognition**, **Live Camera OCR**, and **Download Results**.

---

## 👥 Project Creators

Designed and developed by:

* **Nishan U Shetty**
* **Ravi Kishan Kumar**

---



```

```