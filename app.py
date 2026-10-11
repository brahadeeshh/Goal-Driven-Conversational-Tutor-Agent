
import streamlit as st

from database import create_tables, save_goal
from goal_manager import create_study_plan
from tutor import tutor_chat


# -------------------------
# PAGE CONFIGURATION
# -------------------------

st.set_page_config(
    page_title="GoalTutor | AI Learning",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_tables()


# -------------------------
# CUSTOM CSS
# -------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #6254e8;
    --primary-dark: #5042d8;
    --bg: #f7f8fc;
    --card: #ffffff;
    --text: #20233a;
    --muted: #777d96;
    --border: #e8eaf3;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--bg);
}

.block-container {
    padding: 2rem 3rem 3rem;
    max-width: 1500px;
}

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

h1, h2, h3 {
    color: var(--text);
    letter-spacing: -0.6px;
}

h1 {
    font-size: 2.15rem !important;
    font-weight: 800 !important;
}

h2 {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
}

p, label {
    color: #4f5570;
}

.hero {
    background: linear-gradient(120deg, #6254e8, #8878f4);
    color: white;
    border-radius: 20px;
    padding: 28px 30px;
    margin: 12px 0 25px;
    box-shadow: 0 10px 30px rgba(98, 84, 232, 0.13);
}

.hero h2 {
    color: white !important;
    font-size: 1.7rem !important;
    margin: 0 0 8px;
}

.hero p {
    color: #f0edff !important;
    margin-bottom: 0;
    line-height: 1.7;
}

.eyebrow {
    color: #e1dcff;
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
}

.section-label {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: 0 4px 18px rgba(30, 35, 90, 0.035);
}

.stButton > button {
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 1rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: var(--primary-dark);
    color: white;
    border: none;
    transform: translateY(-1px);
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox [data-baseweb="select"],
.stNumberInput input {
    border-radius: 10px;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: var(--primary);
}

[data-testid="stChatMessage"] {
    background: white;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 15px;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] {
    border-color: #dedff0;
    border-radius: 14px;
}

.stProgress > div > div > div > div {
    background: var(--primary);
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid var(--border);
    padding: 18px;
    border-radius: 15px;
}

div[data-testid="stMetricLabel"] {
    color: var(--muted);
}

div[data-testid="stMetricValue"] {
    color: var(--text);
    font-weight: 800;
}

hr {
    border-color: var(--border);
}

.small-muted {
    color: var(--muted);
    font-size: 0.88rem;
}

@media (max-width: 768px) {
    .block-container {
        padding: 1rem 1rem 2rem;
    }

    h1 {
        font-size: 1.7rem !important;
    }

    .hero {
        padding: 22px;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------------
# INITIAL SESSION STATE
# -------------------------

defaults = {
    "messages": [],
    "study_plan": "",
    "goal_id": None,
    "student_name": "",
    "subject": "",
    "target": "",
    "level": "Beginner",
    "duration": 7,
    "plan_days": 0,
    "plan_goal_id": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -------------------------
# SIDEBAR
# -------------------------

with st.sidebar:

    st.markdown(
        "<h2 style='color:#6254e8;'>🎓 GoalTutor</h2>",
        unsafe_allow_html=True
    )

    st.caption("YOUR PERSONAL AI LEARNING SPACE")
    st.divider()

    st.markdown("### 📚 Learning goal")
    st.caption("Tell us what you want to master.")

    with st.form("goal_form"):

        student_name = st.text_input(
            "Your name",
            value=st.session_state.student_name,
            placeholder="e.g. Alex"
        )

        subject = st.text_input(
            "Subject",
            value=st.session_state.subject,
            placeholder="e.g. Digital Electronics"
        )

        target = st.text_area(
            "Learning goal",
            value=st.session_state.target,
            placeholder="What do you want to achieve?",
            height=110
        )

        duration = st.number_input(
            "Study duration (days)",
            min_value=1,
            max_value=30,
            value=int(st.session_state.duration)
        )

        level = st.selectbox(
            "Your current level",
            ["Beginner", "Intermediate", "Advanced"],
            index=[
                "Beginner",
                "Intermediate",
                "Advanced"
            ].index(st.session_state.level)
        )

        submitted = st.form_submit_button(
            "🎯 Set learning goal",
            use_container_width=True
        )

        if submitted:

            if not student_name.strip() or not subject.strip() or not target.strip():
                st.error("Please complete all fields.")

            else:
                new_goal_id = save_goal(
                    student_name.strip(),
                    subject.strip(),
                    target.strip(),
                    duration,
                    level
                )

                st.session_state.goal_id = new_goal_id
                st.session_state.student_name = student_name.strip()
                st.session_state.subject = subject.strip()
                st.session_state.target = target.strip()
                st.session_state.level = level
                st.session_state.duration = int(duration)

                # Reset data belonging to the previous goal
                st.session_state.messages = []
                st.session_state.study_plan = ""
                st.session_state.plan_days = 0
                st.session_state.plan_goal_id = None

                st.success("Your new learning goal is saved!")
                st.rerun()

    st.divider()

    st.markdown("#### 💡 Learning tip")
    st.info(
        "Small, consistent study sessions are often "
        "more effective than last-minute cramming."
    )

    st.markdown(
        "<p class='small-muted'>Built for curious minds. "
        "Powered by AI.</p>",
        unsafe_allow_html=True
    )


# -------------------------
# MAIN HEADER
# -------------------------

st.markdown(
    "<p class='section-label'>YOUR LEARNING DASHBOARD</p>",
    unsafe_allow_html=True
)

if st.session_state.goal_id is None:

    st.title("Learn with purpose. Grow every day.")

    st.markdown("""
    Welcome to **GoalTutor**, your personal AI-powered learning
    companion. Set a learning goal in the sidebar to get started.
    """)

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">YOUR NEXT CHAPTER STARTS HERE</div>
        <h2>Turn your goals into progress. ✨</h2>
        <p>
            Get personalized explanations, ask questions without
            hesitation, and follow a study plan designed around you.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("### 🤖 AI Tutor")
            st.write(
                "Understand difficult concepts with "
                "conversational, personalized explanations."
            )

    with col2:
        with st.container(border=True):
            st.markdown("### 📅 Study Planner")
            st.write(
                "Break your learning goal into manageable "
                "steps for each study day."
            )

    with col3:
        with st.container(border=True):
            st.markdown("### 🎯 Goal Focus")
            st.write(
                "Choose a subject, set a target, and "
                "keep your learning journey organized."
            )

    st.info("👈 Set your learning goal in the sidebar to begin.")

else:

    # -------------------------
    # ACTIVE GOAL DASHBOARD
    # -------------------------

    st.title(f"Welcome back, {st.session_state.student_name} 👋")

    st.markdown(
        "Ready to make progress on your learning journey?"
    )

    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">YOUR CURRENT LEARNING GOAL</div>
            <h2>{st.session_state.subject}</h2>
            <p>{st.session_state.target}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric("Study duration", f"{st.session_state.duration} days")

    with metric2:
        st.metric("Learning level", st.session_state.level)

    with metric3:
        st.metric("Tutor messages", len(st.session_state.messages))

    st.write("")

    tab1, tab2 = st.tabs(
        ["🤖  AI Tutor", "📅  Study Plan"]
    )

    # -------------------------
    # AI TUTOR
    # -------------------------

    with tab1:

        st.subheader("Your personal AI tutor")

        st.caption(
            f"Ask anything about {st.session_state.subject}. "
            "Learn at your own pace."
        )

        with st.container(border=True):

            if not st.session_state.messages:

                st.markdown("### 👋 Let's start learning!")

                st.write(
                    f"I'm here to help you achieve your goal: "
                    f"**{st.session_state.target}**"
                )

                st.markdown("**Try asking:**")

                suggestions = [
                    f"Teach me the basics of {st.session_state.subject}",
                    "Explain a difficult concept with an example",
                    "Give me practice questions"
                ]

                for suggestion in suggestions:
                    st.markdown(f"- {suggestion}")

            # Conversation history
            for message in st.session_state.messages:

                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        user_message = st.chat_input(
            "Ask your tutor anything..."
        )

        if user_message:

            st.session_state.messages.append({
                "role": "user",
                "content": user_message
            })

            with st.spinner("Your tutor is thinking..."):

                try:
                    response = tutor_chat(
                        st.session_state.student_name,
                        st.session_state.subject,
                        st.session_state.target,
                        "General",
                        0,
                        user_message
                    )

                    response = str(response)

                except Exception as e:
                    response = (
                        "Sorry, I couldn't generate a response. "
                        "Please check your tutor configuration "
                        "and try again."
                    )
                    st.error(f"Tutor error: {e}")

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            st.rerun()

    # -------------------------
    # STUDY PLAN
    # -------------------------

    with tab2:

        st.subheader("Your personalized study roadmap")

        st.caption(
            "Turn your learning goal into a clear, "
            "day-by-day plan."
        )

        col_plan, col_details = st.columns([2, 1])

        with col_plan:

            with st.container(border=True):

                st.markdown("### 🗓️ Your study journey")

                st.write(
                    f"**Subject:** {st.session_state.subject}"
                )

                st.write(
                    f"**Goal:** {st.session_state.target}"
                )

                st.write(
                    f"**Duration:** {st.session_state.duration} days"
                )

                generate = st.button(
                    "✨ Generate my study plan",
                    use_container_width=True
                )

                if generate:

                    with st.spinner("Building your study roadmap..."):

                        try:
                            plan = create_study_plan(
                                st.session_state.subject,
                                st.session_state.target,
                                st.session_state.duration,
                                st.session_state.level
                            )

                            st.session_state.study_plan = str(plan)
                            st.session_state.plan_days = (
                                st.session_state.duration
                            )
                            st.session_state.plan_goal_id = (
                                st.session_state.goal_id
                            )

                        except Exception as e:
                            st.error(
                                f"Unable to generate the study plan: {e}"
                            )

                if (
                    st.session_state.study_plan
                    and st.session_state.plan_goal_id
                    == st.session_state.goal_id
                ):
                    st.divider()
                    st.markdown(
                        st.session_state.study_plan
                    )

                    st.download_button(
                        "⬇️ Download study plan",
                        data=st.session_state.study_plan,
                        file_name="GoalTutor_Study_Plan.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

        with col_details:

            with st.container(border=True):

                st.markdown("### 🎯 Goal overview")

                st.markdown("**Current level**")
                st.write(st.session_state.level)

                st.divider()

                st.markdown("**Time available**")
                st.write(f"{st.session_state.duration} days")

                st.divider()

                st.markdown("**Subject**")
                st.write(st.session_state.subject)

                st.divider()

                st.markdown("**Study tip**")
                st.write(
                    "Review previous concepts before "
                    "moving on to a new topic."
                )


# -------------------------
# FOOTER
# -------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#858aa1;
                font-size:0.82rem; padding:10px 0;">
        🎓 GoalTutor · Learn with purpose, one day at a time.
    </div>
    """,
    unsafe_allow_html=True
)
