import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="랜덤 자리 배치기", page_icon="🪑")

st.title("🪑 랜덤 자리 배치 시스템")
st.write("명단을 입력하고 버튼을 누르면 무작위로 자리를 배치합니다.")

# 1. 입력 섹션
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        # 이름 입력창 (줄바꿈으로 구분)
        input_names = st.text_area("학생/참석자 명단을 입력하세요 (한 줄에 한 명씩)", 
                                  height=200, 
                                  placeholder="홍길동\n김철수\n이영희")
    
    with col2:
        # 가로 행 수 설정
        columns_count = st.number_input("한 줄에 몇 명씩 앉나요?", min_value=1, max_value=10, value=3)
        shuffle_button = st.button("자리 배치 시작!", type="primary")

# 2. 로직 처리 및 출력
if shuffle_button:
    if not input_names.strip():
        st.warning("먼저 명단을 입력해주세요!")
    else:
        # 이름 리스트 만들기
        name_list = [name.strip() for name in input_names.split('\n') if name.strip()]
        
        # 무작위 섞기
        random.shuffle(name_list)
        
        st.divider()
        st.subheader("📍 배치 결과")
        
        # 그리드(Grid) 레이아웃으로 출력
        rows = [name_list[i:i + columns_count] for i in range(0, len(name_list), columns_count)]
        
        for row in rows:
            cols = st.columns(columns_count)
            for i, name in enumerate(row):
                with cols[i]:
                    st.success(f"**{name}**")

st.sidebar.info("Tip: 깃허브에 업데이트하면 자동으로 반영됩니다.")
