import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
import requests
from io import BytesIO

# 페이지 설정
st.set_page_config(page_title="YouTube 데이터 분석 마스터", page_icon="📊", layout="wide")

# YouTube API 설정
# 스트림릿 클라우드 배포 시 'Settings -> Secrets'에 API_KEY = "내키값" 을 넣어주세요.
try:
    API_KEY = st.secrets["API_KEY"]
except:
    st.error("API 키가 설정되지 않았습니다. 사이드바에 직접 입력하거나 Secrets에 추가해주세요.")
    API_KEY = st.sidebar.text_input("YouTube API Key 입력", type="password")

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_details(video_id):
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()
    return response['items'][0] if response['items'] else None

def extract_video_id(url):
    if "youtu.be/" in url:
        return url.split("/")[-1]
    elif "v=" in url:
        return url.split("v=")[1].split("&")[0]
    return url

st.title("📺 YouTube 영상 분석 & 썸네일 마스터")
st.markdown("영상 URL을 입력하면 요약 정보와 통계, 썸네일을 즉시 가져옵니다.")

# 입력창
video_url = st.text_input("YouTube 영상 URL을 입력하세요:", placeholder="https://www.youtube.com/watch?v=...")

if video_url and API_KEY:
    video_id = extract_video_id(video_url)
    
    with st.spinner('데이터를 분석 중입니다...'):
        data = get_video_details(video_id)
        
        if data:
            snippet = data['snippet']
            stats = data['statistics']
            
            # 1. 썸네일 섹션
            st.divider()
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("🖼️ 썸네일 미리보기")
                thumb_url = snippet['thumbnails']['high']['url']
                st.image(thumb_url, use_column_width=True)
                
                # 썸네일 다운로드 버튼
                response = requests.get(thumb_url)
                btn = st.download_button(
                    label="썸네일 다운로드 (JPG)",
                    data=BytesIO(response.content),
                    file_name=f"thumbnail_{video_id}.jpg",
                    mime="image/jpeg"
                )

            # 2. 요약 및 통계 섹션
            with col2:
                st.subheader("📝 영상 요약 정보")
                st.markdown(f"**제목:** {snippet['title']}")
                st.markdown(f"**채널명:** {snippet['channelTitle']}")
                
                # 날짜 및 댓글 수 시각화 (요청사항 3번)
                publish_date = datetime.strptime(snippet['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y년 %m월 %d일')
                
                st.info(f"📅 **게시일:** {publish_date}")
                st.success(f"💬 **총 댓글 수:** {format(int(stats.get('commentCount', 0)), ',')}개")

            # 3. 주요 지표 카드 (요청사항 2번)
            st.divider()
            st.subheader("📈 주요 통계 지표")
            m1, m2, m3 = st.columns(3)
            m1.metric("조회수", f"{format(int(stats.get('viewCount', 0)), ',')}회")
            m2.metric("좋아요", f"{format(int(stats.get('likeCount', 0)), ',')}개")
            m3.metric("댓글수", f"{format(int(stats.get('commentCount', 0)), ',')}개")

        else:
            st.error("영상을 찾을 수 없습니다. URL을 확인해 주세요.")
