import random

def analyze_images(face_path, body_path, gender, interests, budget, lifestyle, mbti):
    core_results = {
        "animal_type": "Fox 🦊",
        "skin_type": "Oily",
        "hair_type": random.choice(["Straight", "Wavy", "Curly", "Coily"]),
        "personal_color": random.choice(["Winter Cool", "Summer Soft", "Spring Bright", "Autumn Warm", "Neutral Classic"]),
        "body_type": random.choice(["Hourglass", "Pear", "Rectangle", "Apple", "Inverted Triangle"]),
        "lifestyle": lifestyle,
        "mbti": mbti,
        "budget": budget,
        "gender": gender
    }
    recommendations = {}
    if "สกินแคร์" in interests:
        recommendations["skincare"] = [
            {"name":"Cerave Cleanser","store":"Sephora","price":350,"url":"https://sephora.com"},
            {"name":"Vitamin Serum","store":"Eve and Boy","price":399,"url":"https://eveandboy.com"}
        ]
    if "แต่งหน้า/เครื่องสำอาง" in interests:
        recommendations["makeup"] = [
            {"name":"Maybelline Fit Me","store":"Eve and Boy","price":249,"url":"https://eveandboy.com"},
        ]
    if "ดูแลเส้นผม" in interests:
        recommendations["haircare"] = [
            {"name":"Olaplex No.3","store":"Sephora","price":1200,"url":"https://sephora.com"},
        ]
    if "แฟชั่นและการแต่งกาย" in interests:
        recommendations["fashion"] = [
            {"style":"Minimalist sharp","brands":["Uniqlo","Pomelo"],"color_suggestion":"Grey/Navy/Black"}
        ]
    core_results["chosen_categories"] = list(recommendations.keys())
    core_results["recommendations"] = recommendations
    core_results["premium_offer"] = True
    return core_results