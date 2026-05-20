import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- Must be the first Streamlit command ---
st.set_page_config(
    page_title="Mfugaji Kwanza",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Initialize session states safely ---
if "language" not in st.session_state:
    st.session_state.language = "English"

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "landing"

# Kumbukumbu ya data ya mauzo na tarehe kama mwanzo
if "sales_data" not in st.session_state:
    st.session_state.sales_data = [
        {"Tarehe": "2026-05-18 09:30", "Aina": "Mayai", "Kiasi": "Tray 10", "Mapato (Tsh)": 85000},
        {"Tarehe": "2026-05-19 14:15", "Aina": "Kuku wa Nyama", "Kiasi": "Kuku 20", "Mapato (Tsh)": 240000},
    ]

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
        "subtext_login": "Enter your security credentials to open dashboard",
        "phone_label": "Phone Number or Email",
        "pass_label": "Password",
        "proceed_btn": "Open Dashboard",
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
        "subtext_login": "Ingiza namba na nenosiri kufungua dashibodi",
        "phone_label": "Namba ya Simu au Barua Pepe",
        "pass_label": "Nenosiri",
        "proceed_btn": "Fungua Dashibodi",
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
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 0;
    }}
    [data-testid="stHeader"] {{
        background-color: transparent !important;
        z-index: 10;
    }}
    .main .block-container {{
        z-index: 1;
        padding-top: 4rem !important;
    }}
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
    
    /* BOX KUU LA FOMU ZA LOGIN/SIGNUP/MALIPO */
    div[data-testid="stForm"] {{
        background-color: #FFFFFF !important;
        border: none !important;
        border-radius: 20px !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6) !important;
        padding: 40px !important;
        max-width: 520px !important;
        margin: auto !important;
    }}
    
    /* DASHBOARD CARD */
    .dashboard-card {{
        background-color: #FFFFFF !important;
        border-radius: 20px !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6) !important;
        padding: 35px !important;
        margin-top: 10px;
    }}

    .green-heading {{
        color: #16300B !important;
        font-weight: 800 !important;
        font-size: 26px !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        text-align: center !important;
        margin-bottom: 8px !important;
    }}
    .card-subtext {{
        color: #555555 !important;
        font-size: 15px !important;
        text-align: center !important;
        margin-bottom: 20px !important;
    }}
    label[data-testid="stWidgetLabel"] p {{
        color: #16300B !important;
        font-weight: 700 !important;
    }}
    
    /* ELECTRIC GLOWING BUTTONS */
    button[kind="formSubmit"], button[data-testid="baseButton-secondary"] {{
        background-color: #00E676 !important; 
        color: #000000 !important;          
        border-radius: 12px !important;       
        border: none !important;
        padding: 10px 20px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        box-shadow: 0 0 12px rgba(0, 230, 118, 0.6) !important;
    }}
    button[kind="formSubmit"]:hover, button[data-testid="baseButton-secondary"]:hover {{
        background-color: #00FF5E !important; 
        box-shadow: 0 0 20px rgba(0, 230, 118, 0.9) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 1. Brand Logo on Top LEFT
st.markdown(f"""
    <div class="brand-title">
        MFUGAJI KWANZA
        <span class="brand-subtitle">{t['subtitle']}</span>
    </div>
""", unsafe_allow_html=True)

st.write("<br><br>", unsafe_allow_html=True)

# --- CORE ROUTER ARCHITECTURE ---

if st.session_state.auth_mode == "view_dashboard":
    # Dashibodi Kuu baada ya KULIPIA au ku-LOG IN
    st.markdown("""
        <div class="dashboard-card">
            <div class="green-heading">📊 Dashibodi Kuu ya Shamba (Sales & Development)</div>
            <div class="card-subtext" style="text-align: center;">Usimamizi wa Maendeleo ya kuku na Mauzo katika sehemu moja</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    
    dash_col1, dash_col2 = st.columns([1.1, 0.9], gap="large")
    
    with dash_col1:
        st.markdown("""
            <div class="dashboard-card">
                <h3 style="color: #16300B; margin-top:0;">📈 Ripoti ya Maendeleo (Development)</h3>
                <p style="color: #666;">Mwelekeo wa takwimu na rekodi za ukuaji wa mradi wako.</p>
            </div>
        """, unsafe_allow_html=True)
        
        df_sales = pd.DataFrame(st.session_state.sales_data)
        jumla_mapato = df_sales["Mapato (Tsh)"].sum()
        
        st.write("")
        st.metric(label="📈 Jumla ya Mapato ya Mauzo", value=f"Tsh {jumla_mapato:,}")
        st.metric(label="🐣 Hali ya Mradi (Afya)", value="Salama (98%)")
        
        st.write("<br>**Kumbukumbu ya Tarehe za Mauzo yaliyopita:**", unsafe_allow_html=True)
        st.dataframe(df_sales, use_container_width=True, hide_index=True)

    with dash_col2:
        st.markdown("""
            <div class="dashboard-card">
                <h3 style="color: #16300B; margin-top:0;">🐔 Sajili Mauzo Mapya (Sales)</h3>
                <p style="color: #666;">Ingiza mauzo ya kuku au mayai yaliyofanyika sasa hivi.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        aina_zao = st.selectbox("Zao Lililouzwa", ["Mayai", "Kuku wa Nyama", "Kuku wa Kienyeji", "Mbolea"])
        kiasi_kilichouzwa = st.text_input("Kiasi (Mf. Kuku 15 au Tray 5)")
        pesa_iliyopatikana = st.number_input("Pesa Zilizopatikana (Tsh)", min_value=0, step=1000)
        
        st.write("<br>", unsafe_allow_html=True)
        if st.button("Hifadhi Mauzo Relasi", use_container_width=True):
            if kiasi_kilichouzwa and pesa_iliyopatikana > 0:
                muda_sasa = datetime.now().strftime('%Y-%m-%d %H:%M')
                st.session_state.sales_data.append({
                    "Tarehe": muda_sasa,
                    "Aina": aina_zao,
                    "Kiasi": kiasi_kilichouzwa,
                    "Mapato (Tsh)": pesa_iliyopatikana
                })
                st.success(f"🎉 Muamala wa mauzo ya {aina_zao} umehifadhiwa kiotomatiki tarehe {muda_sasa}!")
                st.rerun()
            else:
                st.error("Tafadhali jaza kiasi na kiasi cha pesa kilichopatikana!")
                
    st.write("<br><br>", unsafe_allow_html=True)
    if st.button("← Log Out (Ondoka)", use_container_width=False):
        st.session_state.auth_mode = "landing"
        st.rerun()

else:
    _, center_col, _ = st.columns([1, 1.4, 1])
    
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
                            st.session_state.auth_mode = "view_dashboard"
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
                            st.session_state.auth_mode = "view_miamala"
                            st.rerun()
                        else:
                            st.error(t["error_fields"])
                with btn_col2:
                    if st.form_submit_button(t["back_btn"], use_container_width=True):
                        st.session_state.auth_mode = "landing"
                        st.rerun()

        # ========================================================
        # UPDATE MPYA: GATEWAY YA PUSH MALIPO (HELA + NAMBA)
        # ========================================================
        elif st.session_state.auth_mode == "view_miamala":
            with st.form(key="payment_gateway_form"):
                st.markdown('<div class="green-heading">💳 Malipo ya Akaunti</div>', unsafe_allow_html=True)
                st.markdown('<div class="card-subtext">Weka kiasi na namba ya simu ili kuamsha akaunti yako moja kwa moja.</div>', unsafe_allow_html=True)
                
                st.info("🐔 Ada ya kiwango cha chini ya uamilishaji ni **Tsh 10,000**.")
                
                njia_malipo = st.selectbox("Chagua Mtandao", ["M-Pesa", "Tigo Pesa", "Airtel Money", "Halo Pesa"])
                namba_ya_simu = st.text_input("Ingiza Namba ya Simu ya Malipo (Mf. 07xxxxxxxx)")
                kiasi_hapa = st.number_input("Ingiza Kiasi cha Fedha (Tsh)", min_value=10000, value=10000, step=1000)
                
                st.write("")
                
                if st.form_submit_button("LIPA SASA (PUSH PAYMENT)", use_container_width=True):
                    if len(namba_ya_simu) >= 10 and kiasi_hapa >= 10000:
                        # Simulering ya Push API
                        with st.spinner("Inatengeneza muunganisho wa mtandao... Tafadhali weka PIN ya siri kwenye simu yako."):
                            time.sleep(3.5) # Inasubiri sekunde 3 kama notification ya simu
                        
                        st.success("🎉 Malipo yamefanikiwa kwa 100%! Umefunguliwa access ya Dashibodi.")
                        time.sleep(1.5)
                        
                        # Inamuingiza moja kwa moja kwenye Dashibodi Kuu sasa hivi bila kudai ID
                        st.session_state.auth_mode = "view_dashboard"
                        st.rerun()
                    else:
                        st.error("Tafadhali hakikisha namba ya simu imekamilika na kiasi kiko sahihi!")
