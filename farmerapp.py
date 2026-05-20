import streamlit as st
from datetime import datetime, date
import time

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
        "gate_sub": "Enter your amount and phone number below to launch your instance.",
        "gate_info": "🐔 Minimum subscription activation fee is **Tsh 10,000**.",
        "gate_carrier": "Select Payment Network",
        "gate_phone": "Enter Payment Phone Number (e.g., 07xxxxxxxx)",
        "gate_amount": "Enter Activation Amount (TSH)",
        "gate_pay_btn": "LIPA SASA (PUSH PAYMENT) 📱",
        "gate_error": "❌ Please ensure the phone number is valid and amount is at least 10,000 TSH!",
        "gate_success": "🎉 Payment successful! Dashboard access granted.",
        
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
        "gate_sub": "Weka kiasi na namba ya simu ila kuamsha akaunti yako moja kwa moja.",
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
        "search_instruction": "Chagua tarehe hapa chini ili kupata data zote za gharama, vifo, na mauzo ya siku hiyo.",
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
                        st.success(t["login_success"])
                        time.sleep(1.0)
                        st.rerun()
                    else:
                        st.error(t["error_msg"])
            
            # Kitufe cha kubadili kwenda Signup Screen
            if st.button(t["go_to_signup"]):
                st.session_state.auth_screen = "signup"
                st.rerun()

        # ---- CASE 1B: SIGNUP FORM ----
        elif st.session_state.auth_screen == "signup":
            with st.form(key="signup_secure_form"):
                st.markdown(f'<h3 style="color:#00E676; margin-top:0; font-weight:800; text-align:center;">{t["signup_header"]}</h3>', unsafe_allow_html=True)
                st.write("<hr style='border-color: #333; margin-bottom:20px;'>", unsafe_allow_html=True)
                
                reg_name = st.text_input(t["full_name"], placeholder="Mussa Hamisi")
                reg_user = st.text_input(t["username"], placeholder="07xxxxxxxx")
                reg_pass = st.text_input(t["password"], type="password", placeholder="Weka password yako")
                
                if st.form_submit_button(t["signup_btn"]):
                    username_clean = reg_user.strip()
                    if reg_name and username_clean and reg_pass:
                        # Hifadhi mtumiaji kwenye database yetu ya Session State
                        st.session_state.users_db[username_clean] = reg_pass
                        st.session_state.logged_in = True
                        st.session_state.is_activated = False  # Anahitaji kulipia kwanza
                        st.success(t["success_msg"])
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error(t["error_fields"])
            
            # Kitufe cha kurudi Login Screen
            if st.button(t["go_to_login"]):
                st.session_state.auth_screen = "login"
                st.rerun()

# ==========================================
# SEHEMU YA 2: GATEWAY PUSH GATEBOARD (Uamilishaji baada ya Signup)
# ==========================================
elif st.session_state.logged_in and not st.session_state.is_activated:
    _, center_gate, _ = st.columns([1, 1.8, 1])
    with center_gate:
        with st.form(key="payment_activation_form"):
            st.markdown(f'<h3 style="color:#00E676; margin-top:0; font-weight:800; text-align:center;">{t["gate_header"]}</h3>', unsafe_allow_html=True)
            st.markdown(f'<p style="text-align:center; color:#DDD; font-size:14px;">{t["gate_sub"]}</p>', unsafe_allow_html=True)
            st.write("<hr style='border-color: #333;'>", unsafe_allow_html=True)
            
            st.info(t["gate_info"])
            
            carrier = st.selectbox(t["gate_carrier"], ["M-Pesa", "Tigo Pesa", "Airtel Money", "Halo Pesa"])
            push_phone = st.text_input(t["gate_phone"], placeholder="07xxxxxxxx")
            push_amount = st.number_input(t["gate_amount"], min_value=10000, value=10000, step=1000)
            
            if st.form_submit_button(t["gate_pay_btn"]):
                if len(push_phone.strip()) >= 10 and push_amount >= 10000:
                    with st.spinner("Connecting to carrier network... Weka namba ya siri kwenye simu yako kukamilisha."):
                        time.sleep(3.5)  # Simulated API Callback Wait
                    st.session_state.is_activated = True
                    st.success(t["gate_success"])
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error(t["gate_error"])

