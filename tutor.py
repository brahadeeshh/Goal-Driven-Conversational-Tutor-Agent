import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.6-flash"


SYSTEM_PROMPT = """
You are GoalTutor, an intelligent personal tutor.

Your job is to help students achieve their learning goals.

Teaching style:
- Beginner friendly
- Clear and simple
- Step-by-step
- Give examples
- Ask questions to check understanding
- Help students identify mistakes
- Adjust explanations based on the student's level
- Keep the student focused on their learning goal
"""


def ask_ai(user_prompt):
    prompt = f"""
{SYSTEM_PROMPT}

Student request:
{user_prompt}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


def tutor_chat(student_name, subject, goal, current_topic, progress, user_message):
    prompt = f"""
Student name: {student_name}

Subject:
{subject}

Learning goal:
{goal}

Current topic:
{current_topic}

Progress:
{progress}%

Student message:
{user_message}

Act as a personal tutor.

Explain concepts clearly and step-by-step.
If the student is confused, simplify the explanation.
Use examples when useful.
Keep the student moving toward their learning goal.
"""

    return ask_ai(prompt)
