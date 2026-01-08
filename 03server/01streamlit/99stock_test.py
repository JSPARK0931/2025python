# import streamlit as st
# import yfinance as yf
# import pandas as pd
# import matplotlib.pyplot as plt

# # 페이지 설정
# st.set_page_config(page_title="월봉 매매 신호 2026", layout="wide")

# st.title("📈 월봉 기반 장기 투자 전략 분석기")

# # 1. 사용자 입력 (사이드바)
# symbol = st.sidebar.text_input("주식 티커 입력 (예: AAPL, 005930.KS)", value="AAPL")
# period = st.sidebar.selectbox("조회 기간", ["5y", "10y", "max"], index=1)

# if symbol:
#     try:
#         # 데이터 가져오기 (auto_adjust로 가격 구조 단순화)
#         df = yf.download(symbol, period=period, interval="1mo", auto_adjust=True)
        
#         if df.empty:
#             st.error("데이터를 찾을 수 없습니다. 티커를 확인해주세요.")
#         else:
#             # [에러 수정] 멀티인덱스 방지 및 단일 컬럼 선택
#             if isinstance(df.columns, pd.MultiIndex):
#                 df.columns = df.columns.get_level_values(0)
            
#             # 2. 보조지표 계산 (Series로 변환하여 계산 안정성 확보)
#             close_series = df['Close'].squeeze()
            
#             df['MA5'] = close_series.rolling(window=5).mean()
#             df['MA20'] = close_series.rolling(window=20).mean()
            
#             # RSI 계산 (에러 방지형 로직)
#             delta = close_series.diff()
#             gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
#             loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
#             # 0으로 나누기 방지
#             rs = gain / loss.replace(0, 1e-10) 
#             df['RSI'] = 100 - (100 / (1 + rs))
            
#             # 3. 매매 신호
#             df['Signal'] = 0
#             # NaN 값이 아닌 구간에서만 비교
#             valid_idx = df.index[df['MA20'].notna()]
#             df.loc[valid_idx, 'Signal'] = (df.loc[valid_idx, 'MA5'] > df.loc[valid_idx, 'MA20']).astype(int)
#             df['Position'] = df['Signal'].diff()

#             # 4. 차트 시각화
#             fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), sharex=True, 
#                                                 gridspec_kw={'height_ratios': [3, 1, 1]})

#             # 주가 차트
#             ax1.plot(df.index, close_series, label='종가', color='black', alpha=0.3)
#             ax1.plot(df.index, df['MA5'], label='5개월선', color='orange', linewidth=1.5)
#             ax1.plot(df.index, df['MA20'], label='20개월선', color='blue', linewidth=1.5)
            
#             # 매수/매도 화살표 표시 (scatter 사용)
#             buy_points = df[df['Position'] == 1]
#             sell_points = df[df['Position'] == -1]
            
#             ax1.scatter(buy_points.index, buy_points['Close'], marker='^', s=200, color='red', label='매수(GC)', zorder=5)
#             ax1.scatter(sell_points.index, sell_points['Close'], marker='v', s=200, color='blue', label='매도(DC)', zorder=5)
            
#             ax1.set_title(f"[{symbol}] 분석 차트", fontsize=15)
#             ax1.legend(loc='best')
#             ax1.grid(True, linestyle='--', alpha=0.5)

#             # RSI 차트
#             ax2.plot(df.index, df['RSI'], color='purple')
#             ax2.axhline(70, color='red', linestyle='--', alpha=0.5)
#             ax2.axhline(30, color='blue', linestyle='--', alpha=0.5)
#             ax2.set_ylabel('RSI')
#             ax2.set_ylim(0, 100)
#             ax2.grid(True, alpha=0.3)

#             # 거래량 차트
#             ax3.bar(df.index, df['Volume'], color='gray', alpha=0.6)
#             ax3.set_ylabel('Volume')

#             st.pyplot(fig)

#             # 데이터 요약
#             st.subheader("최근 12개월 데이터")
#             st.write(df.tail(12).iloc[::-1]) # 역순 정렬

#     except Exception as e:
#         st.error(f"실행 중 에러가 발생했습니다: {e}")

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# 페이지 설정
st.set_page_config(page_title="주식 차트 분석기 (일/주/월봉)", layout="wide")
st.title("📊 인터랙티브 주식 캔들차트 분석")

# 사이드바 입력 및 옵션
symbol = st.sidebar.text_input("주식 티커 입력 (예: AAPL, 005930.KS)", value="AAPL")
selected_period = st.sidebar.selectbox("조회 기간 단위", ["일봉", "주봉", "월봉"], index=2)
total_history = st.sidebar.selectbox("전체 조회 기간", ["1y", "5y", "10y", "max"], index=1)

