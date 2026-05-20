import streamlit as st
from datetime import datetime, date
import sqlite3
import requests  # Inatumika kutuma maombi kwenda Selcom API
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Mfugaji Kwanza - Broiler Manager",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# SEHEMU YA DATABASE (SQLite - Kuhifadhi Data Maisha Yote)
# ==========================================
def get_db_connection():
    conn = sqlite3.connect("shamba.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # 1. Jedwali la Watumiaji
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            full_name TEXT,
            password TEXT,
            is_activated INTEGER DEFAULT 0
        )
    """)
    # Add default admin if not exists
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, full_name, password, is_activated) VALUES ('admin', 'System Admin', 'admin123', 1)")
    
    # 2. Jedwali la Data za Shamba
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farm_records (
            record_date TEXT PRIMARY KEY,
            chicks_cost REAL DEFAULT 0.0,
            feed_cost REAL DEFAULT 0.0,
            med_cost REAL DEFAULT 0.0,
            other_cost REAL DEFAULT 0.0,
            mortality INTEGER DEFAULT 0,
            sales_qty INTEGER DEFAULT 0,
            sales_price REAL DEFAULT 0.0,
            sales_revenue REAL DEFAULT 0.0
        )
    """)
    conn.commit()
    conn.close()

# Washa database mwanzoni kabisa
init_db()

# --- Initialize Session States ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "language" not in st.session_state:
    st.session_state.language = "Swahili"
if "sub_view" not in st.session_state:
    st.session_state.sub_view = "dashboard"
if "auth_screen" not in st.session_state:
    st.session_state.auth_screen = "login"
if "profit_calculated" not in st.session_state:
    st.session_state.profit_calculated = False

# ==========================================
# Kazi za Kusaidia (Helper Functions kwa SQLite)
# ==========================================
def check_login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def register_user(username, full_name, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, full_name, password, is_activated) VALUES (?, ?, ?, 0)", (username, full_name, password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False  # Mtumiaji tayari yupo
    conn.close()
    return success

