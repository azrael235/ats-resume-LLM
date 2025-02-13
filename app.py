import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
Hey, act like a highly skilled ATS (Applicant Tracking System) with expertise in tech roles like software engineering, data science, and big data engineering.
Evaluate the resume against the provided job description, considering the competitive job market. Provide a structured response with:

{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}

Resume:
{text}

Job Description:
{jd}
"""

# Matrix-Themed UI
st.set_page_config(page_title="Matrix ATS", page_icon="⚛", layout="wide")

matrix_style = """
<style>
    body {
        background-color: black;
        color: #00FF00;
        font-family: 'Courier New', monospace;
    }
    .stTextInput, .stTextArea, .stFileUploader, .stButton {
        background-color: #001a00;
        color: #00FF00;
        border-radius: 10px;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: black !important;
        color: #00FF00 !important;
    }
    .stButton button {
        background-color: #003300;
        color: #00FF00;
        border: 2px solid #00FF00;
    }
    .stButton button:hover {
        background-color: #005500;
    }
</style>
"""

st.markdown(matrix_style, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("< M A T R I X  A T S >")
    st.subheader("About")
    st.write("An advanced ATS powered by Gemini Pro and Streamlit, designed for tech professionals.")
    st.markdown("""
    - [Streamlit](https://streamlit.io/)
    - [Gemini Pro](https://deepmind.google/technologies/gemini/#introduction)
    - [Makersuite API Key](https://makersuite.google.com/)
    - [GitHub Repository](https://github.com/azrael235)
    """)
    add_vertical_space(5)
    st.write("Built by Akash Raj. Enter the Matrix.")

# Main UI
st.title("< M A T R I X  A T S >")
st.text("Optimize Your Resume for ATS Systems")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Upload a PDF resume")

submit = st.button("Analyze")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))
        st.subheader("Analysis Result")
        st.json(json.loads(response))
