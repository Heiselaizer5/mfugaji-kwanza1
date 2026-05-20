import streamlit as st

st.set_page_config(page_title="Mfugaji Kwanza", layout="wide")

# CSS ya kuweka background na rangi ya vitufe
st.markdown("""
    <style>
    .stApp { background: url("https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?q=80&w=1600"); background-size: cover; }
    div.stButton > button { background-color: #00E676 !important; color: black !important; font-weight: bold; border-radius: 8px; width: 100%; border: none; }
    </style>
""", unsafe_allow_html=True)

# Tunatumia column za pembeni (1, 2, 1) ili kupata boksi katikati
_, col_center, _ = st.columns([1, 2, 1])

with col_center:
    # Hii ndio "White Board" inayojenga boksi lenyewe
    with st.container(border=True):
        st.markdown("<h1 style='text-align: center;'>MFUGAJI KWANZA</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><b>Unlock your farm's true profit potential</b></p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Log in or sign up to get started</p>", unsafe_allow_html=True)
        
        # Punguza size ya translator kwa kuiweka kwenye column ndogo
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.selectbox("Language / Lugha", ["English", "Swahili"])
        
        # Vitufe
        b1, b2 = st.columns(2)
        with b1:
            st.button("Log In")
        with b2:
            st.button("Sign Up")
