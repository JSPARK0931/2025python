import streamlit as st
import yfinance as yf
from pykrx import stock as pykrx_stock
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="주식 분석 대시보드", layout="wide")

# 사이드바 설정
st.sidebar.header("설정")
ticker_input = st.sidebar.text_input("종목 코드 입력 (예: AAPL, 005930.KS)", value="005930.KS").upper()
period = st.sidebar.selectbox("조회 기간", ["5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"], index=1)

@st.cache_data
def get_yfinance_data(ticker, period):
    df = yf.download(ticker, period=period, auto_adjust=True)
    try:
        t_info = yf.Ticker(ticker)
        name = t_info.info.get('longName', t_info.info.get('shortName', ticker))
    except:
        name = ticker
    return df.dropna(), name

@st.cache_data
def get_krx_investor_data(ticker):
    try:
        krx_code = ticker.split('.')[0] # 종목번호만 추출
        today = datetime.now()
        start_date = today - timedelta(days=30)
        start_str = start_date.strftime('%Y%m%d')
        today_str = today.strftime('%Y%m%d')
        
        df_investor = pykrx_stock.get_market_trading_volume_by_investor(start_str, today_str, krx_code)
        
        if df_investor is None or df_investor.empty:
            return None

        df_selected = df_investor[['외국인', '개인']].copy()
        df_selected = df_selected.rename(columns={'외국인': 'Foreign_Net_Buy', '개인': 'Individual_Net_Buy'})
        return df_selected
    except Exception as e:
        return None

try:
    df, company_name = get_yfinance_data(ticker_input, period)

    if df.empty or len(df) < 2:
        st.error(f"'{ticker_input}'의 데이터를 불러오지 못했습니다. 티커가 정확한지 확인해 주세요.")
    else:
        st.title(f"📈 {company_name} ({ticker_input}) 분석")

        latest_close = float(df['Close'].iloc[-1])
        prev_close = float(df['Close'].iloc[-2])
        price_diff = latest_close - prev_close
        
        daily_returns = df['Close'].pct_change().dropna()
        std_dev = float(daily_returns.std())
        max_price = float(df['High'].max())

        col1, col2, col3 = st.columns(3)
        col1.metric("현재가", f"{latest_close:,.2f}", f"{price_diff:,.2f}")
        col2.metric("일일 수익률 표준편차", f"{std_dev:.4f}")
        col3.metric("기간 내 최고가", f"{max_price:,.2f}")

        # 가격 차트
        st.subheader(f"주가 추이 ({period})")
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(x=df.index, y=df['Close'].values.flatten(), mode='lines', name='종가'))
        fig_price.update_layout(template="plotly_white", hovermode="x unified", margin=dict(t=20, b=0), height=400)
        st.plotly_chart(fig_price, use_container_width=True)

        # 거래량 차트
        st.subheader(f"거래량 ({period})")
        fig_volume = go.Figure()
        fig_volume.add_trace(go.Bar(x=df.index, y=df['Volume'].values.flatten(), name='거래량', marker_color='rgba(128, 128, 128, 0.5)'))
        fig_volume.update_layout(template="plotly_white", margin=dict(t=0, b=20), height=200)
        st.plotly_chart(fig_volume, use_container_width=True)
        
        # --- [수정된 부분] KS 데이터인 경우 매매동향 분리 표시 ---
        if '.KS' in ticker_input or '.KQ' in ticker_input:
            df_investor = get_krx_investor_data(ticker_input)
            if df_investor is not None and not df_investor.empty:
                st.subheader("외국인 순매수 동향 (최근 1개월, 단위: 주)")
                # 외국인 차트
                fig_foreign = go.Figure()
                fig_foreign.add_trace(go.Bar(x=df_investor.index, y=df_investor['Foreign_Net_Buy'], name='외국인 순매수', marker_color='#1f77b4'))
                fig_foreign.update_layout(template="plotly_white", margin=dict(t=0, b=20), height=200)
                st.plotly_chart(fig_foreign, use_container_width=True)
                
                st.subheader("개인 순매수 동향 (최근 1개월, 단위: 주)")
                # 개인 차트
                fig_individual = go.Figure()
                fig_individual.add_trace(go.Bar(x=df_investor.index, y=df_investor['Individual_Net_Buy'], name='개인 순매수', marker_color='#ff7f0e'))
                fig_individual.update_layout(template="plotly_white", margin=dict(t=0, b=20), height=200)
                st.plotly_chart(fig_individual, use_container_width=True)

        # --------------------------------------------------------

        # 데이터 표
        with st.expander("데이터 상세 보기 (yfinance 기준)"):
            st.dataframe(df.tail(20))

except Exception as e:
    st.error(f"데이터 처리 중 오류 발생: {e}")