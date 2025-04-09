# Page title + instructions
import streamlit as st
from src.summary_client import AISummary
import openai
from dotenv import load_dotenv
import os 

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set up OpenAI client
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
ai_summariser = AISummary(client=openai_client, model="gpt-4o")
st.markdown("""
<style>
/* Simulated Checkatrade-style navbar */
.checka-header {
    background-color: #ffffff;
    border-bottom: 3px solid #0072ce;
    padding: 0.75rem 1.5rem;
    font-family: Helvetica, sans-serif;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.checka-header .logo {
    font-weight: bold;
    font-size: 1.4rem;
    color: #cc0000;
}

.checka-header .logo span {
    color: #0072ce;
}

.checka-header .nav-links {
    display: flex;
    gap: 1.5rem;
    font-size: 0.9rem;
}

.checka-header .nav-links a {
    color: #333333;
    text-decoration: none;
}

.checka-header .cta {
    background-color: #cc0000;
    color: white;
    padding: 0.5rem 1rem;
    font-weight: bold;
    border-radius: 4px;
    text-decoration: none;
}
</style>

<div class="checka-header">
    <div class="logo">Check<span>a</span>trade</div>
    <div class="nav-links">
        <a href="#">Homeowner</a>
        <a href="#">Trades</a>
        <a href="#">Blog</a>
    </div>
    <a href="#" class="cta">Trade sign up</a>
</div>
""", unsafe_allow_html=True)

# st.set_page_config(page_title="Checkatrade Profile Help", page_icon="🧰", layout="centered")

st.title("🔁 Revise Your Checkatrade Profile")
st.markdown("Paste your current draft below and tell us what you’d like to change.")

# Input fields
original_profile = st.text_area("📄 Paste your existing profile here")
revision_request = st.text_area("📝 What needs changing? (e.g. update location, tone too formal, add more services)")

# Submit
if st.button("♻️ Revise Profile"):
    system_prompt = """You are a helpful assistant that revises Checkatrade profile descriptions.
Maintain the same structure and tone unless otherwise instructed.
Keep it warm, clear, and professional. Apply the requested changes carefully."""

    user_message = f"""
    Original profile:
    {original_profile}

    Requested changes:
    {revision_request}
    """

    response = ai_summariser.get_response(user_message=user_message, system_prompt=system_prompt)

    st.markdown("### ✍️ Revised Profile")
    st.success("Here’s your updated profile based on the requested changes:")
    st.markdown(response)
