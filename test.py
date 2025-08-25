import streamlit as st
import datetime
import random

# --- 테마 데이터 (텍스트, 색상, 효과) ---
themes = {
    500: {"name": "숲 테마 🌳", "color": "#2ecc71", "effect": "✨ 반짝임"},
    1000: {"name": "바다 테마 🌊", "color": "#3498db", "effect": "🌊 파도 효과"},
    1500: {"name": "사막 테마 🏜️", "color": "#e67e22", "effect": "☀️ 모래 바람"},
    2000: {"name": "겨울 테마 ❄️", "color": "#ecf0f1", "effect": "❄️ 눈 내림"},
    2500: {"name": "비 오는 테마 🌧️", "color": "#95a5a6", "effect": "🌧️ 빗방울"},
}

# --- 초기 상태 ---
if "points" not in st.session_state:
    st.session_state.points = 0
if "themes" not in st.session_state:
    st.session_state.themes = {}
if "last_attendance" not in st.session_state:
    st.session_state.last_attendance = None
if "new_theme" not in st.session_state:
    st.session_state.new_theme = None
if "page" not in st.session_state:
    st.session_state.page = None

# --- 앱 이름 ---
st.title("🌱 Green Activity for Me")

# --- 네비게이션 버튼 ---
col1, col2 = st.columns(2)
with col1:
    if st.button("내 활동"):
        st.session_state.page = "activity"
with col2:
    if st.button("테마 목록"):
        st.session_state.page = "themes"

# -------------------- 내 활동 페이지 --------------------
if st.session_state.page == "activity":
    st.header("📅 출석 체크")
    today = datetime.date.today()
    if st.session_state.last_attendance != today:
        if st.button("출석 체크 하기 (+100점)"):
            st.session_state.points += 100
            st.session_state.last_attendance = today
            st.success(f"출석 완료! +100점 (총점: {st.session_state.points})")
    else:
        st.info("오늘은 이미 출석했습니다 ✅")

    st.header("♻️ 오늘의 활동 기록")
    activity = st.selectbox("활동 종류", ["분리수거", "전기 절약", "친환경 캠페인", "기타"])
    
    if activity == "기타":
        etc_input = st.text_input("기타 활동 내용을 입력하세요:")
        if st.button("기타 활동 기록하기 (+45점)"):
            if etc_input.strip():
                st.session_state.points += 45
                st.success(f"'{etc_input}' 활동으로 45점 획득! (총점: {st.session_state.points})")
            else:
                st.warning("활동 내용을 입력해주세요!")
    else:
        if st.button("활동 기록하기"):
            activity_points = {"분리수거": 50, "전기 절약": 70, "친환경 캠페인": 100}
            gained = activity_points.get(activity, 0)
            st.session_state.points += gained
            st.success(f"{activity} 활동으로 {gained}점 획득! (총점: {st.session_state.points})")

    # --- 테마 자동 획득 ---
    for score, theme in themes.items():
        if st.session_state.points >= score and theme["name"] not in st.session_state.themes:
            st.session_state.themes[theme["name"]] = theme
            st.session_state.new_theme = theme["name"]
            st.balloons()

    if st.session_state.new_theme:
        st.success(f"🎉 NEW! {st.session_state.new_theme}를 획득했습니다!")
        st.session_state.new_theme = None

# -------------------- 테마 목록 페이지 --------------------
elif st.session_state.page == "themes":
    st.header("📖 테마 목록")
    owned = list(st.session_state.themes.keys())
    not_owned = [theme["name"] for theme in themes.values() if theme["name"] not in owned]

    st.markdown(f"✅ 보유 테마 수: {len(owned)} / {len(themes)}")
    st.markdown(f"❌ 미보유 테마 수: {len(not_owned)}")

    # 테마 표시
    for score, theme in themes.items():
        if theme["name"] in st.session_state.themes:
            st.markdown(
                f"<div style='padding:10px; margin:10px 0; background-color:{theme['color']}; border-radius:10px;'>"
                f"<b>{theme['name']}</b> - {theme['effect']} ✅</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='padding:10px; margin:10px 0; background-color:#bdc3c7; border-radius:10px;'>"
                f"{theme['name']} (미보유, 필요 점수: {score})</div>",
                unsafe_allow_html=True
            )
