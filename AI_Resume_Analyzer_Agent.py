from pypdf import PdfReader
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import streamlit as st
import time as Time

load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
os.environ['GOOGLE_GENAI_API_KEY'] = os.getenv("GOOGLE_API_KEY")
st.set_page_config(
    page_title="AI Resume Analyzer Agent",
    page_icon="📝",
    layout="wide"
)
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "groq:openai/gpt-oss-20b"

sb = st.sidebar

if sb.button("🦙 Ollama Model", use_container_width=True):
    try:
        init_chat_model(model="ollama:llama3")
        st.session_state.selected_model = "ollama:llama3"
    except Exception as e:
        st.toast(str(e))
    else:
        st.success("Model Shift to 🦙 Ollama")
        st.toast("Model Shift to 🦙 Ollama")

if sb.button("🚀 Groq Model", use_container_width=True):
    try:
        init_chat_model(model="groq:openai/gpt-oss-20b") 
        st.session_state.selected_model = "groq:openai/gpt-oss-20b"
    except Exception as e:
        st.toast(str(e))
    else:
        st.toast("Model Shift to 🚀 Groq ")
        st.success("Model Shift to 🚀 Groq ")

if sb.button("✨ Gemini Model", use_container_width=True):
    try:
        init_chat_model(model="google_genai:gemini-2.5-flash")
        st.session_state.selected_model = "google_genai:gemini-2.5-flash"
    except Exception as e:
        st.toast(str(e))
    else:
        st.success(" Model Shift to ✨ Gemini")
        st.toast("Model Shift to ✨ Gemini")
agent = init_chat_model(model=st.session_state.selected_model)

st.markdown("# 🤖 ⚡ AI Resume Analyzer")

prompt = PromptTemplate(
    input_variables=["resume_text"],
    template="""
You are an Expert AI Resume Analyzer, Senior Technical Recruiter, ATS (Applicant Tracking System) Specialist, and Career Coach with years of experience reviewing resumes across software engineering, data science, AI/ML, cloud, cybersecurity, business, and other professional domains.

Your task is to analyze the uploaded resume and generate a clear, professional, and actionable report.

=========================
RESUME
=========================

{resume_text}

=========================
YOUR RESPONSIBILITIES
=========================

1. Resume Analysis
- Evaluate the overall quality of the resume.
- Identify the candidate's strengths.
- Identify weaknesses or missing information.
- Comment on formatting, readability, and organization.
- Mention if any important resume sections appear to be missing.

2. Skill Extraction
Extract all relevant skills found in the resume.

Include skills from categories such as:
- Programming Languages
- Frameworks & Libraries
- Databases
- Cloud Platforms
- Developer Tools
- Technologies
- Soft Skills

Remove duplicate skills.

3. Missing Skills
Based on the candidate's profile, identify valuable skills that are not present but would strengthen the resume.

Only recommend skills that are genuinely relevant to the candidate's domain.

Do NOT recommend unrelated technologies.

4. ATS Score
Assign an ATS score between 0 and 100.

Consider factors such as:
- Resume structure
- Keyword optimization
- Skill relevance
- Experience description
- Project quality
- Education
- Formatting
- ATS compatibility

Provide a short explanation for the score.

5. Improvement Suggestions
Provide practical, actionable suggestions to improve the resume.

Suggestions may include:
- Better resume summary
- Stronger project descriptions
- Quantifying achievements with numbers
- Improving experience bullet points
- Adding certifications
- Adding missing keywords
- Improving ATS formatting
- Highlighting technical skills more effectively

=========================
IMPORTANT RULES
=========================

- Analyze only the information present in the resume.
- Never invent experience, skills, certifications, education, or projects.
- If information is unavailable, clearly state "Not Found".
- Keep the report concise, professional, and recruiter-friendly.
- Use bullet points where appropriate.
- Avoid unnecessary explanations.
- Do not include markdown code blocks.
- Return only the final report.

=========================
OUTPUT FORMAT
=========================

# 📄 AI Resume Analysis Report

## 🎯 ATS Score
**Score:** XX/100

**Reason:**
A brief explanation (2–4 sentences).

---

## 💻 Detected Skills

### Programming Languages
- ...

### Frameworks & Libraries
- ...

### Databases
- ...

### Cloud Platforms
- ...

### Developer Tools
- ...

### Technologies
- ...

### Soft Skills
- ...

---

## ⚠️ Missing Skills
- ...
- ...
- ...

---

## ✅ Resume Analysis

### Strengths
- ...
- ...
- ...

### Weaknesses
- ...
- ...
- ...

---

## 💡 Improvement Suggestions
- ...
- ...
- ...
- ...
- ...

---

## 🏁 Final Verdict

Write a concise paragraph (3–5 sentences) summarizing:

- Overall resume quality
- ATS readiness
- Candidate's current strengths
- Top priorities for improvement

The report should be easy to read, professional, and suitable for both recruiters and job seekers."""
)
with st.form("User"):
    file = st.file_uploader("Uploade Your Resume ", type=["pdf"])
    submit = st.form_submit_button("✨ Analyze Resume ..", use_container_width=True)
if submit:
    if file == None:
        st.warning("⚠️ Please fill all required fields")
        st.stop()
    t = PdfReader(file)
    text = ""
    for i in t.pages:
        text += i.extract_text() or ""
    final_prompt = prompt.format(
        resume_text=text
    )
    pr = st.progress(0)

    for i in range(20):
        Time.sleep(0.03)
        pr.progress((i + 1) * 5)

    st.success("🚀 Generating Output...")
    try:
        with st.spinner("Loading....."):
            response = agent.invoke(final_prompt)

        st.markdown("## 🎯 Generated Output")
        st.markdown(response.content)

        st.success("🎉 Done Successfully!")

    except Exception as e:
        st.error("❌ Model error occurred")
        st.write(str(e))
theme = sb.selectbox("Theme", ["Dark", "Light"])
if theme == "Dark":
    st.markdown("""
    <style>
    .stApp { background-color: black; color: white; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    </style>
    """, unsafe_allow_html=True)