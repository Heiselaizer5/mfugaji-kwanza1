import streamlit as st
from datetime import datetime, date
import time
import requests  # Tumeongeza requests kwa ajili ya kuongea na Selar API

# --- Page Configuration ---
st.set_page_config(
    page_title="Mfugaji Kwanza - Broiler Manager",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Initialize Session States (Database, Login na Malipo) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_activated" not in st.session_state:
    st.session_state.is_activated = False
if "language" not in st.session_state:
    st.session_state.language = "Swahili"
if "sub_view" not in st.session_state:
    st.session_state.sub_view = "dashboard"
if "auth_screen" not in st.session_state:
    st.session_state.auth_screen = "login"  # Inaweza kuwa 'login' au 'signup'
if "profit_calculated" not in st.session_state:
    st.session_state.profit_calculated = False

# Database ya watumiaji waliojisajili (Tunajaza admin kama default)
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin": "admin123"
    }

# Database kuu ya kuhifadhi data za kila tarehe tofauti
if "farm_database" not in st.session_state:
    st.session_state.farm_database = {}

# Mfumo wa kutengeneza nafasi ya tarehe mpya kwenye database
def init_date_entry(target_date_str):
    if target_date_str not in st.session_state.farm_database:
        st.session_state.farm_database[target_date_str] = {
            "chicks_cost": 0.0,
            "feed_cost": 0.0,
            "med_cost": 0.0,
            "other_cost": 0.0,
            "mortality": 0,
            "sales_qty": 0,
            "sales_price": 0.0,
            "sales_revenue": 0.0,
            "has_inputs": False,
            "has_sales": False
        }

# --- Background Image ---
broiler_bg_url = "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?q=80&w=1600&auto=format&fit=crop"

