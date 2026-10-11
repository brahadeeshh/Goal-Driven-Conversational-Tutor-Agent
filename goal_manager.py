from tutor import ask_ai


def create_study_plan(subject, target, duration, level):

    prompt = f"""
You are an educational planning assistant.

Create a simple {duration}-day learning plan.

Subject: {subject}
Student level: {level}
Student goal: {target}

Requirements:
- Divide the subject into logical topics.
- Start from fundamentals.
- Gradually increase difficulty.
- Include practice and revision.
- Keep the plan realistic.
- Give exactly {duration} days.

Return the result in this format:

Day 1: Topic
Day 2: Topic
Day 3: Topic

Continue until Day {duration}.
"""

    return ask_ai(prompt)