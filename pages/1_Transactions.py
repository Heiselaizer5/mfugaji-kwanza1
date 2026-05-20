import streamlit as st

st.set_page_config(page_title="Miamala - Mfugaji Kwanza", page_icon="💰")

st.title("💰 Ukurasa wa Miamala (Transactions)")
st.write("Karibu kwenye sehemu ya kusimamia miamala yako ya shamba.")

# Kitufe cha kurudi nyuma kwenye Login
if st.button("← Rudi Nyuma"):
    st.switch_page("farmerapp.py")
