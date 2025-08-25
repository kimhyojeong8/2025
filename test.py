# app.py
import streamlit as st
import datetime
from streamlit.components.v1 import html

st.set_page_config(page_title="Green Activity for Me", layout="centered")

# ---------------------------
# 테마 설정: 점수 -> 메타 정보
# ---------------------------
THEMES = {
    500:  {"name": "숲 테마 🌳", "color": "#2ecc71", "effect": "sparkle"},
    1000: {"name": "바다 테마 🌊", "color": "#3498db", "effect": "wave"},
    1500: {"name": "사막 테마 🏜️", "color": "#e67e22", "effect": "sparkle"},
    2000: {"name": "겨울 테마 ❄️", "color": "#7fb3d5", "effect": "snow"},
    2500: {"name": "비 오는 테마 🌧️", "color": "#95a5a6", "effect": "rain"},
}

# ---------------------------
# 초기 session_state
# ---------------------------
if "points" not in st.session_state:
    st.session_state.points = 0
if "owned_themes" not in st.session_state:
    st.session_state.owned_themes = {}  # name -> meta (color, effect)
if "last_attendance" not in st.session_state:
    st.session_state.last_attendance = None
if "new_theme_unlocked" not in st.session_state:
    st.session_state.new_theme_unlocked = None
if "page" not in st.session_state:
    st.session_state.page = None
if "active_theme" not in st.session_state:
    st.session_state.active_theme = None  # name of applied theme

# ---------------------------
# 공통 CSS + 애니메이션 정의 (사용자 스타일)
# ---------------------------
BASE_STYLES = """
<style>
/* 기본 귀여운 초록 배경 & 카드 스타일 */
html, body, [class*="css"]  {
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
.app-container {
    padding: 18px;
}
.header {
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}
.green-bg {
    background: linear-gradient(180deg,#e9f8ec, #daf6dd);
    color: #074d17;
}
.card {
    background: white;
    border-radius: 12px;
    padding: 12px;
    margin: 8px 0;
    box-shadow: 0 6px 14px rgba(7,77,23,0.06);
}
.big-btn > button {
    background-color: #39b54a !important;
    color: white !important;
    font-weight: 700;
    border-radius: 10px;
    padding: 8px 14px;
}

/* 반짝이 텍스트 애니메이션 */
.sparkle-text {
    display:inline-block;
    animation: sparkle 1.6s infinite alternate;
    text-shadow: 0 0 6px rgba(255,255,255,0.9);
}
@keyframes sparkle {
    from { text-shadow: 0 0 6px rgba(255,255,255,0.85), 0 0 10px rgba(255,230,120,0.6); transform: translateY(0px); }
    to   { text-shadow: 0 0 12px rgba(255,255,255,1), 0 0 26px rgba(255,230,120,0.9); transform: translateY(-4px); }
}

/* 눈 애니메이션 (여러 개의 눈송이) */
.snow-area { position: relative; overflow: hidden; height: 140px; }
.snowflake {
    position: absolute;
    top: -10px;
    color: #fff;
    font-size: 18px;
    opacity: 0.95;
    animation: fall 5s linear infinite;
}
@keyframes fall {
    0% { transform: translateY(-10px) translateX(0px); opacity: 1; }
    100% { transform: translateY(140px) translateX(60px); opacity: 0.0; }
}

/* 비 애니메이션 */
.rain-area { position: relative; overflow: hidden; height: 140px; }
.drop {
    position: absolute;
    top: -10px;
    width: 2px;
    height: 14px;
    background: rgba(255,255,255,0.8);
    opacity: 0.9;
    border-radius: 1px;
    animation: drop 0.9s linear infinite;
}
@keyframes drop {
    0% { transform: translateY(-10px); opacity: 0.9; }
    100% { transform: translateY(160px); opacity: 0; }
}

/* 파도 효과 (부드러운 좌우 움직임 배경) */
.wave-area {
    height: 140px;
    position: relative;
    overflow: hidden;
}
.ocean {
    position: absolute;
    bottom: -10px;
    left: -10%;
    width: 120%;
    height: 120px;
    background: radial-gradient(circle at 50% 10%, rgba(255,255,255,0.08), rgba(0,0,0,0));
    transform: translateX(0);
    animation: sway 6s ease-in-out infinite;
    opacity: 0.9;
}
@keyframes sway {
    0% { transform: translateX(-4%); }
    50% { transform: translateX(4%); }
    100% { transform: translateX(-4%); }
}

/* NEW 배너 */
.new-banner {
    padding: 10px;
    border-radius: 10px;
    background: linear-gradient(90deg, rgba(255,235,179,1), rgba(255,205,100,1));
    font-weight: 700;
    display:inline-block;
    box-shadow: 0 6px 14px rgba(0,0,0,0.08);
}

/* small utility */
.center { text-align:center; }
.small { font-size:0.9rem; color:#555; }
</style>
"""

