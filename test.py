# app.py
import streamlit as st
import datetime

st.set_page_config(page_title="Green Activity for Me", layout="centered")

# ------------------ 테마 정의 ------------------
themes = {
    500: {"name": "숲 테마 🌳", "color": "#2ecc71", "effect": "sparkle"},
    1000: {"name": "바다 테마 🌊", "color": "#3498db", "effect": "rain"},
    1500: {"name": "사막 테마 🏜️", "color": "#e67e22", "effect": "sparkle"},
    2000: {"name": "겨울 테마 ❄️", "color": "#8ecae6", "effect": "snow"},
}

# ------------------ 동적 배경 적용 ------------------
bg_color = get_background_color()
st.markdown(f"""
    <style>
    .stApp {{
        background: {bg_color};
        transition: background 0.8s ease;
    }}
    </style>
""", unsafe_allow_html=True)


# ------------------ 세션 초기화 ------------------
if "points" not in st.session_state:
    st.session_state.points = 0
if "themes_owned" not in st.session_state:
    st.session_state.themes_owned = {}  # name -> theme dict
if "last_attendance" not in st.session_state:
    st.session_state.last_attendance = None
if "new_theme" not in st.session_state:
    st.session_state.new_theme = None
if "page" not in st.session_state:
    st.session_state.page = None

# ------------------ 공통 CSS (초록 테마 기본 + 애니메이션) ------------------
COMMON_CSS = """
<style>
/* 전체 폰트 / 카드 스타일 */
body, .css-18e3th9, .stApp {
    font-family: "Apple SD Gothic Neo", "Malgun Gothic", Arial, sans-serif;
}
/* 앱 기본 귀여운 초록 배경: (테마 획득 전 조건에 따라 적용) */
.app-bg-cute {
    background: linear-gradient(135deg, #eafaf0 0%, #d7f4dd 50%, #bff0c5 100%);
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}
/* 버튼 스타일 */
.stButton>button {
    background: linear-gradient(180deg, #5cd26a, #3fb24f);
    color: white;
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 700;
}
/* 메인 카드, 헤더 */
.card {
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 12px;
}
/* 작은 뱃지 */
.badge {
    display:inline-block;
    background:#ffffffaa;
    padding:6px 10px;
    border-radius:999px;
    font-weight:700;
    margin-left:8px;
}

/* ----------------- 반짝이 (sparkle) ----------------- */
.sparkle-wrap {
    pointer-events: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    overflow: hidden;
    z-index: 9998;
}
.sparkle {
    position: absolute;
    width: 6px; height: 6px;
    background: radial-gradient(circle, rgba(255,255,255,1) 0%, rgba(255,255,255,0.2) 60%);
    opacity: 0.9;
    border-radius: 50%;
    filter: drop-shadow(0 0 6px rgba(255,255,200,0.9));
    animation: sparkleMove 2s linear infinite;
}
@keyframes sparkleMove {
    0% { transform: translateY(10vh) scale(0.6); opacity:0; }
    30% { opacity:1; }
    100% { transform: translateY(-10vh) scale(1.2); opacity:0; }
}

/* ----------------- 눈 (snow) ----------------- */
.snow-wrap {
    pointer-events: none;
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 100vh;
    z-index: 9998;
}
.snowflake {
    position: absolute;
    top: -10%;
    color: white;
    font-size: 18px;
    user-select:none;
    animation: fall 6s linear infinite;
    opacity: 0.9;
    text-shadow: 0 0 6px rgba(255,255,255,0.9);
}
@keyframes fall {
    0% { transform: translateY(-10vh) translateX(0) rotate(0deg); opacity:1; }
    100% { transform: translateY(110vh) translateX(30vw) rotate(360deg); opacity:0; }
}

/* ----------------- 비 (rain) ----------------- */
.rain-wrap {
    pointer-events: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    overflow: hidden;
    z-index: 9998;
}
.rain-drop {
    position: absolute;
    top: -10%;
    width: 2px;
    height: 18px;
    background: linear-gradient(180deg, rgba(255,255,255,0.8), rgba(255,255,255,0.2));
    opacity: 0.8;
    transform: skewX(-15deg);
    animation: rainFall 0.8s linear infinite;
}
@keyframes rainFall {
    0% { transform: translateY(-5vh) translateX(0) }
    100% { transform: translateY(110vh) translateX(20vw) }
}

/* 작은 꾸밈 (귀여운 타이틀) */
.title-cute {
    font-size:28px;
    font-weight:800;
    display:flex;
    align-items:center;
    gap:12px;
}
.leaf {
    width:44px; height:44px;
    border-radius:12px;
    background: linear-gradient(#6ee7a5, #2ecc71);
    display:flex; align-items:center; justify-content:center;
    box-shadow: 0 6px 18px rgba(74, 222, 128, 0.18);
    font-weight:900;
    color:white;
}
</style>
"""

