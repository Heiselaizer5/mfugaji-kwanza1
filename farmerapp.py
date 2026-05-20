import streamlit as st

# Page Config
st.set_page_config(page_title="Mfugaji Kwanza", layout="wide")

# CSS ya Electric Green na Layout safi
st.markdown("""
    <style>
    .stApp { background: url("https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?q=80&w=1600"); background-size: cover; }
    .white-board { background: white; padding: 40px; border-radius: 20px; color: black; box-shadow: 0 4px 15px rgba(0,0,0,0.3); max-width: 500px; margin: auto; text-align: center; }
    /* Electric Green Buttons */
    div.stButton > button { background-color: #00FF00 !important; color: black !important; font-weight: bold; border-radius: 8px; width: 100%; border: none; }
    div.stButton > button:hover { background-color: #00CC00 !important; }
    </style>
""", unsafe_allow_html=True)

# Main UI
st.markdown('<div class="white-board">', unsafe_allow_html=True)
st.title("MFUGAJI KWANZA")
st.markdown("### Unlock your farm's true profit potential")
st.write("Log in or sign up to get started")

st.selectbox("Language / Lugha", ["English", "Swahili"])

# Vitufe kukaa sambamba
col1, col2 = st.columns(2)
with col1:
    st.button("Log In")
with col2:
    st.button("Sign Up")

st.markdown('</div>', unsafe_allow_html=True)
