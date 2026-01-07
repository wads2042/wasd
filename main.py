import streamlit as st
import random
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="멀티 기능 플레이그라운드", page_icon="🚀", layout="wide")

# 2. 사이드바 내비게이션
with st.sidebar:
    st.title("메뉴 선택")
    page = st.radio("이동할 페이지를 선택하세요:", ["🏠 홈", "🪑 자리 배치기", "🎮 숫자 맞추기 게임"])
    st.info("깃허브에 코드를 올리면 실시간으로 업데이트됩니다.")

# --- 페이지 1: 홈 화면 ---
if page == "🏠 홈":
    st.title("🏠 환영합니다!")
    st.subheader("원하는 서비스를 사이드바에서 선택해주세요.")
    st.write("- **자리 배치기**: 이름 리스트를 무작위로 섞어 배치합니다.")
    st.write("- **숫자 맞추기 게임**: 1~100 사이의 숫자를 맞추는 업다운 게임입니다.")
    
    # 방문자 간단 메모 기능 (세션 활용)
    if 'memo' not in st.session_state:
        st.session_state.memo = ""
    user_memo = st.text_input("오늘의 한 줄 메모를 남겨보세요:", value=st.session_state.memo)
    st.session_state.memo = user_memo
    if user_memo:
        st.success(f"저장된 메모: {user_memo}")

# --- 페이지 2: 자리 배치기 ---
elif page == "🪑 자리 배치기":
    st.title("🪑 랜덤 자리 배치 시스템")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        input_names = st.text_area("명단을 입력하세요 (한 줄에 한 명씩)", height=200)
    with col2:
        cols_count = st.number_input("한 줄 인원수", min_value=1, max_value=10, value=3)
        shuffle_btn = st.button("배치 시작", type="primary")

    if shuffle_btn:
        if input_names.strip():
            names = [n.strip() for n in input_names.split('\n') if n.strip()]
            random.shuffle(names)
            st.divider()
            # 그리드 배치
            rows = [names[i:i + cols_count] for i in range(0, len(names), cols_count)]
            for row in rows:
                display_cols = st.columns(cols_count)
                for i, name in enumerate(row):
                    display_cols[i].success(f"**{name}**")
        else:
            st.warning("명단을 입력해주세요.")

# --- 페이지 3: 숫자 맞추기 게임 ---
elif page == "🎮 숫자 맞추기 게임":
    st.title("🎮 숫자 맞추기 Up & Down")
    
    if 'target' not in st.session_state:
        st.session_state.target = random.randint(1, 100)
        st.session_state.count = 0
        st.session_state.over = False

    def reset():
        st.session_state.target = random.randint(1, 100)
        st.session_state.count = 0
        st.session_state.over = False

    if not st.session_state.over:
        guess = st.number_input("1~100 사이 숫자 입력", 1, 100)
        if st.button("결과 확인"):
            st.session_state.count += 1
            if guess < st.session_state.target:
                st.warning("📈 UP!")
            elif guess > st.session_state.target:
                st.info("📉 DOWN!")
            else:
                st.balloons()
                st.success(f"🎉 정답! {st.session_state.count}번 만에 맞췄어요!")
                st.session_state.over = True
    else:
        st.write(f"정답은 {st.session_state.target}!")
        if st.button("다시 시작"):
            reset()
            st.rerun()
