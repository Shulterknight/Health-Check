import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# ─────────────────────────────────────────────
# Application Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Health Check AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS – Premium Dark Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

:root {
    --bg-primary:#0d0f14;
    --bg-card:rgba(255,255,255,0.04);
    --bg-card-hover:rgba(255,255,255,0.07);
    --border:rgba(255,255,255,0.08);
    --accent-green:#00e5a0;
    --accent-blue:#4f9cf9;
    --accent-amber:#f9a825;
    --accent-red:#ff5c5c;
    --accent-purple:#b57bee;
    --text-primary:#f0f2f6;
    --text-muted:#8b95a5;
    --radius-lg:18px;
    --radius-md:12px;
    --shadow:0 8px 32px rgba(0,0,0,0.45);
}
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;color:var(--text-primary)!important;}
.stApp{background:linear-gradient(135deg,#0d0f14 0%,#111827 50%,#0d1117 100%);min-height:100vh;}
#MainMenu,footer,header{visibility:hidden;}

/* Sidebar */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#111520 0%,#0d1117 100%)!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:var(--text-primary)!important;}
[data-testid="stSidebar"] input{background:rgba(255,255,255,0.06)!important;border:1px solid var(--border)!important;border-radius:var(--radius-md)!important;color:var(--text-primary)!important;font-size:1rem!important;}
[data-testid="stSidebar"] input:focus{border-color:var(--accent-green)!important;box-shadow:0 0 20px rgba(0,229,160,0.25)!important;}
[data-testid="stSidebar"] label{font-size:0.8rem!important;font-weight:600!important;color:var(--text-muted)!important;text-transform:uppercase!important;letter-spacing:0.08em!important;}

.sidebar-section-title{font-family:'Space Grotesk',sans-serif;font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--text-muted)!important;margin:1.4rem 0 0.6rem;}

/* BMI Card */
.bmi-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:1.2rem 1.4rem;margin:1rem 0;backdrop-filter:blur(12px);text-align:center;transition:all 0.3s ease;}
.bmi-card:hover{background:var(--bg-card-hover);box-shadow:var(--shadow);}
.bmi-value{font-family:'Space Grotesk',sans-serif;font-size:2.8rem;font-weight:700;line-height:1;margin:0.3rem 0;}
.bmi-label{font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.1em;}
.bmi-badge{display:inline-block;padding:0.3rem 1rem;border-radius:99px;font-size:0.78rem;font-weight:600;margin-top:0.7rem;letter-spacing:0.05em;}
.badge-underweight{background:rgba(79,156,249,0.18);color:var(--accent-blue);border:1px solid rgba(79,156,249,0.35);}
.badge-normal{background:rgba(0,229,160,0.15);color:var(--accent-green);border:1px solid rgba(0,229,160,0.35);}
.badge-overweight{background:rgba(249,168,37,0.15);color:var(--accent-amber);border:1px solid rgba(249,168,37,0.35);}
.badge-obese{background:rgba(255,92,92,0.15);color:var(--accent-red);border:1px solid rgba(255,92,92,0.35);}