# ------------------ 효과 렌더링 헬퍼 ------------------
def render_effect_html(effect_name, color="#ffffff"):
    """effect_name in {'sparkle','snow','rain'}"""
    if effect_name == "sparkle":
        # generate multiple sparkle spans at random positions
        sparkles_html = "<div class='sparkle-wrap'>"
        # fixed positions for deterministic rendering (no JS RNG)
        positions = [
            (10, 60, 0.9), (20, 30, 1.6), (40, 80, 1.1),
            (60, 20, 1.9), (75, 50, 1.2), (85, 70, 1.5),
            (30, 40, 2.0), (50, 60, 1.3), (65, 35, 1.8)
        ]
        for idx, (left, top, dur) in enumerate(positions):
            sparkles_html += f"<div class='sparkle' style='left:{left}%; top:{top}%; width:{4+idx%4}px; height:{4+idx%4}px; animation-duration:{dur}s; background: radial-gradient(circle, {color} 0%, rgba(255,255,255,0.15) 60%);'></div>"
        sparkles_html += "</div>"
        return sparkles_html

    if effect_name == "snow":
        snow_html = "<div class='snow-wrap'>"
        # multiple snowflakes at different left positions and durations
        lefts = [5, 15, 25, 35, 45, 55, 65, 75, 85, 92]
        sizes = [12, 16, 14, 18, 10, 20, 12, 15, 11, 17]
        durs = [6,7,5.5,8,6.5,7.5,6,8.5,5.8,7.2]
        for i, (l, s, d) in enumerate(zip(lefts, sizes, durs)):
            snow_html += f"<div class='snowflake' style='left:{l}%; font-size:{s}px; animation-duration:{d}s; opacity:{0.7 + i*0.02};'>❄️</div>"
        snow_html += "</div>"
        return snow_html

    if effect_name == "rain":
        rain_html = "<div class='rain-wrap'>"
        lefts = [3, 10, 18, 25, 33, 42, 50, 59, 68, 78, 86, 92]
        durs = [0.8,0.9,0.7,0.85,0.95,0.8,0.7,0.85,0.9,0.8,0.75,0.88]
        for i, (l, d) in enumerate(zip(lefts, durs)):
            height = 14 + (i % 4) * 4
            rain_html += f"<div class='rain-drop' style='left:{l}%; height:{height}px; animation-duration:{d}s; opacity:0.6;'></div>"
        rain_html += "</div>"
        return rain_html

    return ""

# ------------------ 출력: 공통 CSS ------------------
st.markdown(COMMON_CSS, unsafe_allow_html=True)

