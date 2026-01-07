import streamlit as st
import random
import time # 게임 진행을 위해 추가

# 1. 페이지 설정
st.set_page_config(page_title="멀티 기능 플레이그라운드", page_icon="🚀", layout="wide")

# 2. 사이드바 내비게이션
with st.sidebar:
    st.title("메뉴 선택")
    page = st.radio("이동할 페이지를 선택하세요:", ["🏠 홈", "🪑 자리 배치기", "🎮 숫자 맞추기 게임", "🚀 우주선 피하기 게임"])
    st.info("깃허브에 코드를 올리면 실시간으로 업데이트됩니다.")

# --- 페이지 1: 홈 화면 ---
if page == "🏠 홈":
    st.title("🏠 환영합니다!")
    st.subheader("원하는 서비스를 사이드바에서 선택해주세요.")
    st.write("- **자리 배치기**: 이름 리스트를 무작위로 섞어 배치합니다.")
    st.write("- **숫자 맞추기 게임**: 1~100 사이의 숫자를 맞추는 업다운 게임입니다.")
    st.write("- **우주선 피하기 게임**: 날아오는 장애물을 좌우로 움직여 피하는 게임입니다.")
    
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

    def reset_guess_game(): # 함수 이름 변경 (중복 방지)
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
            reset_guess_game()
            st.rerun()

# --- 페이지 4: 우주선 피하기 게임 ---
elif page == "🚀 우주선 피하기 게임":
    st.title("🚀 우주선 피하기 게임")
    st.write("좌우로 움직여 날아오는 장애물을 피하세요!")

    # 게임 상태 초기화 (우주선 게임용)
    if 'player_pos' not in st.session_state:
        st.session_state.player_pos = 1 # 0: 왼쪽, 1: 가운데, 2: 오른쪽
        st.session_state.score = 0
        st.session_state.game_running = False
        st.session_state.obstacle_pos = -1 # -1: 없음, 0: 왼쪽, 1: 가운데, 2: 오른쪽

    def start_dodge_game():
        st.session_state.player_pos = 1
        st.session_state.score = 0
        st.session_state.game_running = True
        st.session_state.obstacle_pos = -1 # 장애물 초기화

    def reset_dodge_game():
        st.session_state.player_pos = 1
        st.session_state.score = 0
        st.session_state.game_running = False
        st.session_state.obstacle_pos = -1 # 장애물 초기화


    if not st.session_state.game_running:
        st.info("게임을 시작하려면 '게임 시작' 버튼을 누르세요.")
        if st.button("게임 시작", key="start_dodge_game_btn"):
            start_dodge_game()
            st.rerun() # 게임 시작 후 화면 갱신
    else:
        # 플레이어 위치 표시
        player_display = ["", "🧑‍🚀", ""]
        player_display[st.session_state.player_pos] = "🚀" # 우주선 아이콘
        st.markdown(f"**현재 위치:** `{' '.join(player_display)}`")

        # 장애물 생성 및 표시
        if st.session_state.obstacle_pos == -1: # 장애물이 없으면 새로 생성
            st.session_state.obstacle_pos = random.randint(0, 2) # 0, 1, 2 중 하나
            
        obstacle_display = ["", "", ""]
        obstacle_display[st.session_state.obstacle_pos] = "☄️" # 장애물 아이콘
        st.markdown(f"**날아오는 것:** `{' '.join(obstacle_display)}`")

        # 충돌 검사
        if st.session_state.player_pos == st.session_state.obstacle_pos:
            st.error(f"💥 게임 오버! 충돌했습니다! 최종 점수: {st.session_state.score}")
            st.session_state.game_running = False
            if st.button("다시하기", key="restart_dodge_game_btn_over"):
                reset_dodge_game()
                st.rerun()
        else:
            st.session_state.score += 1
            st.write(f"점수: {st.session_state.score}")
            st.success("회피 성공! 다음 장애물을 피하세요.")
            st.session_state.obstacle_pos = -1 # 다음 장애물을 위해 초기화

            # 이동 버튼
            col_left, col_center, col_right = st.columns(3)
            with col_left:
                if st.button("⬅️ 왼쪽으로", key="move_left"):
                    if st.session_state.player_pos > 0:
                        st.session_state.player_pos -= 1
                    st.rerun()
            with col_right:
                if st.button("➡️ 오른쪽으로", key="move_right"):
                    if st.session_state.player_pos < 2:
                        st.session_state.player_pos += 1
                    st.rerun()
            with col_center:
                st.markdown("<p style='text-align:center;'>움직이지 않음</p>", unsafe_allow_html=True)
                # 아무것도 안 하는 버튼 추가 또는 메시지 (사용자가 다음 이동을 결정하도록)
                if st.button("제자리에 있기", key="stay_put"):
                    st.rerun() # 다음 턴으로 넘어가기 위해 리런

        st.progress(st.session_state.score % 100) # 점수에 따른 진행바 (예시)
        
        if st.button("게임 포기", key="give_up_dodge_game"):
            st.warning(f"게임 포기! 최종 점수: {st.session_state.score}")
            reset_dodge_game()
            st.rerun()
