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

# ------------------ 공통 CSS + 애니메이션 ------------------
COMMON_CSS = """
<style>
body, .stApp { font-family: "Apple SD Gothic Neo", "Malgun Gothic", Arial, sans-serif; }
/* 버튼 스타일 */
.stButton>button {
    background: linear-gradient(180deg, #5cd26a, #3fb24f);
    color: white; border-radius: 10px; padding: 8px 14px; font-weight: 700;
}
/* 카드 스타일 */
.card { padding: 14px; border-radius: 12px; margin-bottom: 12px; }
/* 작은 뱃지 */
.badge { display:inline-block; background:#ffffffaa; padding:6px 10px; border-radius:999px; font-weight:700; margin-left:8px; }
/* 반짝이 */
.sparkle-wrap { pointer-events:none; position:fixed; top:0; left:0; right:0; bottom:0; overflow:hidden; z-index:9998; }
.sparkle { position:absolute; width:6px; height:6px; background: radial-gradient(circle, rgba(255,255,255,1) 0%, rgba(255,255,255,0.2) 60%); opacity:0.9; border-radius:50%; filter: drop-shadow(0 0 6px rgba(255,255,200,0.9)); animation: sparkleMove 2s linear infinite; }
@keyframes sparkleMove {0% { transform: translateY(10vh) scale(0.6); opacity:0; }30% { opacity:1; }100% { transform: translateY(-10vh) scale(1.2); opacity:0; } }
/* 눈 */
.snow-wrap { pointer-events:none; position:fixed; top:0; left:0; right:0; height:100vh; z-index:9998; }
.snowflake { position:absolute; top:-10%; color:white; font-size:18px; user-select:none; animation: fall 6s linear infinite; opacity:0.9; text-shadow:0 0 6px rgba(255,255,255,0.9);}
@keyframes fall {0% { transform:translateY(-10vh) translateX(0) rotate(0deg); opacity:1;} 100% { transform:translateY(110vh) translateX(30vw) rotate(360deg); opacity:0;} }
/* 비 */
.rain-wrap { pointer-events:none; position:fixed; top:0; left:0; right:0; bottom:0; overflow:hidden; z-index:9998;}
.rain-drop { position:absolute; top:-10%; width:2px; height:18px; background: linear-gradient(180deg, rgba(255,255,255,0.8), rgba(255,255,255,0.2)); opacity:0.8; transform: skewX(-15deg); animation: rainFall 0.8s linear infinite;}
@keyframes rainFall {0% { transform: translateY(-5vh) translateX(0);} 100% { transform: translateY(110vh) translateX(20vw); } }
</style>
"""
st.markdown(COMMON_CSS, unsafe_allow_html=True)

# ------------------ 효과 렌더링 ------------------
def render_effect_html(effect_name, color="#ffffff"):
    if effect_name == "sparkle":
        sparkles_html = "<div class='sparkle-wrap'>"
        positions = [(10,60,0.9),(20,30,1.6),(40,80,1.1),(60,20,1.9),(75,50,1.2),(85,70,1.5),(30,40,2),(50,60,1.3),(65,35,1.8)]
        for idx, (left, top, dur) in enumerate(positions):
            sparkles_html += f"<div class='sparkle' style='left:{left}%; top:{top}%; width:{4+idx%4}px; height:{4+idx%4}px; animation-duration:{dur}s; background: radial-gradient(circle, {color} 0%, rgba(255,255,255,0.15) 60%);'></div>"
        sparkles_html += "</div>"
        return sparkles_html
    if effect_name == "snow":
        snow_html = "<div class='snow-wrap'>"
        lefts=[5,15,25,35,45,55,65,75,85,92]; sizes=[12,16,14,18,10,20,12,15,11,17]; durs=[6,7,5.5,8,6.5,7.5,6,8.5,5.8,7.2]
        for i,(l,s,d) in enumerate(zip(lefts,sizes,durs)):
            snow_html += f"<div class='snowflake' style='left:{l}%; font-size:{s}px; animation-duration:{d}s; opacity:{0.7+i*0.02};'>❄️</div>"
        snow_html += "</div>"; return snow_html
    if effect_name == "rain":
        rain_html = "<div class='rain-wrap'>"
        lefts=[3,10,18,25,33,42,50,59,68,78,86,92]; durs=[0.8,0.9,0.7,0.85,0.95,0.8,0.7,0.85,0.9,0.8,0.75,0.88]
        for i,(l,d) in enumerate(zip(lefts,durs)):
            height = 14+(i%4)*4
            rain_html += f"<div class='rain-drop' style='left:{l}%; height:{height}px; animation-duration:{d}s; opacity:0.6;'></div>"
        rain_html += "</div>"; return rain_html
    return ""

