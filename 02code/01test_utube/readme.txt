error 발생시 운영체제별 해결 방법은 다음과 같습니다.

1. Windows 사용자
Windows는 FFmpeg가 기본 내장되어 있지 않으므로 수동 설치가 필요합니다.
FFmpeg 다운로드: GYAN.dev에 접속하여 ffmpeg-git-full.7z (또는 release build)를 다운로드합니다.
압축 해제: 다운로드한 파일의 압축을 풀고, bin 폴더 안에 있는 ffmpeg.exe와 ffprobe.exe를 확인합니다.
환경 변수 등록:
bin 폴더의 전체 경로(예: C:\ffmpeg\bin)를 복사합니다.
내 PC 우클릭 -> 속성 -> 고급 시스템 설정 -> 환경 변수 -> 시스템 변수 중 Path 선택 후 '편집' -> '새로 만들기' -> 복사한 경로 붙여넣기.
터미널 재시작: VS Code나 CMD를 껐다 켜야 변경 사항이 적용됩니다.

2. Mac 사용자 (Homebrew 이용)
터미널에서 아래 명령어를 한 줄만 입력하면 간단히 해결됩니다.
bash
brew install ffmpeg
코드를 사용할 때는 주의가 필요합니다.

3. Linux (Ubuntu/Debian) 사용자
bash
sudo apt update
sudo apt install ffmpeg
코드를 사용할 때는 주의가 필요합니다.

4. Streamlit Cloud에 배포할 경우
만약 GitHub에 올려서 Streamlit Cloud로 서비스하려는 경우, 코드만으로는 작동하지 않습니다.
프로젝트 루트 폴더(최상단)에 packages.txt 파일을 만듭니다.
파일 내용에 딱 한 줄만 적어주면 Streamlit 서버가 자동으로 FFmpeg를 설치합니다.
text
ffmpeg
코드를 사용할 때는 주의가 필요합니다.

✅ 팁: 설치 없이 실행하고 싶을 때 (Windows 한정)
설치가 번거롭다면, ffmpeg.exe와 ffprobe.exe 파일을 현재 Python 코드(app.py)가 있는 폴더에 직접 복사해 넣으면 환경 변수 설정 없이도 yt-dlp가 알아서 찾아 사용합니다.