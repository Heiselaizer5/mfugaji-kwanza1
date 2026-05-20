import streamlit as st

# Page Config
st.set_page_config(page_title="Mfugaji Kwanza Dashboard", layout="wide")

# CSS ya Kadi za Electric Green
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    /* Style ya Kadi na border ya kijani */
    .custom-card { 
        background-color: #1E2530; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #00E676; 
        margin-bottom: 20px;
    }
    .card-title { color: #888; font-size: 14px; text-transform: uppercase; }
    .card-value { color: white; font-size: 24px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("Dashibodi ya Shamba")

# Row 1: Kadi tatu za taarifa muhimu
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="custom-card">
            <div class="card-title">Idadi ya Kuku</div>
            <div class="card-value">1,250</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="custom-card">
            <div class="card-title">Mauzo ya Leo</div>
            <div class="card-value">TZS 450,000</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="custom-card">
            <div class="card-title">Gharama za Chakula</div>
            <div class="card-value">TZS 120,000</div>
        </div>
    """, unsafe_allow_html=True)

# Row 2: Sehemu ya vitendo
st.subheader("Hatua za Kufanya")
if st.button("🚀 Ongeza Mauzo Mapya"):
    st.write("Fomu ya mauzo itafunguka hapa...")