# ---------------------------
# 애니메이션 렌더 함수 (HTML 문자열 생성)
# ---------------------------
def render_effect_html(effect, color):
    """
    effect: 'sparkle', 'snow', 'rain', 'wave'
    color: hex string for accent
    """
    if effect == "sparkle":
        # 중앙 텍스트에 반짝이 CSS 적용
        html_code = f"""
        <div class="card" style="background:{color}; color: #fff; border-radius:12px;">
            <div class="center" style="padding:24px;">
                <div class="sparkle-text" style="font-size:22px;">✨ 테마 적용중 ✨</div>
                <div style="margin-top:8px; font-weight:700;">{color} 컬러 테마</div>
            </div>
        </div>
        """
    elif effect == "snow":
        # 여러 눈송이 span을 배치
        snow_drops = ""
        # create multiple flakes with varying left and animation-duration
        for i in range(12):
            left = (i * 8) % 100
            dur = 4 + (i % 4) * 0.8
            size = 10 + (i % 4) * 3
            snow_drops += f"<div class='snowflake' style='left:{left}%; animation-duration:{dur}s; font-size:{size}px;'>&#10052;</div>"
        html_code = f"""
        <div class="card" style="background:{color}; color: #fff; border-radius:12px;">
            <div class="snow-area" style="padding:12px;">
                {snow_drops}
                <div style="position:absolute; left:12px; top:8px; font-weight:700;">❄️ 눈 테마가 적용되었습니다</div>
            </div>
        </div>
        """
    elif effect == "rain":
        drops = ""
        for i in range(22):
            left = (i * 4.5) % 100
            delay = (i % 5) * 0.12
            height = 10 + (i % 3) * 6
            drops += f"<div class='drop' style='left:{left}%; animation-duration:{0.7 + (i%3)*0.2}s; top:-10px; height:{height}px; animation-delay:{delay}s;'></div>"
        html_code = f"""
        <div class="card" style="background:{color}; color: #fff; border-radius:12px;">
            <div class="rain-area" style="padding:8px;">
                {drops}
                <div style="position:absolute; left:12px; top:8px; font-weight:700;">🌧️ 비가 내리고 있어요</div>
            </div>
        </div>
        """
    elif effect == "wave":
        html_code = f"""
        <div class="card" style="background:{color}; color:#fff; border-radius:12px;">
            <div class="wave-area" style="padding:8px;">
                <div class="ocean"></div>
                <div style="position:absolute; left:12px; top:12px; font-weight:700;">🌊 바다의 파도 소리</div>
            </div>
        </div>
        """
    else:
        html_code = f"<div class='card'>테마 미리보기</div>"
    return html_code

