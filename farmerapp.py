import streamlit as st

# Page Config
st.set_page_config(page_title="Mfugaji Kwanza", layout="wide")

# CSS ya kusimamia muonekano wa boksi
st.markdown("""
    <style>
    .stApp { background: url("https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?q=80&w=1600"); background-size: cover; }
    /* Hii inafanya boksi letu lionekane vizuri */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    div.stButton > button { 
        background-color: #00E676 !important; 
        color: black !important; 
        font-weight: bold; 
        border-radius: 8px; 
        width: 100%; 
    }
    </style>
""", unsafe_allow_html=True)

# Container kuu inayoshikilia kila kitu ndani ya boksi
with st.container():
    st.title("MFUGAJI KWANZA")
    st.markdown("**Unlock your farm's true profit potential**")
    st.write("Log in or sign up to get started")
    
    st.selectbox("Language / Lugha", ["English", "Swahili"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("Log In")
    with col2:
        st.button("Sign Up")
