import streamlit as st
import requests

# Brand color palette from logo
BACKGROUND_COLOR = "#FAF6F1"
MAIN_BROWN = "#876352"

# Custom CSS for colors and style
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {BACKGROUND_COLOR} !important;
        color: {MAIN_BROWN} !important;
    }}
    div[data-testid="stHeader"] {{
        background-color: {BACKGROUND_COLOR} !important;
    }}
    h1, h2, h3, h4, h5, h6, .stApp {{
        color: {MAIN_BROWN} !important;
    }}
    .stButton>button {{
        background-color: {MAIN_BROWN} !important;
        color: white !important;
        border-radius: 6px;
        border: none;
        font-weight: bold;
    }}
    .stTextInput>div>div>input {{
        background-color: #fffaf3 !important;
        color: {MAIN_BROWN} !important;
        border: 1px solid {MAIN_BROWN} !important;
        border-radius: 4px;
    }}
    .stMultiSelect>div>div>input, .stSelectbox>div>div>input {{
        background-color: #fffaf3 !important;
        color: {MAIN_BROWN} !important;
    }}
    </style>
""", unsafe_allow_html=True)

LANGUAGES = [
    "English", "中文", "Français", "Español", "廣東話", "한국어", "日本語", "ไทย", "हिन्दी"
]

LABELS = {
    # ... (same as provided in previous message — English, ไทย, 中文, Français, Español, 廣東話, 한국어, 日本語, हिन्दी)
    "English": {...},
    "ไทย": {...},
    "中文": {...},
    "Français": {...},
    "Español": {...},
    "廣東話": {...},
    "한국어": {...},
    "日本語": {...},
    "हिन्दी": {...},
}

INTERESTS = {
    "English": [...], "ไทย": [...], "中文": [...], "Français": [...], "Español": [...],
    "廣東話": [...], "한국어": [...], "日本語": [...], "हिन्दी": [...]
}

# ---- LOGO APPEARANCE ----

# Place your logo image as 'assets/skinology_logo.png' in the repo
st.image("assets/skinology_logo.png", width=320, use_column_width=False)

# ---- UI ----

language = st.selectbox(
    "Choose Language / 选择语言 / Sélectionner la langue / Elige idioma / 選擇語言 / 언어 선택 / 言語を選択 / เลือกภาษา / भाषा चुनें",
    LANGUAGES)

labels = LABELS.get(language, LABELS["English"])
interest_options = INTERESTS.get(language, INTERESTS["English"])

st.title(labels["welcome"])

gender = st.selectbox(labels["gender"], [
    "Female", "Male", "Non-binary/Prefer not to say", "Other"
] if language == "English"
    else [
        "หญิง", "ชาย", "ไม่ระบุ/ไม่แบ่งตามเพศ", "อื่นๆ"
    ]) # expand gender for other languages as you wish

interests = st.multiselect(labels["interests"], interest_options)
budget = st.number_input(labels["budget"], min_value=0, value=1000)
lifestyle = st.text_input(labels["lifestyle"])
mbti = st.text_input(labels["mbti"])
face_image = st.file_uploader(labels["face_upload"], type=["jpg", "png"])
body_image = st.file_uploader(labels["body_upload"], type=["jpg", "png"])

if st.button(labels["submit"]):
    files = {}
    if face_image is not None:
        files["face_image"] = (face_image.name, face_image.read(), face_image.type)
    if body_image is not None:
        files["body_image"] = (body_image.name, body_image.read(), body_image.type)

    data = {
        "gender": gender,
        "interests": ",".join(interests),
        "budget": budget,
        "lifestyle": lifestyle,
        "mbti": mbti,
        "language": language
    }
    backend_url = "https://your-backend-service/analyze/"  # CHANGE THIS to your actual backend endpoint!
    try:
        res = requests.post(backend_url, files=files, data=data)
        if res.status_code == 200:
            result_dict = res.json()
            st.success(labels["success"])
            st.write(result_dict["result"])
            pdf_url = result_dict.get("pdf_url", "")
            if pdf_url:
                st.markdown(f"[{labels['pdf_download']}]({pdf_url})")
        else:
            st.error(labels["fail"])
            st.write(res.text)
    except Exception as e:
        st.error(f"{labels['fail']}\n{e}")