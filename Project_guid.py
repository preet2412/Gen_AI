from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import streamlit as st
import time as Time
st.set_page_config(
    page_title="Project Guider",
    page_icon="🚀",
    layout="wide"
)

load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

agent = init_chat_model(model="groq:openai/gpt-oss-20b", max_tokens=8000)

st.markdown("# 🚀 AI Project Builder Assistant")

prompt = PromptTemplate(
    input_variables=["domain", "skills", "level", "time"],
    template="""
You are a Senior Software Architect and Tech Mentor helping students choose the perfect final-year project.

Candidate Profile:
- Domain: {domain}
- Skills: {skills}
- Level: {level}
- Time Available: {time}

════════════════════════════════════════
CRITICAL RULES — FOLLOW EXACTLY OR OUTPUT IS WRONG:
════════════════════════════════════════

RULE 1 — TIME ESTIMATE:
The candidate has EXACTLY {time} available.
⏳ Time Estimate must ALWAYS say: {time}
Do NOT write "1 day", "4 weeks", or any other value. Write {time} exactly.

RULE 2 — LEARNING ROADMAP SCALING:
The roadmap MUST fit inside {time}.
- If time is "1 Day" → give 4 time-blocks (Morning, Late Morning, Afternoon, Evening)
- If time is "2 Days" → give Day 1 and Day 2 blocks
- If time is "3 Days" to "6 Days" → give one block per day
- If time is "1 Week" → give 3 phases (Start, Mid, End)
- If time is "2 Weeks" → give Week 1 and Week 2
- If time is "3 Weeks" → give Week 1, Week 2, Week 3
- If time is "4 Weeks" or "1 Month" → give Week 1 to Week 4
- If time is "2 Months" → give Week 1 to Week 8
- If time is "3 Months" → give Week 1 to Week 12
NEVER give a 4-week roadmap if time is 1 day or 1 week. Match exactly.

RULE 3 — COMPARISON TABLE:
You MUST print the final comparison table after all 5 projects.
The table is MANDATORY. Never skip it. Never truncate output before it.
If you are about to stop before the table, continue until table is printed.

RULE 4 — FORMAT:
- One 🚀 emoji per project title only — nowhere else
- No preamble, no closing remarks, no extra explanation
- No tables inside individual project sections
- Exactly 5 projects

════════════════════════════════════════
OUTPUT FORMAT — REPEAT FOR ALL 5 PROJECTS:
════════════════════════════════════════

---

🚀 PROJECT [N]: [PROJECT NAME]

📘 Definition:
[3–5 lines — what it does and what problem it solves]

⭐ Why It Matters:
[2–3 lines — real-world relevance, career or industry impact]

🏗 Architecture:
[4–6 lines — describe flow: frontend → backend → AI/ML layer → database → output. Use arrows like: "User uploads file via Streamlit → FastAPI receives → LangChain processes → result stored in PostgreSQL → ranked output shown on UI"]

🛠 Tech Stack:
- [Tech 1] — [one-line purpose]
- [Tech 2] — [one-line purpose]
- [Tech 3] — [one-line purpose]
- [add more as needed]

📋 Key Features:
- [Feature 1]
- [Feature 2]
- [Feature 3]
- [Feature 4]
- [Feature 5]

📅 Learning Roadmap (scaled to {time}):
[Use the correct time blocks as per RULE 2 above]
[Each block: label + what to learn/build/test in that period]

⏳ Time Estimate: {time}
🔥 Difficulty: [Beginner / Intermediate / Advanced — one-line reason why]
💰 Use Case: [Job / Startup / Freelance / Research — one line]

⚡ First Steps to Start Today:
- Step 1: [Concrete first action]
- Step 2: [Second action]
- Step 3: [Third action]

---

[Repeat for Projects 2, 3, 4, 5]

════════════════════════════════════════
FINAL COMPARISON TABLE — MANDATORY, ALWAYS PRINT THIS:
════════════════════════════════════════

| # | Project Name | Difficulty | Core Tech Stack | Time Needed | Best For | Unique Value |
|---|--------------|------------|-----------------|-------------|----------|--------------|
| 1 | ...          | ...        | ...             | {time}      | ...      | ...          |
| 2 | ...          | ...        | ...             | {time}      | ...      | ...          |
| 3 | ...          | ...        | ...             | {time}      | ...      | ...          |
| 4 | ...          | ...        | ...             | {time}      | ...      | ...          |
| 5 | ...          | ...        | ...             | {time}      | ...      | ...          |

[END — no text after this table]
"""
)

sb = st.sidebar
sb.title("🚀 Project Studio")

sb.markdown("""
---

💡 **AI Project Generator**

---

⚡ Job • Startup • Freelance Ideas  
🎯 Built for Developers  
🚀 Learn by building real projects  

---

✔ Fast ideas  
✔ Real-world use cases  
✔ Resume-ready projects  

---
""")
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

    col1, col2 = st.columns(2)

    with col1:
        duration = st.number_input("Duration", min_value=1, value=1)

    with col2:
        unit = st.selectbox("Unit", ["Days", "Weeks", "Months"])

    time = f"{duration} {unit}"

    submit = st.form_submit_button("✨ Generate Projects", use_container_width=True)
if submit:
    if not domain or not level or len(skills) == 0 or not time:
        st.warning("⚠️ Please fill all required fields")
        st.stop()

    skills_text = ", ".join(skills)

    final_prompt = prompt.format(
        domain=domain,
        skills=skills_text,
        level=level,
        time=time
    )
    pr = st.progress(0)

    for i in range(20):
        Time.sleep(0.03)
        pr.progress((i + 1) * 5)

    st.success("🚀 Generating your projects...")

    try:
        with st.spinner("Loading....."):
            response = agent.invoke(final_prompt)

        projects_output = response.content

        st.markdown("## 🎯 Generated Output")
        st.markdown(projects_output)

        table_prompt = f"""
You are a Senior Software Architect.

Below are 5 project ideas that were generated for a candidate:

{projects_output}

---

Now generate ONLY the final comparison table for all 5 projects above.
Use this exact format — nothing else, no extra text before or after:

| # | Project Name | Difficulty | Core Tech Stack | Time Needed | Best For | Unique Value |
|---|--------------|------------|-----------------|-------------|----------|--------------|
| 1 | ...          | ...        | ...             | {time}      | ...      | ...          |
| 2 | ...          | ...        | ...             | {time}      | ...      | ...          |
| 3 | ...          | ...        | ...             | {time}      | ...      | ...          |
| 4 | ...          | ...        | ...             | {time}      | ...      | ...          |
| 5 | ...          | ...        | ...             | {time}      | ...      | ...          |

Fill every cell. Time Needed must be {time} for all rows. Output ONLY the table.
"""
        with st.spinner("Generating comparison table..."):
            table_response = agent.invoke(table_prompt)
        st.markdown("---")
       
        st.markdown("## 📊 Project Comparison Table")
        st.markdown(table_response.content)

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