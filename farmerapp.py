import streamlit as st

st.set_page_config(page_title="Mfugaji Kwanza", layout="wide")

# CSS ya kulazimisha boksi kuwa jeupe na vitufe kuwa Electric Green
st.markdown("""
    <style>
    .stApp { background: url("https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?q=80&w=1600"); background-size: cover; }
    
    /* Kulazimisha kontena liwe jeupe */
    .white-box {
        background-color: white !important;
        padding: 40px;
        border-radius: 20px;
        color: black !important;
    }
    
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

# Layout: Boksi katikati
_, col_center, _ = st.columns([1.5, 2, 1.5])

with col_center:
    # Hapa tunatumia div ya HTML iliyo na CSS class ya 'white-box'
    st.markdown('<div class="white-box">', unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: black;'>MFUGAJI KWANZA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: black;'><b>Unlock your farm's true profit potential</b></p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: black;'>Log in or sign up to get started</p>", unsafe_allow_html=True)
    
    # Translator kwenye column ndogo ili ipungue size
    l1, l2, l3 = st.columns([1, 2, 1])
    with l2:
        st.selectbox("Language / Lugha", ["English", "Swahili"])
    
    # Vitufe
    b1, b2 = st.columns(2)
    with b1:
        st.button("Log In")
    with b2:
        st.button("Sign Up")
        
    st.markdown('</div>', unsafe_allow_html=True)
