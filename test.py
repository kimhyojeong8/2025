import streamlit as st
st.write(st.__version__)
'''import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="효율적인 공부중..", page_icon="✏️", layout="centered")
st.title("✏️ 효율적인 공부중..")
st.subheader("성향 분석 또는 목표 분석을 선택해 보세요!")

# ----------------------------
# 질문 풀 정의
# ----------------------------
questions_pool = [
    {
        "id": "animal_style",
        "question": "공부할 때 당신은 어떤 동물이랑 닮았나요?",
        "options": ["🐢 느리지만 꾸준히 가는 거북이", "🦅 몰입해서 끝내는 독수리", "🐿️ 여기저기 관심 많은 다람쥐", "🐕 친구랑 같이 해야 힘나는 강아지"]
    },
    {
        "id": "exam_day",
        "question": "시험 전날이라면 어떻게 할 것 같나요?",
        "options": ["📚 끝까지 벼락치기", "🛌 그냥 잔다", "📝 중요한 것만 정리", "☕ 친구랑 밤새 달린다"]
    },
    {
        "id": "max_time",
        "question": "하루에 집중할 수 있는 최대 학습 시간은 몇 시간인가요?",
        "options": [str(i) for i in range(1, 13)]
    },
    {
        "id": "study_style",
        "question": "공부할 때 선호하는 방식은 무엇인가요?",
        "options": ["요약/정리", "문제풀이", "암기", "토론/설명"]
    },
    {
        "id": "priority",
        "question": "목표 달성 시 가장 중요한 요소는 무엇인가요?",
        "options": ["⏳ 시간 관리", "🎯 성취감", "🌱 꾸준함", "🤝 동기부여"]
    }
]

# ----------------------------
# 상태 초기화
# ----------------------------
if "mode" not in st.session_state:
    st.session_state.mode = None
if "remaining_questions" not in st.session_state:
    st.session_state.remaining_questions = questions_pool.copy()
    random.shuffle(st.session_state.remaining_questions)
    st.session_state.answers = {}
    st.session_state.goals = []

# ----------------------------
# 모드 선택
# ----------------------------
if st.session_state.mode is None:
    st.markdown("## 🚀 시작하기")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("1️⃣ 학습 성향 분석"):
            st.session_state.mode = "questions"
            st.experimental_rerun()
    with col2:
        if st.button("2️⃣ 학습 목표 분석"):
            st.session_state.mode = "goals"
            st.experimental_rerun()

# ----------------------------
# 학습 성향 분석 모드
# ----------------------------
elif st.session_state.mode == "questions":
    if st.session_state.remaining_questions:
        q = st.session_state.remaining_questions[0]

        st.markdown("## ✨ 학습 성향 진단")
        st.write(q["question"])
        answer = st.radio("답변을 선택하세요:", q["options"], key=q["id"])

        if st.button("다음 질문으로"):
            st.session_state.answers[q["id"]] = answer
            st.session_state.remaining_questions.pop(0)
            st.experimental_rerun()

    else:
        st.success("✅ 모든 학습 성향 질문이 완료되었습니다!")
        st.write("### 📊 나의 학습 성향 분석 결과")
        for q_id, ans in st.session_state.answers.items():
            st.write(f"- {q_id}: {ans}")

        if st.button("처음으로 돌아가기"):
            st.session_state.mode = None
            st.session_state.remaining_questions = questions_pool.copy()
            random.shuffle(st.session_state.remaining_questions)
            st.session_state.answers = {}
            st.experimental_rerun()

# ----------------------------
# 학습 목표 분석 모드
# ----------------------------
elif st.session_state.mode == "goals":
    st.markdown("## 🎯 학습 목표 입력")
    st.write("학습 목표, 기한, 중요도를 입력해주세요.")

    with st.form("goal_form", clear_on_submit=True):
        goal = st.text_input("학습 목표")
        deadline = st.date_input("목표 기한", min_value=datetime.today())
        importance = st.selectbox("목표 중요도", ["낮음", "보통", "높음", "매우 높음"])
        submitted = st.form_submit_button("추가하기")

        if submitted and goal:
            st.session_state.goals.append({
                "목표": goal,
                "기한": deadline,
                "중요도": importance
            })
            st.success(f"목표 '{goal}'이(가) 추가되었습니다!")

    if st.session_state.goals:
        df = pd.DataFrame(st.session_state.goals)
        st.dataframe(df, use_container_width=True)

        if st.button("학습 계획 추천받기"):
            importance_map = {"낮음": 1, "보통": 2, "높음": 3, "매우 높음": 4}
            df["중요도점수"] = df["중요도"].map(importance_map)
            df["남은일수"] = (df["기한"] - datetime.today().date()).dt.days
            df = df.sort_values(by=["중요도점수", "남은일수"], ascending=[False, True])

            st.markdown("## 📌 추천 학습 순서")
            for i, row in df.iterrows():
                st.write(f"**{i+1}. {row['목표']}**  (기한: {row['기한']}, 중요도: {row['중요도']})")

            st.markdown("## 🗓️ 오늘의 권장 학습")
            if len(df) == 1:
                st.info(f"오늘은 **{df.iloc[0]['목표']}** 에 집중하세요! 🎯")
            else:
                st.info(f"오늘은 우선 **{df.iloc[0]['목표']}** 부터 시작하는 걸 추천합니다 ✅")

    if st.button("처음으로 돌아가기"):
        st.session_state.mode = None
        st.session_state.goals = []
        st.experimental_rerun()
'''
