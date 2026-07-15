import streamlit as st
import pandas as pd
import io
import base64
from datetime import datetime
import re
import pytesseract
from PIL import Image
import PyPDF2
from docx import Document
import easyocr

# For translation
from deep_translator import GoogleTranslator

# For NER
import spacy

# For live feed processing
import cv2
import numpy as np

# For text-to-speech
try:
    import pyttsx3
    tts_available = True
except ImportError:
    tts_available = False

# Page configuration
st.set_page_config(
    page_title="Smart Document Scanner",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with solid colors and dynamic effects
st.markdown("""
<style>
    /* Modern color scheme */
    :root {
        --primary-color: #2563eb;
        --secondary-color: #1e40af;
        --accent-color: #3b82f6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --dark-bg: #1f2937;
        --light-bg: #f8fafc;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --border-color: #e5e7eb;
        --hover-color: #f3f4f6;
    }
    
    /* App background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Main container */
    .main .block-container {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        margin-top: 1rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Modern header */
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(90deg, #2563eb 0%, #1e40af 100%);
        color: white;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
        border: 2px solid #3b82f6;
    }
    
    .main-header h1 {
        font-size: 2.7rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #fff;
        /* Remove gradient text fill for better visibility */
        background: none;
        -webkit-background-clip: unset;
        -webkit-text-fill-color: #fff;
        background-clip: unset;
        text-fill-color: #fff;
        letter-spacing: 2px;
        text-shadow: 1px 2px 8px rgba(0,0,0,0.10);
    }
    
    .main-header p {
        font-size: 1.25rem;
        opacity: 1;
        margin: 0;
        color: #fff;
        font-weight: 600;
        text-shadow: 1px 2px 8px rgba(0,0,0,0.10);
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: var(--primary-color);
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        background: var(--secondary-color);
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Result boxes */
    .result-box {
        background: var(--light-bg);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        margin: 1.5rem 0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        animation: fade-in 0.5s ease-out;
    }
    
    @keyframes fade-in {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Status boxes */
    .success-box {
        background: #ecfdf5;
        border: 1px solid #10b981;
        color: #065f46;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        animation: slide-in 0.3s ease-out;
    }
    
    .warning-box {
        background: #fffbeb;
        border: 1px solid #f59e0b;
        color: #92400e;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        animation: slide-in 0.3s ease-out;
    }
    
    .error-box {
        background: #fef2f2;
        border: 1px solid #ef4444;
        color: #991b1b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        animation: shake 0.5s ease-out;
    }
    
    @keyframes slide-in {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        color: var(--text-primary);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid var(--border-color);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--primary-color);
    }
    
    .metric-card:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: var(--primary-color);
    }
    
    .metric-card h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        animation: counter-up 0.5s ease-out;
    }
    
    @keyframes counter-up {
        from { transform: scale(0.8); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    .metric-card p {
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    /* Sidebar styling */
    .sidebar .stSelectbox > label {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 1rem;
    }
    
    .stTextArea > label, .stTextInput > label {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 1rem;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    }
    
    /* File uploader */
    .stFileUploader > div > div > div {
        border: 2px dashed var(--border-color);
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div > div:hover {
        border-color: var(--primary-color);
        background: var(--hover-color);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--light-bg);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(90deg, #2563eb 0%, #1e40af 100%);
        color: #fff;
        text-align: center;
        padding: 2rem;
        border-radius: 16px;
        margin-top: 2rem;
        box-shadow: 0 4px 6px -5px rgba(0, 0, 0, 0.1);
        border: 2px solid #3b82f6;
    }
    
    .footer h3 {
        font-size: 1.7rem;
        font-weight: 700;
        color: #fff;
        background: none;
        -webkit-background-clip: unset;
        -webkit-text-fill-color: #fff;
        background-clip: unset;
        text-fill-color: #fff;
        margin-bottom: 0.5rem;
    }
    
    .footer p {
        color: #fff;
        font-weight: 500;
        margin: 0.2rem 0;
    }
    
    /* Animations */
    .fade-in {
        animation: fade-in 0.5s ease-out;
    }
    
    .slide-up {
        animation: slide-up 0.3s ease-out;
    }
    
    @keyframes slide-up {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Loading spinner */
    .loading-spinner {
        border: 3px solid var(--border-color);
        border-top: 3px solid var(--primary-color);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        }
        
        .main .block-container {
            background: #374151;
            color: white;
        }
        
        .feature-card {
            background: #374151;
            border-color: #4b5563;
            color: white;
        }
        
        .metric-card {
            background: #374151;
            border-color: #4b5563;
            color: white;
        }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .metric-card h3 {
            font-size: 1.5rem;
        }
        
        .feature-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_text' not in st.session_state:
    st.session_state.processed_text = ""
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []

# Modern Header
st.markdown("""
<div class="main-header">
    <h1>Smart Document Scanner</h1>
    <p>Extract, Translate, Recognize Entities, OCR, and More</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Features")
feature = st.sidebar.selectbox(
    "Choose your processing tool:",
    ["Text Extraction", "Translation", "Entity Recognition", 
     "Live Camera OCR", "Download Results"]
)

# Helper functions with enhanced error handling
def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file with progress tracking"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        total_pages = len(pdf_reader.pages)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, page in enumerate(pdf_reader.pages):
            text += page.extract_text()
            progress = (i + 1) / total_pages
            progress_bar.progress(progress)
            status_text.text(f'Processing page {i + 1} of {total_pages}')
        
        progress_bar.empty()
        status_text.empty()
        return text
    except Exception as e:
        return f"PDF Extraction Error: {str(e)}"

def extract_text_from_docx(docx_file):
    """Extract text from DOCX file with formatting preservation"""
    try:
        doc = Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n\n"
        return text.strip()
    except Exception as e:
        return f"DOCX Extraction Error: {str(e)}"

def recognize_handwriting_easyocr(image):
    reader = easyocr.Reader(['en'], gpu=False)
    if hasattr(image, 'read'):
        from PIL import Image as PILImage
        import numpy as np
        pil_img = PILImage.open(image).convert('RGB')
        img_np = np.array(pil_img)
        result = reader.readtext(img_np, detail=0)
    else:
        result = reader.readtext(image, detail=0)
    return "\n".join(result)

def extract_text_from_image(image_file):
    """Extract text from image using EasyOCR (preferred) or pytesseract as fallback"""
    try:
        image = Image.open(image_file)
        image = image.convert('RGB')
        # Try EasyOCR first (no mention in UI)
        try:
            text = recognize_handwriting_easyocr(image_file)
            if text and text.strip():
                return text
        except Exception as e:
            pass  # Silently fall back
        # Fallback to pytesseract (no mention in UI)
        text = pytesseract.image_to_string(image, config='--psm 6')
        return text if text.strip() else "No text detected in image"
    except Exception as e:
        return f"Image OCR Error: {str(e)}"


# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_named_entities(text):
    """Extract entities using both spaCy and regex with deduplication"""
    try:
        entities = []

        # --- spaCy NER ---
        doc = nlp(text)
        for ent in doc.ents:
            entities.append({
                "text": ent.text.strip(),
                "label": ent.label_,
                "confidence": "High (spaCy)"
            })

        # --- Regex-based detection ---
        regex_patterns = {
            "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "PHONE": r'\b(?:\+91[-\s]?)?[6-9]\d{9}\b',
            "URL": r'https?://[^\s]+|www\.[^\s]+',
            "MONEY": r'\$\d+(?:,\d{3})*(?:\.\d{2})?|\b\d+(?:\.\d{2})?\s?(?:USD|Rs|INR|dollars?|rupees?)\b',
            "DATE": r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})\b'
        }

        for label, pattern in regex_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if not any(e["text"] == match for e in entities):
                    entities.append({
                        "text": match.strip(),
                        "label": label,
                        "confidence": "Regex"
                    })

        return entities

    except Exception as e:
        return [{"error": str(e)}]