# ---------------------------
# 활용: 상단 프리뷰 영역 렌더
# ---------------------------
def render_top_preview():
    """
    전체 상단 영역(헤더) — 현재 적용된 테마(active_theme)가 있으면 그 색상/효과로 표시,
    없으면 기본 초록색 귀여운 영역을 보여줌.
    """
    st.markdown(BASE_STYLES, unsafe_allow_html=True)

    # 헤더 컨테이너
    if st.session_state.active_theme:
        meta = st.session_state.owned_themes.get(st.session_state.active_theme)
        if meta:
            color = meta["color"]
            effect = meta["effect"]
            # render effect block using component html
            preview_html = render_effect_html(effect, color)
            html(preview_html, height=160)
    else:
        # 기본 초록 귀여운 헤더
        base_html = f"""
        <div class="header green-bg">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h2 style="margin:0 0 4px 0">🌱 Green Activity for Me</h2>
                    <div class="small">친환경 활동으로 점수를 모아 테마를 잠금해제해보세요!</div>
                </div>
                <div style="text-align:right; min-width:150px;">
                    <div style="font-weight:800; font-size:18px;">🏆 현재 점수</div>
                    <div style="font-size:20px; color:#0b7a3a;">{st.session_state.points} 점</div>
                </div>
            </div>
        </div>
        """
        html(base_html, height=140)

# ---------------------------
# 메뉴: 메인 (내 활동 / 테마 목록)
# ---------------------------
st.markdown('<div class="app-container">', unsafe_allow_html=True)
render_top_preview()

cols = st.columns([1,1,1])
with cols[0]:
    if st.button("내 활동", key="menu_activity", help="출석/활동 기록 페이지로 이동"):
        st.session_state.page = "activity"
with cols[1]:
    if st.button("테마 목록", key="menu_themes", help="보유/미보유 테마 확인"):
        st.session_state.page = "themes"
with cols[2]:
    if st.button("테마 적용 해제", key="menu_clear", help="기본 초록 테마로 되돌리기"):
        st.session_state.active_theme = None

st.write("")  # spacing

# ---------------------------
# 페이지: 내 활동
# ---------------------------
if st.session_state.page == "activity":
    st.subheader("♻️ 내 활동")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"**현재 점수:** {st.session_state.points} 점")
    st.markdown('</div>', unsafe_allow_html=True)

    # 출석
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📅 출석 체크")
    today = datetime.date.today()
    if st.session_state.last_attendance != today:
        if st.button("출석 체크 하기 (+100점)"):
            st.session_state.points += 100
            st.session_state.last_attendance = today
            st.success(f"출석 완료! +100점 획득 (총점: {st.session_state.points} 점)")
    else:
        st.info("오늘은 이미 출석했습니다 ✅")
    st.markdown('</div>', unsafe_allow_html=True)

    # 활동 기록
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📝 활동 기록")
    activity = st.selectbox("활동 종류", ["분리수거", "전기 절약", "친환경 캠페인", "기타"], key="act_select")
    if activity == "기타":
        other_text = st.text_input("기타 활동 내용을 입력하세요", key="other_input")
        if st.button("기타 활동 기록하기 (+45점)"):
            if other_text.strip():
                st.session_state.points += 45
                st.success(f"'{other_text}' 활동으로 +45점 획득 (총점: {st.session_state.points} 점)")
            else:
                st.warning("활동 내용을 입력해주세요.")
    else:
        if st.button("활동 기록하기"):
            points_map = {"분리수거":50,"전기 절약":70,"친환경 캠페인":100}
            g = points_map.get(activity, 0)
            st.session_state.points += g
            st.success(f"{activity} 활동으로 +{g}점 획득 (총점: {st.session_state.points} 점)")
    st.markdown('</div>', unsafe_allow_html=True)

    # 테마 자동 획득: 점수 돌면서 체크
    unlocked_any = False
    for threshold, meta in THEMES.items():
        if st.session_state.points >= threshold and meta["name"] not in st.session_state.owned_themes:
            # unlock
            st.session_state.owned_themes[meta["name"]] = {"color":meta["color"], "effect":meta["effect"], "threshold":threshold}
            st.session_state.new_theme_unlocked = meta["name"]
            unlocked_any = True

    if st.session_state.new_theme_unlocked:
        # NEW! 배너와 애니메이션 표시
        new_name = st.session_state.new_theme_unlocked
        st.markdown(f"<div class='new-banner'>🎉 NEW! {new_name} 잠금 해제!</div>", unsafe_allow_html=True)
        # short preview of the new theme effect
        meta = st.session_state.owned_themes[new_name]
        st.markdown(render_effect_html(meta["effect"], meta["color"]), unsafe_allow_html=True)
        st.session_state.new_theme_unlocked = None

    # 뒤로가기
    if st.button("⬅️ 메인으로 돌아가기"):
        st.session_state.page = None

