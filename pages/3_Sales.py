import streamlit as st

st.set_page_config(page_title="Mauzo - Mfugaji Kwanza", page_icon="🐔")

st.title("🐔 Ukurasa wa Mauzo (Sales)")
st.write("Sehemu ya kuingiza na kufuatilia mauzo ya kuku")

if st.button("← Rudi Nyuma"):
    st.switch_page("farmerapp.py")
