import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="주식 분석 대시보드", layout="wide")

st.title("📈 주식 데이터 분석기")

# 사이드바 설정
st.sidebar.header("설정")
ticker_input = st.sidebar.text_input("종목 코드 입력", value="AAPL")
period = st.sidebar.selectbox("조회 기간", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

@st.cache_data
def load_data(ticker, period):
    # auto_adjust=True를 통해 구조 단순화
    df = yf.download(ticker, period=period, auto_adjust=True)
    return df

try:
    df = load_data(ticker_input, period)

    if df.empty:
        st.error("데이터를 불러오지 못했습니다. 종목 코드를 확인해 주세요.")
    else:
        # [중요] 최신 버전 yfinance 대응: .item()을 사용하여 Series를 단일 숫자로 변환
        # 최신 가격 데이터 추출
        latest_close = df['Close'].iloc[-1].item()
        prev_close = df['Close'].iloc[-2].item()
        price_diff = latest_close - prev_close
        
        # 표준편차 계산 (수익률 기준)
        daily_returns = df['Close'].pct_change().dropna()
        std_dev = daily_returns.std().item()
        max_price = df['High'].max().item()

        # 지표 출력 (포맷팅 오류 해결)
        col1, col2, col3 = st.columns(3)
        col1.metric("현재가", f"{latest_close:,.2f}", f"{price_diff:,.2f}")
        col2.metric("기간 내 표준편차 (변동성)", f"{std_dev:.4f}")
        col3.metric("최고가 (기간 내)", f"{max_price:,.2f}")

        # 차트
        st.subheader(f"{ticker_input} 주가 추이")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'].values.flatten(), mode='lines', name='Close'))
        fig.update_layout(template="plotly_white", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        # 데이터 표시
        st.subheader("데이터 상세 정보")
        st.dataframe(df.tail(10))

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
