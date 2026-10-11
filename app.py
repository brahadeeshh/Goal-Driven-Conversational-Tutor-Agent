
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --purple: #6c5ce7;
    --purple-hover: #5847d8;
    --background: #f7f7fc;
    --text: #252541;
    --muted: #85859d;
    --border: #ececf5;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--background);
}

.block-container {
    max-width: 1450px;
    padding: 2.5rem 3rem;
}

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1rem;
}

h1, h2, h3 {
    color: var(--text);
    letter-spacing: -0.5px;
}

h1 {
    font-size: 2.25rem !important;
    font-weight: 800 !important;
}

h2 {
    font-weight: 700 !important;
}

p {
    line-height: 1.7;
}

.stButton > button,
.stFormSubmitButton > button {
    background: var(--purple);
    color: white;
    border: none;
    border-radius: 11px;
    min-height: 44px;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: var(--purple-hover);
    color: white;
    border: none;
    transform: translateY(-1px);
}

.stTextInput input,
.stTextArea textarea {
    border-radius: 10px;
    border: 1px solid var(--border);
    background: #ffffff;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 8px;
    box-shadow: 0 5px 22px rgba(45, 40, 100, 0.035);
}

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px;
}

[data-testid="stMetricValue"] {
    color: var(--purple);
    font-weight: 800;
}

[data-testid="stChatMessage"] {
    background: white;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 14px;
}

[data-testid="stChatInput"] {
    border-radius: 14px;
    background: white;
}

.stProgress > div > div > div > div {
    background: var(--purple);
}

.hero-card {
    background: linear-gradient(120deg, #6c5ce7, #9b8afc);
    color: white;
    padding: 30px;
    border-radius: 22px;
    margin: 20px 0;
    box-shadow: 0 12px 28px rgba(108, 92, 231, 0.16);
}

.hero-card h2 {
    color: white !important;
    font-size: 1.8rem !important;
}

.hero-card p {
    color: #f2efff !important;
}

.eyebrow {
    color: #e9e3ff;
    text-transform: uppercase;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1.5px;
}

.muted {
    color: var(--muted);
    font-size: 0.9rem;
}

@media (max-width: 768px) {
    .block-container {
        padding: 1.2rem 1rem;
    }

    h1 {
        font-size: 1.7rem !important;
    }

    .hero-card {
        padding: 22px;
    }
}
</style>
""", unsafe_allow_html=True)
