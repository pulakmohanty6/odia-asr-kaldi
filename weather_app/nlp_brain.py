import re

# Comprehensive map of Odisha locations to English for the Weather API
LOCATION_MAP = {
    # Major Urban Hubs
    "ଭୁବନେଶ୍ୱର": "Bhubaneswar",
    "ରାଉରକେଲା": "Rourkela",
    "ବ୍ରହ୍ମପୁର": "Berhampur",
    
    # All 30 Districts of Odisha
    "ଅନୁଗୁଳ": "Angul", "ବଲାଙ୍ଗୀର": "Balangir", "ବାଲେଶ୍ୱର": "Balasore",
    "ବାରଗଡ": "Bargarh", "ଭଦ୍ରକ": "Bhadrak", "ବୌଦ୍ଧ": "Boudh",
    "କଟକ": "Cuttack", "ଦେବଗଡ": "Deogarh", "ଢେଙ୍କାନାଳ": "Dhenkanal",
    "ଗଜପତି": "Gajapati", "ଗଞ୍ଜାମ": "Ganjam", "ଜଗତସିଂହପୁର": "Jagatsinghpur",
    "ଯାଜପୁର": "Jajpur", "ଝାରସୁଗୁଡା": "Jharsuguda", "କଳାହାଣ୍ଡି": "Kalahandi",
    "କନ୍ଧମାଳ": "Kandhamal", "କେନ୍ଦ୍ରାପଡା": "Kendrapara", "କେନ୍ଦୁଝର": "Keonjhar",
    "ଖୋର୍ଦ୍ଧା": "Khordha", "କୋରାପୁଟ": "Koraput", "ମାଲକାନଗିରି": "Malkangiri",
    "ମୟୂରଭଞ୍ଜ": "Mayurbhanj", "ନବରଙ୍ଗପୁର": "Nabarangpur", "ନୟାଗଡ": "Nayagarh",
    "ନୂଆପଡା": "Nuapada", "ପୁରୀ": "Puri", "ରାୟଗଡା": "Rayagada",
    "ସମ୍ବଲପୁର": "Sambalpur", "ସୁବର୍ଣ୍ଣପୁର": "Subarnapur", "ସୁନ୍ଦରଗଡ": "Sundargarh"
}

# Synonyms for Intent mapping
RAIN_KEYWORDS = ["ବର୍ଷା", "ମେଘ", "ପାଣି", "ବାତ୍ୟା", "ତୋଫାନ"]
TEMP_KEYWORDS = ["ତାପମାତ୍ରା", "ଗରମ", "ଥଣ୍ଡା", "ଖରା", "ସେଲସିୟସ"]

def parse_odia_query(kaldi_text):
    """
    Parses raw Odia text from Kaldi and extracts (City, Intent, Time)
    """
    detected_city = "Bhubaneswar" # Safe default
    detected_intent = "general"   # Options: general, rain, temperature
    detected_time = "today"       # Options: today, tomorrow
    
    # 1. Match Location
    for odia_city, eng_city in LOCATION_MAP.items():
        if odia_city in kaldi_text:
            detected_city = eng_city
            break
            
    # 2. Match Time Frame
    if "କାଲି" in kaldi_text or "ଆସନ୍ତାକାଲି" in kaldi_text:
        detected_time = "tomorrow"
        
    # 3. Match Weather Intent
    if any(keyword in kaldi_text for keyword in RAIN_KEYWORDS):
        detected_intent = "rain"
    elif any(keyword in kaldi_text for keyword in TEMP_KEYWORDS):
        detected_intent = "temperature"
        
    return detected_city, detected_intent, detected_time
