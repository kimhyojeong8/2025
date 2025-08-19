import streamlit as st
import math
import datetime
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="효율적인 공부중..", page_icon="✏️", layout="centered")

# 제목
st.title("✏️ 효율적인 공부중..")
st.subheader("나의 성향과 목표를 기반으로 효율적인 학습 플랜을 세워드려요!")

# ----------------------------
# 1단계: 학습 성향 진단
# ----------------------------
st.markdown("## ✨ Step 1. 학습 성향 진단")

fun_choice = st.radio(
    "🍫 초콜릿이 좋으세요, ☕ 커피가 좋으세요?",
    ["🍫 초콜릿", "☕ 커피", "📚 둘 다!"]
)

if fun_choice == "🍫 초콜릿":
    style = "🖼️ 시각형 (도표, 이미지 중심)"
elif fun_choice == "☕ 커피":
    style = "🎧 청각형 (강의, 설명 중심)"
else:
    style = "✍️ 실천형 (문제풀이, 실습 위주)"

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

goals_input = st.text_area(
    "📌 학습 목표를 입력하세요 (여러 개 입력 시 줄바꿈으로 구분)",
    placeholder="예) 수학 5단원 완벽 이해\n영어 단어 300개 암기\n한국사 연표 정리",
    height=100
)
goals = [g.strip() for g in goals_input.split("\n") if g.strip()]

days_left = st.number_input("⏳ 남은 일수 (며칠 안에 완료해야 하나요?)", min_value=1, value=7)
hours_per_day = st.slider("🕐 하루에 학습 가능한 시간 (시간)", min_value=1, max_value=12, value=4)

# ----------------------------
# 3단계: 학습 계획 생성
# ----------------------------
if st.button("📖 나만의 학습 계획 세우기"):
    total_hours = days_left * hours_per_day
    study_blocks = int(total_hours / 1.5)   # 1.5시간 단위 블록
    daily_blocks = math.ceil(study_blocks / days_left)

    # 🔹 목표 분배 (균등 배분)
    plan = []
    today = datetime.date.today()
    for i in range(days_left):
        date = today + datetime.timedelta(days=i)
        # 목표 순환 배정
        assigned_goal = goals[i % len(goals)] if goals else "목표 없음"
        plan.append({"날짜": date, "추천 목표": assigned_goal, "블록 수": daily_blocks})

    df_plan = pd.DataFrame(plan)

    # ----------------------------
    # 결과 출력
    # ----------------------------
    st.markdown("## ✅ 맞춤 학습 플랜")

    st.write(f"총 학습 가능 시간: **{total_hours}시간**")
    st.write(f"하루 권장 학습 블록: **{daily_blocks} 블록** (약 {daily_blocks*1.5:.1f}시간)")

    st.markdown("### 📅 학습 캘린더")
    st.dataframe(df_plan, use_container_width=True)

    # ----------------------------
    # 우선순위 추천
    # ----------------------------
    st.markdown("### 📌 추천 학습 순서")
    st.info(
        "1️⃣ 암기 과목 (예: 영어 단어, 한국사) → \n"
        "2️⃣ 이해 과목 (예: 수학, 과학 개념) → \n"
        "3️⃣ 종합 정리/문제풀이 (예: 기출문제, 모의고사)"
    )

    st.success("✨ 목표가 자동으로 캘린더에 분배되고, 우선순위 제안이 완료됐어요!")
