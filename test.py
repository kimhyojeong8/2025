
import streamlit as st
import math
import datetime

# 페이지 기본 설정
st.set_page_config(page_title="📚 맞춤 학습 플래너", page_icon="📝", layout="centered")

# 스타일
st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #d4fc79 0%, #96e6a1 100%);
        font-family: 'Pretendard', sans-serif;
    }
    h1, h2, h3 {
        text-align: center;
        color: #2c3e50;
    }
    .plan-box {
        background: rgba(255,255,255,0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 제목
st.title("📝 맞춤 학습 계획 추천")
st.subheader("나의 학습 성향과 목표를 기반으로 효율적인 학습 계획을 세워드려요!")

# ----------------------------
# 1단계: 학습 성향 진단
# ----------------------------
st.markdown("## ✨ Step 1. 학습 성향 진단")

style = st.radio(
    "📌 선호하는 학습 스타일은?",
    ["🖼️ 시각형 (도표, 이미지 중심)", "🎧 청각형 (강의, 설명 중심)", "✍️ 실천형 (문제풀이, 실습 위주)"]
)

focus_time = st.radio(
    "🕐 집중이 잘 되는 시간대는?",
    ["🌅 아침", "🌞 오후", "🌙 밤"]
)

study_mode = st.radio(
    "📖 선호하는 학습 방식은?",
    ["⏱️ 짧게 자주 반복", "💡 오래 몰입해서 집중"]
)

st.markdown("---")

# ----------------------------
# 2단계: 학습 목표 및 시간
# ----------------------------
st.markdown("## ✨ Step 2. 학습 목표와 시간 입력")

goal = st.text_area("📌 학습 목표를 입력하세요 (예: 수학 5단원 완벽 이해, 영어 단어 300개 암기)", height=80)
days_left = st.number_input("⏳ 남은 일수 (며칠 안에 완료해야 하나요?)", min_value=1, value=7)
hours_per_day = st.slider("🕐 하루에 학습 가능한 시간 (시간)", min_value=1, max_value=12, value=4)

# ----------------------------
# 3단계: 학습 계획 생성
# ----------------------------
if st.button("📖 나만의 학습 계획 세우기"):
    total_hours = days_left * hours_per_day
    study_blocks = int(total_hours / 1.5)   # 1.5시간 단위 블록
    daily_blocks = math.ceil(study_blocks / days_left)

    # 성향별 맞춤 팁
    tips = {
        "🖼️ 시각형 (도표, 이미지 중심)": "👉 플래시카드, 마인드맵, 컬러노트로 정리하면 효과적이에요.",
        "🎧 청각형 (강의, 설명 중심)": "👉 강의 듣기, 설명 녹음 후 반복 청취를 추천해요.",
        "✍️ 실천형 (문제풀이, 실습 위주)": "👉 문제풀이와 실전 연습을 많이 하세요.",
    }
    time_tips = {
        "🌅 아침": "🌅 오전에 중요한 과목을 배치하세요.",
        "🌞 오후": "🌞 오후에 복습과 암기를 집중하세요.",
        "🌙 밤": "🌙 밤에는 정리와 암기 과목을 하면 좋아요.",
    }
    mode_tips = {
        "⏱️ 짧게 자주 반복": "🔁 포모도로 기법(25분 집중 + 5분 휴식)을 활용해보세요.",
        "💡 오래 몰입해서 집중": "⏳ 1.5~2시간 몰입 후 15분 정도 휴식이 좋아요.",
    }

    # 결과 출력
    st.markdown(f"""
        <div class="plan-box">
        <h2>✅ 맞춤 학습 플랜</h2>
        <p><b>학습 목표:</b> {goal}</p>
        <p><b>총 학습 가능 시간:</b> {total_hours}시간</p>
        <p><b>하루 권장 학습 블록:</b> {daily_blocks} 블록</p>
        <hr>
        <p><b>학습 스타일:</b> {style} <br> {tips[style]}</p>
        <p><b>집중 시간대:</b> {focus_time} <br> {time_tips[focus_time]}</p>
        <p><b>학습 방식:</b> {study_mode} <br> {mode_tips[study_mode]}</p>
        </div>
    """, unsafe_allow_html=True)

    # 세부 계획
    st.markdown("### 📅 일별 학습 계획")
    today = datetime.date.today()
    for i in range(days_left):
        date = today + datetime.timedelta(days=i)
        st.write(f"**{date}**: {daily_blocks} 블록 ({daily_blocks*1.5:.1f}시간 학습)")

    st.success("✨ 성향에 맞는 계획을 잘 지키면 목표 달성에 한 발 가까워져요! 🚀")