# ==========================================
# SEHEMU YA 3: DASHBOARD & TRANSACTIONS (Usimamizi wa Shamba)
# ==========================================
else:
    # Kukokotoa jumla ya shamba zima kutoka kwenye database ya tarehe zote
    lifetime_costs = 0.0
    lifetime_revenue = 0.0
    for date_key in st.session_state.farm_database:
        entry = st.session_state.farm_database[date_key]
        lifetime_costs += entry["chicks_cost"] + entry["feed_cost"] + entry["med_cost"] + entry["other_cost"]
        lifetime_revenue += entry["sales_revenue"]

    # ---- VIEW 2A: DASHBOARD KUU ----
    if st.session_state.sub_view == "dashboard":
        st.markdown(f'<h2 style="text-align:center; color:white; text-shadow:2px 2px 4px #000; margin-top:0;">{t["welcome"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center; color:#E0E0E0; font-size:16px; margin-bottom:20px;">{t["instruction"]}</p>', unsafe_allow_html=True)
        
        col_dash1, _, col_dash2 = st.columns([2, 0.4, 2])
        
        with col_dash1:
            st.markdown(f'<div class="dashboard-card"><div class="white-card-heading">{t["choice_inputs"]}</div><div class="card-body-text-white">{t["desc_inputs"]}</div></div>', unsafe_allow_html=True)
            if st.button(t["choice_inputs"], key="go_to_inputs"):
                st.session_state.sub_view = "inputs"
                st.session_state.profit_calculated = False 
                st.rerun()
                
        with col_dash2:
            st.markdown(f'<div class="dashboard-card"><div class="white-card-heading">{t["choice_withdraw"]}</div><div class="card-body-text-white">{t["desc_withdraw"]}</div></div>', unsafe_allow_html=True)
            if st.button(t["choice_withdraw"], key="go_to_sales"):
                st.session_state.sub_view = "withdraw"
                st.session_state.profit_calculated = False 
                st.rerun()

        # --- LIFETIME FINANCIAL SUMMARY CARD ---
        st.write("<br>", unsafe_allow_html=True)
        _, center_calc_col, _ = st.columns([0.5, 3, 0.5])
        
        with center_calc_col:
            st.markdown(f"""
            <div class="summary-card-dark">
                <h3 style="color: #00E676; margin-top:0; font-weight:800;">{t['summary_header']}</h3>
                <hr style="border-color: #333333;">
                <p style="color:#FFF; font-size:16px; margin: 8px 0;"><b>{t['total_expenses']}</b> <span style="color:#FF5252; font-weight:700;">{lifetime_costs:,.2f} TSH</span></p>
                <p style="color:#FFF; font-size:16px; margin: 15px 0 8px 0;"><b>{t['total_revenue']}</b> <span style="color:#00E676; font-weight:700;">{lifetime_revenue:,.2f} TSH</span></p>
                <hr style="border-color: #333333;">
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(t["calc_profit_btn"], key="calc_profit_dashboard"):
                st.session_state.profit_calculated = True
                st.rerun()

            if st.session_state.profit_calculated:
                net_profit = lifetime_revenue - lifetime_costs
                if net_profit > 0:
                    st.success(f"{t['profit_msg']} {net_profit:,.2f} TSH")
                elif net_profit < 0:
                    st.error(f"{t['loss_msg']} {abs(net_profit):,.2f} TSH")

        # --- 🔍 SECTION: HISTORICAL DATE SEARCH BOARD ---
        st.write("<br><hr style='border-color: #333;'><br>", unsafe_allow_html=True)
        _, search_col, _ = st.columns([0.5, 3, 0.5])
        
        with search_col:
            st.markdown(f"""
            <div class="dashboard-card" style="text-align: left; min-height: auto; padding: 20px !important;">
                <h3 style="color: #00E676; margin-top:0; font-weight:800;">{t['search_header']}</h3>
                <p style="color: #DDD; font-size:14px; margin-bottom: 5px;">{t['search_instruction']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            search_date = st.date_input("", value=date.today(), key="farm_search_date_picker")
            search_key = str(search_date)
            
            if search_key in st.session_state.farm_database:
                day_data = st.session_state.farm_database[search_key]
                day_total_cost = day_data["chicks_cost"] + day_data["feed_cost"] + day_data["med_cost"] + day_data["other_cost"]
                day_profit = day_data["sales_revenue"] - day_total_cost
                
                st.markdown(f"""
                <div style="background-color: #1A1A1A; border: 2px solid #2D2D2D; border-radius: 15px; padding: 25px; margin-top: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); border-top: 6px solid #00E676;">
                    <h4 style="color: #00E676; margin-top:0;"><b>{t['day_summary']} {search_key}</b></h4>
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 15px;">
                        <div style="flex: 1; min-width: 200px; background:#252525; padding:15px; border-radius:10px;">
                            <b style="color:#00E676;">🐣 Development & Expenditure:</b><br>
                            <span style="font-size:14px; color:#EEE;">
                            • Vifaranga: {day_data['chicks_cost']:,.2f} TSH<br>
                            • Chakula: {day_data['feed_cost']:,.2f} TSH<br>
                            • Dawa/Chanjo: {day_data['med_cost']:,.2f} TSH<br>
                            • Vikorokoro: {day_data['other_cost']:,.2f} TSH<br>
                            <b>• Vifo vya Vifaranga: <span style="color:#FF5252;">{day_data['mortality']} Kuku</span></b><br>
                            <hr style="margin:5px 0; border-color:#444;">
                            <b>Jumla ya Gharama: {day_total_cost:,.2f} TSH</b>
                            </span>
                        </div>
                        <div style="flex: 1; min-width: 200px; background:#252525; padding:15px; border-radius:10px;">
                            <b style="color:#00E676;">💰 Broiler Sales:</b><br>
                            <span style="font-size:14px; color:#EEE;">
                            • Kuku Waliouzwa: {day_data['sales_qty']} pcs<br>
                            • Bei kwa kila mmoja: {day_data['sales_price']:,.2f} TSH<br>
                            <hr style="margin:5px 0; border-color:#444;">
                            <b>Jumla ya Mauzo: <span style="color:#00E676;">{day_data['sales_revenue']:,.2f} TSH</span></b>
                            </span>
                        </div>
                    </div>
                    <div style="margin-top: 15px; padding: 12px; background: #00E676; border-radius: 8px; text-align: center;">
                        <b style="color: black; font-size: 16px;">Net Profit ya Siku Hii: {day_profit:,.2f} TSH</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info(t["no_records"])
                
        # Logout Custom Option
        st.write("<br>", unsafe_allow_html=True)
        if st.button("Logout (Ondoka)", key="app_logout_btn"):
            st.session_state.logged_in = False
            st.session_state.is_activated = False
            st.session_state.auth_screen = "login"
            st.rerun()

    # ---- VIEW 2B: FOMU YA GHARAMA ----
    elif st.session_state.sub_view == "inputs":
        _, center_form, _ = st.columns([1, 2, 1])
        with center_form:
            if st.button(t["back_btn"], key="back_from_inputs"):
                st.session_state.sub_view = "dashboard"
                st.rerun()
                
            with st.form(key="inputs_data_capture"):
                st.markdown(f'<h3 style="color:#00E676; margin-top:0; font-weight:800;">{t["input_header"]}</h3>', unsafe_allow_html=True)
                st.write("<hr style='border-color: #333;'>", unsafe_allow_html=True)
                
                chosen_date = st.date_input(t["label_date"], value=date.today(), key="input_date_picker")
                date_str = str(chosen_date)
                init_date_entry(date_str) 
                
                current_entry = st.session_state.farm_database[date_str]
                
                chicks = st.number_input(t["label_chicks"], min_value=0.0, value=current_entry["chicks_cost"], step=500.0)
                feeds = st.number_input(t["label_feed"], min_value=0.0, value=current_entry["feed_cost"], step=1000.0)
                meds = st.number_input(t["label_med"], min_value=0.0, value=current_entry["med_cost"], step=500.0)
                other = st.number_input(t["label_other"], min_value=0.0, value=current_entry["other_cost"], step=500.0)
                mortality = st.number_input(t["label_mortality"], min_value=0, value=current_entry["mortality"], step=1)
                
                if st.form_submit_button(t["finish_inputs_btn"]):
                    st.session_state.farm_database[date_str]["chicks_cost"] = chicks
                    st.session_state.farm_database[date_str]["feed_cost"] = feeds
                    st.session_state.farm_database[date_str]["med_cost"] = meds
                    st.session_state.farm_database[date_str]["other_cost"] = other
                    st.session_state.farm_database[date_str]["mortality"] = mortality
                    st.session_state.farm_database[date_str]["has_inputs"] = True
                    
                    st.session_state.sub_view = "dashboard"
                    st.rerun()

    # ---- VIEW 2C: FOMU YA MAUZO ----
    elif st.session_state.sub_view == "withdraw":
        _, center_form, _ = st.columns([1, 2, 1])
        with center_form:
            if st.button(t["back_btn"], key="back_from_sales"):
                st.session_state.sub_view = "dashboard"
                st.rerun()
                
            with st.form(key="sales_data_capture"):
                st.markdown(f'<h3 style="color:#00E676; margin-top:0; font-weight:800;">{t["sales_header"]}</h3>', unsafe_allow_html=True)
                st.write("<hr style='border-color: #333;'>", unsafe_allow_html=True)
                
                chosen_date = st.date_input(t["label_date"], value=date.today(), key="sales_date_picker")
                date_str = str(chosen_date)
                init_date_entry(date_str)
                
                current_entry = st.session_state.farm_database[date_str]
                
                qty = st.number_input(t["label_qty"], min_value=0, value=current_entry["sales_qty"], step=1)
                price = st.number_input(t["label_price"], min_value=0.0, value=6500.0 if current_entry["sales_price"] == 0.0 else current_entry["sales_price"], step=500.0)
                
                if st.form_submit_button(t["finish_sales_btn"]):
                    st.session_state.farm_database[date_str]["sales_qty"] = qty
                    st.session_state.farm_database[date_str]["sales_price"] = price
                    st.session_state.farm_database[date_str]["sales_revenue"] = float(qty * price)
                    st.session_state.farm_database[date_str]["has_sales"] = True
                    
                    st.session_state.sub_view = "dashboard"
                    st.rerun()
