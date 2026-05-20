import streamlit as st

# Page Configuration
st.set_page_config(page_title="Mfugaji Kwanza", layout="wide")

# CSS ya Electric Green na boksi jeupe (White Board)
st.markdown("""
    <style>
    .stApp { 
        background: url("https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?q=80&w=1600"); 
        background-size: cover; 
    }
    /* Boksi jeupe la kati */
    .white-board { 
        background: white; 
        padding: 40px; 
        border-radius: 20px; 
        max-width: 600px; 
        margin: auto; 
        text-align: center;
        color: black;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    /* Electric Green Buttons */
    div.stButton > button { 
        background-color: #00E676 !important; 
        color: black !important; 
        font-weight: bold; 
        border-radius: 8px; 
        width: 100%; 
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# Main UI - Kila kitu kipo ndani ya 'white-board' div
st.markdown('<div class="white-board">', unsafe_allow_html=True)

st.title("MFUGAJI KWANZA")
st.markdown("**Unlock your farm's true profit potential**")
st.write("Log in or sign up to get started")

# Hizi zote zitakaa ndani ya boksi jeupe
st.selectbox("Language / Lugha", ["English", "Swahili"])

col1, col2 = st.columns(2)
with col1:
    st.button("Log In")
with col2:
    st.button("Sign Up")

st.markdown('</div>', unsafe_allow_html=True)
