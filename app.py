import json
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# ==========================
# Load Environment Variables
# ==========================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "llama-3.3-70b-versatile"
)

client = Groq(api_key=GROQ_API_KEY)

# ==========================
# Session State
# ==========================

if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""

# ==========================
# Save TXT
# ==========================

def save_response_txt(task_type, task, response):

    os.makedirs("outputs", exist_ok=True)

    file_path = "outputs/response.txt"

    current_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    with open(file_path, "a", encoding="utf-8") as file:

        file.write(f"Date & Time: {current_time}\n")
        file.write(f"Task Type: {task_type}\n")
        file.write(f"Task: {task}\n")
        file.write("AI Response:\n")
        file.write(response)
        file.write("\n")
        file.write("-" * 60)
        file.write("\n\n")

# ==========================
# Save JSON
# ==========================

def save_response_json(task_type, task, response):

    os.makedirs("outputs", exist_ok=True)

    file_path = "outputs/response.json"

    data = {
        "date": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),
        "task_type": task_type,
        "task": task,
        "response": response
    }

    if os.path.exists(file_path):

        with open(file_path, "r", encoding="utf-8") as file:

            try:
                existing_data = json.load(file)

                if isinstance(existing_data, dict):
                    existing_data = [existing_data]

            except:
                existing_data = []

    else:
        existing_data = []

    existing_data.append(data)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            existing_data,
            file,
            indent=4,
            ensure_ascii=False
        )

# ==========================
# UI
# ==========================

st.title("🤖 AI Productivity Assistant")

task_type = st.selectbox(
    "Choose Task Type",
    [
        "Study Plan",
        "Daily Routine",
        "Project Ideas",
        "Professional Email",
        "Custom Task"
    ]
)

user_input = st.text_area(
    "Enter your topic or task"
)

# ==========================
# Generate Button
# ==========================

if st.button("Generate Response"):

    if not user_input.strip():

        st.warning(
            "Please enter a task first."
        )

    else:

        prompt = f"""
You are an AI Productivity Assistant.

Task Type:
{task_type}

User Request:
{user_input}

Generate a structured response with:

1. Goal
2. Key Steps
3. Suggested Timeline
4. Tools or Resources Needed
5. Final Recommendation

Keep the response practical and beginner-friendly.
"""

        try:

            with st.spinner(
                "🤖 Generating response..."
            ):

                response = (
                    client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        model=MODEL_NAME
                    )
                )

            st.session_state.ai_response = (
                response
                .choices[0]
                .message
                .content
            )

            save_response_txt(
                task_type,
                user_input,
                st.session_state.ai_response
            )

            save_response_json(
                task_type,
                user_input,
                st.session_state.ai_response
            )

            st.success(
                "Response Generated Successfully!"
            )

        except Exception as e:

            st.error(
                f"API Error: {e}"
            )

# ==========================
# Show Response
# ==========================

if st.session_state.ai_response:

    st.subheader("AI Response")

    st.write(
        st.session_state.ai_response
    )

    st.download_button(
        label="📄 Download TXT",
        data=st.session_state.ai_response,
        file_name="response.txt",
        mime="text/plain"
    )

    json_data = {
        "date": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),
        "task_type": task_type,
        "task": user_input,
        "response": st.session_state.ai_response
    }

    st.download_button(
        label="📥 Download JSON",
        data=json.dumps(
            json_data,
            indent=4
        ),
        file_name="response.json",
        mime="application/json"
    )

    st.info(
        "Response saved to outputs/response.txt and outputs/response.json"
    )

# ==========================
# Footer
# ==========================

st.markdown("---")

st.markdown(
    "Developed by Niharika | AI Productivity Assistant | Python + Groq + Streamlit"
)