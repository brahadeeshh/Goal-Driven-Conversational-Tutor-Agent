import streamlit as st
from database import create_tables, save_goal
from goal_manager import create_study_plan
from tutor import tutor_chat


# Create database tables
create_tables()


# Page configuration
st.set_page_config(
    page_title="GoalTutor",
    page_icon="🎓",
    layout="wide"
)


# Title
st.title("🎓 GoalTutor")
st.subheader("Your Goal-Driven Conversational Tutor")


# Sidebar
st.sidebar.header("📚 Learning Goal")

student_name = st.sidebar.text_input(
    "Your Name",
    placeholder="Enter your name"
)

subject = st.sidebar.text_input(
    "Subject",
    placeholder="Example: Digital Electronics"
)

target = st.sidebar.text_area(
    "Learning Goal",
    placeholder="Example: Understand digital logic and solve problems"
)

duration = st.sidebar.number_input(
    "Study Duration (days)",
    min_value=1,
    max_value=30,
    value=7
)

level = st.sidebar.selectbox(
    "Your Level",
    ["Beginner", "Intermediate", "Advanced"]
)


# Save goal
if st.sidebar.button("🎯 Set Goal"):

    if not student_name or not subject or not target:
        st.sidebar.error("Please fill in all fields.")

    else:
        goal_id = save_goal(
            student_name,
            subject,
            target,
            duration,
            level
        )

        st.session_state.goal_id = goal_id
        st.session_state.student_name = student_name
        st.session_state.subject = subject
        st.session_state.target = target
        st.session_state.level = level

        st.session_state.messages = []

        st.sidebar.success("Goal saved successfully! 🎉")


# Main application
if "goal_id" not in st.session_state:

    st.info(
        "👈 Enter your learning goal in the sidebar "
        "and click **Set Goal** to begin."
    )

else:

    st.success(
        f"🎯 Goal: {st.session_state.target}"
    )

    # Tabs
    tab1, tab2 = st.tabs(
        ["🤖 AI Tutor", "📅 Study Plan"]
    )


    # -------------------------
    # AI Tutor
    # -------------------------

    with tab1:

        st.header("🤖 Talk to Your Tutor")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display previous messages
        for message in st.session_state.messages:

            with st.chat_message(message["role"]):
                st.write(message["content"])


        # Chat input
        user_message = st.chat_input(
            "Ask your tutor something..."
        )


        if user_message:

            # Show user message
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_message
                }
            )

            with st.chat_message("user"):
                st.write(user_message)


            # Get AI response
            with st.chat_message("assistant"):

                with st.spinner("Tutor is thinking..."):

                    response = tutor_chat(
                        st.session_state.student_name,
                        st.session_state.subject,
                        st.session_state.target,
                        "General",
                        0,
                        user_message
                    )

                st.write(response)


            # Save assistant response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )


    # -------------------------
    # Study Plan
    # -------------------------

    with tab2:

        st.header("📅 Personalized Study Plan")

        if st.button("✨ Generate Study Plan"):

            with st.spinner("Creating your study plan..."):

                plan = create_study_plan(
                    st.session_state.subject,
                    st.session_state.target,
                    duration,
                    st.session_state.level
                )

            st.session_state.study_plan = plan


        if "study_plan" in st.session_state:

            st.markdown(
                st.session_state.study_plan
            )