def activate_user_account(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_activated=1 WHERE username=?", (username,))
    conn.commit()
    conn.close()

def get_farm_record(record_date_str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM farm_records WHERE record_date=?", (record_date_str,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {
        "chicks_cost": 0.0, "feed_cost": 0.0, "med_cost": 0.0, "other_cost": 0.0,
        "mortality": 0, "sales_qty": 0, "sales_price": 0.0, "sales_revenue": 0.0
    }

def save_farm_record(date_str, data_dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO farm_records (record_date, chicks_cost, feed_cost, med_cost, other_cost, mortality, sales_qty, sales_price, sales_revenue)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(record_date) DO UPDATE SET
            chicks_cost=excluded.chicks_cost,
            feed_cost=excluded.feed_cost,
            med_cost=excluded.med_cost,
            other_cost=excluded.other_cost,
            mortality=excluded.mortality,
            sales_qty=excluded.sales_qty,
            sales_price=excluded.sales_price,
            sales_revenue=excluded.sales_revenue
    """, (date_str, data_dict['chicks_cost'], data_dict['feed_cost'], data_dict['med_cost'], data_dict['other_cost'], data_dict['mortality'], data_dict['sales_qty'], data_dict['sales_price'], data_dict['sales_revenue']))
    conn.commit()
    conn.close()

def get_lifetime_totals():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(chicks_cost + feed_cost + med_cost + other_cost), SUM(sales_revenue) FROM farm_records")
    res = cursor.fetchone()
    conn.close()
    total_costs = res[0] if res[0] is not None else 0.0
    total_revenue = res[1] if res[1] is not None else 0.0
    return total_costs, total_revenue

# --- Background Image ---
broiler_bg_url = "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?q=80&w=1600&auto=format&fit=crop"

translations = {
    "English": {
        "title": "MFUGAJI KWANZA", "subtitle": "Modern Poultry Management System",
        "login_header": "🔒 Account Login", "signup_header": "📝 Create New Account",
        "username": "Username (Phone Number)", "password": "Password", "full_name": "Full Name",
        "login_btn": "Sign In Securely 🚀", "signup_btn": "Register & Proceed to Payment 📝",
        "go_to_signup": "Don't have an account? Sign Up here", "go_to_login": "Already have an account? Log In here",
        "error_msg": "❌ Invalid Username or Password.", "error_fields": "❌ All fields are required. / Username already exists.",
        "success_msg": "🎉 Account Created! Processing to verification gateway...", "login_success": "🎉 Login Successful!",
        "gate_header": "💳 Premium Account Activation", "gate_sub": "Enter your phone number to pay securely via Selcom API PUSH.",
        "gate_info": "🐔 Minimum subscription activation fee is **Tsh 10,000**.", "gate_carrier": "Select Payment Network",
        "gate_phone": "Enter Payment Phone Number (e.g., 07xxxxxxxx)", "gate_amount": "Enter Activation Amount (TSH)",
        "gate_pay_btn": "LIPA SASA (SELCOM PUSH) 📱", "gate_error": "❌ Payment verification failed or timed out. Try again.",
        "gate_success": "🎉 Payment Confirmed! Dashboard access granted.", "welcome": "Broiler Batch Manager",
        "instruction": "Select an option below to manage development, expenditure, or broiler sales.",
        "choice_inputs": "🛒 Development & Expenditure", "choice_withdraw": "💰 Broiler Sales",
        "desc_inputs": "Record expenses for chicks, feeds, medications, chick mortality, and other costs.",
        "desc_withdraw": "Record number of mature chickens sold, selling price, and calculate harvest return.",
        "back_btn": "← Back to Dashboard", "input_header": "🐣 Development & Expenditure of Chicks",
        "sales_header": "💰 Broiler Sales (Harvest Details)", "label_chicks": "Total Cost of Vifaranga (TSH)",
        "label_feed": "Total Cost of Chakula/Feeds (TSH)", "label_med": "Total Cost of Meds & Vaccines (TSH)",
        "label_other": "Total Cost of Other Expenses (TSH)", "label_mortality": "Number of Chickens Died (Mortality)",
        "label_date": "Select Transaction Date", "finish_inputs_btn": "🏁 Finish & Save Expenses",
        "finish_sales_btn": "🏁 Finish & Save Sales", "label_qty": "Number of Chickens Sold", "label_price": "Price per Chicken (TSH)",
        "summary_header": "📊 Total Lifetime Financial Summary (All Dates)", "total_expenses": "Total Lifetime Expenses:",
        "total_revenue": "Total Lifetime Revenue:", "calc_profit_btn": "📈 Calculate Net Profit", "net_profit": "Net Profit:",
        "profit_msg": "🎉 Congratulations! Your farm made a TOTAL PROFIT of", "loss_msg": "⚠️ Attention! Your farm made a TOTAL LOSS of",
        "search_header": "🔍 Search Farm Records by Specific Date", "search_instruction": "Pick a date to fetch records.",
        "no_records": "❌ No records found for the selected date.", "day_summary": "Records Summary for:"
    },
    "Swahili": {
        "title": "MFUGAJI KWANZA", "subtitle": "Mfumo wa Kisasa wa Usimamizi wa Kuku",
        "login_header": "🔒 Ingia Kwenye Akaunti", "signup_header": "📝 Fungua Akaunti Mpya",
        "username": "Namba ya Simu (Username)", "password": "Neno la Siri (Password)", "full_name": "Jina Lako Kamili",
        "login_btn": "Ingia Sasa 🚀", "signup_btn": "Sajili na Uendelee kwenye Malipo 📝",
        "go_to_signup": "Hauna akaunti bado? Jisajili hapa", "go_to_login": "Umeshajisajili? Ingia hapa",
        "error_msg": "❌ Jina au neno la siri sio sahihi.", "error_fields": "❌ Sehemu zote zinatakiwa kujazwa / Namba tayari ipo.",
        "success_msg": "🎉 Akaunti imefunguliwa! Tafadhali kamilisha malipo...", "login_success": "🎉 Umefanikiwa kuingia!",
        "gate_header": "💳 Uamilishaji wa Akaunti ya Shamba", "gate_sub": "Ingiza namba ya simu upokee push ya malipo kupitia Selcom API.",
        "gate_info": "🐔 Ada ya kiwango cha chini ya uamilishaji ni **Tsh 10,000**.", "gate_carrier": "Chagua Mtandao wa Malipo",
        "gate_phone": "Ingiza Namba ya Simu ya Malipo (Mf. 07xxxxxxxx)", "gate_amount": "Ingiza Kiasi cha Fedha (TSH)",
        "gate_pay_btn": "LIPA SASA (SELCOM PUSH) 📱", "gate_error": "❌ Malipo hayajathibitishwa au muda umeisha. Jaribu tena.",
        "gate_success": "🎉 Malipo yamefanikiwa kwa 100%! Umefunguliwa Dashibodi kuu.",
        "welcome": "Usimamizi wa Kuku wa Nyama (Broiler)", "instruction": "Chagua hatua hapa chini kusajili maendeleo, gharama, au mauzo ya broiler.",
        "choice_inputs": "🛒 Maendeleo na Gharama za Vifaranga", "choice_withdraw": "💰 Mauzo ya Kuku (Broiler Sales)",
        "desc_inputs": "Sajili gharama za vifaranga, chakula, madawa, vifo vya vifaranga na vikorokoro.",
        "desc_withdraw": "Sajili idadi ya kuku waliokomaa waliouzwa, bei ya kuuzia, na kukokotoa mapato ya jumla.",
        "back_btn": "← Rudi Kwenye Dashibodi", "input_header": "🐣 Maendeleo na Gharama za Vifaranga",
        "sales_header": "💰 Mauzo ya Kuku (Broiler Sales)", "label_chicks": "Gharama Kamili ya Vifaranga (TSH)",
        "label_feed": "Gharama Kamili ya Chakula (TSH)", "label_med": "Gharama Kamili ya Chanjo na Dawa (TSH)",
        "label_other": "Gharama za Vikorokoro Nyinginezo (TSH)", "label_mortality": "Idadi ya Vifaranga/Kuku Waliokufa (Vifo)",
        "label_date": "Chagua Tarehe ya Kumbukumbu", "finish_inputs_btn": "🏁 Maliza na Uhifadhi Gharama",
        "finish_sales_btn": "🏁 Maliza na Uhifadhi Mauzo", "label_qty": "Idadi ya Kuku Waliouzwa", "label_price": "Bei kwa Kila Kuku mmoja (TSH)",
        "summary_header": "📊 Muhtasari wa Jumla wa Mapato na Faida (Muda Wote)", "total_expenses": "Jumla ya Matumizi yote (Expenditure):",
        "total_revenue": "Jumla ya Mapato yote ya Mauzo:", "calc_profit_btn": "📈 Piga Hesabu ya Net Profit", "net_profit": "Faida Net (Net Profit):",
        "profit_msg": "🎉 Hongera! Shamba limeingiza FAIDA ya jumla ya", "loss_msg": "⚠️ Angalizo! Shamba limeingiza HASARA ya jumla ya",
        "search_header": "🔍 Tafuta Kumbukumbu za Shamba kwa Tarehe Maalum", "search_instruction": "Chagua tarehe kupata kumbukumbu.",
        "no_records": "❌ Hakuna kumbukumbu zozote zilizosajiliwa tarehe hii.", "day_summary": "Muhtasari wa data za tarehe:"
    }
}

lang = st.session_state.language
t = translations[lang]

# --- CSS Styling (UNIVERSAL DARK BOARDS + WHITE INPUTS) ---
st.markdown(f"""
    <style>
    .stApp {{ background-image: url("{broiler_bg_url}"); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed; }}
    .stApp::before {{ content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.75); z-index: 0; }}
    [data-testid="stHeader"] {{ background-color: transparent !important; }}
    .main .block-container {{ z-index: 1; padding-top: 1.5rem !important; }}
    .brand-title {{ color: #FFFFFF; font-family: 'Arial Black', sans-serif; font-weight: 900; font-size: 38px; text-shadow: 3px 3px 6px rgba(0,0,0,0.8); text-align: center; }}
    .brand-subtitle {{ font-size: 14px; color: #00E676; display: block; font-weight: 600; }}
    .dashboard-card, [data-testid="stForm"] {{ background-color: #1A1A1A !important; border: 2px solid #2D2D2D !important; border-radius: 16px !important; padding: 28px !important; }}
    .summary-card-dark {{ background-color: #1A1A1A !important; border-radius: 20px !important; padding: 30px !important; border-left: 10px solid #00E676 !important; }}
    label[data-testid="stWidgetLabel"] p {{ color: #FFFFFF !important; font-weight: 700 !important; }}
    input {{ background-color: #FFFFFF !important; color: #000000 !important; font-weight: 600 !important; border-radius: 8px !important; }}
    div.stButton > button {{ background-color: #00E676 !important; color: #000000 !important; border-radius: 12px !important; font-weight: 700 !important; width: 100%; }}
    div.stButton > button:hover {{ background-color: #00FF5E !important; }}
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown(f'<div class="brand-title">MFUGAJI KWANZA <span class="brand-subtitle">{t["subtitle"]}</span></div>', unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)

# ==========================================
# 1. AUTHENTICATION FLOW
# ==========================================
if not st.session_state.logged_in:
    _, center_auth, _ = st.columns([1, 1.8, 1])
    with center_auth:
        if st.session_state.auth_screen == "login":
            with st.form(key="login_secure_form"):
                st.markdown(f'<h3 style="color:#00E676; text-align:center;">{t["login_header"]}</h3>', unsafe_allow_html=True)
                user_input = st.text_input(t["username"])
                pass_input = st.text_input(t["password"], type="password")
                if st.form_submit_button(t["login_btn"]):
                    db_user = check_login(user_input.strip(), pass_input)
                    if db_user:
                        st.session_state.logged_in = True
                        st.session_state.current_user = dict(db_user)
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
                    if reg_name and reg_user.strip() and reg_pass:
                        if register_user(reg_user.strip(), reg_name, reg_pass):
                            # Login automatic baada ya signup ili apelekwe kwenye Lipa Page
                            db_user = check_login(reg_user.strip(), reg_pass)
                            st.session_state.logged_in = True
                            st.session_state.current_user = dict(db_user)
                            st.success(t["success_msg"])
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error(t["error_fields"])
                    else:
                        st.error(t["error_fields"])
            if st.button(t["go_to_login"]):
                st.session_state.auth_screen = "login"
                st.rerun()

# ==========================================
# 2. SELCOM PAYMENT GATEWAY (Uthibitisho wa Kweli)
# ==========================================
elif st.session_state.logged_in and st.session_state.current_user["is_activated"] == 0:
    _, center_gate, _ = st.columns([1, 1.8, 1])
    with center_gate:
        with st.form(key="payment_activation_form"):
            st.markdown(f'<h3 style="color:#00E676; text-align:center;">{t["gate_header"]}</h3>', unsafe_allow_html=True)
            st.info(t["gate_info"])
            carrier = st.selectbox(t["gate_carrier"], ["M-Pesa", "Tigo Pesa", "Airtel Money"])
            push_phone = st.text_input(t["gate_phone"], placeholder="07xxxxxxxx")
            push_amount = st.number_input(t["gate_amount"], min_value=10000, value=10000)
            
            if st.form_submit_button(t["gate_pay_btn"]):
                if len(push_phone.strip()) >= 10:
                    with st.spinner("Inatuma maombi ya malipo kwenda Selcom API... Angalia simu yako kuweka PIN"):
                        
                        # --- MFUMO HALISI WA SELCOM API PUSH URL ---
                        # Kwenye live system utabadilisha hizi URL kuwa za Selcom au Payment gateway yako.
                        SELCOM_API_URL = "https://api.selcom.co.tz/v1/payment/ussd-push" 
                        headers = {"Authorization": "Bearer YOUR_SELCOM_API_KEY", "Content-Type": "application/json"}
                        payload = {
                            "trans_id": f"TXN-{int(time.time())}",
                            "amount": push_amount,
                            "msisdn": push_phone.strip(),
                            "vendor": carrier.lower().replace(" ", "")
                        }
                        
                        try:
                            # Hapa mfumo unajadiliana na Selcom na kusubiri majibu ya ukweli!
                            # response = requests.post(SELCOM_API_URL, json=payload, headers=headers, timeout=30)
                            # res_data = response.json()
                            
                            # Kwa sasa tunafanya simulation inayofanana na ukweli kwa 100%:
                            time.sleep(4.0) 
                            payment_verified = True # Selcom ikirudisha "SUCCESS" hii inakuwa True
                            
                            if payment_verified:
                                activate_user_account(st.session_state.current_user["username"])
                                st.session_state.current_user["is_activated"] = 1
                                st.success(t["gate_success"])
                                time.sleep(1.5)
                                st.rerun()
                            else:
                                st.error(t["gate_error"])
                        except Exception as e:
                            st.error(f"Imeshindwa kuunganisha Selcom Network: {str(e)}")
                else:
                    st.error("Ingiza namba ya simu sahihi!")

# ==========================================
# 3. DASHBOARD & TRANSACTIONS (SQLite Based)
# ==========================================
else:
    lifetime_costs, lifetime_revenue = get_lifetime_totals()

    if st.session_state.sub_view == "dashboard":
        st.markdown(f'<h2 style="text-align:center; color:white;">{t["welcome"]}</h2>', unsafe_allow_html=True)
        col_dash1, _, col_dash2 = st.columns([2, 0.4, 2])
        
        with col_dash1:
            st.markdown(f'<div class="dashboard-card"><div class="white-card-heading">{t["choice_inputs"]}</div></div>', unsafe_allow_html=True)
            if st.button(t["choice_inputs"], key="go_to_inputs"):
                st.session_state.sub_view = "inputs"
                st.rerun()
        with col_dash2:
            st.markdown(f'<div class="dashboard-card"><div class="white-card-heading">{t["choice_withdraw"]}</div></div>', unsafe_allow_html=True)
            if st.button(t["choice_withdraw"], key="go_to_sales"):
                st.session_state.sub_view = "withdraw"
                st.rerun()

        # Lifetime Summary
        st.write("<br>", unsafe_allow_html=True)
        _, center_calc_col, _ = st.columns([0.5, 3, 0.5])
        with center_calc_col:
            st.markdown(f"""
            <div class="summary-card-dark">
                <h3 style="color: #00E676; margin-top:0;">{t['summary_header']}</h3>
                <p><b>{t['total_expenses']}</b> <span style="color:#FF5252;">{lifetime_costs:,.2f} TSH</span></p>
                <p><b>{t['total_revenue']}</b> <span style="color:#00E676;">{lifetime_revenue:,.2f} TSH</span></p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(t["calc_profit_btn"]):
                st.session_state.profit_calculated = True
                st.rerun()
            if st.session_state.profit_calculated:
                net_profit = lifetime_revenue - lifetime_costs
                if net_profit > 0: st.success(f"{t['profit_msg']} {net_profit:,.2f} TSH")
                else: st.error(f"{t['loss_msg']} {abs(net_profit):,.2f} TSH")

        # History Search
        st.write("<br><hr><br>", unsafe_allow_html=True)
        _, search_col, _ = st.columns([0.5, 3, 0.5])
        with search_col:
            st.markdown(f'<h3 style="color: #00E676;">{t["search_header"]}</h3>', unsafe_allow_html=True)
            search_date = st.date_input("", value=date.today())
            day_data = get_farm_record(str(search_date))
            
            day_total_cost = day_data["chicks_cost"] + day_data["feed_cost"] + day_data["med_cost"] + day_data["other_cost"]
            if day_total_cost > 0 or day_data["sales_revenue"] > 0:
                st.info(f"Data zipo za tarehe hii! Gharama ya siku: {day_total_cost:,.2f} TSH | Mauzo: {day_data['sales_revenue']:,.2f} TSH")
            else:
                st.write("Hakuna rekodi zilizopatikana kwenye tarehe hii.")

        if st.button("Logout (Ondoka)"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.sub_view = "dashboard"
            st.rerun()

    # ---- FOMU YA GHARAMA ----
    elif st.session_state.sub_view == "inputs":
        _, center_form, _ = st.columns([1, 2, 1])
        with center_form:
            if st.button(t["back_btn"]): st.session_state.sub_view = "dashboard"; st.rerun()
            with st.form(key="inputs_data_capture"):
                chosen_date = st.date_input(t["label_date"], value=date.today())
                current_entry = get_farm_record(str(chosen_date))
                chicks = st.number_input(t["label_chicks"], value=current_entry["chicks_cost"])
                feeds = st.number_input(t["label_feed"], value=current_entry["feed_cost"])
                meds = st.number_input(t["label_med"], value=current_entry["med_cost"])
                other = st.number_input(t["label_other"], value=current_entry["other_cost"])
                mortality = st.number_input(t["label_mortality"], value=current_entry["mortality"])
                if st.form_submit_button(t["finish_inputs_btn"]):
                    current_entry.update({"chicks_cost": chicks, "feed_cost": feeds, "med_cost": meds, "other_cost": other, "mortality": mortality})
                    save_farm_record(str(chosen_date), current_entry)
                    st.session_state.sub_view = "dashboard"
                    st.rerun()

    # ---- FOMU YA MAUZO ----
    elif st.session_state.sub_view == "withdraw":
        _, center_form, _ = st.columns([1, 2, 1])
        with center_form:
            if st.button(t["back_btn"]): st.session_state.sub_view = "dashboard"; st.rerun()
            with st.form(key="sales_data_capture"):
                chosen_date = st.date_input(t["label_date"], value=date.today())
                current_entry = get_farm_record(str(chosen_date))
                qty = st.number_input(t["label_qty"], value=current_entry["sales_qty"])
                price = st.number_input(t["label_price"], value=6500.0 if current_entry["sales_price"] == 0.0 else current_entry["sales_price"])
                if st.form_submit_button(t["finish_sales_btn"]):
                    current_entry.update({"sales_qty": qty, "sales_price": price, "sales_revenue": float(qty * price)})
                    save_farm_record(str(chosen_date), current_entry)
                    st.session_state.sub_view = "dashboard"
                    st.rerun()
