import streamlit as st

st.set_page_config(
    page_title="AI Developer Suite",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Developer Suite")

choice = st.selectbox(
    "Choose a Project",
    [
        "💡 AI Project Generator",
        "📄 AI Resume Analyzer",
        "💻 AI Interview Preparation Agent"
    ]
)

if choice == "💡 AI Project Generator":
    import Project_guid

elif choice == "📄 AI Resume Analyzer":
    import AI_Resume_Analyzer_Agent

elif choice == "💻 AI Interview Preparation Agent":
    import AI_Interview_Preparation_Agent