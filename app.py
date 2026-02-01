import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import os
import shutil

# Project Modules
from data_manager import DataManager
from analyzer import Analyzer
from visualizer import save_pattern_chart

# --- PAGE CONFIG (MOBILE OPTIMIZED) ---
st.set_page_config(
    page_title="Hassas BIST Mobile",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Style for Mobile UI
st.markdown("""
<style>
    .stMetric { background-color: #1e1e1e; padding: 10px; border-radius: 8px; border-left: 4px solid #00E676; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background: linear-gradient(135deg, #2e7d32, #1b5e20); color: white; border: none; font-weight: bold; font-size: 1.1em; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { border-radius: 4px 4px 0px 0px; padding: 10px 20px; background-color: #1e1e1e; }
    @media (max-width: 600px) {
        .stMetric { margin-bottom: 10px; }
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD RESOURCES ---
@st.cache_resource
def get_resources():
    return DataManager(), Analyzer()

manager, analyzer = get_resources()

# --- INITIALIZE SESSION STATE ---
if 'results' not in st.session_state:
    st.session_state.results = []
if 'last_scan_time' not in st.session_state:
    st.session_state.last_scan_time = None
if 'active_ticker' not in st.session_state:
    st.session_state.active_ticker = None

# --- TOP KPI NAVIGATION ---
st.title("🛡️ BIST Formasyon Tarama")
if st.session_state.results:
    res_df = pd.DataFrame(st.session_state.results)
    k1, k2, k3 = st.columns(3)
    k1.metric("📊 Taranan", f"{len(st.session_state.results)}")
    k2.metric("🎯 Bulunan", f"{len(res_df[res_df['Formasyon'] != '']) if not res_df.empty else 0}")
    if not res_df.empty:
        top_row = res_df.sort_values(by="Skor", ascending=False).iloc[0]
        k3.metric("🔥 En İyi Oran", f"%{top_row['Potansiyel']:.1f}", top_row['Hisse'])
    else:
        k3.metric("🔥 En İyi Oran", "0", "-")

# --- MOBILE SCAN TRIGGER ---
with st.container():
    start_btn = st.button("🚀 TARAMAYI BAŞLAT", type="primary", use_container_width=True)

# --- SETTINGS (SIDEBAR COLLAPSED) ---
with st.sidebar:
    st.header("⚙️ Tarama Ayarları")
    market_scope = st.selectbox("Tarama Havuzu", ["BIST 30", "BIST 100", "Tüm Hisseler", "Yeni Halka Arzlar"], index=1)
    timeframe = st.selectbox("Zaman Dilimi", ["Günlük", "Saatlik", "Haftalık"], index=0)
    
    with st.expander("🛠️ Teknik Hassasiyet"):
        candle_count = st.slider("Mum Sayısı", 100, 1000, 500)
        zigzag_dev = st.slider("ZigZag %", 0.01, 0.15, 0.04)
        LOG_OLCEK = st.toggle("Logaritmik Ölçek", value=True)
    
    selected_patterns = st.multiselect("Formasyonlar", 
        ["TOBO (Yükseliş)", "OBO (Düşüş)", "Fincan Kulp", "Boğa Bayrak (Yükseliş)", "RSI Uyumsuzluk"],
        default=["TOBO (Yükseliş)", "Fincan Kulp", "Boğa Bayrak (Yükseliş)"]
    )
    
    if st.button("🧹 Sonuçları Temizle"):
        st.session_state.results = []
        if os.path.exists("Grafikler"): shutil.rmtree("Grafikler")
        st.rerun()

# --- SCANNER ENGINE (SEQUENTIAL) ---
if start_btn:
    if market_scope == "BIST 30": tickers = [t['ticker'] for t in manager.get_bist30_tickers()]
    elif market_scope == "BIST 100": tickers = [t['ticker'] for t in manager.get_bist100_tickers()]
    elif market_scope == "Tüm Hisseler": tickers = manager.get_ipo_list(sort_by='Name (A-Z)')['ticker'].tolist()
    else: tickers = manager.get_ipo_list(sort_by='Date (Newest)')['ticker'].tolist()[:100]

    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    analyzer.config['zigzag_deviation'] = zigzag_dev
    
    for i, ticker in enumerate(tickers):
        status_text.text(f"🔍 {ticker} ({i+1}/{len(tickers)})")
        try:
            api_interval = '1h' if timeframe == "Saatlik" else '1d'
            df = manager.fetch_stock_data(ticker, interval=api_interval)
            if df is not None:
                df_res = analyzer.resample_data(df, timeframe)
                detection_df = df_res.tail(candle_count)
                indicators = analyzer.add_indicators(detection_df)
                patterns = analyzer.detect_classic_patterns(indicators, timeframe=timeframe)
                
                if patterns:
                    # Sequential chart saving if drawing is implicitly requested by showing gallery
                    p = patterns[0]
                    p['Hisse'] = ticker
                    p['log_scale'] = LOG_OLCEK
                    chart_path = save_pattern_chart(detection_df, p, filename_prefix="Mobile")
                    
                    results.append({
                        'Hisse': ticker,
                        'Formasyon': p['name'],
                        'Skor': p['score'],
                        'Potansiyel': p.get('target_pct', p.get('score', 0) / 10),
                        'Fiyat': float(df_res['Close'].iloc[-1]),
                        'ChartPath': chart_path,
                        'Points': p.get('Points')
                    })
        except: pass
        progress_bar.progress((i + 1) / len(tickers))
    
    st.session_state.results = results
    st.session_state.last_scan_time = datetime.now().strftime("%H:%M")
    status_text.empty()
    progress_bar.empty()
    st.rerun()

# --- MAIN UI TABS ---
tab_list, tab_gallery, tab_detail = st.tabs(["📋 Liste", "🖼️ Galeri", "🔍 Detay"])

with tab_list:
    if not st.session_state.results:
        st.info("💡 Aramayı başlatmak için yeşil butona tıklayın.")
    else:
        st.subheader(f"Piyasa Fırsatları ({st.session_state.last_scan_time})")
        df_display = pd.DataFrame(st.session_state.results)[['Hisse', 'Formasyon', 'Skor', 'Potansiyel', 'Fiyat']]
        selection = st.dataframe(
            df_display.style.background_gradient(subset=['Potansiyel'], cmap='Greens'),
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single_row"
        )
        if selection.selection.rows:
            st.session_state.active_ticker = df_display.iloc[selection.selection.rows[0]]['Hisse']
            st.success(f"Seçildi: {st.session_state.active_ticker}")

with tab_gallery:
    if not st.session_state.results:
        st.info("Henüz taranmış formasyon yok.")
    else:
        chart_files = [(r['Hisse'], r['Formasyon'], r['ChartPath']) for r in st.session_state.results if r.get('ChartPath') and os.path.exists(r['ChartPath'])]
        if not chart_files:
            st.warning("Grafik oluşturulamadı.")
        else:
            for hisse, pat, path in chart_files:
                with st.container():
                    st.image(path, caption=f"{hisse} - {pat}", use_container_width=True)
                    st.divider()

with tab_detail:
    target = st.session_state.active_ticker
    if not target:
        st.info("Detaylı grafik için listeden bir hisseye dokunun.")
    else:
        st.subheader(f"📊 {target} İnteraktif Görünüm")
        det_df = manager.fetch_stock_data(target)
        if det_df is not None:
            import plotly.graph_objects as go
            df_plot = analyzer.resample_data(det_df, timeframe).tail(200)
            fig = go.Figure(data=[go.Candlestick(x=df_plot['Date'], open=df_plot['Open'], high=df_plot['High'], low=df_plot['Low'], close=df_plot['Close'])])
            fig.update_layout(template='plotly_dark', height=400, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
            fig.update_yaxes(type='log' if LOG_OLCEK else 'linear')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Veri alınamadı.")