# ---------------------------
# 페이지: 테마 목록
# ---------------------------
elif st.session_state.page == "themes":
    st.subheader("📖 테마 목록")
    owned = list(st.session_state.owned_themes.keys())
    not_owned = [v["name"] for v in THEMES.values() if v["name"] not in owned]
    st.markdown(f"**보유 테마:** {len(owned)} / {len(THEMES)}　　**미보유 테마 수:** {len(not_owned)}")

    # 리스트 형태로 각 테마 표시. 보유시 적용/해제 버튼 제공, 미보유시 필요 점수 안내
    for threshold, meta in THEMES.items():
        name = meta["name"]
        color = meta["color"]
        effect = meta["effect"]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        cols = st.columns([3,1,1])
        with cols[0]:
            if name in st.session_state.owned_themes:
                st.markdown(f"<div style='font-weight:800; color:{color};'>{name}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='small'>효과: {effect} · 획득 기준: {threshold}점</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='font-weight:800; color:gray'>{name} (미보유)</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='small'>필요 점수: {threshold} 점</div>", unsafe_allow_html=True)
        with cols[1]:
            if name in st.session_state.owned_themes:
                if st.button(f"적용", key=f"apply_{name}"):
                    st.session_state.active_theme = name
            else:
                st.write("")  # spacing
        with cols[2]:
            if name in st.session_state.owned_themes:
                if st.button("해제", key=f"clear_{name}"):
                    # apply none (if the theme being cleared is currently active, unset)
                    if st.session_state.active_theme == name:
                        st.session_state.active_theme = None
                    # remove from owned? probably keep owned; provide 'remove' if desired
                    # here we keep as owned but just allow "해제" to deactivate theme
                    st.success(f"{name} 적용을 해제했습니다.")
            else:
                if st.session_state.points >= threshold:
                    if st.button("구매(즉시 해제없이 소유)", key=f"buy_{name}"):
                        st.session_state.owned_themes[name] = {"color":color, "effect":effect, "threshold":threshold}
                        st.success(f"{name}을(를) 소유 목록에 추가했습니다.")
                else:
                    st.write("")  # not enough points: no button
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    st.markdown("**테마 미리보기 영역**")
    # 작은 미리보기: 현재 활성 테마가 없으면 기본 안내, 있으면 그 테마 효과 렌더
    if st.session_state.active_theme:
        meta = st.session_state.owned_themes.get(st.session_state.active_theme)
        st.markdown(render_effect_html(meta["effect"], meta["color"]), unsafe_allow_html=True)
    else:
        st.info("적용된 테마가 없습니다. 보유 테마에서 '적용'을 눌러보세요!")

    if st.button("⬅️ 메인으로 돌아가기"):
        st.session_state.page = None

# ---------------------------
# 기본(메인) 화면: page == None
# ---------------------------
else:
    st.markdown("### 환영합니다! 메뉴에서 `내 활동` 또는 `테마 목록`을 선택하세요.")
    st.markdown("앱은 기본적으로 **초록색 귀여운 디자인**으로 표시됩니다. 테마를 획득하면 `테마 적용`으로 배경과 애니메이션을 미리 볼 수 있어요.")
    st.markdown("---")

st.markdown('</div>', unsafe_allow_html=True)
