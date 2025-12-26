import streamlit as st
import yt_dlp
import os
import tempfile

st.title("🎵 유튜브 MP3 다운로더")

url = st.text_input("유튜브 영상 URL을 입력하세요:")

if url:
    with st.spinner('음원 정보를 분석 중입니다...'):
        # 임시 폴더 생성 및 설정
        with tempfile.TemporaryDirectory() as tmpdirname:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(tmpdirname, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    # 실제 생성된 파일 경로 확인
                    file_path = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
                    
                    with open(file_path, "rb") as f:
                        st.audio(f.read(), format="audio/mp3") # 미리듣기
                        st.download_button(
                            label="MP3 다운로드",
                            data=f,
                            file_name=os.path.basename(file_path),
                            mime="audio/mpeg"
                        )
                st.success("변환 완료!")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")