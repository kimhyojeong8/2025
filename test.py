import streamlit as st
import pandas as pd
import datetime

# 앱 이름
st.set_page_config(page_title="효율적인 공부중..", layout="wide")

st.title("✏️ 효율적인 공부중..")
st.markdown("당신의 공부 성향과 목표를 입력하면, 오늘의 권장 학습과 캘린더를 추천해드립니다!")

# --------------------------
# 1. 학습 성향 질문
# --------------------------
st.header("🔎 학습 성향 진단")

q1 = st.radio("1) 만약 공부 도중 슈퍼파워가 생긴다면, 어떤 능력을 갖고 싶나요?",
              ["⏱ 시간을 멈추는 능력", "📚 책 내용을 바로 기억하는 능력", "🌙 밤새 집중할 수 있는 능력"])

q2 = st.radio("2) 보통 공부는 언제 가장 잘 되나요?",
              ["아침", "오후", "밤"])

q3 = st.radio("3) 공부할 때 선호하는 방식은 무엇인가요?",
              ["긴 시간 몰입하기", "짧게 나누어 자주 하기", "시각 자료(그림/도표) 활용하기"])

# --------------------------
# 2. 학습 목표 입력
# --------------------------
st.header("🎯 학습 목표 입력하기")

num_goals = st.number_input("학습 목표는 몇 개인가요?", min_value=2, max_value=10, value=2, step=1)

goals = []
goal_periods = []

for i in range(num_goals):
    goal = st.text_input(f"학습 목표 {i+1}를 입력하세요:")
    period = st.number_input(f"'{goal or f'목표 {i+1}'}'를 완료할 남은 기간 (일수)", min_value=1, value=1, step=1)
    if goal:
        goals.append(goal)
        goal_periods.append(period)

# --------------------------
# 3. 계획 생성
# --------------------------
if st.button("📌 학습 계획 추천받기"):

    if len(goals) < 2:
        st.warning("목표를 최소 2개 이상 입력해주세요!")
    else:
        today = datetime.date.today()
        plan = []

        # 각 목표마다 입력된 기간만큼 날짜에 배치
        current_date = today
        for goal, period in zip(goals, goal_periods):
            for i in range(period):
                plan.append({"날짜": current_date, "학습 목표": goal})
                current_date += datetime.timedelta(days=1)

        df = pd.DataFrame(plan)

        # --------------------------
        # 오늘의 권장 학습
        # --------------------------
        st.subheader(f"📅 오늘의 권장 학습 ({today})")
        today_tasks = df[df["날짜"] == today]["학습 목표"].tolist()
        if today_tasks:
            for idx, task in enumerate(today_tasks, 1):
                st.write(f"{idx}. {task}")
        else:
            st.write("오늘은 특별한 학습 목표가 없어요! 여유롭게 보내세요 🌿")

        # --------------------------
        # 전체 캘린더
        # --------------------------
        st.subheader("🗓 전체 학습 캘린더")
        st.dataframe(df, use_container_width=True)

