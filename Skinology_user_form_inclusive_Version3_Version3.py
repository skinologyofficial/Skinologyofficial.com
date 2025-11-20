import streamlit as st
import requests

st.set_page_config(page_title="AI Beauty & Lifestyle Platform")

st.title("ยินดีต้อนรับสู่ AI Beauty & Lifestyle Platform ระดับโลก 🇨🇦")

gender = st.selectbox("อัตลักษณ์ทางเพศของคุณ", ["หญิง", "ชาย", "Non-binary/ไม่ระบุ", "อื่นๆ"])
interests = st.multiselect("เลือกหมวดคำแนะนำที่สนใจ", [
    "สกินแคร์",
    "แต่งหน้า/เครื่องสำอาง",
    "ดูแลเส้นผม",
    "แฟชั่นและการแต่งกาย",
    "โภชนาการ/สุขภาพ",
    "ไลฟ์สไตล์/บุคลิกภาพ",
    "อื่นๆ"
], default=["สกินแคร์", "ดูแลเส้นผม", "แฟชั่นและการแต่งกาย"])

budget = st.number_input("งบประมาณสำหรับสินค้า/แฟชั่น (CAD)", min_value=0, value=1000)
lifestyle = st.text_input("ไลฟ์สไตล์ (เช่น ทำงานออฟฟิศ, เล่นกีฬา, เที่ยวบ่อย)")
mbti = st.text_input("บุคลิกภาพ (MBTI ถ้ามี)")
face_image = st.file_uploader("อัปโหลดรูปใบหน้า (jpg/png)", type=["jpg", "png"])
body_image = st.file_uploader("อัปโหลดรูปเต็มตัว (jpg/png)", type=["jpg", "png"])

if st.button("ยืนยันและรับโปรโตคอลเฉพาะบุคคล"):
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
        "mbti": mbti
    }
    # ใส่ URL backend จริงที่นี่เมื่อต้องการ deploy cloud
    backend_url = "https://<your-fastapi-server>/analyze/"
    try:
        res = requests.post(backend_url, files=files, data=data)
        if res.status_code == 200:
            result_dict = res.json()
            st.success("สร้างสำเร็จ! ผลลัพธ์ของคุณพร้อมแล้ว 🎉")
            st.write(result_dict["result"])
            pdf_url = result_dict.get("pdf_url", "")
            if pdf_url:
                st.markdown(f"ดาวน์โหลด PDF รายงานเฉพาะตัว [คลิกที่นี่]({pdf_url})")
        else:
            st.error(f"ไม่สามารถสร้างผลลัพธ์ โปรดตรวจสอบรูปและข้อมูลที่ส่ง\n{res.text}")
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")