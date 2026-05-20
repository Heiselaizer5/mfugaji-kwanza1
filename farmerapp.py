import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Mfugeji Kwanza - Transactions",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Initialize Language Session State ---
if "language" not in st.session_state:
    st.session_state.language = "English"

# --- High-Quality White Broiler Background ---
broiler_bg_url = "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?q=80&w=1600&auto=format&fit=crop"

# --- Translations Dictionary for Transactions ---
translations = {
    "English": {
        "subtitle": "Modern Solutions for Every Poultry Farmer",
        "welcome": "Welcome back, Farmer!",
        "instruction": "What transaction would you like to perform today?",
        "choice_inputs": "🛒 Farm Inputs",
        "choice_withdraw": "💰 Withdraw Funds",
        "desc_inputs": "Purchase feeds, vaccines, and equipment directly for your flock.",
        "desc_withdraw": "Transfer your poultry sale earnings straight to your mobile wallet.",
        "selected_msg": "You selected:"
    },
    "Swahili": {
        "subtitle": "Ufumbuzi wa Kisasa kwa Kila Mfugaji wa Kuku",
        "welcome": "Karibu tena, Mfugaji!",
        "instruction": "Je, ungependa kufanya muamala gani leo?",
        "choice_inputs": "🛒 Pembejeo za Shamba",
        "choice_withdraw": "💰 Kutoa Fedha",
        "desc_inputs": "Nunua vyakula, chanjo, na vifaa moja kwa moja kwa ajili ya kuku wako.",
        "desc_withdraw": "Hamisha mapato ya mauzo ya kuku moja kwa moja kwenda kwenye pochi yako ya simu.",
        "selected_msg": "Umechagua:"
    }
}

# Apply current language mapping
lang = st.session_state.language
t = translations[lang]

# --- Frontend CSS Injector (Vibrant Green Buttons + Pure White Cards) ---
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

    /* Solid White Premium Dashboard Cards */
    .transaction-card {{
        background-color: #FFFFFF !important;
        border-radius: 20px !important;
        box-shadow: 0 12px 28px rgba(0,0,0,0.5) !important;
        padding: 35px !important;
        text-align: center;
        margin-top: 20px;
    }}

    /* Premium Dark Green Typography */
    .green-main-heading {{
        color: #16300B !important;
        font-weight: 800 !important;
        font-size: 32px !important;
        font-family: 'Segoe UI', Arial, sans-serif !important;
        margin-bottom: 5px;
    }}

    .green-card-heading {{
        color: #16300B !important;
        font-weight: 700 !important;
        font-size: 24px !important;
        margin-bottom: 12px;
    }}

    .custom-subtext {{
        color: #FFFFFF !important;
        font-size: 18px !important;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.6);
        margin-bottom: 30px;
    }}
    
    .card-body-text {{
        color: #444444 !important;
        font-size: 15px !important;
        line-height: 1.5;
        margin-bottom: 25px;
        min-height: 45px;
    }}

    /* VIBRANT ELECTRIC GREEN BUTTONS (Sharp Black Text) */
    div.stButton > button {{
        background-color: #00E676 !important; 
        color: #000000 !important;          
        border-radius: 12px !important;       
        border: none !important;
        padding: 14px 28px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(0, 230, 118, 0.3) !important;
        transition: all 0.2s ease-in-out;
        width: 100%;
    }}
    
    div.stButton > button:hover {{
        background-color: #00C853 !important; 
        box-shadow: 0 6px 16px rgba(0, 230, 118, 0.5) !important;
        transform: scale(1.03);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- Top Header / Branding ---
st.markdown(f"""
    <div class="brand-title">
        MFUGAJI KWANZA
        <span class="brand-subtitle">{t['subtitle']}</span>
    </div>
""", unsafe_allow_html=True)

# Spacing down to clear absolute top header positioning
st.write("<br><br><br><br>", unsafe_allow_html=True)

# --- Quick Language Changer Row ---
lang_col1, lang_col2 = st.columns([5, 1])
with lang_col2:
    chosen_lang = st.selectbox("", ["English", "Swahili"], index=0 if lang == "English" else 1, key="trans_lang_toggle")
    if chosen_lang != st.session_state.language:
        st.session_state.language = chosen_lang
        st.rerun()

# --- Main Welcome Banner ---
st.markdown(f'<div style="text-align: center;"><span class="green-main-heading" style="color:#FFF !important; text-shadow: 2px 2px 4px #000;">{t["welcome"]}</span></div>', unsafe_allow_html=True)
st.markdown(f'<div class="custom-subtext" style="text-align: center;">{t["instruction"]}</div>', unsafe_allow_html=True)

# --- Dual Option Dashboard Selection Columns ---
_, center_grid_left, _, center_grid_right, _ = st.columns([0.5, 2, 0.3, 2, 0.5])

with center_grid_left:
    st.markdown(f"""
        <div class="transaction-card">
            <div class="green-card-heading">{t['choice_inputs']}</div>
            <div class="card-body-text">{t['desc_inputs']}</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button(t['choice_inputs'], key="btn_inputs"):
        st.info(f"{t['selected_msg']} {t['choice_inputs']}")
        # Next Step: Add logic/switch pages to open your farm input catalog form here!

with center_grid_right:
    st.markdown(f"""
        <div class="transaction-card">
            <div class="green-card-heading">{t['choice_withdraw']}</div>
            <div class="card-body-text">{t['desc_withdraw']}</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button(t['choice_withdraw'], key="btn_withdraw"):
        st.info(f"{t['selected_msg']} {t['choice_withdraw']}")
        # Next Step: Add logic/switch pages to open your mobile payment payout gateway form here!
