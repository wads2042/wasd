import streamlit as st
import pandas as pd
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title="나의 첫 스트림릿 사이트", layout="wide")

# 2. 사이드바 구성
with st.sidebar:
    st.header("설정")
    user_name = st.text_input("이름을 입력하세요", "방문자")
    selected_page = st.selectbox("페이지 선택", ["홈", "데이터 분석", "정보"])

# 3. 메인 페이지 로직
if selected_page == "홈":
    st.title(f"👋 반갑습니다, {user_name}님!")
    st.write("이 사이트는 스트림릿과 깃허브를 통해 배포되었습니다.")
    
    # 간단한 그래프 예시
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
    st.line_chart(chart_data)

elif selected_page == "데이터 분석":
    st.title("📊 데이터 분석 페이지")
    st.info("여기에 분석 결과를 시각화할 수 있습니다.")
    
    # 데이터 프레임 출력
    df = pd.DataFrame({
        '과일': ['사과', '바나나', '딸기', '포도'],
        '가격': [1000, 500, 2500, 3000],
        '재고': [10, 20, 5, 12]
    })
    st.table(df)

elif selected_page == "정보":
    st.title("ℹ️ 정보")
    st.write("이 앱은 Streamlit 라이브러리를 사용해 제작되었습니다.")
