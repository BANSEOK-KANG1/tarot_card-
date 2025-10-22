import streamlit as st
from pathlib import Path
import pandas as pd
import random
import base64

# -------------------------------------
# 기본 설정
# -------------------------------------
APP_TITLE = "🔮 타로 카드 리딩 (뒤집기 애니메이션 버전)"
DECK_DIR = Path("deck")
IMG_DIR = DECK_DIR / "images"
META_XLSX = DECK_DIR / "metadata.xlsx"
BACK_IMAGE = IMG_DIR / "card_back.png"

DEFAULT_SPREADS = {
    "3장 스프레드 (과거-현재-미래)": ["과거", "현재", "미래"],
    "5장 스프레드 (과거-현재-미래-장점-단점)": ["과거", "현재", "미래", "장점", "단점"],
}

# -------------------------------------
# 유틸: 파일 → base64 data URI
# -------------------------------------
def image_to_data_uri(path: Path) -> str | None:
    try:
        if not path.exists():
            return None
        ext = path.suffix.lower().lstrip(".")
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}.get(ext, "image/png")
        b = path.read_bytes()
        enc = base64.b64encode(b).decode("utf-8")
        return f"data:{mime};base64,{enc}"
    except Exception:
        return None

# -------------------------------------
# 데이터 로드
# -------------------------------------
@st.cache_data
def load_metadata():
    if META_XLSX.exists():
        df = pd.read_excel(META_XLSX)
    else:
        df = pd.DataFrame([
            {"id":0, "name":"The Fool (바보)", "image_file":"MAJOR_00.png"},
            {"id":1, "name":"Ace of Wands (완드 1)", "image_file":"WANDS_1.png"},
            {"id":2, "name":"Ace of Cups (컵 1)", "image_file":"CUPS_1.png"},
            {"id":3, "name":"Ace of Swords (소드 1)", "image_file":"SWORDS_1.png"},
            {"id":4, "name":"Ace of Pentacles (펜타클 1)", "image_file":"PENTS_1.png"},
        ])
    return df

df = load_metadata()

# -------------------------------------
# Streamlit 페이지 설정
# -------------------------------------
st.set_page_config(page_title=APP_TITLE, page_icon="🔮", layout="wide")
st.title(APP_TITLE)
st.caption("처음에는 뒷면이 보이고, 버튼을 누르면 카드가 앞면으로 부드럽게 뒤집힙니다.")

# -------------------------------------
# 사이드바
# -------------------------------------
with st.sidebar:
    st.header("🧿 리딩 설정")
    spread_choice = st.selectbox("스프레드 선택", list(DEFAULT_SPREADS.keys()))
    positions = DEFAULT_SPREADS[spread_choice]
    k = len(positions)
    seed_input = st.text_input("시드 (선택)", "")
    seed = int(seed_input) if seed_input.strip().isdigit() else None

    if st.button("카드 뽑기 🎴", type="primary", use_container_width=True):
        random.seed(seed)
        st.session_state.cards = random.sample(df.to_dict("records"), k)
        st.session_state.revealed = [False] * k
        st.rerun()

# -------------------------------------
# 초기 상태 가이드
# -------------------------------------
if "cards" not in st.session_state:
    st.info("사이드바에서 스프레드를 선택하고 **카드 뽑기 🎴** 버튼을 눌러주세요.")
    st.stop()

cards = st.session_state.cards
revealed = st.session_state.revealed

# -------------------------------------
# CSS (3D flip)
# -------------------------------------
st.markdown("""
<style>
.cards-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 28px; margin-top: 24px; }
.flip-card { background: transparent; width: 100%; aspect-ratio: 11/18; perspective: 1000px; }
.flip-card-inner { position: relative; width: 100%; height: 100%; transition: transform 0.8s; transform-style: preserve-3d; }
.flip-card.flipped .flip-card-inner { transform: rotateY(180deg); }
.flip-face { position: absolute; inset: 0; backface-visibility: hidden; border-radius: 14px; box-shadow: 0 8px 26px rgba(0,0,0,0.25); overflow: hidden; background: #fff; }
.flip-face img { width: 100%; height: 100%; object-fit: cover; display: block; }
.flip-back { transform: rotateY(180deg); }
.card-title { text-align: center; font-weight: 700; margin-top: 10px; }
button[title="Toggle fullscreen view"]{display:none;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------
# 렌더
# -------------------------------------
cols = st.columns(len(cards))

for i, (col, card) in enumerate(zip(cols, cards)):
    with col:
        front_path = (IMG_DIR / str(card.get("image_file", "")).strip())
        back_path = BACK_IMAGE

        front_data = image_to_data_uri(front_path) or ""
        back_data = image_to_data_uri(back_path) or ""

        flipped_class = "flipped" if revealed[i] else ""

        html = f"""
        <div class="flip-card {flipped_class}">
          <div class="flip-card-inner">
            <div class="flip-face flip-front">
              <img src="{back_data}" alt="Back">
            </div>
            <div class="flip-face flip-back">
              <img src="{front_data}" alt="{card.get('name','Card')}">
            </div>
          </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

        # 👉 카드가 앞면일 때만 제목/버튼 표시
        if revealed[i]:
            st.markdown(f"<div class='card-title'>{card.get('name','')}</div>", unsafe_allow_html=True)
            st.button(f"카드 {i+1} 다시 뒤집기", key=f"flip_{i}_back", use_container_width=True, disabled=True)
        else:
            if st.button(f"카드 {i+1} 뒤집기", key=f"flip_{i}", use_container_width=True):
                st.session_state.revealed[i] = True
                st.rerun()

# -------------------------------------
# 전체 뒤집기 버튼
# -------------------------------------
if any(not x for x in revealed):
    st.divider()
    if st.button("모든 카드 뒤집기 ✨", use_container_width=True):
        st.session_state.revealed = [True] * len(revealed)
        st.rerun()
