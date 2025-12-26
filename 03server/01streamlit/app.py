import streamlit as st

st.title("나의 첫 앱")
st.text("hello streamlit")
# st.write("이것은 데이터 프레임입니다.")
st.header("여기는 헤더입니다")
st.subheader("여기는 서브헤더입니다.")

sample_code = '''

def fun():
    print("test")

'''
st.code(sample_code, language="python")

st.markdown("sample **마크다운**을 지원합니다")

mark_text = '''
### 마크다운 테스트
sample **마크다운**을 지원합니다"
- test
- test1

|test|test1|
|---|---|
|1|2|
'''
st.markdown(mark_text)

here = st.button("버튼테스트")
if here:
    st.write("버튼 테스트 클릭")

button = st.button("버튼을 누르세요")
if button:
    st.write("버튼이 눌렸습니다")

iptext = st.text_input(
    label = "가고 싶은 여행지는?",
    placeholder="여행지를 입력하세요."
)
if st.button("확인"):
    st.write(f"당산이 선택한 여행지 : {iptext}")