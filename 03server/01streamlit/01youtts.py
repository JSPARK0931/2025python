import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

st.title("youtube script 가지고 오기")

youtube_url = st.text_input("youtube url")

def extract_video_id(url):
    match = re.search(r"(?:v=)([^&]+)",url)
    return  match.group(1) if match else None

# def get_transcript(video_id):
#     ytt_api = YouTubeTranscriptApi()
#     transcript = ytt_api.fetch(video_id,languages=["ko","en"]).to_raw_data()
#     full_text = "\n".join([item['text'] for item in transcript])
#     return full_text

if st.button("요약하기"):
    video_id = extract_video_id(youtube_url)
    if video_id:
        st.success("자료완료")
        st.write(video_id)

        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id,languages=["ko","en"]).to_raw_data()
        full_text = "\n".join([item['text'] for item in transcript])

        st.text_area('전체텍스트', full_text, height=400)
    else:
        st.error("올바른 URL을 입력하세요.")
        # print("올바른 URL을 입력하세요.")


# if __name__ == "__main__":
#     # print("자동실행합니다.")
#     youtube_url = input("경로를 입력하세요: ").strip()
#     video_id = extract_video_id(youtube_url)
#     print(f'값추출 : {video_id}')

#     if video_id:
#         text = get_transcript(video_id)
#         print(text)
#     else:
#         print("올바른 url을 입력하세요")
        

