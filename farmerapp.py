import streamlit as st

# --- Must be the first Streamlit command ---
st.set_page_config(
    page_title="Mfugaji Kwanza - Login",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Initialize session states safely ---
if "language" not in st.session_state:
    st.session_state.language = "English"

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "landing"

if "run_redirect" not in st.session_state:
    st.session_state.run_redirect = False

# --- THE PERMANENT ERROR FIX: Switch page safely OUTSIDE of the forms ---
if st.session_state.run_redirect:
    st.session_state.run_redirect = False  # Reset flag
    st.switch_page("pages/1_Transactions.py")

# --- High-Quality White Broiler Background Image Link ---
broiler_bg_url = "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?q=80&w=1600&auto=format&fit=crop"

# --- Translation Dictionary ---
translations = {
    "English": {
        "subtitle": "Modern Solutions for Every Poultry Farmer",
        "heading_landing": "Unlock your farm's true profit potential",
        "subtext_landing": "Log in or sign up to get started",
        "login_btn": "Log In",
        "signup_btn": "Sign Up",
        "heading_login": "Welcome Back",
        "subtext_login": "Enter details to access transactions",
        "phone_label": "Phone Number or Email",
        "pass_label": "Password",
        "proceed_btn": "Proceed to Account",
        "back_btn": "← Back",
        "heading_signup": "Create Account",
        "subtext_signup": "Register your poultry farm profile",
        "name_label": "Full Farmer Name",
        "phone_signup_label": "Phone Number (For Payments)",
        "pass_signup_label": "Create Security Password",
        "complete_btn": "Complete Registration",
        "error_fields": "All fields are required.",
        "success_reg": "Account created successfully!"
    },
    "Swahili": {
        "subtitle": "Ufumbuzi wa Kisasa kwa Kila Mfugaji wa Kuku",
        "heading_landing": "Fungua uwezo halisi wa faida wa shamba lako",
        "subtext_landing": "Ingia au jisajili ili kuanza",
        "login_btn": "Ingia",
        "signup_btn": "Jisajili",
        "heading_login": "Karibu Tena",
        "subtext_login": "Ingiza maelezo ili kupata miamala",
        "phone_label": "Namba ya Simu au Barua Pepe",
        "pass_label": "Nenosiri",
        "proceed_btn": "Endelea kwenye Akaunti",
        "back_btn": "← Nyuma",
        "heading_signup": "Fungua Akaunti",
        "subtext_signup": "Sajili wasifu wa shamba lako la kuku",
        "name_label": "Jina Kamili la Mfugaji",
        "phone_signup_label": "Namba ya Simu (Kwa Ajili ya Malipo)",
        "pass_signup_label": "Weka Nenosiri la Usalama",
        "complete_btn": "Kamilisha Usajili",
        "error_fields": "Sehemu zote zinahitajika.",
        "success_reg": "Akaunti imefunguliwa kwa mafanikio!"
    }
}

lang = st.session_state.language
t = translations[lang]

# --- Frontend CSS Layout Engine ---
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{broiler_bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.5); z-index: 0;
    }}
    .brand-title {{
        position: absolute; top: 25px; left: 40px; text-align: left; color: #FFFFFF;
        font-family: 'Arial Black', sans-serif; font-weight: 900; font-size: 38px;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.8); z-index: 100;
    }}
    .stForm, div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: #FFFFFF !important; border-radius: 20px !important;
        padding: 40px !important; max-width: 480px !important; margin: auto !important;
        margin-top: 15vh !important; box-shadow: 0 15px 35px rgba(0,0,0,0.6) !important;
    }}
    /* ELECTRIC GREEN GLOWING BUTTONS */
    div.stButton > button {{
        background-color: #00E676 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 800 !important;
        box-shadow: 0 0 15px rgba(0, 230, 118, 0.6) !important;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        background-color: #00FF5E !important;
        box-shadow: 0 0 25px rgba(0, 230, 118, 0.9) !important;
        transform: scale(1.03);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- Render ---
st.markdown(f'<div class="brand-title">MFUGAJI KWANZA<div style="font-size:14px; font-weight:normal;">{t["subtitle"]}</div></div>', unsafe_allow_html=True)

_, center_col, _ = st.columns([1, 1.3, 1])
with center_col:
    if st.session_state.auth_mode == "landing":
        with st.form(key="landing_form"):
            st.markdown(f'<div style="text-align:center; font-size:24px; font-weight:bold;">{t["heading_landing"]}</div>', unsafe_allow_html=True)
            chosen_lang = st.selectbox("Language / Lugha", ["English", "Swahili"], index=0 if lang == "English" else 1)
            if chosen_lang != st.session_state.language:
                st.session_state.language = chosen_lang
                st.rerun()
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.form_submit_button(t["login_btn"], use_container_width=True):
                    st.session_state.auth_mode = "login"; st.rerun()
            with btn_col2:
                if st.form_submit_button(t["signup_btn"], use_container_width=True):
                    st.session_state.auth_mode = "signup"; st.rerun()
    elif st.session_state.auth_mode == "login":
        with st.form(key="login_form"):
            username = st.text_input(t["phone_label"])
            password = st.text_input(t["pass_label"], type="password")
            if st.form_submit_button(t["proceed_btn"], use_container_width=True):
                st.session_state.run_redirect = True; st.rerun()
    elif st.session_state.auth_mode == "signup":
        with st.form(key="signup_form"):
            st.text_input(t["name_label"])
            st.text_input(t["phone_signup_label"])
            st.text_input(t["pass_signup_label"], type="password")
            if st.form_submit_button(t["complete_btn"], use_container_width=True):
                st.session_state.run_redirect = True; st.rerun()
