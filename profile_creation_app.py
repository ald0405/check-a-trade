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

# st.title("Generate Your Checkatrade Profile")

# Custom CSS to match Checkatrade style
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: "Helvetica", sans-serif;
    }
    h1 {
        color: #cc0000;
    }
    h3 {
        color: #003057;
    }
    .stTextInput > label, .stTextArea > label {
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🧰 Create Your Checkatrade Profile")

st.markdown("Welcome! Let’s build a strong, customer-friendly profile that makes a great first impression.")

# Step 1: About
st.markdown("### 📍 Step 1: About Your Business")
trade = st.text_input(label = "🔧 What’s your trade? (e.g. plumber, electrician)",value = 'I am an electrician')
location = st.text_input("🌍 Where are you based and what areas do you cover?",value = "I cover South London and Kent")
business_intro = st.text_area("📣 Tell us about your business in 1-2 sentences.")

# Step 2: Story & Values
st.markdown("### 🧱 Step 2: Your Story & Values")
story = st.text_area("📘 How did you get started? What are your values?")

# Step 3: Experience
st.markdown("### 🏗 Step 3: Experience & Qualifications")
experience = st.text_input("🛠 How many years of experience do you have?")
qualifications = st.text_area("🎓 List any qualifications, accreditations or memberships.")

# Step 4: Services
st.markdown("### 🔨 Step 4: Services")
services = st.text_area("🧾 List the services you offer (one per line).")
extra_value = st.text_area("💡 Any added value? (e.g. free quotes, flexible hours)")

# Step 5: Work Highlights
st.markdown("### 📸 Step 5: Highlight Your Work")
example_job = st.text_area("🛠 Describe a recent job you're proud of.")
review_quote = st.text_input("🗣 Add a customer quote or review (optional).")

# Step 6: SEO
st.markdown("### 🔍 Step 6: SEO Keywords")
keywords = st.text_input("💬 What keywords should be included? (e.g. boiler repair in Leeds)")

# Submit
if st.button("🚀 Generate Profile"):
    system_prompt = """You are an assistant that writes friendly, effective Checkatrade profile descriptions for tradespeople. 
Follow this structure:
1. A warm intro that says what they do and where.
2. A brief story of how they got started and their values.
3. Experience and qualifications.
4. A bullet list of services.
5. Any extras or added value.
6. A recent job or happy customer quote.
7. SEO-friendly keywords subtly included.
The tone should be professional but warm and clear."""

    user_message = f"""
    Trade: {trade}
    Location: {location}
    Intro: {business_intro}
    Story/Values: {story}
    Experience: {experience}
    Qualifications: {qualifications}
    Services: {services}
    Added Value: {extra_value}
    Example Job: {example_job}
    Review Quote: {review_quote}
    Keywords: {keywords}
    """

    with st.spinner("Generating your profile..."):
        response = ai_summariser.get_response(user_message=user_message, system_prompt=system_prompt)

    st.markdown("### ✍️ Your Draft Profile")
    st.success("Here’s your draft profile. Feel free to copy it, edit it, or ask the assistant to revise it.")
    st.markdown(response)