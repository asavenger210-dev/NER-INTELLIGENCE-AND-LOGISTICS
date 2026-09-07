import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import sqlite3
import os
from datetime import datetime
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
import hashlib
import secrets
# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="NER Logistics Intelligence (SIH 26002)",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======# =========================================================
# LOGIN SYSTEM
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "login_page" not in st.session_state:
    st.session_state.login_page = "home"
# =========================================================
# USER ACCOUNT DATABASE
# =========================================================

USER_DB = "users.db"


def init_user_database():
    conn = sqlite3.connect(USER_DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password, stored_password):
    try:
        salt, saved_hash = stored_password.split("$", 1)

        check_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            100000
        ).hex()

        return secrets.compare_digest(check_hash, saved_hash)

    except ValueError:
        return False


def create_user(username, password):
    conn = sqlite3.connect(USER_DB)

    try:
        conn.execute(
            """
            INSERT INTO users
            (username, password_hash, created_at)
            VALUES (?, ?, ?)
            """,
            (
                username,
                hash_password(password),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def authenticate_user(username, password):
    conn = sqlite3.connect(USER_DB)

    row = conn.execute(
        "SELECT password_hash FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    conn.close()

    if row:
        return verify_password(password, row[0])

    return False


init_user_database()


# ---------------------------------------------------------
# LOGIN PAGE
# ---------------------------------------------------------

if not st.session_state.logged_in:

    st.markdown("""
        <h1 style="text-align:center;">
            🚚 NER Smart Logistics
        </h1>
        <p style="text-align:center;">
            AI-Powered Logistics & Accessibility Intelligence
        </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    # USER
    with col1:
        st.subheader("👤 User")
        st.write("Access logistics tools, maps and reporting.")

        if st.button("👤 User Login", use_container_width=True):
            st.session_state.login_page = "user"

    # ADMIN
    with col2:
        st.subheader("👨‍💼 Admin")
        st.write("Manage reports, users and logistics intelligence.")

        if st.button("👨‍💼 Admin Login", use_container_width=True):
            st.session_state.login_page = "admin"


    # -----------------------------------------------------
        # USER LOGIN FORM
    # -----------------------------------------------------

        if st.session_state.login_page == "user":

            st.markdown("---")
            st.subheader("👤 User Login")

            user_mode = st.radio(
        "Account",
        ["🔐 Login", "📝 Sign Up"],
        horizontal=True
    )


         # -----------------------------------------------------
# USER LOGIN FORM
# -----------------------------------------------------

        if st.session_state.login_page == "user":

         st.markdown("---")
         st.subheader("👤 User Login")

    user_mode = st.radio(
        "Account",
        ["🔐 Login", "📝 Sign Up"],
        horizontal=True,
        key="user_account_mode"
    )

    if user_mode == "🔐 Login":

        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "🔐 LOGIN AS USER",
            use_container_width=True
        ):

            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.role = "user"
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    else:

        new_username = st.text_input("Create Username")
        new_password = st.text_input(
            "Create Password",
            type="password"
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button(
            "📝 CREATE ACCOUNT",
            use_container_width=True
        ):

            if not new_username or not new_password:
                st.warning("⚠️ Fill all fields.")

            elif new_password != confirm_password:
                st.error("❌ Passwords do not match.")

            elif create_user(new_username, new_password):
                st.success("✅ Account created!")
                st.info("Now switch to Login.")

            else:
                st.error("❌ Username already exists.")
# -----------------------------------------------------
# ADMIN LOGIN FORM
# -----------------------------------------------------

    if st.session_state.login_page == "admin":    

       st.markdown("---")
       st.subheader("👨‍💼 Admin Login")

    admin_username = st.text_input(
        "Admin Username",
        key="admin_username"
    )

    admin_password = st.text_input(
        "Admin Password",
        type="password",
        key="admin_password"
    )

    if st.button(
        "🔐 LOGIN AS ADMIN",
        use_container_width=True
    ):

        if admin_username == "admin" and admin_password == "admin123":

            st.session_state.logged_in = True
            st.session_state.role = "admin"

            st.success("✅ Admin Login Successful!")
            st.rerun()

        else:
            st.error("❌ Invalid admin username or password")
    
    # STOP DASHBOARD FROM LOADING
    st.stop()
#===================================================
# FUTURISTIC COMMAND CENTER CSS & DESIGN TOKENS
# =========================================================

COMMAND_CENTER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800;900&family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-base: #060913;
    --bg-surface: #0b1120;
    --bg-card: rgba(15, 23, 42, 0.75);
    --bg-card-hover: rgba(22, 34, 61, 0.85);
    --border-dim: rgba(56, 189, 248, 0.15);
    --border-neon: rgba(0, 242, 254, 0.4);
    --border-glow: 0 0 15px rgba(0, 242, 254, 0.2);
    --accent-cyan: #00f2fe;
    --accent-blue: #38bdf8;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
    --accent-rose: #f43f5e;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
}

/* Background & Core Typography */
.stApp {
    background: radial-gradient(circle at 50% 0%, #0e1c38 0%, #060913 70%) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Futuristic Scanline Effect Overlay */
.stApp::before {
    content: " ";
    display: block;
    position: fixed;
    top: 0; left: 0; bottom: 0; right: 0;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 255, 0, 0.03));
    z-index: 999;
    background-size: 100% 3px, 6px 100%;
    pointer-events: none;
    opacity: 0.35;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #090e1a 0%, #060913 100%) !important;
    border-right: 1px solid var(--border-dim) !important;
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    font-family: 'Rajdhani', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    color: var(--accent-cyan) !important;
}

/* Top Command Header */
.command-header {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(11, 17, 32, 0.95) 100%);
    border: 1px solid var(--border-neon);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 22px 28px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px);
}

.command-header::after {
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 3px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), var(--accent-emerald), transparent);
}

.header-top-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--accent-blue);
    letter-spacing: 1.5px;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.header-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.85rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 2px;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 14px;
    text-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
}

.header-subtitle {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.05rem;
    color: var(--text-secondary);
    letter-spacing: 1px;
    margin-top: 6px;
    margin-bottom: 0;
}

.status-beacon {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: #10b981;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
}

.beacon-dot {
    width: 8px;
    height: 8px;
    background: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 10px #10b981;
    animation: pulse-beacon 2s infinite;
}

@keyframes pulse-beacon {
    0% { transform: scale(0.9); opacity: 0.8; }
    50% { transform: scale(1.3); opacity: 1; box-shadow: 0 0 14px #10b981; }
    100% { transform: scale(0.9); opacity: 0.8; }
}

/* KPI Telemetry Grid */
.telemetry-card {
    background: var(--bg-card);
    border: 1px solid var(--border-dim);
    border-radius: 10px;
    padding: 16px 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    position: relative;
    transition: all 0.25s ease;
    backdrop-filter: blur(10px);
}

.telemetry-card:hover {
    border-color: var(--accent-cyan);
    box-shadow: 0 6px 24px rgba(0, 242, 254, 0.15);
    transform: translateY(-2px);
}

.telemetry-card::before {
    content: "";
    position: absolute;
    top: 0; left: 15%; width: 70%; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
}

.telemetry-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.telemetry-value {
    font-family: 'Orbitron', monospace;
    font-size: 1.75rem;
    font-weight: 800;
    color: #ffffff;
    margin: 6px 0 2px 0;
    text-shadow: 0 0 12px rgba(255, 255, 255, 0.2);
}

.telemetry-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
}

.badge-cyan { background: rgba(0, 242, 254, 0.12); color: var(--accent-cyan); border: 1px solid rgba(0, 242, 254, 0.3); }
.badge-rose { background: rgba(244, 63, 94, 0.12); color: var(--accent-rose); border: 1px solid rgba(244, 63, 94, 0.3); }
.badge-amber { background: rgba(245, 158, 11, 0.12); color: var(--accent-amber); border: 1px solid rgba(245, 158, 11, 0.3); }
.badge-emerald { background: rgba(16, 185, 129, 0.12); color: var(--accent-emerald); border: 1px solid rgba(16, 185, 129, 0.3); }

/* Tactical Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(11, 17, 32, 0.8) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 10px !important;
    padding: 6px 8px !important;
    gap: 8px !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
    padding: 10px 18px !important;
    border-radius: 8px !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    transition: all 0.2s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
    border-color: rgba(56, 189, 248, 0.2) !important;
    background: rgba(56, 189, 248, 0.05) !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0, 242, 254, 0.15), rgba(56, 189, 248, 0.08)) !important;
    border: 1px solid var(--border-neon) !important;
    color: var(--accent-cyan) !important;
    box-shadow: 0 0 16px rgba(0, 242, 254, 0.2) !important;
}

/* Glass Panels & HUD Frames */
.hud-glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border-dim);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.4);
    margin-bottom: 18px;
    backdrop-filter: blur(12px);
    position: relative;
}

.hud-panel-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--accent-cyan);
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Map HUD Wrapper */
.map-hud-frame {
    border: 1px solid var(--border-neon);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 0 25px rgba(0, 0, 0, 0.6), inset 0 0 15px rgba(0, 242, 254, 0.08);
    position: relative;
}

.map-hud-header {
    background: rgba(11, 17, 32, 0.95);
    border-bottom: 1px solid var(--border-dim);
    padding: 10px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-secondary);
}

/* Tactical Alert Banner */
.tactical-alert-container {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid var(--accent-rose);
    box-shadow: 0 0 25px rgba(239, 68, 68, 0.35);
    border-radius: 10px;
    padding: 18px 22px;
    margin-bottom: 22px;
    animation: alert-glow 3s infinite;
}

@keyframes alert-glow {
    0% { border-color: rgba(244, 63, 94, 0.4); }
    50% { border-color: rgba(244, 63, 94, 1); box-shadow: 0 0 30px rgba(244, 63, 94, 0.5); }
    100% { border-color: rgba(244, 63, 94, 0.4); }
}

.alert-header-row {
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #ff4d6d;
    margin-bottom: 8px;
}

.alert-meta-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: var(--text-secondary);
    background: rgba(0, 0, 0, 0.3);
    padding: 10px 14px;
    border-radius: 6px;
    margin-top: 8px;
    margin-bottom: 12px;
}

/* Futuristic Buttons */
.stButton > button {
    background: linear-gradient(135deg, rgba(14, 28, 54, 0.9) 0%, rgba(10, 18, 38, 0.95) 100%) !important;
    color: #ffffff !important;
    border: 1px solid var(--border-neon) !important;
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.98rem !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 242, 254, 0.1) !important;
    transition: all 0.25s ease !important;
}

.stButton > button:hover {
    border-color: var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
    box-shadow: 0 0 20px rgba(0, 242, 254, 0.4), inset 0 0 15px rgba(0, 242, 254, 0.2) !important;
    transform: translateY(-1px) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0284c7 0%, #00f2fe 100%) !important;
    color: #060913 !important;
    border: none !important;
    font-weight: 800 !important;
    box-shadow: 0 0 20px rgba(0, 242, 254, 0.5) !important;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #38bdf8 0%, #00f2fe 100%) !important;
    box-shadow: 0 0 28px rgba(0, 242, 254, 0.8) !important;
}

/* Metric Widgets Styling */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    color: var(--text-secondary) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.45rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
}

/* Responsive Overrides */
@media (max-width: 768px) {
    .header-title { font-size: 1.3rem; }
    .command-header { padding: 16px; }
    .telemetry-value { font-size: 1.3rem; }
    .alert-meta-grid { grid-template-columns: 1fr; }
}
</style>
"""

st.markdown(COMMAND_CENTER_CSS, unsafe_allow_html=True)

# =========================================================
# AI MODEL CACHING & TRAINING
# XGBOOST RISK PREDICTOR (PRESERVED BACKEND)
# =========================================================

@st.cache_resource
def load_trained_risk_model():
    np.random.seed(42)
    n_samples = 1500

    data = {
        "rainfall_mm": np.random.uniform(10, 350, n_samples),
        "soil_moisture": np.random.uniform(20, 95, n_samples),
        "slope_degrees": np.random.uniform(5, 65, n_samples),
        "historical_landslide_freq": np.random.poisson(1, n_samples),
    }

    df = pd.DataFrame(data)

    risk_rule = (
        (df["rainfall_mm"] > 180).astype(int) * 0.4
        + (df["soil_moisture"] > 80).astype(int) * 0.3
        + (df["slope_degrees"] > 40).astype(int) * 0.3
    )

    df["disruption_risk"] = (
        risk_rule
        + np.random.normal(0, 0.1, n_samples)
        > 0.5
    ).astype(int)

    X = df[
        [
            "rainfall_mm",
            "soil_moisture",
            "slope_degrees",
            "historical_landslide_freq",
        ]
    ]

    y = df["disruption_risk"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)
    return model

# Load trained AI model
ml_risk_model = load_trained_risk_model()

# =========================================================
# SQLITE DATABASE (PRESERVED BACKEND)
# =========================================================

DB_NAME = "field_reports.db"
IMAGE_FOLDER = "field_report_images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS field_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT,
            description TEXT,
            latitude REAL,
            longitude REAL,
            report_time TEXT,
            image_path TEXT
        )
    """)
    conn.commit()
    conn.close()

init_database()

# =========================================================
# ALERT NOTIFICATION SYSTEM (PRESERVED BACKEND)
# =========================================================

def get_latest_report():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            id,
            incident_type,
            description,
            latitude,
            longitude,
            report_time,
            image_path
        FROM field_reports
        ORDER BY id DESC
        LIMIT 1
    """)
    report = cursor.fetchone()
    conn.close()
    return report

def get_latest_report_id():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM field_reports")
    result = cursor.fetchone()
    conn.close()
    if result and result[0] is not None:
        return result[0]
    return 0

# =========================================================
# INITIALIZE NOTIFICATION STATE
# =========================================================

if "last_seen_report_id" not in st.session_state:
    st.session_state.last_seen_report_id = get_latest_report_id()

if "new_report_alert" not in st.session_state:
    st.session_state.new_report_alert = None

# =========================================================
# LIVE ALERT CHECK (MODERNIZED TACTICAL HUD UI)
# =========================================================

@st.fragment(run_every=5)
def live_alert_notification():
    latest_report = get_latest_report()
    if latest_report is None:
        return

    (
        report_id,
        report_type,
        report_description,
        report_latitude,
        report_longitude,
        report_time,
        report_image
    ) = latest_report

    if report_id > st.session_state.last_seen_report_id:
        st.session_state.last_seen_report_id = report_id
        st.session_state.new_report_alert = {
            "id": report_id,
            "type": report_type,
            "description": report_description,
            "lat": report_latitude,
            "lon": report_longitude,
            "time": report_time
        }

    if st.session_state.new_report_alert:
        alert = st.session_state.new_report_alert
        st.markdown(
            f"""
            <div class="tactical-alert-container">
                <div class="alert-header-row">
                    <span style="font-size: 1.4rem;">🚨</span>
                    <span>TACTICAL INCIDENT DISPATCH • REPORT #{alert['id']}</span>
                    <span style="margin-left: auto; font-size: 0.75rem; background: rgba(244,63,94,0.3); border: 1px solid #f43f5e; padding: 2px 8px; border-radius: 4px; font-family: 'JetBrains Mono', monospace;">PRIORITY HAZARD</span>
                </div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 6px;">
                    {alert['type']}
                </div>
                <div class="alert-meta-grid">
                    <div>📍 <b>COORDINATES:</b> {alert['lat']:.6f}, {alert['lon']:.6f}</div>
                    <div>🕒 <b>TIMESTAMP:</b> {alert['time']}</div>
                    <div>📡 <b>STATUS:</b> BROADCAST ACTIVE</div>
                </div>
                <div style="font-size: 0.92rem; color: #cbd5e1; margin-bottom: 8px;">
                    <b>Field Intelligence:</b> {alert['description']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        ack_col1, ack_col2 = st.columns([1, 4])
        with ack_col1:
            if st.button("✅ ACKNOWLEDGE ALERT", key=f"mark_alert_{alert['id']}"):
                st.session_state.new_report_alert = None
                st.rerun()

# Execute top alert check
live_alert_notification()

# =========================================================
# SAVE FIELD REPORT (PRESERVED BACKEND)
# =========================================================

def save_field_report(
    incident_type,
    description,
    latitude,
    longitude,
    report_time,
    image_file
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    image_path = ""

    if image_file is not None:
        original_name = image_file.name
        if "." in original_name:
            extension = original_name.rsplit(".", 1)[1].lower()
        else:
            extension = "jpg"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        image_filename = f"incident_{timestamp}.{extension}"
        image_path = os.path.join(IMAGE_FOLDER, image_filename)

        with open(image_path, "wb") as file:
            file.write(image_file.getvalue())

    cursor.execute("""
        INSERT INTO field_reports
        (
            incident_type,
            description,
            latitude,
            longitude,
            report_time,
            image_path
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        incident_type,
        description,
        latitude,
        longitude,
        report_time,
        image_path
    ))

    conn.commit()
    report_id = cursor.lastrowid
    conn.close()
    return report_id, image_path

# =========================================================
# CITY COORDINATES
# =========================================================

CITY_COORDS = {
    "Guwahati": [26.1445, 91.7362],
    "Shillong": [25.5788, 91.8933],
    "Imphal": [24.8074, 93.9384],
    "Agartala": [23.8315, 91.2868],
    "Aizawl": [23.7271, 92.7176],
    "Itanagar": [27.0844, 93.6053],
    "Kohima": [25.6751, 94.1086],
    "Gangtok": [27.3389, 88.6065],
    "Bareilly": [28.3670, 79.4304]
}

# =========================================================
# OPENWEATHER API KEY
# =========================================================

WEATHER_API_KEY = "8588811be768c6415d90e64a77e7c41c"

# =========================================================
# API 1 — LIVE WEATHER (PRESERVED BACKEND)
# =========================================================

def fetch_live_weather(lat, lon):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return {
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"] * 3.6,
                "condition": data["weather"][0]["description"],
                "city": data.get("name", "Unknown"),
                "visibility": data.get("visibility", 0) / 1000
            }
        elif response.status_code == 401:
            st.error("❌ OpenWeather API key is invalid or not activated.")
        elif response.status_code == 404:
            st.error("❌ Weather location not found.")
        else:
            st.error(f"❌ Weather API Error: {response.status_code}")
    except requests.exceptions.Timeout:
        st.error("⏱️ Weather API request timed out.")
    except requests.exceptions.RequestException as e:
        st.error(f"🌐 Weather connection error: {e}")
    except Exception as e:
        st.error(f"⚠️ Weather data error: {e}")
    return None

# =========================================================
# API 2 — PREDICTIVE DISRUPTION (PRESERVED BACKEND)
# =========================================================

def fetch_predictive_disruptions(lat, lon):
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            "&hourly=precipitation_probability,precipitation,windspeed_10m"
            "&forecast_days=1"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        res = response.json()

        if "hourly" in res:
            precip_prob = res["hourly"].get("precipitation_probability", [0])
            precip = res["hourly"].get("precipitation", [0])
            winds = res["hourly"].get("windspeed_10m", [0])

            max_prob = max(precip_prob) if precip_prob else 0
            max_precip = max(precip) if precip else 0.0
            max_wind = max(winds) if winds else 0.0

            disruption_risk = "Low"
            alerts = []

            if max_precip > 15.0 or max_prob > 80:
                disruption_risk = "High"
                alerts.append("🚨 **High Landslide & Flash Flood Risk** predicted in next 24h.")
            elif max_precip > 5.0 or max_prob > 50:
                disruption_risk = "Moderate"
                alerts.append("⚠️ **Moderate Waterlogging Risk** along mountain passes.")

            if max_wind > 35.0:
                alerts.append("💨 **High Wind Hazard:** Risk of fallen trees/debris.")

            if not alerts:
                alerts.append("✅ **Clear Driving Conditions:** Minimal weather blockage risk.")

            return disruption_risk, max_prob, max_precip, alerts

    except Exception as e:
        st.error(f"Predictive Engine Error: {e}")

    return "Unknown", 0, 0.0, ["Unable to calculate predictive risk."]

# =========================================================
# API 3 — ELEVATION (PRESERVED BACKEND)
# =========================================================

def fetch_elevation_profile(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        res = response.json()
        elevation = res.get("elevation", [0])
        if elevation:
            return elevation[0]
    except Exception:
        pass
    return 500

# =========================================================
# API 4 — OSRM ROUTING (PRESERVED BACKEND)
# =========================================================

def fetch_osrm_routes(start_lat, start_lon, end_lat, end_lon):
    osrm_url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{start_lon},{start_lat};{end_lon},{end_lat}"
        "?overview=full&geometries=geojson&alternatives=true"
    )
    try:
        response = requests.get(osrm_url, timeout=10)
        response.raise_for_status()
        res = response.json()
        if res.get("routes"):
            routes_data = []
            for route in res["routes"]:
                routes_data.append({
                    "geometry": route["geometry"],
                    "distance_km": route["distance"] / 1000,
                    "duration_min": route["duration"] / 60
                })
            return routes_data
    except Exception as e:
        st.error(f"Routing API Error: {e}")
    return []

# =========================================================
# API 5 — REROUTING (PRESERVED BACKEND)
# =========================================================

def fetch_rerouted_route(start_lat, start_lon, via_lat, via_lon, end_lat, end_lon):
    osrm_url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{start_lon},{start_lat};{via_lon},{via_lat};{end_lon},{end_lat}"
        "?overview=full&geometries=geojson"
    )
    try:
        response = requests.get(osrm_url, timeout=15)
        if response.status_code != 200:
            st.error(f"❌ Rerouting API Error: {response.status_code}")
            return None
        data = response.json()
        if data.get("code") != "Ok" or not data.get("routes"):
            st.error("❌ No rerouted route found.")
            return None

        route = data["routes"][0]
        return {
            "geometry": route["geometry"],
            "distance_km": route["distance"] / 1000,
            "duration_min": route["duration"] / 60
        }
    except requests.exceptions.Timeout:
        st.error("⏱️ Rerouting API timed out.")
    except requests.exceptions.RequestException as e:
        st.error(f"🌐 Rerouting connection error: {e}")
    except Exception as e:
        st.error(f"⚠️ Rerouting error: {e}")
    return None

# =========================================================
# MULTILINGUAL UI DICTIONARY (PRESERVED)
# =========================================================

LANGUAGES = {
    "English": {
        "title": "NER Smart Logistics & Accessibility Intelligence",
        "subtitle": "Ministry of Development of North Eastern Region (MDoNER) • AI Tactical Operations",
        "analyze": "⚡ EXECUTE CORRIDOR & RISK ANALYSIS",
        "primary_route": "Primary Strategic Corridor",
        "alt_route": "AI Alternate Corridor",
        "cargo": "Essential Cargo Category",
        "fleet": "GPS Live Fleet Tracking Telemetry"
    },
    "Hindi (हिन्दी)": {
        "title": "पूर्वोत्तर स्मार्ट लॉजिस्टिक्स एवं सुगम मार्ग प्लेटफॉर्म",
        "subtitle": "पूर्वोत्तर क्षेत्र विकास मंत्रालय (MDoNER) एआई प्लेटफॉर्म",
        "analyze": "⚡ मार्ग एवं जोखिम विश्लेषण निष्पादित करें",
        "primary_route": "मुख्य मार्ग",
        "alt_route": "एआई वैकल्पिक मार्ग",
        "cargo": "सामग्री श्रेणी",
        "fleet": "जीपीएस लाइव वाहन ट्रैकिंग"
    },
    "Assamese (অসমীয়া)": {
        "title": "উত্তৰ-পূৰ্বাঞ্চল স্মাৰ্ট লজিষ্টিক আৰু পথাৰ যোগাযোগ প্লেটফৰ্ম",
        "subtitle": "MDoNER কৃত্ৰিম বুদ্ধিমত্তা ভিত্তিক পৰিবহণ ব্যৱস্থা",
        "analyze": "⚡ পথ আৰু বিপদাশংকা বিশ্লেষণ কৰক",
        "primary_route": "মুখ্য পথ",
        "alt_route": "বিকল্প পথ",
        "cargo": "পৰিবহণ সামগ্ৰী",
        "fleet": "জিপিএছ প্ৰত্যক্ষ বাহন অনুসৰণ"
    }
}

# =========================================================
# SIDEBAR CONTROLS (MISSION CONTROL DECK)
# =========================================================

st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 10px 0 16px 0; border-bottom: 1px solid rgba(56,189,248,0.2); margin-bottom: 15px;">
        <div style="font-family: 'Orbitron', sans-serif; font-size: 1.15rem; font-weight: 800; color: #00f2fe; letter-spacing: 2px;">
            COMMAND DECK
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #64748b; letter-spacing: 1px;">
            SECURE OPS // LEVEL 4
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

lang_choice = st.sidebar.selectbox(
    "🌐 System Interface Language",
    ["English", "Hindi (हिन्दी)", "Assamese (অসমীয়া)"],
    key="sidebar_lang_select"
)

txt = LANGUAGES[lang_choice]

st.sidebar.markdown(
    """
    <div style="font-family: 'Rajdhani', sans-serif; font-size: 0.88rem; font-weight: 700; color: #38bdf8; letter-spacing: 1.2px; text-transform: uppercase; margin: 16px 0 8px 0;">
        📍 Corridor Coordinates
    </div>
    """,
    unsafe_allow_html=True
)

source = st.sidebar.selectbox(
    "Source District Hub",
    list(CITY_COORDS.keys()),
    index=0,
    key="source_district_select"
)

destination = st.sidebar.selectbox(
    "Destination District Hub",
    list(CITY_COORDS.keys()),
    index=1,
    key="destination_district_select"
)

st.sidebar.markdown(
    """
    <div style="font-family: 'Rajdhani', sans-serif; font-size: 0.88rem; font-weight: 700; color: #38bdf8; letter-spacing: 1.2px; text-transform: uppercase; margin: 16px 0 8px 0;">
        🔄 Tactical Override
    </div>
    """,
    unsafe_allow_html=True
)

enable_rerouting = st.sidebar.checkbox(
    "Dynamic Blockage Reroute",
    value=False,
    key="enable_rerouting"
)

reroute_city = None
if enable_rerouting:
    reroute_options = [
        city for city in CITY_COORDS.keys()
        if city not in [source, destination]
    ]
    reroute_city = st.sidebar.selectbox(
        "Reroute Via Intermediate Node",
        reroute_options,
        key="reroute_city_select"
    )

st.sidebar.markdown(
    """
    <div style="font-family: 'Rajdhani', sans-serif; font-size: 0.88rem; font-weight: 700; color: #38bdf8; letter-spacing: 1.2px; text-transform: uppercase; margin: 16px 0 8px 0;">
        📦 Fleet & Payload Profiling
    </div>
    """,
    unsafe_allow_html=True
)

cargo_type = st.sidebar.selectbox(
    "Essential Payload Type",
    [
        "Medicines & Vaccines",
        "Food Supplies",
        "Agricultural Produce",
        "Construction Materials"
    ],
    key="cargo_type_select"
)

vehicle = st.sidebar.selectbox(
    "Transport Carrier Class",
    [
        "Heavy Duty Truck",
        "Mini Freight Carrier",
        "4x4 Emergency Van"
    ],
    key="vehicle_type_select"
)

analyze_clicked = st.sidebar.button(
    txt["analyze"],
    key="analyze_button",
    type="primary"
)
# =========================================================
# HELP & SUPPORT
# =========================================================

st.sidebar.markdown("---")
st.sidebar.markdown("## 🆘 Help & Support")

st.sidebar.caption("Need help? We're here to assist you.")

# Contact Support
st.sidebar.markdown(
    '<a href="tel:+91XXXXXXXXXX">'
    '<button style="width:100%; padding:10px; cursor:pointer;">'
    '📞 Contact Support'
    '</button>'
    '</a>',
    unsafe_allow_html=True
)

# Report an Issue
if st.sidebar.button("🐛 Report an Issue", use_container_width=True):
    st.session_state["show_issue_form"] = True

if st.session_state.get("show_issue_form", False):

    st.sidebar.markdown("### 🐛 Report an Issue")

    issue_type = st.sidebar.selectbox(
        "Issue Type",
        [
            "🗺️ Map Problem",
            "🚨 Alert Problem",
            "🔄 Route/Rerouting Problem",
            "🤖 Prediction Problem",
            "🌐 Website Problem",
            "📌 Other"
        ],
        key="issue_type"
    )

    issue_description = st.sidebar.text_area(
        "Describe the issue",
        placeholder="Tell us what went wrong...",
        key="issue_description"
    )

    if st.sidebar.button("🚀 Submit Issue", use_container_width=True):

        if issue_description.strip():
            st.sidebar.success("✅ Issue reported successfully!")
            st.session_state["show_issue_form"] = False
        else:
            st.sidebar.warning("⚠️ Please describe the issue first.")
# =========================================================
# TOP FUTURISTIC COMMAND HEADER
# =========================================================

st.markdown(
    f"""
    <div class="command-header">
        <div class="header-top-meta">
            <span>GOVERNMENT OF INDIA • MINISTRY OF DEVELOPMENT OF NORTH EASTERN REGION</span>
            <div class="status-beacon">
                <span class="beacon-dot"></span>
                <span>SYSTEM ACTIVE • SIH 26002</span>
            </div>
        </div>
        <h1 class="header-title">
            <span>🚚</span> {txt["title"]}
        </h1>
        <p class="header-subtitle">
            {txt["subtitle"]} | AI-Powered Dynamic Strategic Corridor Vulnerability & Routing Engine
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# TOP KPI TELEMETRY METRICS
# =========================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        """
        <div class="telemetry-card">
            <div class="telemetry-label">
                <span>🛣️</span> Monitored NER Routes
            </div>
            <div class="telemetry-value">24</div>
            <span class="telemetry-badge badge-cyan">HIGHWAY RADAR ACTIVE</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        """
        <div class="telemetry-card">
            <div class="telemetry-label">
                <span>⚠️</span> Active Disruptions
            </div>
            <div class="telemetry-value" style="color: #ff4d6d;">07</div>
            <span class="telemetry-badge badge-rose">SEVERITY LEVEL 2</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        """
        <div class="telemetry-card">
            <div class="telemetry-label">
                <span>🌧️</span> Weather Hazard Alerts
            </div>
            <div class="telemetry-value" style="color: #f59e0b;">03</div>
            <span class="telemetry-badge badge-amber">PRECIPITATION ADVISORY</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        """
        <div class="telemetry-card">
            <div class="telemetry-label">
                <span>🚛</span> GPS Supply Fleets
            </div>
            <div class="telemetry-value" style="color: #10b981;">156</div>
            <span class="telemetry-badge badge-emerald">100% ENCRYPTED TELEMETRY</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# =========================================================
# ROUTE COMPUTATION & API CALLS (PRESERVED BACKEND)
# =========================================================

start_lat, start_lon = CITY_COORDS[source]
end_lat, end_lon = CITY_COORDS[destination]

routes = fetch_osrm_routes(start_lat, start_lon, end_lat, end_lon)

rerouted_route = None
if enable_rerouting and reroute_city:
    via_lat, via_lon = CITY_COORDS[reroute_city]
    rerouted_route = fetch_rerouted_route(start_lat, start_lon, via_lat, via_lon, end_lat, end_lon)

dest_weather = fetch_live_weather(end_lat, end_lon)
risk_level, max_prob, max_precip, pred_alerts = fetch_predictive_disruptions(end_lat, end_lon)
dest_elevation = fetch_elevation_profile(end_lat, end_lon)

# =========================================================
# MAIN COMMAND CENTER TABS
# =========================================================

tab_map, tab_fleet, tab_report, tab_district, tab_ai = st.tabs(
    [
        "🗺️ Strategic Corridor Radar & GIS",
        "🚛 Live Fleet GPS Telemetry",
        "📸 Incident Field Dispatch Terminal",
        "📊 District Readiness Matrix",
        "🤖 AI Disruption Risk Predictor"
    ]
)

# =========================================================
# TAB 1 — STRATEGIC GIS MAP & TACTICAL WEATHER
# =========================================================

with tab_map:
    left, right = st.columns([2, 1])

    with left:
        st.markdown(
            f"""
            <div class="map-hud-frame">
                <div class="map-hud-header">
                    <span><b>🛰️ SATELLITE RADAR:</b> {source} ➔ {destination}</span>
                    <span><b>STATUS:</b> LIVE OSRM CORRIDOR GEOJSON</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Folium Tactical Dark Map
        m = folium.Map(
            location=[(start_lat + end_lat) / 2, (start_lon + end_lon) / 2],
            zoom_start=6,
            tiles="CartoDB dark_matter"
        )

        # City Markers
        for city, coords in CITY_COORDS.items():
            folium.CircleMarker(
                location=coords,
                radius=6,
                color="#00f2fe",
                fill=True,
                fill_color="#00f2fe",
                fill_opacity=0.8,
                popup=f"District Hub: {city}",
                tooltip=city
            ).add_to(m)

        # Landslide Road Blockage Marker
        folium.Marker(
            location=[26.1158, 91.7086],
            popup="🚧 Landslide Road Blockage (Route A12)",
            tooltip="Active Disruption Point",
            icon=folium.Icon(color="red", icon="exclamation-sign")
        ).add_to(m)

        # Primary Strategic Route (Cyan Glow)
        if routes:
            folium.GeoJson(
                routes[0]["geometry"],
                name="Primary Route",
                style_function=lambda feature: {
                    "color": "#00f2fe",
                    "weight": 5,
                    "opacity": 0.85
                }
            ).add_to(m)

            # Alternate AI Route (Emerald)
            if len(routes) > 1:
                folium.GeoJson(
                    routes[1]["geometry"],
                    name="Alternate AI Route",
                    style_function=lambda feature: {
                        "color": "#10b981",
                        "weight": 4,
                        "dashArray": "6,6",
                        "opacity": 0.9
                    }
                ).add_to(m)

        # Source & Destination Markers
        folium.Marker(
            location=[start_lat, start_lon],
            popup=f"Origin: {source}",
            icon=folium.Icon(color="green", icon="play")
        ).add_to(m)

        folium.Marker(
            location=[end_lat, end_lon],
            popup=f"Destination: {destination}",
            icon=folium.Icon(color="red", icon="flag")
        ).add_to(m)

        # Rerouted Track (Tactical Amber)
        if enable_rerouting and rerouted_route:
            folium.GeoJson(
                rerouted_route["geometry"],
                name="🔄 Live Rerouted Route",
                style_function=lambda feature: {
                    "color": "#f59e0b",
                    "weight": 6,
                    "opacity": 0.95
                },
                tooltip=f"Dynamic Detour via {reroute_city}"
            ).add_to(m)

            via_lat, via_lon = CITY_COORDS[reroute_city]
            folium.Marker(
                location=[via_lat, via_lon],
                popup=f"🔄 Waypoint Reroute: {reroute_city}",
                tooltip=f"Detour Hub: {reroute_city}",
                icon=folium.Icon(color="orange", icon="random")
            ).add_to(m)

        st_folium(m, width="100%", height=460, key="main_route_map")

        # Telemetry Metadata Strip
        st.markdown(
            f"""
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 8px; padding: 10px 16px; margin-top: 10px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #94a3b8; display: flex; flex-wrap: wrap; gap: 14px; justify-content: space-between;">
                <span>📍 <b>CORRIDOR:</b> <span style="color: #f8fafc;">{source} ➔ {destination}</span></span>
                <span>📦 <b>PAYLOAD:</b> <span style="color: #38bdf8;">{cargo_type}</span></span>
                <span>🚛 <b>CARRIER:</b> <span style="color: #38bdf8;">{vehicle}</span></span>
                <span>⛰️ <b>DESTINATION ELEVATION:</b> <span style="color: #10b981;">{dest_elevation} m MSL</span></span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Weather & Predictive Intelligence Column
    with right:
        st.markdown(
            """
            <div class="hud-glass-card">
                <div class="hud-panel-title">
                    <span>🌤️</span> Live Destination Atmospheric Telemetry
                </div>
            """,
            unsafe_allow_html=True
        )

        if dest_weather:
            wcol1, wcol2 = st.columns(2)
            with wcol1:
                st.metric("🌡️ Temperature", f"{dest_weather['temperature']:.1f} °C")
                st.metric("💧 Humidity", f"{dest_weather['humidity']}%")
            with wcol2:
                st.metric("🌡️ Feels Like", f"{dest_weather['feels_like']:.1f} °C")
                st.metric("💨 Wind Speed", f"{dest_weather['wind_speed']:.1f} km/h")

            st.markdown(
                f"""
                <div style="background: rgba(56, 189, 248, 0.1); border-left: 3px solid #38bdf8; padding: 8px 12px; border-radius: 4px; font-size: 0.85rem; margin-top: 10px;">
                    <b>Atmospheric Condition:</b> {dest_weather['condition'].title()}<br>
                    <span style="font-size: 0.76rem; color: #94a3b8;">Station: {dest_weather['city']} • Barometer: {dest_weather['pressure']} hPa • Visibility: {dest_weather['visibility']:.1f} km</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("⚠️ Atmospheric weather telemetry offline.")

        st.markdown("</div>", unsafe_allow_html=True)

        # Predictive Disruption HUD Card
        st.markdown(
            """
            <div class="hud-glass-card">
                <div class="hud-panel-title">
                    <span>🔮</span> Corridor Disruption Intelligence
                </div>
            """,
            unsafe_allow_html=True
        )

        risk_color = "#10b981" if risk_level == "Low" else ("#f59e0b" if risk_level == "Moderate" else "#ff4d6d")
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(0,0,0,0.3); border: 1px solid {risk_color}; padding: 10px 14px; border-radius: 8px; margin-bottom: 12px;">
                <span style="font-family: 'Rajdhani', sans-serif; font-size: 0.95rem; font-weight: 700; text-transform: uppercase;">Disruption Vulnerability</span>
                <span style="font-family: 'Orbitron', monospace; font-size: 1.1rem; font-weight: 800; color: {risk_color};">{risk_level.upper()} RISK</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        p1, p2 = st.columns(2)
        with p1:
            st.metric("🌧️ Rain Probability", f"{max_prob}%")
        with p2:
            st.metric("🌧️ Max Precipitation", f"{max_precip:.1f} mm")

        for alert in pred_alerts:
            st.markdown(f"<div style='font-size: 0.85rem; color: #cbd5e1; margin-top: 6px;'>{alert}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 2 — LIVE FLEET GPS TRACKING TELEMETRY
# =========================================================

with tab_fleet:
    st.markdown(
        f"""
        <div class="hud-glass-card">
            <div class="hud-panel-title">
                <span>🚛</span> {txt["fleet"]}
            </div>
            <p style="color: #94a3b8; font-size: 0.92rem; margin: 0 0 16px 0;">
                High-frequency real-time telemetry tracking of essential supply carriers navigating North Eastern transit corridors.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    simulated_lat = start_lat + (end_lat - start_lat) * 0.45
    simulated_lon = start_lon + (end_lon - start_lon) * 0.45

    col_f1, col_f2, col_f3 = st.columns(3)
    col_f1.metric("Transponder ID", "TRK-NER-9082")
    col_f2.metric("Telemetry Velocity", "38 km/h")
    col_f3.metric("Transponder Status", "🟢 100% Encrypted Signal")

    st.write("")

    f_map = folium.Map(
        location=[simulated_lat, simulated_lon],
        zoom_start=9,
        tiles="CartoDB dark_matter"
    )

    folium.Marker(
        location=[simulated_lat, simulated_lon],
        popup=f"TRK-NER-9082 ({cargo_type})",
        tooltip="TRK-NER-9082 (Active Transponder)",
        icon=folium.Icon(color="orange", icon="truck", prefix="fa")
    ).add_to(f_map)

    st_folium(f_map, width="100%", height=380, key="fleet_tracking_map")

# =========================================================
# TAB 3 — GEO-TAGGED FIELD INCIDENT DISPATCH TERMINAL
# =========================================================

with tab_report:
    st.markdown(
        """
        <div class="hud-glass-card">
            <div class="hud-panel-title">
                <span>📸</span> Incident Field Dispatch & Geo-Surveillance Terminal
            </div>
            <p style="color: #94a3b8; font-size: 0.92rem; margin: 0;">
                Upload real-time geo-tagged photographic evidence and incident telemetry from field personnel to update regional corridor intelligence.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    rep_col1, rep_col2 = st.columns(2)

    with rep_col1:
        incident_type = st.selectbox(
            "Incident Classification",
            [
                "Landslide / Mudslide",
                "Flash Flood / Waterlogging",
                "Bridge Damage",
                "Heavy Traffic Congestion"
            ],
            key="incident_type_select"
        )

        st.markdown(
            """
            <div style="font-size: 0.85rem; color: #38bdf8; font-family: 'JetBrains Mono', monospace; margin: 8px 0 4px 0;">
                📍 TARGET ACQUISITION: Click anywhere on the map to pinpoint coordinates
            </div>
            """,
            unsafe_allow_html=True
        )

        report_map = folium.Map(
            location=[start_lat, start_lon],
            zoom_start=7,
            tiles="CartoDB dark_matter"
        )

        if "report_lat" in st.session_state:
            folium.Marker(
                [st.session_state.report_lat, st.session_state.report_lon],
                tooltip="Selected Incident Target",
                popup=f"Lat: {st.session_state.report_lat:.6f}<br>Lon: {st.session_state.report_lon:.6f}",
                icon=folium.Icon(color="red", icon="crosshairs", prefix="fa")
            ).add_to(report_map)

        map_data = st_folium(
            report_map,
            width="100%",
            height=340,
            key="incident_report_map",
            returned_objects=["last_clicked"]
        )

        if map_data and map_data.get("last_clicked"):
            st.session_state.report_lat = map_data["last_clicked"]["lat"]
            st.session_state.report_lon = map_data["last_clicked"]["lng"]

        inc_lat = st.session_state.get("report_lat", start_lat)
        inc_lon = st.session_state.get("report_lon", start_lon)

        st.markdown(
            f"""
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 8px; padding: 10px 14px; margin: 10px 0; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;">
                <span style="color: #00f2fe;">TARGET GPS LOCK:</span>
                <span style="color: #ffffff; margin-left: 10px;">LAT: <b>{inc_lat:.6f}</b></span>
                <span style="color: #ffffff; margin-left: 10px;">LON: <b>{inc_lon:.6f}</b></span>
            </div>
            """,
            unsafe_allow_html=True
        )

        notes = st.text_area(
            "Tactical Situation Report / Ground Observations",
            placeholder="Document road accessibility, blockage severity, estimated clearance timeframe, and ground conditions...",
            key="incident_notes",
            height=110
        )

    with rep_col2:
        st.markdown(
            """
            <div style="font-family: 'Rajdhani', sans-serif; font-size: 0.95rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; margin-bottom: 6px;">
                📷 Optical Surveillance & Photo Evidence
            </div>
            """,
            unsafe_allow_html=True
        )

        img_file = st.file_uploader(
            "Transference Dropzone (Photo Upload)",
            type=["jpg", "jpeg", "png"],
            key="incident_image_upload"
        )

        st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.8rem; font-weight: bold;'>— OR LIVE OPTICAL RECONNAISSANCE —</div>", unsafe_allow_html=True)

        cam_file = st.camera_input(
            "Activate Optical Camera Sensor",
            key="incident_camera"
        )

        if img_file:
            st.markdown("<b>Captured Surveillance Evidence:</b>", unsafe_allow_html=True)
            st.image(img_file, caption="Uploaded Field Evidence", width=340)
        elif cam_file:
            st.markdown("<b>Live Camera Optical Frame:</b>", unsafe_allow_html=True)
            st.image(cam_file, caption="Live Reconnaissance Capture", width=340)

    st.write("")

    # SUBMIT REPORT BUTTON (PRESERVED BACKEND)
    if st.button("📤 TRANSMIT FIELD INTELLIGENCE DOSSIER", type="primary", key="submit_incident_report"):
        selected_image = img_file if img_file is not None else cam_file

        if selected_image is None:
            st.warning("⚠️ Please provide photographic evidence (upload or capture).")
        elif not notes.strip():
            st.warning("⚠️ Please enter tactical situation report details.")
        else:
            report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                report_id, saved_image_path = save_field_report(
                    incident_type,
                    notes,
                    inc_lat,
                    inc_lon,
                    report_time,
                    selected_image
                )

                st.session_state.last_seen_report_id = report_id
                st.session_state.new_report_alert = {
                    "id": report_id,
                    "type": incident_type,
                    "description": notes,
                    "lat": inc_lat,
                    "lon": inc_lon,
                    "time": report_time
                }

                st.success(f"✅ Field Intelligence Dossier #{report_id} transmitted and indexed!")
            except Exception as e:
                st.error(f"❌ Intelligence transmission failed: {e}")

    # SUBMITTED FIELD REPORTS ARCHIVE
    st.write("")
    st.markdown(
        """
        <div class="hud-panel-title" style="margin-top: 20px;">
            <span>🗄️</span> Declassified Field Incident Archives
        </div>
        """,
        unsafe_allow_html=True
    )

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, incident_type, description, latitude, longitude, report_time, image_path
            FROM field_reports
            ORDER BY id DESC
        """)
        reports = cursor.fetchall()
        conn.close()

        if reports:
            for rep in reports:
                r_id, r_type, r_desc, r_lat, r_lon, r_time, r_img = rep
                with st.expander(f"📋 DOSSIER #{r_id} • {r_type} • {r_time}"):
                    dc1, dc2 = st.columns([1, 1])
                    with dc1:
                        st.markdown(
                            f"""
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #cbd5e1; line-height: 1.8;">
                                📍 <b>LATITUDE:</b> {r_lat:.6f}<br>
                                📍 <b>LONGITUDE:</b> {r_lon:.6f}<br>
                                🕒 <b>LOGGED TIME:</b> {r_time}<br>
                                ⚠️ <b>CLASSIFICATION:</b> <span style="color: #f59e0b;">{r_type}</span><br>
                                📝 <b>SUMMARY:</b> {r_desc}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    with dc2:
                        if r_img and os.path.exists(r_img):
                            st.image(r_img, caption=f"Optical Evidence #{r_id}", width=340)
                        else:
                            st.caption("No optical image record attached.")
        else:
            st.info("No field reports currently logged in the intelligence database.")
    except Exception as e:
        st.error(f"❌ Archive query error: {e}")

# =========================================================
# TAB 4 — DISTRICT READINESS MATRIX
# =========================================================

with tab_district:
    st.markdown(
        """
        <div class="hud-glass-card">
            <div class="hud-panel-title">
                <span>📊</span> Regional Corridor Readiness & Bottleneck Matrix
            </div>
            <p style="color: #94a3b8; font-size: 0.92rem; margin: 0 0 16px 0;">
                Comprehensive strategic accessibility status across key North Eastern logistics hubs.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    accessibility_data = [
        {
            "District Hub": "Guwahati",
            "Readiness Status": "🟢 Fully Accessible",
            "Active Vulnerabilities / Bottlenecks": "None Detected",
            "Strategic Evacuation Route": "NH-27"
        },
        {
            "District Hub": "Shillong",
            "Readiness Status": "🟡 Partially Disrupted",
            "Active Vulnerabilities / Bottlenecks": "Landslide on NH-6 (Km 42)",
            "Strategic Evacuation Route": "SH-1 Alternative Pass"
        },
        {
            "District Hub": "Imphal",
            "Readiness Status": "🔴 Severely Restricted",
            "Active Vulnerabilities / Bottlenecks": "Bridge Structural Degradation near Jiribam",
            "Strategic Evacuation Route": "NH-37 (Armed Escort Bypass)"
        },
        {
            "District Hub": "Agartala",
            "Readiness Status": "🟢 Fully Accessible",
            "Active Vulnerabilities / Bottlenecks": "None Detected",
            "Strategic Evacuation Route": "NH-8"
        },
        {
            "District Hub": "Aizawl",
            "Readiness Status": "🟡 Partially Disrupted",
            "Active Vulnerabilities / Bottlenecks": "Heavy Mountain Fog & Low-Lying Waterlogging",
            "Strategic Evacuation Route": "NH-54 Hill Route"
        }
    ]

    st.table(pd.DataFrame(accessibility_data))

# =========================================================
# TAB 5 — AI VULNERABILITY SIMULATOR (XGBOOST ML)
# =========================================================

with tab_ai:
    st.markdown(
        """
        <div class="hud-glass-card">
            <div class="hud-panel-title">
                <span>🤖</span> XGBoost AI Disruption Risk Simulator
            </div>
            <p style="color: #94a3b8; font-size: 0.92rem; margin: 0 0 16px 0;">
                Pre-trained supervised gradient boosted decision trees predicting North Eastern mountain pass vulnerability based on real-time soil and meteorological vectors.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    ai_c1, ai_c2 = st.columns(2)

    with ai_c1:
        ml_rain = st.slider(
            "🌧️ Simulated Rainfall (mm/24h)",
            0.0, 350.0, 150.0,
            key="ml_rain_slider"
        )
        ml_moisture = st.slider(
            "💧 Soil Moisture Saturation (%)",
            10.0, 100.0, 75.0,
            key="ml_soil_slider"
        )

    with ai_c2:
        ml_slope = st.slider(
            "⛰️ Corridor Slope Incline (Degrees)",
            0.0, 70.0, 35.0,
            key="ml_slope_slider"
        )
        ml_freq = st.number_input(
            "🪨 Historical Landslide Frequency",
            min_value=0, max_value=10, value=1,
            key="ml_freq_slider"
        )

    ml_input_df = pd.DataFrame(
        [[ml_rain, ml_moisture, ml_slope, ml_freq]],
        columns=[
            "rainfall_mm",
            "soil_moisture",
            "slope_degrees",
            "historical_landslide_freq"
        ]
    )

    ml_pred = ml_risk_model.predict(ml_input_df)[0]
    ml_prob = ml_risk_model.predict_proba(ml_input_df)[0][1] * 100

    risk_accent = "#ff3366" if ml_pred == 1 else "#10b981"
    risk_title = "CRITICAL DISRUPTION RISK" if ml_pred == 1 else "OPTIMAL SECURE CORRIDOR"
    risk_desc = "AI forecasts high probability of slope instability or waterlogging." if ml_pred == 1 else "Corridor physics indicators remain well below failure thresholds."

    st.markdown(
        f"""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid {risk_accent}; border-radius: 12px; padding: 20px; margin-top: 14px; box-shadow: 0 0 20px {risk_accent}33;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="font-family: 'Orbitron', sans-serif; font-size: 1.25rem; font-weight: 800; color: {risk_accent};">
                    {risk_title}
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.45rem; font-weight: 800; color: #ffffff;">
                    {ml_prob:.1f}% PROBABILITY
                </div>
            </div>
            <div style="width: 100%; height: 10px; background: rgba(255, 255, 255, 0.1); border-radius: 5px; overflow: hidden; margin-bottom: 12px;">
                <div style="width: {ml_prob}%; height: 100%; background: linear-gradient(90deg, #10b981, #f59e0b, #ff3366); transition: width 0.5s ease;"></div>
            </div>
            <div style="font-size: 0.9rem; color: #94a3b8;">
                {risk_desc}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# AI ROUTE OPTIMIZATION ENGINE SUMMARY CARD
# =========================================================

st.write("")
st.markdown(
    """
    <div class="hud-panel-title" style="margin-top: 24px;">
        <span>🤖</span> AI Strategic Route Advisory
    </div>
    """,
    unsafe_allow_html=True
)

if routes:
    prim = routes[0]
    delay_mult = 1.45 if risk_level == "High" else (1.20 if risk_level == "Moderate" else 1.0)
    adjusted_duration = prim['duration_min'] * delay_mult

    sum_col1, sum_col2 = st.columns([2, 1])

    with sum_col1:
        st.markdown(
            f"""
            <div class="hud-glass-card">
                <div style="font-family: 'Orbitron', sans-serif; font-size: 1.05rem; font-weight: 700; color: #00f2fe; margin-bottom: 10px;">
                    Strategic Corridor: {source} ➔ {destination}
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; font-family: 'JetBrains Mono', monospace; font-size: 0.88rem;">
                    <div>📏 <b>DISTANCE:</b> <span style="color: #ffffff;">{prim['distance_km']:.2f} km</span></div>
                    <div>⏱️ <b>EST. TRANSIT:</b> <span style="color: #ffffff;">{prim['duration_min']:.0f} mins</span></div>
                    <div>⚠️ <b>RISK MULTIPLIER:</b> <span style="color: #f59e0b;">{delay_mult:.2f}x</span></div>
                    <div>🕒 <b>ADJUSTED ETA:</b> <span style="color: #10b981;">{adjusted_duration:.0f} mins</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with sum_col2:
        if enable_rerouting and rerouted_route:
            st.markdown(
                f"""
                <div class="hud-glass-card" style="border-color: #f59e0b;">
                    <div style="font-family: 'Orbitron', sans-serif; font-size: 0.95rem; font-weight: 700; color: #f59e0b; margin-bottom: 8px;">
                        Dynamic Reroute (via {reroute_city})
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #cbd5e1;">
                        📏 <b>Detour Dist:</b> {rerouted_route['distance_km']:.2f} km<br>
                        ⏱️ <b>Detour Time:</b> {rerouted_route['duration_min']:.0f} mins
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif len(routes) > 1:
            alt = routes[1]
            st.markdown(
                f"""
                <div class="hud-glass-card" style="border-color: #10b981;">
                    <div style="font-family: 'Orbitron', sans-serif; font-size: 0.95rem; font-weight: 700; color: #10b981; margin-bottom: 8px;">
                        AI Alternate Route Available
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #cbd5e1;">
                        📏 <b>Alt Dist:</b> {alt['distance_km']:.2f} km<br>
                        ⏱️ <b>Alt Time:</b> ~{alt['duration_min']:.0f} mins
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("Single strategic route available for selected district pair.")
else:
    st.error("No valid corridor found between selected districts.")

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div style="border-top: 1px solid rgba(56, 189, 248, 0.15); padding: 22px 0; margin-top: 36px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #64748b; letter-spacing: 1px;">
        SIH 2026 PROTOTYPE • PROBLEM STATEMENT 26002 • MDoNER LOGISTICS INTELLIGENCE COMMAND CENTER
    </div>
    """,
    unsafe_allow_html=True
)