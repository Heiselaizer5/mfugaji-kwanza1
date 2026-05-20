import streamlit as st
from datetime import datetime, date
import time

# ==========================================
# SUPABASE CONNECTION SETUP
# ==========================================
SUPABASE_URL = "https://nmdvmarfpujdxidmtlxc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5tZHZtYXJmcHVqZHhpZG10bHhjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkyOTU3NjksImV4cCI6MjA5NDg3MTc2OX0.yAVCEbNjoGlI9gkvUqvrZLSaK0i4x5LmanJo2KoFfrg"

# --- Page Configuration ---
st.set_page_config(
    page_title="Mfugaji Kwanza - Broiler Manager",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Initialize Session States ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_activated" not in st.session_state:
    st.session_state.is_activated = False
if "language" not in st.session_state:
    st.session_state.language = "Swahili"
if "sub_view" not in st.session_state:
    st.session_state.sub_view = "dashboard"
if "auth_screen" not in st.session_state:
    st.session_state.auth_screen = "login"  
if "profit_calculated" not in st.session_state:
    st.session_state.profit_calculated = False

# Database ya watumiaji na data zao
if "users_db" not in st.session_state:
    st.session_state.users_db = {"admin": "admin123"}
if "farm_database" not in st.session_state:
    st.session_state.farm_database = {}

# ==========================================
# MFUMO WA KIOTOMATIKI WA KUSOMA MALIPO KUTOKA SELAR
# ==========================================
query_params = st.query_params
if "status" in query_params and "token" in query_params:
    if query_params["status"] == "success" and query_params["token"] == "Erasto_HEIS5_Boss_2026":
        st.session_state.is_activated = True

def init_date_entry(target_date_str):
    if target_date_str not in st.session_state.farm_database:
        st.session_state.farm_database[target_date_str] = {
            "chicks_qty": 0,       # Idadi ya vifaranga/kuku walioingizwa bandani
            "chicks_cost": 0.0, 
            "feed_cost": 0.0, 
            "med_cost": 0.0, 
            "other_cost": 0.0,
            "mortality": 0, 
            "sales_records": [],   # Orodha ya mauzo ya wateja: [{"customer": "Name", "qty": X, "price": Y, "revenue": Z}]
            "has_inputs": False, 
            "has_sales": False
        }

broiler_bg_url = "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?q=80&w=1600&auto=format&fit=crop"

# --- Kamusi ya Lugha ---
translations = {
    "English": {
        "title": "MFUGAJI KWANZA", "subtitle": "Modern Poultry Management System",
        "login_header": "🔒 Account Login", "signup_header": "📝 Create New Account",
        "username": "Username", "password": "Password", "full_name": "Full Name",
        "login_btn": "Sign In Securely 🚀", "signup_btn": "Register & Proceed to Payment 📝",
        "go_to_signup": "Don't have an account? Sign Up here", "go_to_login": "Already have an account? Log In here",
        "error_msg": "❌ Invalid Username or Password.", "error_fields": "❌ All fields are required.",
        "success_msg": "🎉 Account Created! Please process activation payment...", "login_success": "🎉 Login Successful!",
        "welcome": "Broiler Batch Manager", "instruction": "Select an option below to manage development or sales.",
        "choice_inputs": "🛒 Development & Expenditure", "choice_withdraw": "💰 Broiler Sales (Customers)",
        "desc_inputs": "Record expenses for chicks, feeds, medications, and batch entry.", "desc_withdraw": "Record customer names, chickens bought, and sales revenue.",
        "back_btn": "← Back to Dashboard", "input_header": "🐣 Development & Expenditure",
        "sales_header": "💰 Broiler Sales", 
        "label_chicks_qty": "Number of Chicks Introduced / Idadi ya Vifaranga",
        "label_chicks": "Total Cost of Vifaranga (TSH)",
        "label_feed": "Total Cost of Feeds (TSH)", "label_med": "Total Cost of Meds (TSH)",
        "label_other": "Total Cost of Other Expenses (TSH)", "label_mortality": "Mortality Count",
        "label_date": "Select Date:", "finish_inputs_btn": "🏁 Save Expenses & Batch Details",
        "finish_sales_btn": "🏁 Save & Record Customer Purchase", "label_qty": "Number of Chickens Bought by Customer",
        "label_customer": "Customer Name / Jina la Mteja", "label_price": "Price per Chicken (TSH)", "summary_header": "📊 Total Lifetime Financial Summary",
        "total_expenses": "Total Lifetime Expenses:", "total_revenue": "Total Lifetime Revenue:",
        "calc_profit_btn": "📈 Calculate Net Profit", "profit_msg": "🎉 Net Profit:", "loss_msg": "⚠️ Net Loss:",
        "search_header": "🔍 View Farm Records by Date", "search_instruction": "Pick a date to fetch records.",
        "no_records": "❌ No records found.", "day_summary": "Summary for:"
    },
    "Swahili": {
        "title": "MFUGAJI KWANZA", "subtitle": "Mfumo wa Kisasa wa Usimamizi wa Kuku",
        "login_header": "🔒 Ingia Kwenye Akaunti", "signup_header": "📝 Fungua Akaunti Mpya",
        "username": "Jina la Mtumiaji", "password": "Neno la Siri (Password)", "full_name": "Jina Lako Kamili",
        "login_btn": "Ingia Sasa 🚀", "signup_btn": "Sajili na Uendelee kwenye Malipo 📝",
        "go_to_signup": "Hauna akaunti bado? Jisajili hapa", "go_to_login": "Umeshajisajili? Ingia hapa",
        "error_msg": "❌ Jina au neno la siri sio sahihi.", "error_fields": "❌ Sehemu zote zinatakiwa kujazwa.",
        "success_msg": "🎉 Akaunti imefunguliwa! Tafadhali kamilisha malipo...", "login_success": "🎉 Umefanikiwa kuingia!",
        "welcome": "Usimamizi wa Kuku wa Nyama (Broiler)", "instruction": "Chagua hatua hapa chini kusajili gharama au mauzo.",
        "choice_inputs": "🛒 Maendeleo na Gharama za Vifaranga", "choice_withdraw": "💰 Mauzo ya Kuku (Wateja)",
        "desc_inputs": "Sajili gharama, idadi ya vifaranga walioingia, chakula na vifo.", "desc_withdraw": "Sajili majina ya wateja, idadi ya kuku walionunua na pesa waliyolipa.",
        "back_btn": "← Rudi Kwenye Dashibodi", "input_header": "🐣 Maendeleo na Gharama za Vifaranga",
        "sales_header": "💰 Mauzo ya Kuku (Broiler Sales)", 
        "label_chicks_qty": "Idadi ya Vifaranga Walioingia Siku Hii",
        "label_chicks": "Gharama ya Kununua Vifaranga (TSH)",
        "label_feed": "Gharama ya Chakula (TSH)", "label_med": "Gharama ya Chanjo na Dawa (TSH)",
        "label_other": "Gharama Nyinginezo (TSH)", "label_mortality": "Idadi ya Waliokufa (Vifo vya Leo)",
        "label_date": "Chagua Tarehe:", "finish_inputs_btn": "🏁 Hifadhi Matumizi na Data za Vifaranga",
        "finish_sales_btn": "🏁 Hifadhi Mauzo ya Mteja Huyu", "label_qty": "Idadi ya Kuku Alionunua Mteja",
        "label_customer": "Jina la Mteja", "label_price": "Bei kwa Kila Kuku (TSH)", "summary_header": "📊 Muhtasari wa Jumla wa Mapato na Faida",
        "total_expenses": "Jumla ya Matumizi:", "total_revenue": "Jumla ya Mapato:",
        "calc_profit_btn": "📈 Piga Hesabu ya Net Profit", "profit_msg": "🎉 Shamba limeingiza FAIDA ya", "loss_msg": "⚠️ Shamba limeingiza HASARA ya",
        "search_header": "🔍 Angalia Kumbukumbu kwa Tarehe", "search_instruction": "Chagua tarehe kupata data.",
        "no_records": "❌ Hakuna kumbukumbu tarehe hii.", "day_summary": "Muhtasari wa:"
    }
}

lang = st.session_state.language
t = translations[lang]

# --- CSS Styling ---
st.markdown(f"""
    <style>
    .stApp {{ background-image: url("{broiler_bg_url}"); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed; }}
    .stApp::before {{ content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.75); z-index: 0; }}
    [data-testid="stHeader"] {{ background-color: transparent !important; z-index: 10; }}
    .main .block-container {{ z-index: 1; padding-top: 1.5rem !important; }}
    .brand-title {{ color: #FFFFFF; font-family: 'Arial Black', sans-serif; font-weight: 900; font-size: 38px; text-shadow: 3px 3px 6px rgba(0,0,0,0.8); text-align: center; }}
    .brand-subtitle {{ font-size: 14px; color: #00E676; display: block; margin-top: -5px; font-weight: 600; }}
    .dashboard-card, [data-testid="stForm"], .stForm {{ background-color: #1A1A1A !important; border: 2px solid #2D2D2D !important; border-radius: 16px !important; padding: 28px !important; margin-top: 10px; }}
    .dashboard-card {{ text-align: center; }}
    .summary-card-dark {{ background-color: #1A1A1A !important; border-radius: 20px !important; padding: 30px !important; border-left: 10px solid #00E676 !important; margin-top: 15px; }}
    label[data-testid="stWidgetLabel"] p {{ color: #FFFFFF !important; font-weight: 700 !important; }}
    input {{ background-color: #FFFFFF !important; color: #000000 !important; font-weight: 600 !important; border-radius: 8px !important; }}
    
    div.stButton > button {{ background-color: #00E676 !important; color: #000000 !important; border-radius: 12px !important; border: none !important; padding: 12px 24px !important; font-weight: 700 !important; width: 100%; }}
    div.stButton > button:hover {{ background-color: #00FF5E !important; transform: scale(1.02); }}
    
    div.stLinkButton > a {{
        background-color: #2563eb !important; 
        color: #FFFFFF !important; 
        border-radius: 12px !important; 
        padding: 14px 24px !important; 
        font-weight: 700 !important; 
        font-size: 16px !important;
        text-align: center !important;
        display: block !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4) !important;
        border: none !important;
        text-decoration: none !important;
    }}
    div.stLinkButton > a:hover {{
        background-color: #1d4ed8 !important; 
        color: #FFFFFF !important;
        transform: scale(1.02) !important;
        text-decoration: none !important;
    }}
    
    .activation-box {{
        background-color: #112233 !important;
        border: 2px solid #1f3a60 !important;
        border-radius: 12px !important;
        padding: 30px !important;
        text-align: center;
        margin-top: 20px;
    }}
    .data-display {{
        background-color: #222222;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #38bdf8;
        margin-top: 10px;
    }}
    .customer-badge {{
        background-color: #2d2d2d;
        padding: 6px 12px;
        border-radius: 6px;
        margin: 4px 0;
        border-left: 3px solid #00E676;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- Top Header ---
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
# SEHEMU YA 1: AUTHENTICATION FLOW
# ==========================================
if not st.session_state.logged_in:
    _, center_auth, _ = st.columns([1, 1.8, 1])
    with center_auth:
        if st.session_state.auth_screen == "login":
            with st.form(key="login_secure_form"):
                st.markdown(f'<h3 style="color:#00E676; text-align:center;">{t["login_header"]}</h3>', unsafe_allow_html=True)
                user_input = st.text_input(t["username"], placeholder="admin / 07xxxxxxxx")
                pass_input = st.text_input(t["password"], type="password")
                if st.form_submit_button(t["login_btn"]):
                    username_clean = user_input.strip()
                    if username_clean in st.session_state.users_db and st.session_state.users_db[username_clean] == pass_input:
                        st.session_state.logged_in = True
                        if username_clean == "admin":
                            st.session_state.is_activated = True
                        st.success(t["login_success"])
                        time.sleep(1.0)
                        st.rerun()
                    else:
                        st.error(t["error_msg"])
            if st.button(t["go_to_signup"]):
                st.session_state.auth_screen = "signup"
                st.rerun()

        elif st.session_state.auth_screen == "signup":
            with st.form(key="signup_secure_form"):
                st.markdown(f'<h3 style="color:#00E676; text-align:center;">{t["signup_header"]}</h3>', unsafe_allow_html=True)
                reg_name = st.text_input(t["full_name"])
                reg_user = st.text_input(t["username"])
                reg_pass = st.text_input(t["password"], type="password")
                if st.form_submit_button(t["signup_btn"]):
                    username_clean = reg_user.strip()
                    if reg_name and username_clean and reg_pass:
                        st.session_state.users_db[username_clean] = reg_pass
                        st.session_state.logged_in = True
                        st.session_state.is_activated = False  
                        st.success(t["success_msg"])
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error(t["error_fields"])
            if st.button(t["go_to_login"]):
                st.session_state.auth_screen = "login"
                st.rerun()

# ==========================================
# SEHEMU YA 2: BANGO LA MALIPO
# ==========================================
elif st.session_state.logged_in and not st.session_state.is_activated:
    _, center_gate, _ = st.columns([1, 2.2, 1])
    with center_gate:
        st.markdown("""
        <div class="activation-box">
            <h3 style="color: #38bdf8; margin-top:0; font-weight:700;">🔓 Uamilishaji wa Akaunti ya Shamba / Account Activation</h3>
            <p style="color: #DDD; font-size: 15px; margin-bottom: 10px;">
                Lipia uamilishaji wa mwezi mmoja ili kupata huduma zote za usimamizi wa kuku wako.
            </p>
            <p style="color: #00E676; font-size: 14px; font-weight: 600; margin-bottom: 20px;">
                Easy payment via Tigo Pesa, Halopesa, or Airtel Money.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.link_button(
            label="🐔 BONYEZA HAPA KULIPIA / 1-MONTH PASS (10,000 TZS)", 
            url="https://selar.co/9o12h598n9"
        )
        st.write("<br>", unsafe_allow_html=True)
        st.warning("⚠️ Dashibodi itafunguka yenyewe pindi utakapomaliza malipo yako kule Selar na kurudishwa kwenye mfumo.")

# ==========================================
# SEHEMU YA 3: DASHBOARD & TRANSACTIONS
# ==========================================
else:
    if st.query_params:
        st.query_params.clear()
        
    # Hesabu Jumla ya Maisha ya Shamba (Lifetime Summary)
    lifetime_costs = 0.0
    lifetime_revenue = 0.0
    for date_key in st.session_state.farm_database:
        entry = st.session_state.farm_database[date_key]
        lifetime_costs += entry["chicks_cost"] + entry["feed_cost"] + entry["med_cost"] + entry["other_cost"]
        for record in entry["sales_records"]:
            lifetime_revenue += record["revenue"]

    if st.session_state.sub_view == "dashboard":
        st.markdown(f'<h2 style="text-align:center; color:white; margin-top:0;">{t["welcome"]}</h2>', unsafe_allow_html=True)
        
        col_dash1, _, col_dash2 = st.columns([2, 0.4, 2])
        with col_dash1:
            st.markdown(f'<div class="dashboard-card"><div style="color:white; font-size:20px; font-weight:700;">{t["choice_inputs"]}</div><p style="color:#AAA; font-size:14px;">{t["desc_inputs"]}</p></div>', unsafe_allow_html=True)
            if st.button(t["choice_inputs"], key="go_to_inputs"):
                st.session_state.sub_view = "inputs"
                st.session_state.profit_calculated = False 
                st.rerun()
        with col_dash2:
            st.markdown(f'<div class="dashboard-card"><div style="color:white; font-size:20px; font-weight:700;">{t["choice_withdraw"]}</div><p style="color:#AAA; font-size:14px;">{t["desc_withdraw"]}</p></div>', unsafe_allow_html=True)
            if st.button(t["choice_withdraw"], key="go_to_sales"):
                st.session_state.sub_view = "withdraw"
                st.session_state.profit_calculated = False 
                st.rerun()

        # Summary Display
        st.write("<br>", unsafe_allow_html=True)
        _, center_calc_col, _ = st.columns([0.5, 3, 0.5])
        with center_calc_col:
            st.markdown(f"""
            <div class="summary-card-dark">
                <h3 style="color: #00E676; margin-top:0; font-weight:800;">{t['summary_header']}</h3>
                <p style="color:#FFF;"><b>{t['total_expenses']}</b> <span style="color:#FF5252;">{lifetime_costs:,.2f} TSH</span></p>
                <p style="color:#FFF;"><b>{t['total_revenue']}</b> <span style="color:#00E676;">{lifetime_revenue:,.2f} TSH</span></p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(t["calc_profit_btn"]):
                st.session_state.profit_calculated = True
                st.rerun()
            if st.session_state.profit_calculated:
                net_profit = lifetime_revenue - lifetime_costs
                if net_profit > 0: st.success(f"{t['profit_msg']} {net_profit:,.2f} TSH")
                else: st.error(f"{t['loss_msg']} {abs(net_profit):,.2f} TSH")

        # Sehemu ya Kutafuta Data kwa Tarehe (Search Engine iliyoboreshwa)
        st.write("<br><hr style='border-color: #333;'><br>", unsafe_allow_html=True)
        _, search_col, _ = st.columns([0.5, 3, 0.5])
        with search_col:
            st.markdown(f"<h3 style='color: white; margin-bottom:10px;'>{t['search_header']}</h3>", unsafe_allow_html=True)
            search_date = st.date_input("", value=date.today(), key="farm_search_date_picker")
            search_date_str = str(search_date)
            
            if search_date_str in st.session_state.farm_database:
                data_found = st.session_state.farm_database[search_date_str]
                day_total_qty = sum(r["qty"] for r in data_found["sales_records"])
                day_total_rev = sum(r["revenue"] for r in data_found["sales_records"])
                chicks_entered = data_found.get("chicks_qty", 0)
                
                st.markdown(f"""
                <div class="data-display">
                    <h4 style="color:#00E676; margin-top:0;">📅 {t['day_summary']} {search_date_str}</h4>
                    <p style="color:#38bdf8; margin:4px 0;">• Vifaranga Walioingia: <b>{chicks_entered} Kuku</b></p>
                    <p style="color:white; margin:4px 0;">• Gharama ya Vifaranga: <b>{data_found['chicks_cost']:,.1f} TSH</b></p>
                    <p style="color:white; margin:4px 0;">• Gharama ya Chakula: <b>{data_found['feed_cost']:,.1f} TSH</b></p>
                    <p style="color:white; margin:4px 0;">• Gharama ya Dawa: <b>{data_found['med_cost']:,.1f} TSH</b></p>
                    <p style="color:white; margin:4px 0;">• Nyinginezo: <b>{data_found['other_cost']:,.1f} TSH</b></p>
                    <p style="color:#FF5252; margin:4px 0;">• Idadi ya Vifo: <b>{data_found['mortality']} Kuku</b></p>
                    <hr style="border-color:#444; margin:10px 0;">
                    <h5 style="color:#38bdf8; margin:5px 0;">👥 Orodha ya Wateja wa Leo:</h5>
                """, unsafe_allow_html=True)
                
                if data_found["sales_records"]:
                    for r in data_found["sales_records"]:
                        st.markdown(f"""
                        <div class="customer-badge">
                            👤 Mteja: <b>{r['customer']}</b> | Alichukua: <b style="color:#00E676;">{r['qty']} Kuku</b> @ {r['price']:,.0f} TSH (Jumla: {r['revenue']:,.0f} TSH)
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("<span style='color:#AAA;'>Hakuna mteja aliyesajiliwa tarehe hii bado.</span>", unsafe_allow_html=True)
                    
                st.markdown(f"""
                    <hr style="border-color:#444; margin:10px 0;">
                    <p style="color:white; margin:4px 0;">• Jumla ya Kuku Waliouzwa Leo: <b>{day_total_qty} Kuku</b></p>
                    <p style="color:#00E676; font-size:16px; margin:4px 0;">• Jumla ya Mapato ya Leo: <b>{day_total_rev:,.1f} TSH</b></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(t["no_records"])
                
        st.write("<br><br>", unsafe_allow_html=True)
        if st.button("Logout (Ondoka)"):
            st.session_state.logged_in = False
            st.session_state.is_activated = False
            st.session_state.auth_screen = "login"
            st.rerun()

    elif st.session_state.sub_view == "inputs":
        _, center_form, _ = st.columns([1, 2, 1])
        with center_form:
            if st.button(t["back_btn"]): st.session_state.sub_view = "dashboard"; st.rerun()
            
            chosen_date = st.date_input(t["label_date"], value=date.today())
            date_str = str(chosen_date)
            init_date_entry(date_str)
            current_entry = st.session_state.farm_database[date_str]
            
            with st.form(key="inputs_data_capture"):
                st.markdown("<h4 style='color:#38bdf8; margin-top:0;'>🐣 Ingiza Idadi & Gharama za Siku</h4>", unsafe_allow_html=True)
                
                # Uwanja wa Idadi ya vifaranga walioingia bandani leo
                chicks_qty = st.number_input(t["label_chicks_qty"], min_value=0, value=int(current_entry.get("chicks_qty", 0)), step=1)
                
                chicks_cost = st.number_input(t["label_chicks"], value=current_entry["chicks_cost"])
                feeds = st.number_input(t["label_feed"], value=current_entry["feed_cost"])
                meds = st.number_input(t["label_med"], value=current_entry["med_cost"])
                other = st.number_input(t["label_other"], value=current_entry["other_cost"])
                mortality = st.number_input(t["label_mortality"], value=current_entry["mortality"], step=1)
                
                if st.form_submit_button(t["finish_inputs_btn"]):
                    st.session_state.farm_database[date_str].update({
                        "chicks_qty": int(chicks_qty),
                        "chicks_cost": chicks_cost, 
                        "feed_cost": feeds, 
                        "med_cost": meds, 
                        "other_cost": other, 
                        "mortality": int(mortality), 
                        "has_inputs": True
                    })
                    st.success("🎉 Data za gharama na idadi ya kuku zimehifadhiwa!")
                    time.sleep(1.0)
                    st.session_state.sub_view = "dashboard"
                    st.rerun()

    elif st.session_state.sub_view == "withdraw":
        _, center_form, _ = st.columns([1, 2, 1])
        with center_form:
            if st.button(t["back_btn"]): st.session_state.sub_view = "dashboard"; st.rerun()
            
            chosen_date = st.date_input(t["label_date"], value=date.today())
            date_str = str(chosen_date)
            init_date_entry(date_str)
            
            st.markdown("<h3 style='color:#00E676;'>💰 Sajili Mauzo ya Mteja</h3>", unsafe_allow_html=True)
            
            with st.form(key="sales_data_capture", clear_on_submit=True):
                customer_name = st.text_input(t["label_customer"], placeholder="Mfano: Juma, Mama Maria, n.k.")
                qty = st.number_input(t["label_qty"], min_value=1, value=1, step=1)
                price = st.number_input(t["label_price"], value=6500.0)
                
                if st.form_submit_button(t["finish_sales_btn"]):
                    if customer_name.strip() == "":
                        st.error("❌ Tafadhali ingiza Jina la Mteja!")
                    else:
                        revenue = float(qty * price)
                        st.session_state.farm_database[date_str]["sales_records"].append({
                            "customer": customer_name.strip(),
                            "qty": int(qty),
                            "price": price,
                            "revenue": revenue
                        })
                        st.session_state.farm_database[date_str]["has_sales"] = True
                        st.success(f"🎉 Mauzo ya {customer_name} yamehifadhiwa kikamilifu!")
                        time.sleep(1.0)
                        st.session_state.sub_view = "dashboard"
                        st.rerun()
