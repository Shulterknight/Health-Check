import re
import os

UPDATED_NUTRITION_DATA = {
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
    'misti_doi': 150, 'modak': 250, 'mussels': 172, 'mysore_pak': 550, 'naan': 310, 'nachos': 300, 
    'navrattan_korma': 140, 'omelette': 154, 'onion_rings': 410, 'oysters': 80, 'pad_thai': 170, 
    'paella': 150, 'palak_paneer': 160, 'pancakes': 227, 'paneer_butter_masala': 280, 'panna_cotta': 300, 
    'peking_duck': 337, 'phirni': 160, 'pho': 90, 'pithe': 220, 'pizza': 266, 'poha': 150, 
    'poornalu': 280, 'pootharekulu': 350, 'pork_chop': 250, 'poutine': 240, 'prime_rib': 350, 
    'pulled_pork_sandwich': 230, 'qubani_ka_meetha': 280, 'rabri': 200, 'ramen': 85, 'ras_malai': 250, 
    'rasgulla': 180, 'ravioli': 170, 'red_velvet_cake': 380, 'risotto': 160, 'samosa': 260, 
    'sandesh': 300, 'sashimi': 140, 'scallops': 110, 'seaweed_salad': 45, 'shankarpali': 480, 
    'sheer_korma': 220, 'sheera': 320, 'shrikhand': 260, 'shrimp_and_grits': 150, 'sohan_halwa': 520, 
    'sohan_papdi': 500, 'spaghetti_bolognese': 130, 'spaghetti_carbonara': 200, 'spring_rolls': 250, 'steak': 270, 
    'strawberry_shortcake': 340, 'sushi': 143, 'sutar_feni': 480, 'tacos': 226, 'takoyaki': 180, 
    'tiramisu': 300, 'tuna_tartare': 180, 'unni_appam': 320, 'waffles': 290
}

# Sweets/Desserts get sweet emojis, etc.
SWEETS = ['adhirasam', 'anarsa', 'apple_pie', 'ariselu', 'baklava', 'bandar_laddu', 'basundi', 'beignets', 'bread_pudding', 'cannoli', 'carrot_cake', 'chak_hao_kheer', 'cham_cham', 'cheesecake', 'chhena_kheeri', 'chikki', 'chocolate_cake', 'chocolate_mousse', 'churros', 'creme_brulee', 'cup_cakes', 'dharwad_pedha', 'donuts', 'doodhpak', 'double_ka_meetha', 'french_toast', 'frozen_yogurt', 'gajar_ka_halwa', 'gavvalu', 'ghevar', 'gulab_jamun', 'ice_cream', 'imarti', 'jalebi', 'kajjikaya', 'kakinada_khaja', 'kalakand', 'kuzhi_paniyaram', 'ledikeni', 'lyangcha', 'macarons', 'malapua', 'misti_doi', 'modak', 'mysore_pak', 'pancakes', 'panna_cotta', 'phirni', 'pithe', 'poornalu', 'pootharekulu', 'qubani_ka_meetha', 'rabri', 'ras_malai', 'rasgulla', 'red_velvet_cake', 'sandesh', 'shankarpali', 'sheer_korma', 'sheera', 'shrikhand', 'sohan_halwa', 'sohan_papdi', 'strawberry_shortcake', 'sutar_feni', 'tiramisu', 'unni_appam', 'waffles']
MEATS = ['baby_back_ribs', 'beef_carpaccio', 'beef_tartare', 'ceviche', 'chicken_curry', 'chicken_quesadilla', 'chicken_razala', 'chicken_tikka', 'chicken_tikka_masala', 'chicken_wings', 'club_sandwich', 'crab_cakes', 'croque_madame', 'escargots', 'filet_mignon', 'fish_and_chips', 'foie_gras', 'fried_calamari', 'grilled_salmon', 'hamburger', 'hot_dog', 'lobster_bisque', 'lobster_roll_sandwich', 'maach_jhol', 'mussels', 'oysters', 'peking_duck', 'pork_chop', 'prime_rib', 'pulled_pork_sandwich', 'sashimi', 'scallops', 'shrimp_and_grits', 'steak', 'sushi', 'tuna_tartare']
VEG = ['aloo_gobi', 'aloo_matar', 'aloo_methi', 'aloo_shimla_mirch', 'aloo_tikki', 'beet_salad', 'bhatura', 'bhindi_masala', 'bibimbap', 'biryani', 'boondi', 'breakfast_burrito', 'bruschetta', 'butter_chicken', 'caesar_salad', 'caprese_salad', 'chana_masala', 'chapati', 'cheese_plate', 'daal_baati_churma', 'daal_puri', 'dal_makhani', 'dal_tadka', 'deviled_eggs', 'dum_aloo', 'dumplings', 'edamame', 'eggs_benedict', 'falafel', 'french_fries', 'french_onion_soup', 'fried_rice', 'garlic_bread', 'gnocchi', 'greek_salad', 'grilled_cheese_sandwich', 'guacamole', 'gyoza', 'hot_and_sour_soup', 'huevos_rancheros', 'hummus', 'kachori', 'kadai_paneer', 'kadhi_pakoda', 'karela_bharta', 'kofta', 'lasagna', 'lassi', 'litti_chokha', 'macaroni_and_cheese', 'makki_di_roti_sarson_da_saag', 'misi_roti', 'miso_soup', 'naan', 'nachos', 'navrattan_korma', 'omelette', 'onion_rings', 'pad_thai', 'paella', 'palak_paneer', 'paneer_butter_masala', 'pho', 'pizza', 'poha', 'poutine', 'ramen', 'ravioli', 'risotto', 'samosa', 'seaweed_salad', 'spaghetti_bolognese', 'spaghetti_carbonara', 'spring_rolls', 'tacos', 'takoyaki']

def get_density(c):
    if c <= 150: return "Low"
    elif c <= 250: return "Medium"
    else: return "High"

def get_emoji(name):
    if name in SWEETS: return "🍰"
    if name in MEATS: return "🍖"
    if name in VEG: return "🥗"
    return "🍛"

db_lines = ["NUTRITION_DB = {"]
for name, c in UPDATED_NUTRITION_DATA.items():
    emoji = get_emoji(name)
    dens = get_density(c)
    db_lines.append(f'    "{name}": {{"calories": {c}, "density": "{dens}", "emoji": "{emoji}"}},')

db_lines.append("}")
db_str = "\\n".join(db_lines)

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

pattern = r"NUTRITION_DB\s*=\s*\{.*?\}"
updated_content, count = re.subn(pattern, db_str, content, flags=re.DOTALL)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(updated_content)