def create_download_link(text, filename="processed_text.txt"):
    """Create a download link"""
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}" class="download-btn">Download {filename}</a>'
    return href

def speak_text(text):
    if not tts_available:
        st.warning("pyttsx3 is not installed. Please run 'pip install pyttsx3' in your environment.")
        return
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.warning(f"TTS Error: {str(e)}")

# Feature implementations
if feature == "Text Extraction":
    st.markdown('<div class="feature-card fade-in" style="background: linear-gradient(120deg, #f8fafc 60%, #e0e7ff 100%, #f0abfc 100%);">', unsafe_allow_html=True)
    st.header("Text Extraction")
    st.write("Extract text from various document formats—including printed and handwritten images—with precision and speed.")
    
    col1, col2 = st.columns(2)
    with col1:
        upload_type = st.selectbox("Input method:", ["Upload Document", "Paste Text"])
    with col2:
        if upload_type == "Upload Document":
            file_format = st.selectbox("Format:", ["Auto-detect", "PDF", "Word", "Text", "Image"])
    
    extracted_text = ""
    
    if upload_type == "Upload Document":
        uploaded_file = st.file_uploader(
            "Choose your document (PDF, DOCX, TXT, or image with printed/handwritten text)", 
            type=['txt', 'pdf', 'docx', 'png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            help="Supported: PDF, DOCX, TXT, Images (printed or handwritten text)"
        )
        
        if uploaded_file is not None:
            file_details = {
                "filename": uploaded_file.name,
                "filetype": uploaded_file.type,
                "filesize": uploaded_file.size
            }
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.write(f"**File:** {file_details['filename']}")
            st.write(f"**Type:** {file_details['filetype']}")
            st.write(f"**Size:** {file_details['filesize']:,} bytes")
            st.markdown('</div>', unsafe_allow_html=True)
            file_type = uploaded_file.type
            # Show image preview if image file
            if file_type in ["image/png", "image/jpeg", "image/jpg", "image/bmp", "image/tiff"]:
                st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
                extracted_text = extract_text_from_image(uploaded_file)
            elif file_type == "text/plain":
                extracted_text = str(uploaded_file.read(), "utf-8")
            elif file_type == "application/pdf":
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                extracted_text = extract_text_from_docx(uploaded_file)
    else:
        extracted_text = st.text_area("Enter your text:", height=200, placeholder="Paste your text here...")
    
    if extracted_text:
        st.session_state.processed_text = extracted_text
        st.markdown('<div class="result-box slide-up">', unsafe_allow_html=True)
        st.subheader("Extracted Text")
        st.text_area("", extracted_text, height=300, key="extracted_display")
        if tts_available and st.button("Speak Extracted Text", key="speak_extracted"):
            speak_text(extracted_text)
        elif not tts_available:
            st.info("Text-to-speech is available after installing pyttsx3.")
        st.markdown('</div>', unsafe_allow_html=True)

elif feature == "Translation":
    st.markdown('<div class="feature-card fade-in" style="background: linear-gradient(120deg, #f0abfc 0%, #a5b4fc 100%, #f8fafc 100%);">', unsafe_allow_html=True)
    st.header("Universal Translation")
    st.write("Translate text between multiple languages with high accuracy.")
    
    # Language selection
    languages = {
        'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de',
        'Italian': 'it', 'Portuguese': 'pt', 'Russian': 'ru', 'Chinese': 'zh',
        'Japanese': 'ja', 'Korean': 'ko', 'Arabic': 'ar', 'Hindi': 'hi', 'Kannada': 'kn'
    }
    
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("From:", ['Auto-detect'] + list(languages.keys()))
    with col2:
        target_lang = st.selectbox("To:", list(languages.keys()), index=1)
    
    # Text input
    if st.session_state.processed_text:
        use_extracted = st.checkbox("Use extracted text", value=True)
        if use_extracted:
            text_to_translate = st.session_state.processed_text
            st.text_area("Text to translate:", text_to_translate, height=150, disabled=True)
        else:
            text_to_translate = st.text_area("Enter text to translate:", height=150)
    else:
        text_to_translate = st.text_area("Enter text to translate:", height=150)
    
    if st.button("Translate", type="primary"):
        if text_to_translate:
            try:
                with st.spinner("Translating..."):
                    translator = GoogleTranslator(
                        source='auto' if source_lang == 'Auto-detect' else languages[source_lang],
                        target=languages[target_lang]
                    )
                    translated_text = translator.translate(text_to_translate)
                
                st.markdown('<div class="result-box slide-up">', unsafe_allow_html=True)
                st.subheader(f"Translation Result ({target_lang})")
                st.text_area("", translated_text, height=200, key="translation_result")
                if tts_available and st.button("Speak Translation", key="speak_translation"):
                    speak_text(translated_text)
                elif not tts_available:
                    st.info("Text-to-speech is available after installing pyttsx3.")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Save to history
                st.session_state.translation_history.append({
                    'source': source_lang,
                    'target': target_lang,
                    'original': text_to_translate[:100] + "..." if len(text_to_translate) > 100 else text_to_translate,
                    'translated': translated_text,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.write("Translation completed successfully!")
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.write(f"Translation error: {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.write("Please enter text to translate.")
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif feature == "Entity Recognition":
    st.markdown('<div class="feature-card fade-in" style="background: linear-gradient(120deg, #a7f3d0 0%, #fef9c3 100%, #f8fafc 100%);">', unsafe_allow_html=True)
    st.header("Smart Entity Recognition")
    st.write("Identify and extract named entities from your text automatically.")

    if st.session_state.processed_text:
        use_extracted = st.checkbox("Use extracted text", value=True)
        if use_extracted:
            text_to_analyze = st.session_state.processed_text
            st.text_area("Text to analyze:", text_to_analyze, height=150, disabled=True)
        else:
            text_to_analyze = st.text_area("Enter text to analyze:", height=150)
    else:
        text_to_analyze = st.text_area("Enter text to analyze:", height=150)

    if st.button("Analyze Entities", type="primary"):
        if text_to_analyze:
            with st.spinner("Analyzing entities..."):
                entities = extract_named_entities(text_to_analyze)

            if entities and not any('error' in entity for entity in entities):
                st.markdown('<div class="result-box slide-up">', unsafe_allow_html=True)
                st.subheader(f"Found {len(entities)} Entities")

                # Group entities by label
                entity_groups = {}
                for entity in entities:
                    label = entity['label']
                    if label not in entity_groups:
                        entity_groups[label] = []
                    entity_groups[label].append(entity['text'])

                # Filter partial names (e.g., remove "Lena" if "Lena Voss" exists)
                def filter_partial_names(names):
                    unique = list(set(names))
                    filtered = []
                    for name in unique:
                        if not any(name != other and name in other for other in unique):
                            filtered.append(name)
                    return filtered

                # Display each group
                for label, items in entity_groups.items():
                    cleaned = filter_partial_names(items)
                    with st.expander(f"{label} ({len(cleaned)})"):
                        for item in sorted(cleaned):
                            st.write(f"• {item}")

                st.markdown('</div>', unsafe_allow_html=True)

                # Optional text-to-speech
                all_entities_text = '\n'.join([entity['text'] for entity in entities])
                if tts_available and st.button("Speak Entities", key="speak_entities"):
                    speak_text(all_entities_text)
                elif not tts_available:
                    st.info("Text-to-speech is available after installing pyttsx3.")
            else:
                st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                st.write("No entities found in the text.")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.write("Please enter text to analyze.")
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


elif feature == "Live Camera OCR":
    st.markdown('<div class="feature-card fade-in" style="background: linear-gradient(120deg, #fca5a5 0%, #fef9c3 100%, #f8fafc 100%);">', unsafe_allow_html=True)
    st.header("Live Camera OCR")
    st.write("Capture text from your camera feed using OCR.")
    st.info("This feature requires camera access and may not work in all browsers/environments.")
    if st.button("Start Camera", type="primary"):
        import cv2
        import pytesseract
        import tempfile
        from PIL import Image as PILImage
        import time
        st.info("Camera started. Position your document. The image will be captured automatically after 5 seconds.")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Could not open camera.")
        else:
            frame_placeholder = st.empty()
            last_frame = None
            start_time = time.time()
            captured = False
            while True:
                ret, frame = cap.read()
                if not ret:
                    st.warning("Failed to capture frame from camera.")
                    break
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True, caption="Live Camera Feed (Auto capture in 5 seconds)")
                last_frame = frame.copy()
                elapsed = time.time() - start_time
                if elapsed >= 5 and not captured:
                    pil_img = PILImage.fromarray(cv2.cvtColor(last_frame, cv2.COLOR_BGR2RGB))
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
                        pil_img.save(tmpfile.name)
                        captured_img_path = tmpfile.name
                    try:
                        text = pytesseract.image_to_string(last_frame)
                        if not text or not text.strip():
                            text = recognize_handwriting_easyocr(pil_img)
                        if not text or not text.strip():
                            text = "No text detected in image"
                    except Exception:
                        text = "No text detected in image"
                    st.success("Image captured and text extracted!")
                    st.markdown('<div class="result-box slide-up">', unsafe_allow_html=True)
                    st.subheader("Extracted Text:")
                    st.text_area("", text, height=200, key="live_extracted_camera")
                    if tts_available and st.button("Speak Camera OCR Text", key="speak_camera_ocr"):
                        speak_text(text)
                    elif not tts_available:
                        st.info("Text-to-speech is available after installing pyttsx3.")
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.session_state.processed_text = text
                    st.image(captured_img_path, caption="Captured Image", use_container_width=True)
                    st.info("Camera stopped. You may close this window.")
                    captured = True
                    break
            cap.release()
    st.markdown('</div>', unsafe_allow_html=True)

elif feature == "Download Results":
    st.markdown('<div class="feature-card fade-in" style="background: linear-gradient(120deg, #a5b4fc 0%, #fca5a5 100%, #f8fafc 100%);">', unsafe_allow_html=True)
    st.header("Download Results")
    st.write("Download your processed or translated text.")
    if st.session_state.processed_text:
        st.subheader("Processed Text")
        st.text_area("", st.session_state.processed_text, height=200, key="download_text", disabled=True)
        if tts_available and st.button("Speak Downloaded Text", key="speak_downloaded"):
            speak_text(st.session_state.processed_text)
        elif not tts_available:
            st.info("Text-to-speech is available after installing pyttsx3.")
        st.markdown(create_download_link(st.session_state.processed_text, "processed_text.txt"), unsafe_allow_html=True)
    else:
        st.info("No processed text available for download.")
    if st.session_state.translation_history:
        st.subheader("Translation History")
        for entry in st.session_state.translation_history:
            st.write(f"{entry['timestamp']}: {entry['source']} → {entry['target']}: {entry['original']} → {entry['translated']}")
        history_text = '\n'.join([
            f"{entry['timestamp']}: {entry['source']} → {entry['target']}: {entry['original']} → {entry['translated']}"
            for entry in st.session_state.translation_history
        ])
        st.markdown(create_download_link(history_text, "translation_history.txt"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <h3>Smart Document Scanner</h3>
    <p>Built with Streamlit | Fast, Accurate, and Modern Document Analysis</p>
    <p><strong>Features:</strong> Extraction • Translation • Entity Recognition • Camera OCR • Download</p>
</div>
""", unsafe_allow_html=True)