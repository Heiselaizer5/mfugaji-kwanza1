import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Mfugaji Kwanza - Login",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Initialize Session States (Kusawazisha na ukurasa wa pili) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "language" not in st.session_state:
    st.session_state.language = "Swahili"

# Kuhakikisha Database ipo tayari tangu mwanzo kabisa hapa login
if "farm_database" not in st.session_state:
    st.session_state.farm_database = {}

# --- Background Image ---
broiler_bg_url = "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?q=80&w=1600&auto=format&fit=crop"

# --- Kamusi ya Lugha ya Login ---
translations = {
    "English": {
        "title": "MFUGAJI KWANZA",
        "subtitle": "Modern Poultry Management System",
        "login_header": "🔒 Account Login",
        "username": "Username or Phone Number",
        "password": "Password",
        "login_btn": "Sign In Securely 🚀",
        "error_msg": "❌ Invalid Username or Password. Please try again.",
        "success_msg": "🎉 Login Successful! Redirecting to Dashboard..."
    },
    "Swahili": {
        "title": "MFUGAJI KWANZA",
        "subtitle": "Mfumo wa Kisasa wa Usimamizi wa Kuku",
        "login_header": "🔒 Ingia Kwenye Akaunti",
        "username": "Jina la Mtumiaji / Namba ya Simu",
        "password": "Neno la Siri (Password)",
        "login_btn": "Ingia Sasa 🚀",
        "error_msg": "❌ Jina au neno la siri sio sahihi. Jaribu tena.",
        "success_msg": "🎉 Umefanikiwa kuingia! Unapelekwa kwenye Dashibodi..."
    }
}

lang = st.session_state.language
t = translations[lang]

# --- CSS Styling (PREMIUM DARK LOGIN BOARD + WHITE INPUTS + STABLE) ---
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{broiler_bg_url}");
        background-size: cover; background-position: center;
        background-repeat: no-repeat; background-attachment: fixed;
    }}
    .stApp::before {{
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.7); z-index: 0;
    }}
    [data-testid="stHeader"] {{ background-color: transparent !important; z-index: 10; }}
    .main .block-container {{ z-index: 1; padding-top: 3rem !important; }}

    .brand-container {{ text-align: center; margin-bottom: 20px; }}
    .brand-title {{
        color: #FFFFFF; font-family: 'Arial Black', sans-serif; font-weight: 900;
        font-size: 45px; letter-spacing: 3px; text-shadow: 3px 3px 8px rgba(0,0,0,0.9);
        margin: 0;
    }}
    .brand-subtitle {{ font-size: 16px; font-family: Arial, sans-serif; color: #00E676; font-weight: 600; }}

    /* Bodi ya Login kuwa Nyeusi ya Kishindo kufanana na kadi za ndani */
    [data-testid="stForm"], .stForm {{
        background-color: #1A1A1A !important; 
        border: 2px solid #2D2D2D !important;
        border-radius: 20px !important;
        padding: 40px !important; 
        box-shadow: 0 15px 40px rgba(0,0,0,0.8) !important;
        max-width: 500px;
        margin: 0 auto;
    }}

    /* Labels nyeupe safi */
    label[data-testid="stWidgetLabel"] p {{ 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
        font-size: 15px !important; 
    }}

    /* Sehemu za kuandikia (Inputs) kuwa Nyeupe Safi na Maandishi Meusi ili kutocheza */
    input {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        height: 45px !important;
    }}

    /* Electric Green Login Button */
    div.stButton > button {{
        background-color: #00E676 !important; color: #000000 !important;          
        border-radius: 12px !important; border: none !important;
        padding: 14px 24px !important; font-size: 16px !important; font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(0, 230, 118, 0.4) !important; 
        transition: all 0.2s ease-in-out; width: 100%;
        margin-top: 10px;
    }}
    div.stButton > button:hover {{
        background-color: #00C853 !important; 
        box-shadow: 0 6px 20px rgba(0, 230, 118, 0.6) !important; 
        transform: scale(1.02);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- Header & Language Switcher ---
_, lang_col = st.columns([4, 1])
with lang_col:
    chosen_lang = st.selectbox("", ["Swahili", "English"], index=0 if lang == "Swahili" else 1, key="login_lang_select")
    if chosen_lang != st.session_state.language:
        st.session_state.language = chosen_lang
        st.rerun()

# --- Brand Logo Area ---
st.markdown(f"""
<div class="brand-container">
    <div class="brand-title">{t['title']}</div>
    <div class="brand-subtitle">{t['subtitle']}</div>
</div>
""", unsafe_allow_html=True)

# --- Login Form Container ---
if not st.session_state.logged_in:
    with st.form(key="login_secure_form"):
        st.markdown(f'<h3 style="color:#00E676; margin-top:0; font-weight:800; text-align:center;">{t["login_header"]}</h3>', unsafe_allow_html=True)
        st.write("<hr style='border-color: #333; margin-bottom:20px;'>", unsafe_allow_html=True)
        
        user_input = st.text_input(t["username"], placeholder="admin / 0712345678")
        pass_input = st.text_input(t["password"], type="password", placeholder="••••••••")
        
        submit_login = st.form_submit_button(t["login_btn"])
        
        if submit_login:
            # Hapa unaweza kuweka username na password unazozitaka wewe, kwa sasa nimeweka 'admin' na 'admin123'
            if user_input.strip() == "admin" and pass_input == "admin123":
                st.session_state.logged_in = True
                st.success(t["success_msg"])
                st.rerun()
            else:
                st.error(t["error_msg"])
else:
    # Kama tayari alishaingia (is logged in), mtunzie ujumbe mzuri na umruhusu kwenda kurasa za pembeni
    st.markdown(f"""
    <div style="background-color: #1A1A1A; border: 2px solid #2D2D2D; border-radius: 15px; padding: 30px; text-align: center; max-width: 500px; margin: 0 auto;">
        <h3 style="color: #00E676;">🔓 Tayari Umeingia Kazini!</h3>
        <p style="color: white;">Tafadhali tumia menu ya pembeni (Sidebar) kwenda kwenye ukurasa wa <b>Transactions</b> kuanza kurekodi.</p>
    </div>
    """, unsafe_allow_html=True)