/* Hero */
.hero-header{background:linear-gradient(135deg,rgba(79,156,249,0.12) 0%,rgba(0,229,160,0.10) 100%);border:1px solid rgba(79,156,249,0.2);border-radius:var(--radius-lg);padding:2.4rem 2.8rem;margin-bottom:2rem;position:relative;overflow:hidden;}
.hero-header::before{content:'';position:absolute;top:-60px;right:-60px;width:220px;height:220px;background:radial-gradient(circle,rgba(0,229,160,0.12) 0%,transparent 70%);border-radius:50%;}
.hero-title{font-family:'Space Grotesk',sans-serif;font-size:2.4rem;font-weight:700;background:linear-gradient(135deg,#ffffff 0%,var(--accent-green) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin:0 0 0.4rem;line-height:1.1;}
.hero-sub{color:var(--text-muted);font-size:1rem;font-weight:400;margin:0;}

/* Status pill */
.status-pill{display:inline-flex;align-items:center;gap:0.45rem;padding:0.35rem 0.9rem;border-radius:99px;font-size:0.78rem;font-weight:600;margin:0.5rem 0;}
.status-ok{background:rgba(0,229,160,0.12);color:var(--accent-green);border:1px solid rgba(0,229,160,0.3);}
.status-err{background:rgba(255,92,92,0.12);color:var(--accent-red);border:1px solid rgba(255,92,92,0.3);}
.status-dot{width:7px;height:7px;border-radius:50%;display:inline-block;}
.dot-ok{background:var(--accent-green);animation:pulse-green 2s infinite;}
.dot-err{background:var(--accent-red);}
@keyframes pulse-green{0%,100%{box-shadow:0 0 0 0 rgba(0,229,160,0.6);}50%{box-shadow:0 0 0 5px rgba(0,229,160,0);}}

/* Upload zone */
[data-testid="stFileUploader"]{background:rgba(255,255,255,0.03)!important;border:2px dashed rgba(79,156,249,0.35)!important;border-radius:var(--radius-lg)!important;padding:1rem!important;transition:all 0.3s ease!important;}
[data-testid="stFileUploader"]:hover{border-color:var(--accent-blue)!important;background:rgba(79,156,249,0.05)!important;}
[data-testid="stFileUploader"] *{color:var(--text-primary)!important;}
[data-testid="stFileUploader"] button{background:linear-gradient(135deg,var(--accent-blue),#7b5cf6)!important;color:white!important;border:none!important;border-radius:var(--radius-md)!important;font-weight:600!important;padding:0.5rem 1.4rem!important;transition:all 0.25s ease!important;}
[data-testid="stFileUploader"] button:hover{transform:translateY(-1px);box-shadow:0 6px 20px rgba(79,156,249,0.4)!important;}

/* Metric cards */
.metric-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;margin:1.2rem 0;}
.metric-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:1.3rem 1.5rem;backdrop-filter:blur(12px);transition:all 0.3s ease;position:relative;overflow:hidden;}
.metric-card::before{content:'';position:absolute;top:0;left:0;height:3px;width:100%;border-radius:var(--radius-lg) var(--radius-lg) 0 0;}
.metric-card.green::before{background:linear-gradient(90deg,var(--accent-green),#00b4d8);}
.metric-card.blue::before{background:linear-gradient(90deg,var(--accent-blue),#b57bee);}
.metric-card.amber::before{background:linear-gradient(90deg,var(--accent-amber),#ff8f00);}
.metric-card.red::before{background:linear-gradient(90deg,var(--accent-red),#ff8c42);}
.metric-card:hover{background:var(--bg-card-hover);transform:translateY(-3px);box-shadow:var(--shadow);}
.mc-label{font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:var(--text-muted);margin-bottom:0.5rem;}
.mc-value{font-family:'Space Grotesk',sans-serif;font-size:1.9rem;font-weight:700;line-height:1;color:var(--text-primary);}
.mc-unit{font-size:0.8rem;font-weight:400;color:var(--text-muted);margin-top:0.25rem;}
.mc-icon{font-size:1.4rem;margin-bottom:0.4rem;display:block;}
.result-heading{font-family:'Space Grotesk',sans-serif;font-size:1.6rem;font-weight:700;color:var(--text-primary);margin:0 0 0.15rem;}
.result-confidence{font-size:0.85rem;color:var(--text-muted);margin:0;}

/* Advice cards */
.advice-card{border-radius:var(--radius-lg);padding:1.3rem 1.6rem;margin-top:0.5rem;border-left:4px solid;backdrop-filter:blur(12px);font-size:0.95rem;line-height:1.6;}
.advice-success{background:rgba(0,229,160,0.08);border-color:var(--accent-green);color:#a0f2d8;}
.advice-warning{background:rgba(249,168,37,0.08);border-color:var(--accent-amber);color:#fce08a;}
.advice-info{background:rgba(79,156,249,0.08);border-color:var(--accent-blue);color:#a8ceff;}
.advice-danger{background:rgba(255,92,92,0.08);border-color:var(--accent-red);color:#ffacac;}
.advice-icon{font-size:1.2rem;margin-right:0.5rem;}
.advice-title{font-weight:700;font-size:1rem;margin-bottom:0.3rem;}

/* Utilities */
.fancy-divider{height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:2rem 0;border:none;}
.section-header{display:flex;align-items:center;gap:0.6rem;margin:1.8rem 0 1rem;}
.section-header-icon{font-size:1.2rem;}
.section-header-text{font-family:'Space Grotesk',sans-serif;font-size:1.1rem;font-weight:700;color:var(--text-primary);letter-spacing:-0.01em;}
[data-testid="stImage"] img{border-radius:var(--radius-lg)!important;border:1px solid var(--border)!important;box-shadow:var(--shadow)!important;}
.stSpinner>div{border-top-color:var(--accent-green)!important;}
::-webkit-scrollbar{width:6px;}
::-webkit-scrollbar-track{background:var(--bg-primary);}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.12);border-radius:99px;}
::-webkit-scrollbar-thumb:hover{background:rgba(255,255,255,0.2);}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Food Classes & Nutrition DB
# ─────────────────────────────────────────────
FOOD_CLASSES = ['adhirasam', 'aloo_gobi', 'aloo_matar', 'aloo_methi', 'aloo_shimla_mirch', 'aloo_tikki', 'anarsa', 'apple_pie', 'ariselu', 'baby_back_ribs', 'baklava', 'bandar_laddu', 'basundi', 'beef_carpaccio', 'beef_tartare', 'beet_salad', 'beignets', 'bhatura', 'bhindi_masala', 'bibimbap', 'biryani', 'boondi', 'bread_pudding', 'breakfast_burrito', 'bruschetta', 'butter_chicken', 'caesar_salad', 'cannoli', 'caprese_salad', 'carrot_cake', 'ceviche', 'chak_hao_kheer', 'cham_cham', 'chana_masala', 'chapati', 'cheese_plate', 'cheesecake', 'chhena_kheeri', 'chicken_curry', 'chicken_quesadilla', 'chicken_razala', 'chicken_tikka', 'chicken_tikka_masala', 'chicken_wings', 'chikki', 'chocolate_cake', 'chocolate_mousse', 'churros', 'clam_chowder', 'club_sandwich', 'crab_cakes', 'creme_brulee', 'croque_madame', 'cup_cakes', 'daal_baati_churma', 'daal_puri', 'dal_makhani', 'dal_tadka', 'deviled_eggs', 'dharwad_pedha', 'donuts', 'doodhpak', 'double_ka_meetha', 'dum_aloo', 'dumplings', 'edamame', 'eggs_benedict', 'escargots', 'falafel', 'filet_mignon', 'fish_and_chips', 'foie_gras', 'french_fries', 'french_onion_soup', 'french_toast', 'fried_calamari', 'fried_rice', 'frozen_yogurt', 'gajar_ka_halwa', 'garlic_bread', 'gavvalu', 'ghevar', 'gnocchi', 'greek_salad', 'grilled_cheese_sandwich', 'grilled_salmon', 'guacamole', 'gulab_jamun', 'gyoza', 'hamburger', 'hot_and_sour_soup', 'hot_dog', 'huevos_rancheros', 'hummus', 'ice_cream', 'imarti', 'jalebi', 'kachori', 'kadai_paneer', 'kadhi_pakoda', 'kajjikaya', 'kakinada_khaja', 'kalakand', 'karela_bharta', 'kofta', 'kuzhi_paniyaram', 'lasagna', 'lassi', 'ledikeni', 'litti_chokha', 'lobster_bisque', 'lobster_roll_sandwich', 'lyangcha', 'maach_jhol', 'macaroni_and_cheese', 'macarons', 'makki_di_roti_sarson_da_saag', 'malapua', 'misi_roti', 'miso_soup', 'misti_doi', 'modak', 'mussels', 'mysore_pak', 'naan', 'nachos', 'navrattan_korma', 'omelette', 'onion_rings', 'oysters', 'pad_thai', 'paella', 'palak_paneer', 'pancakes', 'paneer_butter_masala', 'panna_cotta', 'peking_duck', 'phirni', 'pho', 'pithe', 'pizza', 'poha', 'poornalu', 'pootharekulu', 'pork_chop', 'poutine', 'prime_rib', 'pulled_pork_sandwich', 'qubani_ka_meetha', 'rabri', 'ramen', 'ras_malai', 'rasgulla', 'ravioli', 'red_velvet_cake', 'risotto', 'samosa', 'sandesh', 'sashimi', 'scallops', 'seaweed_salad', 'shankarpali', 'sheer_korma', 'sheera', 'shrikhand', 'shrimp_and_grits', 'sohan_halwa', 'sohan_papdi', 'spaghetti_bolognese', 'spaghetti_carbonara', 'spring_rolls', 'steak', 'strawberry_shortcake', 'sushi', 'sutar_feni', 'tacos', 'takoyaki', 'tiramisu', 'tuna_tartare', 'unni_appam', 'waffles']

NUTRITION_DB = {
    "adhirasam": {"calories": 415, "density": "High", "emoji": "🍰"},
    "aloo_gobi": {"calories": 130, "density": "Low", "emoji": "🥗"},
    "aloo_matar": {"calories": 105, "density": "Low", "emoji": "🥗"},
    "aloo_methi": {"calories": 120, "density": "Low", "emoji": "🥗"},
    "aloo_shimla_mirch": {"calories": 95, "density": "Low", "emoji": "🥗"},
    "aloo_tikki": {"calories": 270, "density": "High", "emoji": "🥗"},
    "anarsa": {"calories": 580, "density": "High", "emoji": "🍰"},
    "apple_pie": {"calories": 237, "density": "Medium", "emoji": "🍰"},
    "ariselu": {"calories": 415, "density": "High", "emoji": "🍰"},
    "baby_back_ribs": {"calories": 360, "density": "High", "emoji": "🍖"},
    "baklava": {"calories": 428, "density": "High", "emoji": "🍰"},
    "bandar_laddu": {"calories": 450, "density": "High", "emoji": "🍰"},
    "basundi": {"calories": 215, "density": "Medium", "emoji": "🍰"},
    "beef_carpaccio": {"calories": 150, "density": "Low", "emoji": "🍖"},
    "beef_tartare": {"calories": 240, "density": "Medium", "emoji": "🍖"},
    "beet_salad": {"calories": 90, "density": "Low", "emoji": "🥗"},
    "beignets": {"calories": 400, "density": "High", "emoji": "🍰"},
    "bhatura": {"calories": 300, "density": "High", "emoji": "🥗"},
    "bhindi_masala": {"calories": 95, "density": "Low", "emoji": "🥗"},
    "bibimbap": {"calories": 160, "density": "Medium", "emoji": "🥗"},
    "biryani": {"calories": 175, "density": "Medium", "emoji": "🥗"},
    "boondi": {"calories": 480, "density": "High", "emoji": "🥗"},
    "bread_pudding": {"calories": 300, "density": "High", "emoji": "🍰"},
    "breakfast_burrito": {"calories": 200, "density": "Medium", "emoji": "🥗"},
    "bruschetta": {"calories": 160, "density": "Medium", "emoji": "🥗"},
    "butter_chicken": {"calories": 205, "density": "Medium", "emoji": "🥗"},
    "caesar_salad": {"calories": 150, "density": "Low", "emoji": "🥗"},
    "cannoli": {"calories": 320, "density": "High", "emoji": "🍰"},
    "caprese_salad": {"calories": 130, "density": "Low", "emoji": "🥗"},
    "carrot_cake": {"calories": 415, "density": "High", "emoji": "🍰"},
    "ceviche": {"calories": 110, "density": "Low", "emoji": "🍖"},
    "chak_hao_kheer": {"calories": 180, "density": "Medium", "emoji": "🍰"},
    "cham_cham": {"calories": 350, "density": "High", "emoji": "🍰"},
    "chana_masala": {"calories": 120, "density": "Low", "emoji": "🥗"},
    "chapati": {"calories": 297, "density": "High", "emoji": "🥗"},
    "cheese_plate": {"calories": 380, "density": "High", "emoji": "🥗"},
    "cheesecake": {"calories": 321, "density": "High", "emoji": "🍰"},
    "chhena_kheeri": {"calories": 220, "density": "Medium", "emoji": "🍰"},
    "chicken_curry": {"calories": 140, "density": "Low", "emoji": "🍖"},
    "chicken_quesadilla": {"calories": 280, "density": "High", "emoji": "🍖"},
    "chicken_razala": {"calories": 160, "density": "Medium", "emoji": "🍖"},
    "chicken_tikka": {"calories": 150, "density": "Low", "emoji": "🍖"},
    "chicken_tikka_masala": {"calories": 170, "density": "Medium", "emoji": "🍖"},
    "chicken_wings": {"calories": 290, "density": "High", "emoji": "🍖"},
    "chikki": {"calories": 480, "density": "High", "emoji": "🍰"},
    "chocolate_cake": {"calories": 380, "density": "High", "emoji": "🍰"},
    "chocolate_mousse": {"calories": 350, "density": "High", "emoji": "🍰"},
    "churros": {"calories": 360, "density": "High", "emoji": "🍰"},
    "clam_chowder": {"calories": 100, "density": "Low", "emoji": "🍛"},
    "club_sandwich": {"calories": 220, "density": "Medium", "emoji": "🍖"},
    "crab_cakes": {"calories": 200, "density": "Medium", "emoji": "🍖"},
    "creme_brulee": {"calories": 350, "density": "High", "emoji": "🍰"},
    "croque_madame": {"calories": 280, "density": "High", "emoji": "🍖"},
    "cup_cakes": {"calories": 380, "density": "High", "emoji": "🍰"},
    "daal_baati_churma": {"calories": 380, "density": "High", "emoji": "🥗"},
    "daal_puri": {"calories": 280, "density": "High", "emoji": "🥗"},
    "dal_makhani": {"calories": 120, "density": "Low", "emoji": "🥗"},
    "dal_tadka": {"calories": 110, "density": "Low", "emoji": "🥗"},
    "deviled_eggs": {"calories": 250, "density": "Medium", "emoji": "🥗"},
    "dharwad_pedha": {"calories": 420, "density": "High", "emoji": "🍰"},
    "donuts": {"calories": 420, "density": "High", "emoji": "🍰"},
    "doodhpak": {"calories": 180, "density": "Medium", "emoji": "🍰"},
    "double_ka_meetha": {"calories": 320, "density": "High", "emoji": "🍰"},
    "dum_aloo": {"calories": 140, "density": "Low", "emoji": "🥗"},
    "dumplings": {"calories": 120, "density": "Low", "emoji": "🥗"},
    "edamame": {"calories": 121, "density": "Low", "emoji": "🥗"},
    "eggs_benedict": {"calories": 230, "density": "Medium", "emoji": "🥗"},
    "escargots": {"calories": 110, "density": "Low", "emoji": "🍖"},
    "falafel": {"calories": 333, "density": "High", "emoji": "🥗"},
    "filet_mignon": {"calories": 267, "density": "High", "emoji": "🍖"},
    "fish_and_chips": {"calories": 230, "density": "Medium", "emoji": "🍖"},
    "foie_gras": {"calories": 462, "density": "High", "emoji": "🍖"},
    "french_fries": {"calories": 312, "density": "High", "emoji": "🥗"},
    "french_onion_soup": {"calories": 50, "density": "Low", "emoji": "🥗"},
    "french_toast": {"calories": 230, "density": "Medium", "emoji": "🍰"},
    "fried_calamari": {"calories": 175, "density": "Medium", "emoji": "🍖"},
    "fried_rice": {"calories": 163, "density": "Medium", "emoji": "🥗"},
    "frozen_yogurt": {"calories": 159, "density": "Medium", "emoji": "🍰"},
    "gajar_ka_halwa": {"calories": 350, "density": "High", "emoji": "🍰"},
    "garlic_bread": {"calories": 350, "density": "High", "emoji": "🥗"},
    "gavvalu": {"calories": 430, "density": "High", "emoji": "🍰"},
    "ghevar": {"calories": 450, "density": "High", "emoji": "🍰"},
    "gnocchi": {"calories": 133, "density": "Low", "emoji": "🥗"},
    "greek_salad": {"calories": 100, "density": "Low", "emoji": "🥗"},
    "grilled_cheese_sandwich": {"calories": 330, "density": "High", "emoji": "🥗"},
    "grilled_salmon": {"calories": 206, "density": "Medium", "emoji": "🍖"},
    "guacamole": {"calories": 160, "density": "Medium", "emoji": "🥗"},
    "gulab_jamun": {"calories": 320, "density": "High", "emoji": "🍰"},
    "gyoza": {"calories": 160, "density": "Medium", "emoji": "🥗"},
    "hamburger": {"calories": 295, "density": "High", "emoji": "🍖"},
    "hot_and_sour_soup": {"calories": 40, "density": "Low", "emoji": "🥗"},
    "hot_dog": {"calories": 290, "density": "High", "emoji": "🍖"},
    "huevos_rancheros": {"calories": 150, "density": "Low", "emoji": "🥗"},
    "hummus": {"calories": 166, "density": "Medium", "emoji": "🥗"},
    "ice_cream": {"calories": 207, "density": "Medium", "emoji": "🍰"},
    "imarti": {"calories": 380, "density": "High", "emoji": "🍰"},
    "jalebi": {"calories": 380, "density": "High", "emoji": "🍰"},
    "kachori": {"calories": 350, "density": "High", "emoji": "🥗"},
    "kadai_paneer": {"calories": 260, "density": "High", "emoji": "🥗"},
    "kadhi_pakoda": {"calories": 150, "density": "Low", "emoji": "🥗"},
    "kajjikaya": {"calories": 420, "density": "High", "emoji": "🍰"},
    "kakinada_khaja": {"calories": 420, "density": "High", "emoji": "🍰"},
    "kalakand": {"calories": 350, "density": "High", "emoji": "🍰"},
    "karela_bharta": {"calories": 100, "density": "Low", "emoji": "🥗"},
    "kofta": {"calories": 180, "density": "Medium", "emoji": "🥗"},
    "kuzhi_paniyaram": {"calories": 200, "density": "Medium", "emoji": "🍰"},
    "lasagna": {"calories": 135, "density": "Low", "emoji": "🥗"},
    "lassi": {"calories": 85, "density": "Low", "emoji": "🥗"},
    "ledikeni": {"calories": 330, "density": "High", "emoji": "🍰"},
    "litti_chokha": {"calories": 250, "density": "Medium", "emoji": "🥗"},
    "lobster_bisque": {"calories": 120, "density": "Low", "emoji": "🍖"},
    "lobster_roll_sandwich": {"calories": 220, "density": "Medium", "emoji": "🍖"},
    "lyangcha": {"calories": 350, "density": "High", "emoji": "🍰"},
    "maach_jhol": {"calories": 140, "density": "Low", "emoji": "🍖"},
    "macaroni_and_cheese": {"calories": 210, "density": "Medium", "emoji": "🥗"},
    "macarons": {"calories": 450, "density": "High", "emoji": "🍰"},
    "makki_di_roti_sarson_da_saag": {"calories": 150, "density": "Low", "emoji": "🥗"},
    "malapua": {"calories": 330, "density": "High", "emoji": "🍰"},
    "misi_roti": {"calories": 280, "density": "High", "emoji": "🥗"},
    "miso_soup": {"calories": 35, "density": "Low", "emoji": "🥗"},
    "misti_doi": {"calories": 150, "density": "Low", "emoji": "🍰"},
    "modak": {"calories": 250, "density": "Medium", "emoji": "🍰"},
    "mussels": {"calories": 172, "density": "Medium", "emoji": "🍖"},
    "mysore_pak": {"calories": 550, "density": "High", "emoji": "🍰"},
    "naan": {"calories": 310, "density": "High", "emoji": "🥗"},
    "nachos": {"calories": 300, "density": "High", "emoji": "🥗"},
    "navrattan_korma": {"calories": 140, "density": "Low", "emoji": "🥗"},
    "omelette": {"calories": 154, "density": "Medium", "emoji": "🥗"},
    "onion_rings": {"calories": 410, "density": "High", "emoji": "🥗"},
    "oysters": {"calories": 80, "density": "Low", "emoji": "🍖"},
    "pad_thai": {"calories": 170, "density": "Medium", "emoji": "🥗"},
    "paella": {"calories": 150, "density": "Low", "emoji": "🥗"},
    "palak_paneer": {"calories": 160, "density": "Medium", "emoji": "🥗"},
    "pancakes": {"calories": 227, "density": "Medium", "emoji": "🍰"},
    "paneer_butter_masala": {"calories": 280, "density": "High", "emoji": "🥗"},
    "panna_cotta": {"calories": 300, "density": "High", "emoji": "🍰"},
    "peking_duck": {"calories": 337, "density": "High", "emoji": "🍖"},
    "phirni": {"calories": 160, "density": "Medium", "emoji": "🍰"},
    "pho": {"calories": 90, "density": "Low", "emoji": "🥗"},
    "pithe": {"calories": 220, "density": "Medium", "emoji": "🍰"},
    "pizza": {"calories": 266, "density": "High", "emoji": "🥗"},
    "poha": {"calories": 150, "density": "Low", "emoji": "🥗"},
    "poornalu": {"calories": 280, "density": "High", "emoji": "🍰"},
    "pootharekulu": {"calories": 350, "density": "High", "emoji": "🍰"},
    "pork_chop": {"calories": 250, "density": "Medium", "emoji": "🍖"},
    "poutine": {"calories": 240, "density": "Medium", "emoji": "🥗"},
    "prime_rib": {"calories": 350, "density": "High", "emoji": "🍖"},
    "pulled_pork_sandwich": {"calories": 230, "density": "Medium", "emoji": "🍖"},
    "qubani_ka_meetha": {"calories": 280, "density": "High", "emoji": "🍰"},
    "rabri": {"calories": 200, "density": "Medium", "emoji": "🍰"},
    "ramen": {"calories": 85, "density": "Low", "emoji": "🥗"},
    "ras_malai": {"calories": 250, "density": "Medium", "emoji": "🍰"},
    "rasgulla": {"calories": 180, "density": "Medium", "emoji": "🍰"},
    "ravioli": {"calories": 170, "density": "Medium", "emoji": "🥗"},
    "red_velvet_cake": {"calories": 380, "density": "High", "emoji": "🍰"},
    "risotto": {"calories": 160, "density": "Medium", "emoji": "🥗"},
    "samosa": {"calories": 260, "density": "High", "emoji": "🥗"},
    "sandesh": {"calories": 300, "density": "High", "emoji": "🍰"},
    "sashimi": {"calories": 140, "density": "Low", "emoji": "🍖"},
    "scallops": {"calories": 110, "density": "Low", "emoji": "🍖"},
    "seaweed_salad": {"calories": 45, "density": "Low", "emoji": "🥗"},
    "shankarpali": {"calories": 480, "density": "High", "emoji": "🍰"},
    "sheer_korma": {"calories": 220, "density": "Medium", "emoji": "🍰"},
    "sheera": {"calories": 320, "density": "High", "emoji": "🍰"},
    "shrikhand": {"calories": 260, "density": "High", "emoji": "🍰"},
    "shrimp_and_grits": {"calories": 150, "density": "Low", "emoji": "🍖"},
    "sohan_halwa": {"calories": 520, "density": "High", "emoji": "🍰"},
    "sohan_papdi": {"calories": 500, "density": "High", "emoji": "🍰"},
    "spaghetti_bolognese": {"calories": 130, "density": "Low", "emoji": "🥗"},
    "spaghetti_carbonara": {"calories": 200, "density": "Medium", "emoji": "🥗"},
    "spring_rolls": {"calories": 250, "density": "Medium", "emoji": "🥗"},
    "steak": {"calories": 270, "density": "High", "emoji": "🍖"},
    "strawberry_shortcake": {"calories": 340, "density": "High", "emoji": "🍰"},
    "sushi": {"calories": 143, "density": "Low", "emoji": "🍖"},
    "sutar_feni": {"calories": 480, "density": "High", "emoji": "🍰"},
    "tacos": {"calories": 226, "density": "Medium", "emoji": "🥗"},
    "takoyaki": {"calories": 180, "density": "Medium", "emoji": "🥗"},
    "tiramisu": {"calories": 300, "density": "High", "emoji": "🍰"},
    "tuna_tartare": {"calories": 180, "density": "Medium", "emoji": "🍖"},
    "unni_appam": {"calories": 320, "density": "High", "emoji": "🍰"},
    "waffles": {"calories": 290, "density": "High", "emoji": "🍰"},
    "burger":         {"calories": 295, "density": "High",   "emoji": "🍔"},
    "donuts":         {"calories": 420, "density": "High",   "emoji": "🍩"},
    "french_fries":   {"calories": 312, "density": "High",   "emoji": "🍟"},
    "pizza":          {"calories": 266, "density": "High",   "emoji": "🍕"},
    "salad":          {"calories": 100, "density": "Low",    "emoji": "🥗"},
    "sushi":          {"calories": 143, "density": "Low",    "emoji": "🍣"},
    "tacos":          {"calories": 226, "density": "Medium", "emoji": "🌮"},
    "biryani":        {"calories": 175, "density": "Medium", "emoji": "🍛"},
    "butter_chicken": {"calories": 205, "density": "Medium", "emoji": "🍗"},
    "chole_bhature":  {"calories": 300, "density": "High",   "emoji": "🫓"},
    "dosa":           {"calories": 170, "density": "Low",    "emoji": "🥞"},
    "idli":           {"calories": 60,  "density": "Low",    "emoji": "⚪"},
    "jalebi":         {"calories": 380, "density": "High",   "emoji": "🍬"},
    "paneer_tikka":   {"calories": 260, "density": "Medium", "emoji": "🧀"},
    "samosa":         {"calories": 260, "density": "High",   "emoji": "🔺"},
}

DENSITY_COLOR = {"Low": "green", "Medium": "blue", "High": "amber"}

# ─────────────────────────────────────────────
# Dynamic Calorie Base Data (kcal per 100g)
# ─────────────────────────────────────────────
NUTRITION_DATA = {
    'adhirasam': 415, 'aloo_gobi': 130, 'aloo_matar': 105, 'aloo_methi': 120, 'aloo_shimla_mirch': 95,
    'aloo_tikki': 270, 'anarsa': 580, 'apple_pie': 237, 'ariselu': 415, 'baby_back_ribs': 360,
    'baklava': 428, 'bandar_laddu': 450, 'basundi': 215, 'beef_carpaccio': 150, 'beef_tartare': 240,
    'beet_salad': 90, 'beignets': 400, 'bhatura': 300, 'bhindi_masala': 95, 'bibimbap': 160,
    'biryani': 175, 'boondi': 480, 'bread_pudding': 300, 'breakfast_burrito': 200, 'bruschetta': 160,
    'butter_chicken': 205, 'caesar_salad': 150, 'cannoli': 320, 'caprese_salad': 130, 'carrot_cake': 415,
    'ceviche': 110, 'chak_hao_kheer': 180, 'cham_cham': 350, 'chana_masala': 120, 'chapati': 297,
    'cheese_plate': 380, 'cheesecake': 321, 'chhena_kheeri': 220, 'chicken_curry': 140, 'chicken_quesadilla': 280,
    'chicken_razala': 160, 'chicken_tikka': 150, 'chicken_tikka_masala': 170, 'chicken_wings': 290, 'chikki': 480,
    'chocolate_cake': 380, 'chocolate_mousse': 350, 'churros': 360, 'clam_chowder': 100, 'club_sandwich': 220,
    'crab_cakes': 200, 'creme_brulee': 350, 'croque_madame': 280, 'cup_cakes': 380, 'daal_baati_churma': 380,
    'daal_puri': 280, 'dal_makhani': 120, 'dal_tadka': 110, 'deviled_eggs': 250, 'dharwad_pedha': 420,
    'donuts': 420, 'doodhpak': 180, 'double_ka_meetha': 320, 'dum_aloo': 140, 'dumplings': 120,
    'edamame': 121, 'eggs_benedict': 230, 'escargots': 110, 'falafel': 333, 'filet_mignon': 267,
    'fish_and_chips': 230, 'foie_gras': 462, 'french_fries': 312, 'french_onion_soup': 50, 'french_toast': 230,
    'fried_calamari': 175, 'fried_rice': 163, 'frozen_yogurt': 159, 'gajar_ka_halwa': 350, 'garlic_bread': 350,
    'gavvalu': 430, 'ghevar': 450, 'gnocchi': 133, 'greek_salad': 100, 'grilled_cheese_sandwich': 330,
    'grilled_salmon': 206, 'guacamole': 160, 'gulab_jamun': 320, 'gyoza': 160, 'hamburger': 295,
    'hot_and_sour_soup': 40, 'hot_dog': 290, 'huevos_rancheros': 150, 'hummus': 166, 'ice_cream': 207,
    'imarti': 380, 'jalebi': 380, 'kachori': 350, 'kadai_paneer': 260, 'kadhi_pakoda': 150,
    'kajjikaya': 420, 'kakinada_khaja': 420, 'kalakand': 350, 'karela_bharta': 100, 'kofta': 180,
    'kuzhi_paniyaram': 200, 'lasagna': 135, 'lassi': 85, 'ledikeni': 330, 'litti_chokha': 250,
    'lobster_bisque': 120, 'lobster_roll_sandwich': 220, 'lyangcha': 350, 'maach_jhol': 140, 'macaroni_and_cheese': 210,
    'macarons': 450, 'makki_di_roti_sarson_da_saag': 150, 'malapua': 330, 'misi_roti': 280, 'miso_soup': 35,
    'misti_doi': 150, 'modak': 250, 'mussels': 172, 'mysore_pak': 550, 'naan': 310,
    'nachos': 300, 'navrattan_korma': 140, 'omelette': 154, 'onion_rings': 410, 'oysters': 80,
    'pad_thai': 170, 'paella': 150, 'palak_paneer': 160, 'pancakes': 227, 'paneer_butter_masala': 280,
    'panna_cotta': 300, 'peking_duck': 337, 'phirni': 160, 'pho': 90, 'pithe': 220,
    'pizza': 266, 'poha': 150, 'poornalu': 280, 'pootharekulu': 350, 'pork_chop': 250,
    'poutine': 240, 'prime_rib': 350, 'pulled_pork_sandwich': 230, 'qubani_ka_meetha': 280, 'rabri': 200,
    'ramen': 85, 'ras_malai': 250, 'rasgulla': 180, 'ravioli': 170, 'red_velvet_cake': 380,
    'risotto': 160, 'samosa': 260, 'sandesh': 300, 'sashimi': 140, 'scallops': 110,
    'seaweed_salad': 45, 'shankarpali': 480, 'sheer_korma': 220, 'sheera': 320, 'shrikhand': 260,
    'shrimp_and_grits': 150, 'sohan_halwa': 520, 'sohan_papdi': 500, 'spaghetti_bolognese': 130, 'spaghetti_carbonara': 200,
    'spring_rolls': 250, 'steak': 270, 'strawberry_shortcake': 340, 'sushi': 143, 'sutar_feni': 480,
    'tacos': 226, 'takoyaki': 180, 'tiramisu': 300, 'tuna_tartare': 180, 'unni_appam': 320,
    'waffles': 290
}

# ─────────────────────────────────────────────
# Helper Components
# ─────────────────────────────────────────────
def metric_card(icon, label, value, unit, color="green"):
    return (
        f'<div class="metric-card {color}">'
        f'<span class="mc-icon">{icon}</span>'
        f'<div class="mc-label">{label}</div>'
        f'<div class="mc-value">{value}</div>'
        f'<div class="mc-unit">{unit}</div>'
        f'</div>'
    )


def advice_card(style, icon, title, body):
    return (
        f'<div class="advice-card advice-{style}">'
        f'<div class="advice-title"><span class="advice-icon">{icon}</span>{title}</div>'
        f'<div>{body}</div>'
        f'</div>'
    )


# ─────────────────────────────────────────────
# Sidebar – BMI Profiler
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-section-title">Health Profile</div>', unsafe_allow_html=True)
    st.markdown("#### 🧬 BMI Calculator")
    st.markdown(
        '<div style="color:var(--text-muted);font-size:0.82rem;margin-bottom:1rem;">'
        'Enter your details for personalised nutritional advice.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-section-title">Body Metrics</div>', unsafe_allow_html=True)
    weight    = st.number_input("Weight (kg)",  min_value=1.0,  value=70.0,  step=0.5)
    height_cm = st.number_input("Height (cm)",  min_value=50.0, value=170.0, step=1.0)

    bmi_category = "Unknown"
    if height_cm > 0:
        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)

        if bmi < 18.5:
            bmi_category, badge_cls, bmi_color = "Underweight", "badge-underweight", "#4f9cf9"
        elif bmi < 24.9:
            bmi_category, badge_cls, bmi_color = "Normal", "badge-normal", "#00e5a0"
        elif bmi < 29.9:
            bmi_category, badge_cls, bmi_color = "Overweight", "badge-overweight", "#f9a825"
        else:
            bmi_category, badge_cls, bmi_color = "Obese", "badge-obese", "#ff5c5c"

        st.markdown(
            f'<div class="bmi-card">'
            f'<div class="bmi-label">Body Mass Index</div>'
            f'<div class="bmi-value" style="color:{bmi_color};">{bmi:.1f}</div>'
            f'<div class="bmi-label">kg/m\u00b2</div>'
            f'<span class="bmi-badge {badge_cls}">{bmi_category}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="sidebar-section-title">BMI Reference</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.78rem;color:var(--text-muted);line-height:1.8;">'
        '🔵&nbsp;<b style="color:#4f9cf9;">Underweight</b>&nbsp;— &lt;18.5<br>'
        '🟢&nbsp;<b style="color:#00e5a0;">Normal</b>&nbsp;— 18.5–24.9<br>'
        '🟡&nbsp;<b style="color:#f9a825;">Overweight</b>&nbsp;— 25–29.9<br>'
        '🔴&nbsp;<b style="color:#ff5c5c;">Obese</b>&nbsp;— ≥30'
        '</div>',
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────
# Main Page – Hero
# ─────────────────────────────────────────────
st.markdown(
    '<div class="hero-header">'
    '<div class="hero-title">🥗 Health Check AI</div>'
    '<p class="hero-sub">Upload a food photo to instantly identify the dish, estimate calories,'
    ' and receive personalised dietary guidance based on your health profile.</p>'
    '</div>',
    unsafe_allow_html=True
)


# ── Model loading ─────────────────────────────
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model("efficientnet_v2s_food_model_ULTIMATE.keras")
        return model
    except Exception:
        return None


model = load_model()

if model is None:
    st.markdown(
        '<div class="status-pill status-err">'
        '<span class="status-dot dot-err"></span>'
        'Model not found — place <code>efficientnet_v2s_food_model_ULTIMATE.keras</code> in the app directory.'
        '</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="status-pill status-ok">'
        '<span class="status-dot dot-ok"></span>'
        'Health Check AI model loaded &amp; ready'
        '</div>',
        unsafe_allow_html=True
    )

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# ── Upload zone ────────────────────────────────
st.markdown(
    '<div class="section-header">'
    '<span class="section-header-icon">📸</span>'
    '<span class="section-header-text">Scan Your Food</span>'
    '</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Drop or browse a food image (JPG / PNG)",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed",
)

# ── Analysis ───────────────────────────────────
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    col_img, col_result = st.columns([1, 1], gap="large")

    with col_img:
        st.markdown(
            '<div class="section-header">'
            '<span class="section-header-icon">🖼️</span>'
            '<span class="section-header-text">Uploaded Image</span>'
            '</div>',
            unsafe_allow_html=True
        )
        st.image(image, use_column_width=True)

    with col_result:
        if model is not None:
            with st.spinner("Analysing with Health Check AI…"):
                img_resized  = image.resize((224, 224))
                img_array    = tf.keras.utils.img_to_array(img_resized)
                img_array    = tf.expand_dims(img_array, 0)
                predictions  = model.predict(img_array, verbose=0)
                pred_idx     = int(np.argmax(predictions, axis=1)[0])
                predicted_class = FOOD_CLASSES[pred_idx]
                confidence   = float(np.max(predictions))

            nutrition  = NUTRITION_DB.get(predicted_class, {"calories": "—", "density": "Unknown", "emoji": "🍽️"})
            calories   = nutrition["calories"]
            density    = nutrition["density"]
            food_emoji = nutrition["emoji"]
            food_name  = predicted_class.replace("_", " ").title()
            card_color = DENSITY_COLOR.get(density, "blue")

            st.markdown(
                f'<div class="result-heading">{food_emoji} {food_name}</div>'
                f'<p class="result-confidence">Confidence: <strong style="color:var(--accent-green);">{confidence:.1%}</strong></p>',
                unsafe_allow_html=True
            )

            # ── Dynamic Calorie Predictor ──
            st.markdown(
                '<div class="section-header" style="margin-top:1.2rem;">'
                '<span class="section-header-icon">⚖️</span>'
                '<span class="section-header-text">Portion Size</span>'
                '</div>',
                unsafe_allow_html=True
            )
            
            # 1. Quantity Input (reusing your dark theme number input styles)
            portion_g = st.number_input("Enter estimated weight in grams:", min_value=1, value=100, step=10)
            
            # 2. Dynamic Calculation (defaulting to 200 kcal/100g if item is missing from NUTRITION_DATA)
            base_cals_per_100g = NUTRITION_DATA.get(predicted_class, 200)
            total_calories = (base_cals_per_100g / 100.0) * portion_g
            
            # 3. UI Display (reusing your premium glassmorphism metric_card component)
            st.markdown(
                f'<div class="metric-grid">'
                f'{metric_card("🎯", "Total Calories", f"{total_calories:.0f}", f"kcal for {portion_g}g portion", "amber")}'
                f'</div>',
                unsafe_allow_html=True
            )

            # Nutritional metric cards
            st.markdown(
                '<div class="section-header" style="margin-top:1.2rem;">'
                '<span class="section-header-icon">📊</span>'
                '<span class="section-header-text">Nutritional Snapshot</span>'
                '</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="metric-grid">'
                f'{metric_card("🔥", "Estimated Calories", calories, "kcal per 100g", card_color)}'
                f'{metric_card("⚡", "Calorie Density", density, "energy concentration", card_color)}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown('<div class="fancy-divider" style="margin:1.2rem 0;"></div>', unsafe_allow_html=True)

            # Personalised health advice
            st.markdown(
                '<div class="section-header">'
                '<span class="section-header-icon">💡</span>'
                '<span class="section-header-text">Personalised Health Advice</span>'
                '</div>',
                unsafe_allow_html=True
            )

            if bmi_category == "Underweight":
                if density == "High":
                    html_advice = advice_card(
                        "info", "✅", "Great Pick for Gaining!",
                        f"Since you are <b>underweight</b>, calorie-dense foods like <b>{food_name}</b> "
                        f"can help you achieve a caloric surplus. Pair with nutritious whole foods for best results."
                    )
                else:
                    html_advice = advice_card(
                        "info", "💪", "Light Meal — Boost It!",
                        f"<b>{food_name}</b> is a light option. Consider pairing it with healthy fats "
                        f"(nuts, avocados, dairy) to meet your caloric surplus goals."
                    )
            elif bmi_category == "Normal":
                html_advice = advice_card(
                    "success", "🎯", "Balanced Choice!",
                    f"<b>{food_name}</b> fits well into a normal maintenance diet. Keep a balanced mix "
                    f"of proteins, fats, and carbohydrates throughout the day."
                )
            elif bmi_category == "Overweight":
                if density == "High":
                    html_advice = advice_card(
                        "warning", "⚠️", "Consume in Moderation",
                        f"Your BMI indicates <b>overweight</b>. High-calorie items like <b>{food_name}</b> "
                        f"should be enjoyed in strict moderation. Consider smaller portions or a lighter alternative."
                    )
                else:
                    html_advice = advice_card(
                        "success", "✅", "Smart, Lower-Calorie Choice!",
                        f"Good pick! <b>{food_name}</b> is relatively low in calories — "
                        f"great for your weight-management goals. Keep it up!"
                    )
            elif bmi_category == "Obese":
                if density == "High":
                    html_advice = advice_card(
                        "danger", "🚨", "Strict Limit Recommended",
                        f"Your BMI indicates <b>obesity</b>. High-calorie foods like <b>{food_name}</b> "
                        f"should be avoided or consumed only occasionally. Consult a healthcare professional."
                    )
                else:
                    html_advice = advice_card(
                        "success", "🌿", "Better Choice!",
                        f"<b>{food_name}</b> is a lower-density option — a positive step towards managing "
                        f"your weight. Focus on whole, unprocessed foods and maintain regular physical activity."
                    )
            else:
                html_advice = advice_card(
                    "info", "ℹ️", "Set Your Health Profile",
                    "Enter your weight and height in the sidebar to get personalised nutritional advice "
                    "tailored to your BMI."
                )

            st.markdown(html_advice, unsafe_allow_html=True)

        else:
            st.markdown(
                advice_card(
                    "danger", "⚠️", "Model Unavailable",
                    "The AI model could not be loaded. Please ensure the model file is present "
                    "in the application directory."
                ),
                unsafe_allow_html=True
            )


