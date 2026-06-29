from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import streamlit as st
import time as Time
st.set_page_config(
    page_title="AI Interview Preparation Agent",
    page_icon="🎯",
    layout="wide"
)
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY", "")
os.environ['GOOGLE_GENAI_API_KEY'] = os.getenv("GOOGLE_API_KEY", "")

if "model_name" not in st.session_state:
    st.session_state.model_name = "groq:openai/gpt-oss-20b"
    st.session_state.model_label = "🚀 Groq Model"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []         

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False
if "interview_done" not in st.session_state:
    st.session_state.interview_done = False

if "question_count" not in st.session_state:
    st.session_state.question_count = 0        

if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = {}
@st.cache_resource(show_spinner=False)
def load_model(model_name: str):
    return init_chat_model(model=model_name)

def get_agent():
    return load_model(st.session_state.model_name)
sb = st.sidebar
sb.markdown("## ⚙️ Model Settings")

if sb.button("🦙 Ollama Model", use_container_width=True):
    st.session_state.model_name = "ollama:llama3"
    st.session_state.model_label = "🦙 Ollama Model"
    st.toast("Switched to 🦙 Ollama")

if sb.button("🚀 Groq Model", use_container_width=True):
    st.session_state.model_name = "groq:openai/gpt-oss-20b"
    st.session_state.model_label = "🚀 Groq Model"
    st.toast("Switched to 🚀 Groq")

if sb.button("✨ Gemini Model", use_container_width=True):
    st.session_state.model_name = "google_genai:gemini-2.5-flash"
    st.session_state.model_label = "✨ Gemini Model"
    st.toast("Switched to ✨ Gemini")

sb.markdown(f"**Active:** {st.session_state.model_label}")
sb.divider()

theme = sb.selectbox("🎨 Theme", ["Dark", "Light"])
if theme == "Dark":
    st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: white; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    </style>
    """, unsafe_allow_html=True)

sb.divider()
if st.session_state.interview_started:
    sb.markdown(f"**Questions Done:** {st.session_state.question_count} / 5")
    if sb.button("🔄 Reset Interview", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.interview_started = False
        st.session_state.interview_done = False
        st.session_state.question_count = 0
        st.session_state.candidate_info = {}
        st.rerun()
SYSTEM_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["domain", "skills", "level"],
    template="""You are an expert AI Technical Interviewer, HR Interviewer, Coding Interviewer, and Career Mentor.

You are conducting a complete mock interview.

Candidate Information

Domain:
{domain}

Skills:
{skills}

Experience Level:
{level}

Your responsibilities:

1. Conduct a realistic interview consisting of exactly **5 questions**.

Question Distribution:

* Question 1 → Technical
* Question 2 → HR
* Question 3 → Coding / Problem Solving
* Question 4 → Scenario / Project Based
* Question 5 → Advanced Technical or Behavioral

Rules:

* Ask only ONE question at a time.
* Never reveal future questions.
* Never provide the answer before the candidate responds.
* Wait for the candidate's reply.
* Maintain the complete interview context throughout the conversation.

After every candidate answer:

1. Evaluate the answer.
2. Give a score out of 10.
3. Mention:

   * Strengths
   * Weaknesses
   * Missing Points
   * Improvement Suggestions
4. Show a short ideal answer (4–8 lines maximum).
5. Encourage the candidate.
6. Immediately ask the NEXT interview question (if fewer than 5 questions have been asked).

Repeat this process until all five questions are completed.

After Question 5 has been evaluated, DO NOT ask another question.

Instead, generate a final interview report using this exact structure.

# 🎯 Interview Summary

## Overall Score

* Overall Score: XX/50
* Percentage: XX%
* Interview Performance: Excellent / Good / Average / Needs Improvement

---

## Question-wise Performance

| Question | Category | Score (/10) | Remarks |
| -------- | -------- | ----------- | ------- |

---

## Strengths

* ...

---

## Areas to Improve

(Only include topics that actually need improvement.)

---

## Common Mistakes

* ...

---

## Technical Skills Evaluation

Rate each area from 1–10.

* Programming
* Problem Solving
* Debugging
* System Design
* Database
* Communication
* Confidence

---

## Recommended Learning Plan

