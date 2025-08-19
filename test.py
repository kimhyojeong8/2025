import streamlit as st
import datetime
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="효율적인 공부중..", page_icon="✏️", layout="centered")

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
# 2단계: 학습 목표 및 각 목표 남은 기간 입력
# ----------------------------
st.markdown("## ✨ Step 2. 학습 목표와 목표별 남은 기간 입력")

goals_input = st.text_area(
    "📌 학습 목표를 입력하세요 (줄바꿈으로 구분)",
    placeholder="예) 수학 5단원 완벽 이해\n영어 단어 300개 암기\n한국사 연표 정리",
    height=100
)
goals = [g.strip() for g in goals_input.split("\n") if g.strip()]

goal_periods = []
for goal in goals:
    period = st.number_input(f"'{goal}'를 완료할 남은 기간 (일수)", min_value=1, value=1, step=1, key=goal)
    goal_periods.append(period)

# ----------------------------
# 3단계: 학습 계획 생성
# ----------------------------
if st.button("📖 나만의 학습 계획 세우기"):
    if not goals:
        st.warning("학습 목표를 입력해주세요!")
    else:
        today = datetime.date.today()
        plan = []

        # 각 목표별 기간만큼 캘린더에 배치
        for goal, period in zip(goals, goal_periods):
            for i in range(period):
                plan.append({"날짜": today + datetime.timedelta(days=i), "학습 목표": goal})

        df_plan = pd.DataFrame(plan)

        # ----------------------------
        # 오늘의 권장 학습
        # ----------------------------
        st.subheader(f"📅 오늘의 권장 학습 ({today})")
        today_tasks = df_plan[df_plan["날짜"] == today]["학습 목표"].tolist()
        if today_tasks:
            for idx, task in enumerate(today_tasks, 1):
                st.write(f"{idx}. {task}")
        else:
            st.write("오늘은 특별한 학습 목표가 없어요! 여유롭게 보내세요 🌿")

        # ----------------------------
        # 전체 캘린더
        # ----------------------------
        st.subheader("🗓 전체 학습 캘린더")
        st.dataframe(df_plan, use_container_width=True)
