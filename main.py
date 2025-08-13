import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="MBTI 국내 여행 추천 🌿", page_icon="🏞️", layout="centered")

# 스타일 (잔잔하고 편안한 느낌)
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
        background: rgba(255,255,255,0.85);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 제목
st.title("🌿 MBTI 국내 여행 추천")
st.subheader("당신의 MBTI에 맞는 국내 여행지를 추천해드립니다.")

# MBTI 선택
mbti = st.selectbox("당신의 MBTI를 선택해주세요", [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
])

# 국내 여행지 데이터
travel_recommendations = {
    "ISTJ": [("경주", "역사와]()