Suggest practical topics and resources based on the mistakes.

Week 1 / Week 2 / Week 3 / Week 4

---

## Hiring Recommendation

Choose one: Ready for Interviews / Almost Ready / Needs More Practice

Explain your decision.

---

## Final Motivation

Provide a short encouraging message.

Important Rules:

* Never skip evaluation after a candidate answer.
* Never ask multiple questions together.
* Never reveal remaining questions.
* Always remember previous questions and answers.
* Do not repeat questions.
* Base the final report only on the candidate's actual answers during this interview.
* Start the interview immediately by greeting the candidate and asking Question 1.
"""
)
st.markdown("# 🎯 AI Interview Preparation Agent")
if not st.session_state.interview_started:
    with st.form("User"):
        domain = st.selectbox(
            "🌍 Select Domain",
            [
                "Agentic AI","Generative AI","Machine Learning","Deep Learning",
                "Data Science","Data Engineering","MLOps","Computer Vision",
                "NLP","Backend Development","Frontend Development",
                "Full Stack Development","Cloud Computing","Cyber Security",
                "DevOps","Blockchain","Mobile App Development","Game Development",
                "IoT","System Design"
            ]
        )
        skills = st.multiselect(
            "🛠 Select Your Skills",
            [
                "Python","Java","JavaScript","TypeScript","React","Next.js",
                "Node.js","FastAPI","Django","Flask","SQL","PostgreSQL",
                "MongoDB","Redis","Docker","Kubernetes","AWS","Git",
                "LangChain","LangGraph","RAG","OpenAI API","Ollama",
                "PyTorch","TensorFlow","Pandas","NumPy","NLP","CV"
            ]
        )
        level = st.selectbox("🎯 Level", ["Beginner", "Intermediate", "Advanced"])

        submit = st.form_submit_button("✨ Start Interview", use_container_width=True)

    if submit:
        if not domain or not level or len(skills) == 0:
            st.warning("⚠️ Please fill all required fields")
            st.stop()

        skills_text = ", ".join(skills)
        system_content = SYSTEM_PROMPT_TEMPLATE.format(
            domain=domain,
            skills=skills_text,
            level=level,
        )

        
        st.session_state.candidate_info = {
            "domain": domain,
            "skills": skills_text,
            "level": level,
        }

        pr = st.progress(0)
        for i in range(20):
            Time.sleep(0.03)
            pr.progress((i + 1) * 5)

        st.success("🚀 Starting your interview...")

        # Get AI to greet + ask Q1
        try:
            agent = get_agent()
            messages = [
                SystemMessage(content=system_content),
                HumanMessage(content="Hello, I am ready for my interview. Please begin.")
            ]
            with st.spinner("Preparing your interview..."):
                response = agent.invoke(messages)

            opening = response.content
            st.session_state.system_prompt = system_content
            st.session_state.chat_history = [
                {"role": "assistant", "content": opening}
            ]
            st.session_state.interview_started = True
            st.session_state.question_count = 0
            st.rerun()

        except Exception as e:
            st.error("❌ Model error occurred")
            st.write(str(e))
else:
    info = st.session_state.candidate_info
    st.markdown(
        f"**Domain:** {info.get('domain')} &nbsp;|&nbsp; "
        f"**Skills:** {info.get('skills')} &nbsp;|&nbsp; "
        f"**Level:** {info.get('level')}"
    )
    st.divider()
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if not st.session_state.interview_done:
        user_input = st.chat_input("Enter Your Answer...")

        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            messages = [SystemMessage(content=st.session_state.system_prompt)]
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                else:
                    messages.append(AIMessage(content=msg["content"]))

            try:
                agent = get_agent()
                with st.spinner("Evaluating your answer..."):
                    response = agent.invoke(messages)

                ai_reply = response.content

                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                st.session_state.question_count += 1
                if st.session_state.question_count >= 5 and "Interview Summary" in ai_reply:
                    st.session_state.interview_done = True

                st.rerun()
            except Exception as e:
                st.error("❌ Model error occurred")
                st.write(str(e))
    else:
        st.success("🎉 Interview Complete! Scroll up to review your full report.")
        st.info("Click **Reset Interview** in the sidebar to start a new session.")