# 기간 단위 매핑
interval_map = {"일봉": "1d", "주봉": "1wk", "월봉": "1mo"}
interval = interval_map[selected_period]

if symbol:
    try:
        # 1. 데이터 가져오기 및 종목명 추출
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=total_history, interval=interval, auto_adjust=False)
        
        stock_name = ticker.info.get('longName', symbol) 
        
        if len(df) < 20:
            st.warning("분석을 위한 데이터가 부족합니다. (최소 20개 이상의 데이터가 필요합니다.)")
        else:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # 2. 지표 계산
            close_prices = df['Close'].squeeze()
            df['MA5'] = close_prices.rolling(window=5).mean()
            df['MA20'] = close_prices.rolling(window=20).mean()
            
            delta = close_prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            df['RSI'] = 100 - (100 / (1 + (gain / loss.replace(0, 1e-10))))

            df['Signal'] = (df['MA5'] > df['MA20']).astype(int)
            df['Position'] = df['Signal'].diff()

            # 3. Plotly 차트 생성
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.15, row_heights=[0.7, 0.3],
                                subplot_titles=(f'{stock_name} ({symbol}) - {selected_period} 차트', 'RSI 지표'))

            # (1) 캔들스틱 차트 (Hover 정보 포함)
            fig.add_trace(go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                name='OHLC', increasing_line_color='red', decreasing_line_color='blue',
                hovertext=[
                    f"날짜: {d.strftime('%Y-%m-%d')}<br>" +
                    f"시가: {o:.2f}<br>고가: {h:.2f}<br>저가: {l:.2f}<br>종가: {c:.2f}<br>" +
                    f"MA5: {ma5:.2f}<br>MA20: {ma20:.2f}"
                    for d, o, h, l, c, ma5, ma20 in zip(df.index, df['Open'], df['High'], df['Low'], df['Close'], df['MA5'], df['MA20'])
                ],
                hoverinfo='text'
            ), row=1, col=1)

            # (2) 이동평균선 추가 (hoverinfo='skip'으로 중복 방지)
            fig.add_trace(go.Scatter(x=df.index, y=df['MA5'], name='5이평', line=dict(color='orange', width=1.5), hoverinfo='skip'), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='20이평', line=dict(color='dodgerblue', width=1.5), hoverinfo='skip'), row=1, col=1)

            # (3) 매수/매도 신호 화살표
            buy_df = df[df['Position'] == 1]
            sell_df = df[df['Position'] == -1]

            fig.add_trace(go.Scatter(
                x=buy_df.index, y=buy_df['Low'] * 0.95, mode='markers',
                marker=dict(symbol='triangle-up', size=15, color='red'), name='매수 신호', hoverinfo='skip'
            ), row=1, col=1)

            fig.add_trace(go.Scatter(
                x=sell_df.index, y=sell_df['High'] * 1.05, mode='markers',
                marker=dict(symbol='triangle-down', size=15, color='blue'), name='매도 신호', hoverinfo='skip'
            ), row=1, col=1)

            # (4) RSI 차트
            fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='purple'), hoverinfo='skip'), row=2, col=1)
            # RSI 과매수/과매도 라인 추가
            fig.add_shape(type="line", xref="x", yref="y2", x0=df.index[0], y0=70, x1=df.index[-1], y1=70, line=dict(color="red", dash="dash"), row=2, col=1)
            fig.add_shape(type="line", xref="x", yref="y2", x0=df.index[0], y0=30, x1=df.index[-1], y1=30, line=dict(color="blue", dash="dash"), row=2, col=1)


            # 4. 레이아웃 및 Hover 설정
            fig.update_layout(
                height=800,
                xaxis_rangeslider_visible=False,
                hovermode='closest',
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)

            # 5. 최신 정보 출력 추가
            st.subheader("📊 현재 분석 요약")
            
            last_close = df['Close'].iloc[-1]
            last_rsi = df['RSI'].iloc[-1]
            last_signal_value = df['Signal'].iloc[-1]
            
            if last_signal_value == 1:
                signal_text = "🟢 매수 신호 (골든 크로스)"
                color = "green"
            else:
                signal_text = "🔴 매도/관망 신호 (데드 크로스 또는 추세 하락)"
                color = "red"
            
            # Streamlit Metric과 Markdown을 사용하여 보기 좋게 표시
            col1, col2, col3 = st.columns(3)
            col1.metric("현재가", f"{last_close:,.0f} 원/달러")
            col2.metric("RSI (14)", f"{last_rsi:.2f}", delta_color="off")
            col3.markdown(f"**현재 신호:** <span style='color:{color}'>{signal_text}</span>", unsafe_allow_html=True)
            
            st.caption(f"* RSI 70 이상은 과매수, 30 이하는 과매도 구간입니다.")

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")