# ------------------ 앱 타이틀 / 네비 ------------------
st.markdown("<div class='app-bg-cute card'>", unsafe_allow_html=True)
st.markdown(
    "<div class='title-cute'><div class='leaf'>GA</div>"
    "<div>Green Activity for Me <span class='badge'>친환경 × 리워드</span></div></div>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# 네비 버튼
col1, col2 = st.columns([1,1])
with col1:
    if st.button("내 활동"):
        st.session_state.page = "activity"
with col2:
    if st.button("테마 목록"):
        st.session_state.page = "themes"

# ------------------ 메인 로직: 페이지 분기 ------------------
# 기본: 메인 안내 (페이지 None)
if st.session_state.page is None:
    st.markdown("<br>")
    st.markdown("<div class='card app-bg-cute'>"
                "<h3>안내</h3>"
                "<ul>"
                "<li>출석과 친환경 활동으로 점수를 얻으세요.</li>"
                "<li>점수는 테마(숲/바다/사막/겨울)를 자동 획득하는 데 사용됩니다.</li>"
                "<li>획득 전 기본 앱 배경은 귀여운 초록 테마입니다.</li>"
                "</ul></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'><b>현재 점수:</b> <span style='font-size:18px; font-weight:800'>{st.session_state.points}점</span></div>", unsafe_allow_html=True)

# ------------------ 내 활동 페이지 ------------------
if st.session_state.page == "activity":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📅 내 활동")
    # current score
    st.markdown(f"### 🏆 현재 점수: {st.session_state.points}")
    # 출석 체크
    today = datetime.date.today()
    if st.session_state.last_attendance != today:
        if st.button("출석 체크 하기 (+100점)"):
            st.session_state.points += 100
            st.session_state.last_attendance = today
            st.success(f"출석 완료! +100점 (총점: {st.session_state.points})")
    else:
        st.info("오늘은 이미 출석했습니다 ✅")

    st.markdown("---")
    # 활동 기록
    st.markdown("#### ♻️ 활동 기록")
    activity = st.selectbox("활동 종류", ["분리수거", "전기 절약", "친환경 캠페인", "기타"])
    if activity == "기타":
        etc_input = st.text_input("기타 활동 내용을 입력하세요:")
        if st.button("기타 활동 기록하기 (+45점)"):
            if etc_input.strip():
                st.session_state.points += 45
                st.success(f"'{etc_input}' 활동으로 45점 획득! (총점: {st.session_state.points})")
            else:
                st.warning("활동 내용을 입력해 주세요.")
    else:
        if st.button("활동 기록하기"):
            activity_points = {"분리수거": 50, "전기 절약": 70, "친환경 캠페인": 100}
            gained = activity_points.get(activity, 0)
            st.session_state.points += gained
            st.success(f"{activity} 활동으로 {gained}점 획득! (총점: {st.session_state.points})")

    # 자동 테마 획득 (점수 도달 시)
    newly_awarded = []
    for score in sorted(themes.keys()):
        theme = themes[score]
        if st.session_state.points >= score and theme["name"] not in st.session_state.themes_owned:
            st.session_state.themes_owned[theme["name"]] = theme
            newly_awarded.append(theme)

    # 만약 새 테마가 생겼다면 알림과 애니메이션 (가장 최근 테마 기준)
    if newly_awarded:
        last_new = newly_awarded[-1]
        st.session_state.new_theme = last_new
        st.success(f"🎉 NEW! {last_new['name']} 획득!")
        # show big badge + effect
        st.markdown(
            f"<div style='padding:12px; margin:10px 0; border-radius:12px; background:linear-gradient(90deg,{last_new['color']}, #ffffff33);'>"
            f"<h3 style='margin:6px 0'>{last_new['name']} 획득!</h3>"
            f"<div style='font-weight:700'>효과: {last_new['effect']}</div></div>",
            unsafe_allow_html=True
        )

    # 새 테마에 대한 에니메이션을 페이지에 추가 (if new_theme)
    if st.session_state.new_theme:
        effect_html = render_effect_html(st.session_state.new_theme["effect"], color=st.session_state.new_theme["color"])
        st.markdown(effect_html, unsafe_allow_html=True)
        # 한 번 표시 후 None으로 (유저가 페이지 전환하면 다시 재발동 가능)
        st.session_state.new_theme = None

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("⬅️ 메인으로"):
        st.session_state.page = None

# ------------------ 테마 목록 페이지 ------------------
elif st.session_state.page == "themes":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📖 테마 목록")

    owned = list(st.session_state.themes_owned.keys())
    not_owned = [themes[s]["name"] for s in themes if themes[s]["name"] not in owned]

    st.markdown(f"✅ 보유 테마 수: {len(owned)} / {len(themes)}")
    st.markdown(f"❌ 미보유 테마 수: {len(not_owned)}")
    st.markdown("---")

    # 각 테마 카드 표시 — 보유하면 색상 + 작은 애니메이션 표시
    for score in sorted(themes.keys()):
        theme = themes[score]
        if theme["name"] in st.session_state.themes_owned:
            # 보유: 배경 색 적용 + 소형 효과 프래그먼트
            st.markdown(
                f"<div style='padding:12px; margin:8px 0; border-radius:12px; background: linear-gradient(90deg, {theme['color']}, #ffffff33);'>"
                f"<b>{theme['name']}</b> — 보유 ✅ <div style='font-size:13px; color:#222'>{theme['effect']}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
            # 소형 애니메이션 조각 (텍스트 기반)
            eff = render_effect_html(theme["effect"], color=theme["color"])
            # 작은 영역에만 출력하기 위해 래핑 (danger: it's full page but it's ok visually)
            st.markdown(eff, unsafe_allow_html=True)
        else:
            st.markdown(
                f"<div style='padding:12px; margin:8px 0; border-radius:12px; background:#f0f0f0;'>"
                f"{theme['name']} (미보유) — 필요 점수: <b>{score}</b></div>",
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("⬅️ 메인으로"):
        st.session_state.page = None

# ------------------ 기본 배경 유지 (테마 미보유 시 초록 배경 강조) ------------------
# 만약 아직 어떤 테마도 획득하지 않았다면 페이지 하단에 '초록 기본 배경' 안내 표시
if len(st.session_state.themes_owned) == 0:
    st.markdown(
        "<div style='position:fixed; left:16px; bottom:16px; padding:10px 14px; border-radius:12px; background:linear-gradient(90deg,#e6f9ea,#c8f1d0); box-shadow:0 8px 20px rgba(0,0,0,0.06)'>"
        "앱 기본 테마: <b style='color:#2ecc71;'>초록 귀여운 테마</b> — 테마를 획득하면 다양한 효과를 즐길 수 있어요!</div>",
        unsafe_allow_html=True
    )
