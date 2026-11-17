import streamlit as st
import requests

st.set_page_config(
    page_title="TN Government Schemes AI Assistant", 
    page_icon="🌿", 
    layout="centered"
)

# Custom CSS for Framer-like Green Aesthetic with Agricultural Banner & Background Imagery
st.markdown("""
<style>
    /* Main app background with a lush agricultural landscape and a dark green overlay */
    .stApp {
        background: linear-gradient(rgba(27, 67, 50, 0.88), rgba(45, 106, 79, 0.92)), 
                    url('https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sleek Framer-style Hero Banner Card with Farmer & Agriculture Imagery */
    .hero-card {
        background: linear-gradient(rgba(27, 67, 50, 0.78), rgba(45, 106, 79, 0.85)), 
                    url('https://images.unsplash.com/photo-1595974482597-4f6c4f0b3554?auto=format&fit=crop&w=1000&q=80');
        background-size: cover;
        background-position: center;
        padding: 40px 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.35);
        border: 1px solid rgba(82, 183, 136, 0.4);
    }
    .hero-card h1 {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 0 2px 5px rgba(0,0,0,0.4);
    }
    .hero-card p {
        color: #E2F0D9;
        font-size: 16px;
        margin: 0;
        font-weight: 500;
        text-shadow: 0 1px 3px rgba(0,0,0,0.4);
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(233, 245, 237, 0.95);
        border-right: 1px solid #D0E8D6;
    }

    /* Chat input rounded modern border */
    .stChatInputContainer input {
        border-radius: 14px !important;
        border: 2px solid #52B788 !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
    }
    
    /* Chat message bubble styling */
    .stChatMessage {
        border-radius: 14px;
        padding: 12px;
        background-color: rgba(255, 255, 255, 0.92) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Language & Controls
with st.sidebar:
    st.markdown("### ⚙️ Settings / அமைப்புகள்")
    lang = st.selectbox("Select Language / மொழியைத் தேர்ந்தெடுக்கவும்", ["English", "Tamil"])
    st.markdown("---")
    st.markdown("🌱 **TN Schemes Assistant**\nPowered by Neo4j & OpenAI GraphRAG.")
    st.markdown("Empowering farmers, women, and students with welfare schemes.")

# Hero Header Banner with Farmer/Agricultural Imagery
if lang == "English":
    st.markdown("""
    <div class="hero-card">
        <h1>🌿 Tamil Nadu Government Schemes AI Assistant</h1>
        <p>Your intelligent guide to welfare schemes, agricultural support, and financial aids.</p>
    </div>
    """, unsafe_allow_html=True)
    input_placeholder = "Ask about schemes (e.g., educational grants, farmer welfare, women assistance)..."
else:
    st.markdown("""
    <div class="hero-card">
        <h1>🌿 தமிழ்நாடு அரசுத் திட்டங்கள் AI உதவியாளர்</h1>
        <p>அரசு நலத்திட்டங்கள், விவசாய ஆதரவு மற்றும் நிதியுதவி பற்றிய உங்கள் வழிகாட்டி.</p>
    </div>
    """, unsafe_allow_html=True)
    input_placeholder = "திட்டங்கள் பற்றி கேளுங்கள் (எ.கா., கல்வி உதவித்தொகை, விவசாயிகள்)..."

# Chat Session Management
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(input_placeholder):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching Knowledge Graph... / அறிவுரைக் களஞ்சியத்தைத் தேடுகிறது..."):
            try:
                lang_code = "ta" if lang == "Tamil" else "en"
                res = requests.post(
                    "http://localhost:8000/chat", 
                    json={"query": prompt, "language": lang_code}
                )
                if res.status_code == 200:
                    answer = res.json().get("response", "No response received.")
                else:
                    answer = "Backend server error."
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Connection error: {e}")