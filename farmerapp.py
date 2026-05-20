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
    /* Full-screen layout background */
    .stApp {{
        background-image: url("{broiler_bg_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* Dark overlay over background image */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 0;
    }}

    /* Transparent top app bar */
    [data-testid="stHeader"] {{
        background-color: transparent !important;
        z-index: 10;
    }}

    .main .block-container {{
        z-index: 1;
        padding-top: 3rem !important;
    }}

    /* Top-Left Title "MFUGAJI KWANZA" */
    .brand-title {{
        position: absolute;
        top: 25px;
        left: 40px;
        text-align: left;
        color: #FFFFFF;
        font-family: 'Arial Black', Gadget, sans-serif;
        font-weight: 900;
        font-size: 38px;
        letter-spacing: 2px;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.8);
        z-index: 100;
    }}
    
    .brand-subtitle {{
        font-size: 14px;
        font-family: Arial, sans-serif;
        font-weight: normal;
        color: #F0F0F0;
        display: block;
        margin-top: -5px;
    }}

    /* SOLID PURE WHITE CARD CONTAINER BOX */
    .stForm, div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: #FFFFFF !important;
        border: none !important;
        border-radius: 20px !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6) !important;
        padding: 40px !important;
        max-width: 480px !important;
        margin: auto !important;
        margin-top: 15vh !important;
    }}

    /* PREMIUM DARK GREEN HEDINGS */
    .green-heading {{
        color: #16300B !important;
        font-weight: 800 !important;
        font-size: 26px !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        text-align: center !important;
        margin-bottom: 8px !important;
        line-height: 1.3 !important;
    }}
    
    .card-subtext {{
        color: #555555 !important;
        font-size: 15px !important;
        text-align: center !important;
        margin-bottom: 20px !important;
        font-family: 'Segoe UI', Arial, sans-serif !important;
    }}

    /* HIGH LEGIBILITY INPUT LABELS (Dark Forest Green) */
    label[data-testid="stWidgetLabel"] p {{
        color: #16300B !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }}

    /* VIBRANT ELECTRIC GREEN BUTTONS (Matching your screenshot sample) */
    div.stButton > button {{
        background-color: #00E676 !important; /* Vivid Electric Green */
        color: #000000 !important;          /* Sharp Black Text */
        border-radius: 12px !important;       /* Clean rounded edges */
        border: none !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(0, 230, 118, 0.3) !important;
        transition: all 0.2s ease-in-out;
    }}
    
    div.stButton > button:hover {{
        background-color: #00C853 !important; /* Slightly deeper green on hover */
        box-shadow: 0 6px 16px rgba(0, 230, 118, 0.5) !important;
        transform: scale(1.02);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- Render Elements ---

# 1. Brand Logo on Top LEFT
st.markdown(f"""
    <div class="brand-title">
        MFUGAJI KWANZA
        <span class="brand-subtitle">{t['subtitle']}</span>
    </div>
""", unsafe_allow_html=True)

# 2. Central Layout Core Router
_, center_col, _ = st.columns([1, 1.3, 1])

with center_col:
    
    # CASE A: LANDING SCREEN
    if st.session_state.auth_mode == "landing":
        with st.form(key="landing_form"):
            st.markdown(f'<div class="green-heading">{t["heading_landing"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-subtext">{t["subtext_landing"]}</div>', unsafe_allow_html=True)
            
            chosen_lang = st.selectbox("Language / Lugha", ["English", "Swahili"], index=0 if lang == "English" else 1)
            if chosen_lang != st.session_state.language:
                st.session_state.language = chosen_lang
                st.rerun()
                
            st.write("") 

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.form_submit_button(t["login_btn"], use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()
            with btn_col2:
                if st.form_submit_button(t["signup_btn"], use_container_width=True):
                    st.session_state.auth_mode = "signup"
                    st.rerun()

    # CASE B: LOGIN INPUT SCREEN
    elif st.session_state.auth_mode == "login":
        with st.form(key="login_form"):
            st.markdown(f'<div class="green-heading">{t["heading_login"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-subtext">{t["subtext_login"]}</div>', unsafe_allow_html=True)
            
            username = st.text_input(t["phone_label"])
            password = st.text_input(t["pass_label"], type="password")
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.form_submit_button(t["proceed_btn"], use_container_width=True):
                    if username and password:
                        # Set flag and rerun so the safe switch outside the form block catches it!
                        st.session_state.run_redirect = True
                        st.rerun()
                    else:
                        st.error(t["error_fields"])
            with btn_col2:
                if st.form_submit_button(t["back_btn"], use_container_width=True):
                    st.session_state.auth_mode = "landing"
                    st.rerun()

    # CASE C: SIGN UP INPUT SCREEN
    elif st.session_state.auth_mode == "signup":
        with st.form(key="signup_capture_form"):
            st.markdown(f'<div class="green-heading">{t["heading_signup"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-subtext">{t["subtext_signup"]}</div>', unsafe_allow_html=True)
            
            new_name = st.text_input(t["name_label"])
            new_phone = st.text_input(t["phone_signup_label"])
            new_pass = st.text_input(t["pass_signup_label"], type="password")
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.form_submit_button(t["complete_btn"], use_container_width=True):
                    if new_name and new_phone and new_pass:
                        st.session_state.run_redirect = True
                        st.rerun()
                    else:
                        st.error(t["error_fields"])
            with btn_col2:
                if st.form_submit_button(t["back_btn"], use_container_width=True):
                    st.session_state.auth_mode = "landing"
                    st.rerun()