# --- Kamusi ya Lugha zote (Login + Signup + Gateway + Dashboard) ---
translations = {
    "English": {
        "title": "MFUGAJI KWANZA",
        "subtitle": "Modern Poultry Management System",
        "login_header": "🔒 Account Login",
        "signup_header": "📝 Create New Account",
        "username": "Username or Phone Number",
        "password": "Password",
        "full_name": "Full Name",
        "login_btn": "Sign In Securely 🚀",
        "signup_btn": "Register & Proceed to Payment 📝",
        "go_to_signup": "Don't have an account? Sign Up here",
        "go_to_login": "Already have an account? Log In here",
        "error_msg": "❌ Invalid Username or Password.",
        "error_fields": "❌ All fields are required.",
        "success_msg": "🎉 Account Created! Please process activation payment...",
        "login_success": "🎉 Login Successful!",
        
        # Gateway Key
        "gate_header": "💳 Premium Account Activation",
        "gate_sub": "Enter your phone number below and click pay to launch your link.",
        "gate_info": "🐔 Minimum subscription activation fee is **Tsh 10,000**.",
        "gate_carrier": "Select Payment Network",
        "gate_phone": "Enter Payment Phone Number (e.g., 07xxxxxxxx)",
        "gate_amount": "Enter Activation Amount (TSH)",
        "gate_pay_btn": "LIPA SASA (PUSH PAYMENT) 📱",
        "gate_error": "❌ Please ensure the phone number is valid and amount is at least 10,000 TSH!",
        "gate_success": "🎉 Payment verified successfully! Dashboard access granted.",
        
        "welcome": "Broiler Batch Manager",
        "instruction": "Select an option below to manage development, expenditure, or broiler sales.",
        "choice_inputs": "🛒 Development & Expenditure of Chicks",
        "choice_withdraw": "💰 Broiler Sales",
        "desc_inputs": "Record expenses for chicks, feeds, medications, chick mortality, and other costs.",
        "desc_withdraw": "Record number of mature chickens sold, selling price, and calculate harvest return.",
        "back_btn": "← Back to Dashboard",
        
        # Forms
        "input_header": "🐣 Development & Expenditure of Chicks",
        "sales_header": "💰 Broiler Sales (Harvest Details)",
        "label_chicks": "Total Cost of Vifaranga (TSH)",
        "label_feed": "Total Cost of Chakula/Feeds (TSH)",
        "label_med": "Total Cost of Meds & Vaccines (TSH)",
        "label_other": "Total Cost of Other Expenses (TSH)",
        "label_mortality": "Number of Chickens Died (Mortality)",
        "label_date": "Select Transaction Date",
        "finish_inputs_btn": "🏁 Finish & Calculate Expenses",
        "finish_sales_btn": "🏁 Finish & Calculate Sales",
        "label_qty": "Number of Chickens Sold",
        "label_price": "Price per Chicken (TSH)",
        
        # Financial Summary Card
        "summary_header": "📊 Total Lifetime Financial Summary (All Dates)",
        "total_expenses": "Total Lifetime Expenses:",
        "total_revenue": "Total Lifetime Revenue:",
        "calc_profit_btn": "📈 Calculate Net Profit",
        "net_profit": "Net Profit:",
        "profit_msg": "🎉 Congratulations! Your farm made a TOTAL PROFIT of",
        "loss_msg": "⚠️ Attention! Your farm made a TOTAL LOSS of",

        # Search History Section
        "search_header": "🔍 Search Farm Records by Specific Date",
        "search_instruction": "Pick a date to fetch all expenditures, chick mortality, and sales recorded on that day.",
        "no_records": "❌ No records found for the selected date.",
        "day_summary": "Records Summary for:"
    },
    "Swahili": {
        "title": "MFUGAJI KWANZA",
        "subtitle": "Mfumo wa Kisasa wa Usimamizi wa Kuku",
        "login_header": "🔒 Ingia Kwenye Akaunti",
        "signup_header": "📝 Fungua Akaunti Mpya",
        "username": "Jina la Mtumiaji / Namba ya Simu",
        "password": "Neno la Siri (Password)",
        "full_name": "Jina Lako Kamili",
        "login_btn": "Ingia Sasa 🚀",
        "signup_btn": "Sajili na Uendelee kwenye Malipo 📝",
        "go_to_signup": "Hauna akaunti bado? Jisajili hapa",
        "go_to_login": "Umeshajisajili? Ingia hapa",
        "error_msg": "❌ Jina au neno la siri sio sahihi.",
        "error_fields": "❌ Sehemu zote zinatakiwa kujazwa.",
        "success_msg": "🎉 Akaunti imefunguliwa! Tafadhali kamilisha malipo...",
        "login_success": "🎉 Umefanikiwa kuingia!",
        
        # Gateway Key
        "gate_header": "💳 Uamilishaji wa Akaunti ya Shamba",
        "gate_sub": "Weka namba ya simu ya malipo kupata ukurasa wa kukamilisha muamala.",
        "gate_info": "🐔 Ada ya kiwango cha chini ya uamilishaji ni **Tsh 10,000**.",
        "gate_carrier": "Chagua Mtandao wa Malipo",
        "gate_phone": "Ingiza Namba ya Simu ya Malipo (Mf. 07xxxxxxxx)",
        "gate_amount": "Ingiza Kiasi cha Fedha (TSH)",
        "gate_pay_btn": "LIPA SASA (PUSH PAYMENT) 📱",
        "gate_error": "❌ Hakikisha namba ya simu imekamilika na kiasi hakipungui Tsh 10,000!",
        "gate_success": "🎉 Malipo yamefanikiwa kwa 100%! Umefunguliwa Dashibodi kuu.",
        
        "welcome": "Usimamizi wa Kuku wa Nyama (Broiler)",
        "instruction": "Chagua hatua hapa chini kusajili maendeleo, gharama, au mauzo ya broiler.",
        "choice_inputs": "🛒 Maendeleo na Gharama za Vifaranga",
        "choice_withdraw": "💰 Mauzo ya Kuku (Broiler Sales)",
        "desc_inputs": "Sajili gharama za vifaranga, chakula, madawa, vifo vya vifaranga na vikorokoro.",
        "desc_withdraw": "Sajili idadi ya kuku waliokomaa waliouzwa, bei ya kuuzia, na kukokotoa mapato ya jumla.",
        "back_btn": "← Rudi Kwenye Dashibodi",
        
        # Forms
        "input_header": "🐣 Maendeleo na Gharama za Vifaranga",
        "sales_header": "💰 Mauzo ya Kuku (Broiler Sales)",
        "label_chicks": "Gharama Kamili ya Vifaranga (TSH)",
        "label_feed": "Gharama Kamili ya Chakula (TSH)",
        "label_med": "Gharama Kamili ya Chanjo na Dawa (TSH)",
        "label_other": "Gharama za Vikorokoro Nyinginezo (TSH)",
        "label_mortality": "Idadi ya Vifaranga/Kuku Waliokufa (Vifo)",
        "label_date": "Chagua Tarehe ya Kumbukumbu",
        "finish_inputs_btn": "🏁 Maliza na Ukokotoe Gharama (Finish)",
        "finish_sales_btn": "🏁 Maliza na Ukokotoe Mauzo (Finish)",
        "label_qty": "Idadi ya Kuku Waliouzwa",
        "label_price": "Bei kwa Kila Kuku mmoja (TSH)",
        
        # Financial Summary Card
        "summary_header": "📊 Muhtasari wa Jumla wa Mapato na Faida (Muda Wote)",
        "total_expenses": "Jumla ya Matumizi yote (Expenditure):",
        "total_revenue": "Jumla ya Mapato yote ya Mauzo:",
        "calc_profit_btn": "📈 Piga Hesabu ya Net Profit",
        "net_profit": "Faida Net (Net Profit):",
        "profit_msg": "🎉 Hongera! Shamba limeingiza FAIDA ya jumla ya",
        "loss_msg": "⚠️ Angalizo! Shamba limeingiza HASARA ya jumla ya",

        # Search History Section
        "search_header": "🔍 Tafuta Kumbukumbu za Shamba kwa Tarehe Maalum",
        "search_instruction": "Chagua tarehe hapa chini iti kupata data zote za gharama, vifo, na mauzo ya siku hiyo.",
        "no_records": "❌ Hakuna kumbukumbu zozote zilizosajiliwa tarehe hii.",
        "day_summary": "Muhtasari wa data za tarehe:"
    }
}

