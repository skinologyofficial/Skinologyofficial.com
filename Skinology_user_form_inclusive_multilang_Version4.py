import streamlit as st
import requests

# Brand color palette (from logo)
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
    "中文": {
        "welcome": "欢迎来到 AI 美妆与生活方式平台",
        "gender": "您的性别身份",
        "interests": "选择您的兴趣领域",
        "budget": "美妆/时尚预算 (加元)",
        "lifestyle": "生活方式（例如，办公室职员，运动，旅游）",
        "mbti": "个性（如知道 MBTI 类型）",
        "face_upload": "上传人脸照片（jpg/png）",
        "body_upload": "上传全身照片（jpg/png）",
        "submit": "提交并获取个性化协议",
        "success": "成功！您的个性化结果已准备好 🎉",
        "fail": "未能创建结果，请检查上传的照片和信息。",
        "pdf_download": "下载您的个性化 PDF 报告请点击",
    },
    "Français": {
        "welcome": "Bienvenue sur la plateforme d’IA Beauté & Mode",
        "gender": "Votre identité de genre",
        "interests": "Sélectionnez vos domaines d’intérêt",
        "budget": "Budget Beauté/Mode (CAD)",
        "lifestyle": "Mode de vie (ex: employé de bureau, sportif, voyages)",
        "mbti": "Personnalité (MBTI si connu)",
        "face_upload": "Téléchargez une photo de votre visage (jpg/png)",
        "body_upload": "Téléchargez une photo en pied (jpg/png)",
        "submit": "Soumettre et obtenir votre protocole personnalisé",
        "success": "Succès ! Vos résultats personnalisés sont prêts 🎉",
        "fail": "Échec de la création des résultats. Veuillez vérifier les images téléchargées et vos informations.",
        "pdf_download": "Téléchargez votre rapport PDF personnalisé ici",
    },
    "Español": {
        "welcome": "Bienvenido a la plataforma de Belleza y Estilo de Vida IA",
        "gender": "Tu identidad de género",
        "interests": "Selecciona tus áreas de interés",
        "budget": "Presupuesto para belleza/moda (CAD)",
        "lifestyle": "Estilo de vida (ejemplo: oficina, deportes, viajes)",
        "mbti": "Personalidad (MBTI si lo sabes)",
        "face_upload": "Sube tu foto de rostro (jpg/png)",
        "body_upload": "Sube tu foto de cuerpo completo (jpg/png)",
        "submit": "Enviar y obtener tu protocolo personalizado",
        "success": "¡Éxito! Tus resultados personalizados están listos 🎉",
        "fail": "No se pudo crear el resultado. Por favor revisa las fotos y la información.",
        "pdf_download": "Descarga tu reporte PDF personalizado aquí",
    },
    "廣東話": {
        "welcome": "歡迎來到 AI 美容生活平台",
        "gender": "您的性別認同",
        "interests": "選擇您的興趣範疇",
        "budget": "美容/時尚預算 (CAD)",
        "lifestyle": "生活方式（如：辦公室職員、運動、旅遊）",
        "mbti": "個性（如知道 MBTI 類型）",
        "face_upload": "上載面部照片（jpg/png）",
        "body_upload": "上載全身照片（jpg/png）",
        "submit": "提交並取得個人化建議",
        "success": "成功！您的個人化結果已準備好 🎉",
        "fail": "未能建立結果，請檢查照片及資料。",
        "pdf_download": "下載您的專屬 PDF 報告",
    },
    "한국어": {
        "welcome": "AI 뷰티 & 라이프스타일 플랫폼에 오신 것을 환영합니다",
        "gender": "성별",
        "interests": "관심 분야를 선택하세요",
        "budget": "뷰티/패션 예산 (CAD)",
        "lifestyle": "라이프스타일 (예: 직장인, 운동, 여행)",
        "mbti": "성격 (MBTI 등)",
        "face_upload": "얼굴 사진 업로드 (jpg/png)",
        "body_upload": "전신 사진 업로드 (jpg/png)",
        "submit": "제출하여 맞춤 프로토콜 받기",
        "success": "성공! 맞춤 결과가 준비되었습니다 🎉",
        "fail": "결과 생성에 실패했습니다. 사진과 정보를 확인하세요.",
        "pdf_download": "맞춤 PDF 리포트 다운로드",
    },
    "日本語": {
        "welcome": "AI美容＆ライフスタイルプラットフォームへようこそ",
        "gender": "あなたの性別・認識",
        "interests": "ご興味のある分野を選択してください",
        "budget": "美容・ファッション予算 (CAD)",
        "lifestyle": "ライフスタイル（例：会社員、スポーツ、旅行）",
        "mbti": "性格（MBTI等）",
        "face_upload": "顔写真アップロード (jpg/png)",
        "body_upload": "全身写真アップロード (jpg/png)",
        "submit": "送信してあなた専用プロトコルを取得",
        "success": "成功！あなただけの結果が準備できました 🎉",
        "fail": "結果が作成できません。写真や情報をご確認ください。",
        "pdf_download": "パーソナルPDFレポートをダウンロード",
    },
    "हिन्दी": {
        "welcome": "AI ब्यूटी और लाइफस्टाइल प्लैटफॉर्म में आपका स्वागत है",
        "gender": "आपकी जेंडर पहचान",
        "interests": "अपने रुचि के क्षेत्र चुनें",
        "budget": "ब्यूटी/फैशन बजट (CAD)",
        "lifestyle": "लाइफस्टाइल (जैसे: ऑफिस वर्कर, स्पोर्ट्स, ट्रैवल)",
        "mbti": "व्यक्तित्व (MBTI यदि ज्ञात हो)",
        "face_upload": "चेहरे की फोटो अपलोड करें (jpg/png)",
        "body_upload": "फुल-बॉडी फोटो अपलोड करें (jpg/png)",
        "submit": "सबमिट करें और पर्सनलाइज्ड प्रोटोकॉल प्राप्त करें",
        "success": "सफलता! आपके पर्सनल परिणाम तैयार हैं 🎉",
        "fail": "रिज़ल्ट बनाने में विफल। कृपया फोटो व जानकारी जांचें।",
        "pdf_download": "पर्सनल PDF रिपोर्ट डाउनलोड करें",
    },
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
    "中文": ["护肤", "化妆品", "美发", "时尚与服饰", "营养与健康", "生活方式/个性", "其他"],
    "Français": ["Soin de la peau", "Maquillage", "Soins capillaires", "Mode & Vêtements", "Nutrition/Santé", "Lifestyle/Personnalité", "Autre"],
    "Español": ["Cuidado de la piel", "Maquillaje/Cosméticos", "Cuidado del cabello", "Moda y ropa", "Nutrición/Salud", "Estilo de vida/Personalidad", "Otro"],
    "廣東話": ["護膚", "化妝品", "護髮", "時裝與衣履", "營養健康", "生活方式/個性", "其他"],
    "한국어": ["스킨케어", "메이크업/화장품", "헤어케어", "패션/의류", "영양/건강", "라이프스타일/성격", "기타"],
    "日本語": ["スキンケア", "メイク/化粧品", "ヘアケア", "ファッション/服", "栄養/健康", "ライフスタイル/性格", "その他"],
    "हिन्दी": ["त्वचा की देखभाल", "मेकअप/कॉस्मेटिक्स", "हेयर केयर", "फैशन और कपड़े", "पोषण/स्वास्थ्य", "लाइफस्टाइल/व्यक्तित्व", "अन्य"]
}

st.set_page_config(page_title="AI Beauty & Lifestyle Platform", page_icon="assets/skinology_logo.png")

# ---- LOGO APPEARANCE ----
st.image("assets/skinology_logo.png", width=320)

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
    ])  # You can expand to other languages like above

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
    backend_url = "https://your-backend-service/analyze/"  # <<<< CHANGE TO YOUR LIVE BACKEND URL!
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