# ------------------ 배경 색상 계산 ------------------
def get_background_color():
    if not st.session_state.themes_owned:
        return "linear-gradient(135deg, #eafaf0 0%, #d7f4dd 50%, #bff0c5 100%)"
    else:
        top_score = max([score for score, theme in themes.items() if theme["name"] in st.session_state.themes_owned])
        theme = themes[top_score]
        color_map = {
            "숲 테마 🌳": "#2ecc71",
            "바다 테마 🌊": "#3498db",
            "사막 테마 🏜️": "#e67e22",
            "겨울 테마 ❄️": "#8ecae6"
        }
        return color_map.get(theme["name"], "#ffffff")
bg_color = get_background_color()
st.markdown(f"<style>.stApp {{ background: {bg_color}; transition: background 0.8s ease; }}</style>", unsafe_allow_html=True)

# ------------------ 앱 타이틀 / 버튼 ------------------
st.markdown(f"<h1 style='text-align:center; color:#065f46;'>🌱 Green Activity for Me</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([1,1])
with col1:
    if st.button("내 활동"): st.session_state.page="activity"
with col2:
    if st.button("테마 목록"): st.session_state.page="themes"

# ------------------ 페이지 로직 ------------------
if st.session_state.page is None:
    st.info("상단 버튼으로 '내 활동' 또는 '테마 목록'으로 이동하세요.")

# ------------------ 내 활동 ------------------
if st.session_state.page=="activity":
    st.subheader("📅 내 활동")
    today=datetime.date.today()
    if st.session_state.last_attendance != today:
        if st.button("출석 체크 (+100점)"):
            st.session_state.points+=100; st.session_state.last_attendance=today; st.success(f"출석 완료! +100점 (총 {st.session_state.points})")
    else: st.info("오늘은 이미 출석했습니다 ✅")

    activity=st.selectbox("활동 종류",["분리수거","전기 절약","친환경 캠페인","기타"])
    if activity=="기타":
        etc=st.text_input("기타 활동")
        if st.button("기록 (+45점)"):
            if etc.strip(): st.session_state.points+=45; st.success(f"'{etc}' 활동으로 45점 획득! (총 {st.session_state.points})")
            else: st.warning("활동 내용을 입력하세요.")
    else:
        if st.button("기록"):
            points_map={"분리수거":50,"전기 절약":70,"친환경 캠페인":100}
            gained=points_map[activity]; st.session_state.points+=gained; st.success(f"{activity} 활동으로 {gained}점 획득! (총 {st.session_state.points})")

    newly=[]
    for score in sorted(themes.keys()):
        theme=themes[score]
        if st.session_state.points>=score and theme["name"] not in st.session_state.themes_owned:
            st.session_state.themes_owned[theme["name"]]=theme; newly.append(theme)
    if newly:
        last_new=newly[-1]; st.session_state.new_theme=last_new; st.success(f"🎉 NEW! {last_new['name']} 획득!")
        st.markdown(render_effect_html(last_new["effect"], color=last_new["color"]), unsafe_allow_html=True)

    if st.button("⬅️ 메인"): st.session_state.page=None

# ------------------ 테마 목록 ------------------
if st.session_state.page=="themes":
    st.subheader("📖 테마 목록")
    owned=list(st.session_state.themes_owned.keys())
    for score in sorted(themes.keys()):
        theme=themes[score]
        if theme["name"] in owned:
            st.markdown(f"<div style='padding:10px; margin:6px 0; background:{theme['color']}; border-radius:12px; font-weight:700;'>{theme['name']} — 보유 ✅</div>", unsafe_allow_html=True)
            st.markdown(render_effect_html(theme["effect"], color=theme["color"]), unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='padding:10px; margin:6px 0; background:#f0f0f0; border-radius:12px;'>{theme['name']} (미보유, 필요 점수 {score})</div>", unsafe_allow_html=True)
    if st.button("⬅️ 메인"): st.session_state.page=None
