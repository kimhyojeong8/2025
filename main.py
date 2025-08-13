import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="MBTI 국내 여행 추천 🌿", page_icon="🏞️", layout="centered")

# 스타일 (그라데이션 배경 + 카드 디자인)
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        font-family: 'Pretendard', sans-serif;
    }
    h1, h2, h3 {
        text-align: center;
        color: #2c3e50;
    }
    .recommend-box {
        background: rgba(255,255,255,0.88);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
        text-align: center;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 제목
st.title("🌿 MBTI 국내 여행 추천")
st.subheader("당신의 MBTI에 딱 맞는 여행지를 추천해드립니다!")

# MBTI 선택
mbti = st.selectbox("당신의 MBTI를 선택해주세요", [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
])

# MBTI별 국내 여행지 데이터 + 이모지
travel_recommendations = {
    "ISTJ": [("🏯 경주", "역사와 전통이 살아있는 도시", "https://cdn.pixabay.com/photo/2017/05/28/10/43/korea-2351650_1280.jpg")],
    "ISFJ": [("🏘️ 전주", "한옥마을과 전통 음식의 고향", "https://cdn.pixabay.com/photo/2016/03/05/19/02/korean-house-1239043_1280.jpg")],
    "INFJ": [("🌊 강릉", "잔잔한 바다와 커피향 가득한 도시", "https://cdn.pixabay.com/photo/2019/07/10/12/01/korea-4327166_1280.jpg")],
    "INTJ": [("🏘️ 서울 북촌", "계획적이고 고즈넉한 한옥 골목", "https://cdn.pixabay.com/photo/2020/01/14/16/32/seoul-4764792_1280.jpg")],
    "ISTP": [("⛰️ 속초", "바다와 산을 모두 즐기는 액티비티 천국", "https://cdn.pixabay.com/photo/2017/08/06/12/11/sea-2594101_1280.jpg")],
    "ISFP": [("🎨 남해", "자연과 예술이 조화를 이루는 섬", "https://cdn.pixabay.com/photo/2016/03/05/19/02/korean-village-1239045_1280.jpg")],
    "INFP": [("🎋 담양", "대나무숲과 감성 가득한 소도시", "https://cdn.pixabay.com/photo/2017/03/07/07/32/bamboo-2120513_1280.jpg")],
    "INTP": [("🏞️ 춘천", "호수와 조용한 카페 거리", "https://cdn.pixabay.com/photo/2019/06/06/10/20/korea-4254246_1280.jpg")],
    "ESTP": [("🏖️ 부산 해운대", "활기찬 해변과 야경", "https://cdn.pixabay.com/photo/2016/05/05/02/37/korea-1377069_1280.jpg")],
    "ESFP": [("🏝️ 제주도", "자유롭고 아름다운 자연", "https://cdn.pixabay.com/photo/2017/04/03/15/39/jeju-2191649_1280.jpg")],
    "ENFP": [("🌅 여수", "낭만 가득한 바닷가 도시", "https://cdn.pixabay.com/photo/2016/03/09/09/29/korea-1246286_1280.jpg")],
    "ENTP": [("🏮 인천 차이나타운", "다채로운 문화와 먹거리", "https://cdn.pixabay.com/photo/2020/01/14/16/36/incheon-4764804_1280.jpg")],
    "ESTJ": [("🏯 수원 화성", "체계적인 역사 여행", "https://cdn.pixabay.com/photo/2020/02/13/09/25/korea-4843955_1280.jpg")],
    "ESFJ": [("⛩️ 안동", "전통과 공동체 문화의 중심지", "https://cdn.pixabay.com/photo/2016/03/05/19/02/korean-temple-1239046_1280.jpg")],
    "ENFJ": [("🎭 통영", "사람과 바다가 함께하는 예술의 도시", "https://cdn.pixabay.com/photo/2016/03/05/19/02/korean-bridge-1239047_1280.jpg")],
    "ENTJ": [("🌉 서울 한강", "도시와 자연의 완벽한 조화", "https://cdn.pixabay.com/photo/2017/06/02/17/09/seoul-2367730_1280.jpg")]
}

# 추천 버튼
if st.button("여행지 추천 받기 ✈️"):
    if mbti in travel_recommendations:
        place, desc, img = random.choice(travel_recommendations[mbti])
        st.markdown(
            f"<div class='recommend-box'><h2>{place}</h2><p>{desc}</p></div>",
            unsafe_allow_html=True
        )
        st.image(img, use_container_width=True)
    else:
        st.warning("추천 여행지가 없습니다.")