lang = st.session_state.language
t = translations[lang]

# --- CSS Styling (UNIVERSAL DARK BOARDS + WHITE INPUTS + ZERO PAGE JUMPING) ---
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{broiler_bg_url}");
        background-size: cover; background-position: center;
        background-repeat: no-repeat; background-attachment: fixed;
    }}
    .stApp::before {{
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.70); z-index: 0;
    }}
    [data-testid="stHeader"] {{ background-color: transparent !important; z-index: 10; }}
    .main .block-container {{ z-index: 1; padding-top: 1.5rem !important; padding-bottom: 1.5rem !important; }}
    
    .brand-container {{ text-align: center; margin-bottom: 20px; }}
    .brand-title {{
        color: #FFFFFF; font-family: 'Arial Black', sans-serif; font-weight: 900;
        font-size: 38px; letter-spacing: 2px; text-shadow: 3px 3px 6px rgba(0,0,0,0.8);
    }}
    .brand-subtitle {{ font-size: 14px; font-family: Arial, sans-serif; color: #00E676; display: block; margin-top: -5px; font-weight: 600; }}

    .dashboard-card, [data-testid="stForm"], .stForm {{
        background-color: #1A1A1A !important; 
        border: 2px solid #2D2D2D !important;
        border-radius: 16px !important; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.7) !important; 
        padding: 28px !important; 
        margin-top: 10px;
    }}
    
    .dashboard-card {{ text-align: center; min-height: 200px; }}

    .summary-card-dark {{
        background-color: #1A1A1A !important; border-radius: 20px !important; 
        padding: 30px !important; box-shadow: 0 12px 35px rgba(0,0,0,0.7) !important; 
        border-left: 10px solid #00E676 !important; margin-top: 15px;
    }}
    
    .white-card-heading {{ color: #FFFFFF !important; font-weight: 700; font-size: 22px; margin-bottom: 10px; }}
    .card-body-text-white {{ color: #DDDDDD !important; font-size: 14px; margin-bottom: 20px; line-height: 1.5; }}

    label[data-testid="stWidgetLabel"] p {{ 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
        font-size: 15px !important; 
    }}

    div[data-testid="stMarkdownContainer"] p {{ color: #FFFFFF; }}
    input {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }}
    
    div[data-baseweb="select"] {{
        background-color: #1A1A1A !important;
    }}

    /* Electric Green Buttons */
    div.stButton > button {{
        background-color: #00E676 !important; color: #000000 !important;          
        border-radius: 12px !important; border: none !important;
        padding: 12px 24px !important; font-size: 16px !important; font-weight: 700 !important;
        box-shadow: 0 0 15px rgba(0, 230, 118, 0.5) !important; transition: all 0.3s ease-in-out; width: 100%;
    }}
    div.stButton > button:hover {{
        background-color: #00FF5E !important; box-shadow: 0 0 25px rgba(0, 230, 118, 0.8) !important; transform: scale(1.02);
    }}
    
    .link-button-custom {{
        color: #00E676 !important;
        text-align: center;
        display: block;
        margin-top: 15px;
        cursor: pointer;
        text-decoration: underline;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- Top Header & Language Selector ---
row_top1, row_top2 = st.columns([4, 1])
with row_top1:
    st.markdown(f'<div class="brand-title">MFUGAJI KWANZA <span class="brand-subtitle">{t["subtitle"]}</span></div>', unsafe_allow_html=True)
with row_top2:
    chosen_lang = st.selectbox("", ["Swahili", "English"], index=0 if lang == "Swahili" else 1, key="app_lang_select")
    if chosen_lang != st.session_state.language:
        st.session_state.language = chosen_lang
        st.rerun()

st.write("<br>", unsafe_allow_html=True)

# ==========================================
# SEHEMU YA 1: AUTHENTICATION FLOW (Login / Signup)
# ==========================================
if not st.session_state.logged_in:
    _, center_auth, _ = st.columns([1, 1.8, 1])
    
    with center_auth:
        # ---- CASE 1A: LOGIN FORM ----
        if st.session_state.auth_screen == "login":
            with st.form(key="login_secure_form"):
                st.markdown(f'<h3 style="color:#00E676; margin-top:0; font-weight:800; text-align:center;">{t["login_header"]}</h3>', unsafe_allow_html=True)
                st.write("<hr style='border-color: #333; margin-bottom:20px;'>", unsafe_allow_html=True)
                
                user_input = st.text_input(t["username"], placeholder="admin / 0712345678")
                pass_input = st.text_input(t["password"], type="password", placeholder="••••••••")
                
                if st.form_submit_button(t["login_btn"]):
                    username_clean = user_input.strip()
                    if username_clean in st.session_state.users_db and st.session_state.users_db[username_clean] == pass_input:
                        st.session_state.logged_in = True
                        # Kama ni admin anaingia direct, wengine wanapitia malipo
                        st.session_state.is_activated = True if username_clean == "admin" else False
                        st.success(t["login_success"])
                        time.sleep(1.0)
