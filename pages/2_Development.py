import streamlit as st

st.set_page_config(page_title="Maendeleo - Mfugaji Kwanza", page_icon="📈")

st.title("📈 Ukurasa wa Maendeleo (Development)")
st.write("Hapa utaona ripoti na takwimu za ukuaji wa kuku wako.")

if st.button("← Rudi Nyuma"):
    st.switch_page("farmerapp.py")
