import os
import json
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Please add it to your .env file.")

client = Groq(api_key=GROQ_API_KEY)

def get_user_input():
    task = input("Enter your productivity task: ")
    return task

def generate_response(task):

    prompt = f"""
You are an AI Productivity Assistant.

User task:
{task}

Generate a clear, structured response with the following sections:

1. Goal
2. Key Steps
3. Suggested Timeline
4. Tools or Resources Needed
5. Final Recommendation

Keep the response practical and beginner-friendly.
"""

    try:

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI productivity assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=MODEL_NAME,
            temperature=0.4,
        )

        return chat_completion.choices[0].message.content

    except Exception as e:

        return f"API Error: {e}"

def save_response(task, response):

    os.makedirs("outputs", exist_ok=True)

    file_path = "outputs/response.txt"

    with open(file_path, "a", encoding="utf-8") as file:
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        file.write(f"Date & Time: {current_time}\n")
        file.write(f"Task: {task}\n")
        file.write("AI Response:\n")
        file.write(response)
        file.write("\n")
        file.write("-" * 60)
        file.write("\n\n")

    print(f"\nResponse saved to {file_path}")

def save_json(task, response):

    os.makedirs("outputs", exist_ok=True)

    file_path = "outputs/response.json"

    data = {
        "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "task": task,
        "response": response
    }

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                existing_data = json.load(file)
            except:
                existing_data = []
    else:
        existing_data = []

    existing_data.append(data)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4)

    print("Response saved to outputs/response.json")

def choose_task_type():

    print("\n" + "=" * 40)
    print(" AI PRODUCTIVITY ASSISTANT ")
    print("=" * 40)

    print("1. Study Plan")
    print("2. Daily Routine")
    print("3. Project Ideas")
    print("4. Professional Email")
    print("5. Custom Task")
    print("6. Exit")

    print("=" * 40)

    choice = input("Enter your choice: ")

    return choice

def main():

    print("AI Productivity Assistant using Groq")
    print("-" * 40)

    choice = choose_task_type()

    if choice == "1":
      topic = input("Enter study topic: ")
      task = f"Create a study plan for {topic}"

    elif choice == "2":
      topic = input("Enter learning goal: ")
      task = f"Create a daily routine for {topic}"

    elif choice == "3":
      topic = input("Enter technology/domain: ")
      task = f"Generate project ideas for {topic}"

    elif choice == "4":
      topic = input("Enter email purpose: ")
      task = f"Write a professional email for {topic}"

    elif choice == "5":
      task = input("Enter your custom task: ")

    elif choice == "6":
      print("\nThank you for using AI Productivity Assistant!")
      return

    else:
      print("\nInvalid choice! Please select a number between 1 and 6.")
      return
    response = generate_response(task)

    print("\nAI Response:\n")
    print(response)

    save_response(task, response)
    save_json(task, response)

if __name__ == "__main__":
    main()