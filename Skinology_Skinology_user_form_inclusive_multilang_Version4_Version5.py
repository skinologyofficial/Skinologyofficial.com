import streamlit as st
import requests

# Main color palette (from Skinology logo)
BACKGROUND_COLOR = "#FAF6F1"
MAIN_BROWN = "#876352"

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
    "English": {
        "welcome": "Welcome to AI Beauty & Lifestyle Platform",
        "gender": "Your Gender Identity",
        "interests": "Select your areas of interest",
        "budget": "Budget for Beauty/Fashion (CAD)",
        "lifestyle": "Lifestyle (e.g. office worker, sports, travel)",
        "mbti": "Personality (MBTI if known)",
        "face_upload": "Upload Face Photo (jpg/png)",
        "body_upload": "Upload Full-body Photo (jpg/png)",
        "submit": "Submit and get your personalized protocol",
        "success": "Success! Your personalized results are ready 🎉",
        "fail": "Failed to create results. Please check the uploaded images and your information.",
        "pdf_download": "Download your personalized PDF report here",
    },
    "ไทย": {
        "welcome": "ยินดีต้อนรับสู่ AI Beauty & Lifestyle Platform ระดับโลก 🇨🇦",
        "gender": "อัตลักษณ์ทางเพศของคุณ",
        "interests": "เลือกหมวดคำแนะนำที่สนใจ",
        "budget": "งบประมาณสำหรับสินค้า/แฟชั่น (CAD)",
        "lifestyle": "ไลฟ์สไตล์ (เช่น ทำงานออฟฟิศ, เล่นกีฬา, เที่ยวบ่อย)",
        "mbti": "บุคลิกภาพ (MBTI ถ้ามี)",
        "face_upload": "อัปโหลดรูปใบหน้า (jpg/png)",
        "body_upload": "อัปโหลดรูปเต็มตัว (jpg/png)",
        "submit": "ยืนยันและรับโปรโตคอลเฉพาะบุคคล",
        "success": "สร้างสำเร็จ! ผลลัพธ์ของคุณพร้อมแล้ว 🎉",
        "fail": "ไม่สามารถสร้างผลลัพธ์ โปรดตรวจสอบรูปและข้อมูลที่ส่ง",
        "pdf_download": "ดาวน์โหลด PDF รายงานเฉพาะตัว [คลิกที่นี่]",
    },
    # Add other languages as needed...
}

INTERESTS = {
    "English": [
        "Skincare", "Makeup/Cosmetics", "Hair Care",
        "Fashion & Clothing", "Nutrition/Health",
        "Lifestyle/Personality", "Other"
    ],
    "ไทย": [
        "สกินแคร์", "แต่งหน้า/เครื่องสำอาง", "ดูแลเส้นผม",
        "แฟชั่นและการแต่งกาย", "โภชนาการ/สุขภาพ",
        "ไลฟ์สไตล์/บุคลิกภาพ", "อื่นๆ"
    ],
    # Add other languages as needed...
}

st.set_page_config(page_title="AI Beauty & Lifestyle Platform", page_icon="assets/skinology_logo.png")

st.image("assets/skinology_logo.png", width=320)

language = st.selectbox(
    "Choose Language / 选择语言 / Sélectionner la langue / Elige idioma / 選擇語言 / 언어 선택 / 言語を選択 / เลือกภาษา / भाषा चुनें",
    LANGUAGES
)

labels = LABELS.get(language, LABELS["English"])
interest_options = INTERESTS.get(language, INTERESTS["English"])

st.title(labels["welcome"])

gender = st.selectbox(labels["gender"], [
    "Female", "Male", "Non-binary/Prefer not to say", "Other"
] if language == "English"
    else [
        "หญิง", "ชาย", "ไม่ระบุ/ไม่แบ่งตามเพศ", "อื่นๆ"
    ])  # You can expand for other languages

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
    backend_url = "https://your-backend-service/analyze/"  # CHANGE to your actual backend endpoint!
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