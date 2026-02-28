from dotenv import load_dotenv
import os
load_dotenv()
from groq import Groq
import streamlit as st

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Page config
st.set_page_config(page_title="StudyBuddy", page_icon="📚", layout="centered")

# Title
st.title("📚 StudyBuddy")
st.subheader("Your AI Study Assistant for Middle School")

# Subject selector
subject = st.selectbox("Select your subject:", [
    "General", "Maths", "Science", "English",
    "History", "Geography", "Biology", "Physics"
])

# System prompt
system_prompt = f"""You are StudyBuddy, a friendly and encouraging AI tutor for middle school students aged 11-14.
You are currently helping with {subject}.
- Always explain things in simple, clear language
- Use examples and analogies students can relate to
- Be encouraging and positive
- If asked to solve homework directly, guide them through the steps instead
- Keep responses concise and easy to understand
- Use emojis occasionally to keep it fun"""

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                *[{"role": m["role"], "content": m["content"]}
                  for m in st.session_state.messages]
            ],
            max_tokens=1000
        )
        reply = response.choices[0].message.content
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Sidebar
with st.sidebar:
    st.header("📖 Features")
    st.write("✅ Ask any subject question")
    st.write("✅ Get simple explanations")
    st.write("✅ Step by step help")
    st.write("✅ Encouragement and tips")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.header("🎯 Quiz Mode")
    quiz_topic = st.text_input("Enter a topic for quiz:")
    if st.button("Generate Quiz"):
        if quiz_topic:
            quiz_prompt = f"""Generate a 5 question multiple choice quiz about {quiz_topic} for middle school students.
Format each question exactly like this:
Q1: Question here?
A) Option 1
B) Option 2
C) Option 3
D) Option 4
Answer: A
Make it fun and educational!"""

            quiz_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a quiz generator for middle school students."},
                    {"role": "user", "content": quiz_prompt}
                ],
                max_tokens=1000
            )
            st.session_state.messages.append({
                "role": "assistant",
                "content": "🎯 **Quiz Time!**\n\n" + quiz_response.choices[0].message.content
            })
            st.rerun()
        else:
            st.warning("Please enter a topic first!")

    st.divider()
    st.caption("Made by Izaan Hashmi")