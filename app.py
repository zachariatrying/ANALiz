import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

# --- 1. AYARLAR & CSS (DARK MODE PRO) ---
st.set_page_config(
    page_title="ZACHARIA X", 
    page_icon="💎", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Profesyonel "Quant" Görünümü CSS
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; }
    /* Kart Yapısı */
    div.css-1r6slb0 { border: 1px solid #333; border-radius: 12px; padding: 15px; background-color: #111; }
    /* Metrikler */
    [data-testid="stMetricValue"] { font-family: 'Courier New', monospace; font-weight: bold; color: #00ffcc; }
    [data-testid="stMetricLabel"] { font-size: 0.8rem; color: #888; }
    /* Tablo */
    .stDataFrame { border: 1px solid #222; }
    /* Buton */
    .stButton>button { 
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%); 
        color: black; font-weight: bold; border: none; height: 3.5em; border-radius: 8px;
    }
    .stButton>button:hover { transform: scale(1.02); }
    /* Expander */
    .streamlit-expanderHeader { background-color: #1a1a1a; color: white; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# --- 2. HİSSE HAVUZU (BIST TÜM & 30) ---
BIST_30 = "AKBNK,ARCLK,ASELS,ASTOR,BIMAS,BRSAN,EKGYO,ENKAI,EREGL,FROTO,GARAN,GUBRF,HEKTS,ISCTR,KCHOL,KONTR,KOZAL,KRDMD,ODAS,OYAKC,PETKM,PGSUS,SAHOL,SASA,SISE,TCELL,THYAO,TOASO,TUPRS,YKBNK".split(',')
TUM_LISTE_STR = """
THYAO, ASELS, GARAN, AKBNK, TCELL, EREGL, SASA, HEKTS, FROTO, KCHOL, PETKM, BIMAS, SISE, KOZAL, TUPRS, SAHOL, ENKAI, ISCTR, YKBNK, ARCLK, KONTR, OYAKC, GUBRF, EKGYO, ODAS, KRDMD, ASTOR, SMRTG, EGEEN, DOAS, MGROS, PGSUS, TTRAK, TOASO, VESTL, ZOREN, SOKM, ALARK, TKFEN, TAVHL, ULKER, TTKOM, HALKB, VAKBN, SKBNK, ISMEN, MAVI, KOZAA, IPEKE, CIMSA, AKSEN, ALBRK, AYDEM, BASGZ, BERA, BIOEN, BRISA, BRSAN, CANTE, CEMTS, CCOLA, DEVA, ECILC, EGEN, ENJSA, GENIL, GESAN, GLYHO, GOZDE, GWIND, HEDEF, HLGYO, INDES, INVES, ISGYO, IZMDC, KARSN, KARTN, KCAER, KMPUR, KORDS, KZBGY, LOGO, MAVI, MEDTR, NTHOL, OTKAR, OZKGY, PENTA, PSGYO, QUAGR, RTALB, SARKY, SELEC, SKTAS, SMART, SNGYO, TATGD, TSKB, TURSG, ULUSE, VAKKO, VERUS, VESBE, YATAS, YYLGD, ZRGYO, MIATK, REEDR, ADEL
"""

# --- 3. MATEMATİK MOTORU (QUANT ENGINE) ---
@st.cache_data(ttl=300)
def veri_getir_ve_hesapla(hisse, bar_sayisi=150):
    try:
        symbol = f"{hisse}.IS" if not hisse.endswith(".IS") else hisse
        # Veri Çekme
        df = yf.download(symbol, period="1y", progress=False)
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        df = df.rename(columns={'Open':'Open', 'High':'High', 'Low':'Low', 'Close':'Close', 'Volume':'Volume'})
        
        if len(df) < 50: return None

        # --- GELİŞMİŞ İNDİKATÖRLER ---
        
        # 1. Trend (SMA & EMA)
        df['SMA20'] = df['Close'].rolling(20).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()
        df['SMA200'] = df['Close'].rolling(200).mean()
        
        # 2. Momentum (RSI)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # 3. Trend Gücü (MACD)
        ema12 = df['Close'].ewm(span=12, adjust=False).mean()
        ema26 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = ema12 - ema26
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        # 4. Volatilite (Bollinger Bands)
        std = df['Close'].rolling(20).std()
        df['BB_Upper'] = df['SMA20'] + (std * 2)
        df['BB_Lower'] = df['SMA20'] - (std * 2)
        
        # 5. Hacim Ortalaması
        df['Vol_SMA20'] = df['Volume'].rolling(20).mean()

        return df.tail(bar_sayisi)
    except:
        return None

def quant_skorlama(df):
    """
    Bu fonksiyon hisseye 0-100 arası bir 'Karne Notu' verir.
    """
    son = df.iloc[-1]
    prev = df.iloc[-2]
    score = 0
    reasons = []
    
    # 1. TREND PUANI (Max 40)
    if son['Close'] > son['SMA50']: 
        score += 20
        if son['SMA50'] > son['SMA200']: score += 20 # Golden Cross Bölgesi
    
    # 2. MOMENTUM PUANI (Max 30)
    if 50 < son['RSI'] < 70: # En sağlıklı yükseliş bölgesi
        score += 20
        reasons.append("RSI Güçlü")
    elif son['RSI'] > 70: # Aşırı alım (Riskli ama güçlü)
        score += 10
        reasons.append("RSI Zirve")
    elif son['RSI'] < 30: # Aşırı satım (Dip tepkisi)
        score += 10
        reasons.append("Dip Tepkisi")
        
    # MACD Kesişimi
    if son['MACD'] > son['Signal_Line']:
        score += 10
        reasons.append("MACD Al")
        
    # 3. HACİM PUANI (Max 20)
    if son['Volume'] > son['Vol_SMA20']:
        score += 20
        reasons.append("Hacim Patlaması")
        
    # 4. FORMASYON PUANI (Max 10)
    # Basit bir kırılım kontrolü
    if son['Close'] > df['High'].iloc[-20:].max() * 0.98: # Zirveye yakın
        score += 10
        reasons.append("Zirve Zorluyor")
        
    return score, reasons

def formasyon_tespiti(df, score):
    son = df.iloc[-1]
    
    # Skor düşükse hiç bakma
    if score < 60: return None
    
    formasyon = "Güçlü Trend" # Varsayılan
    hedef = son['Close'] * 1.10
    stop = son['SMA20'] # Stop loss dinamik
    
    # 1. HIGH TIGHT FLAG (Roket)
    # 40 günde %50 artmış ve düşmemiş
    ref_price = df['Close'].iloc[-40] if len(df) > 40 else df['Close'].iloc[0]
    if son['Close'] > ref_price * 1.50 and son['Close'] > df['High'].max() * 0.85:
        formasyon = "HIGH TIGHT FLAG 🚀"
        hedef = son['Close'] * 1.40
        stop = son['Close'] * 0.92
        
    # 2. BOĞA BAYRAK
    elif son['Close'] > son['SMA20'] and son['RSI'] < 70:
        formasyon = "BOĞA BAYRAK 🐂"
        hedef = son['Close'] * 1.25
        stop = son['SMA50']
        
    # 3. DIP DÖNÜŞÜ (RSI < 30'dan çıkış)
    elif df['RSI'].iloc[-5:].min() < 30 and son['RSI'] > 30:
        formasyon = "DİP DÖNÜŞÜ 🎣"
        hedef = son['Close'] * 1.15
        stop = df['Low'].iloc[-5:].min()
        
    return {
        "Formasyon": formasyon,
        "Skor": score,
        "Fiyat": son['Close'],
        "Hedef": hedef,
        "Stop": stop,
        "Potansiyel": ((hedef - son['Close']) / son['Close']) * 100
    }

# --- 4. GRAFİK MOTORU (INTERAKTİF PLOTLY) ---
def ciz_interaktif_grafik(df, hisse, sinyal):
    # Candlestick
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, row_heights=[0.7, 0.3],
                        subplot_titles=(f"{hisse} - {sinyal['Formasyon']}", "Hacim & RSI"))

    # Fiyatlar
    fig.add_trace(go.Candlestick(x=df.index,
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close'],
                    name='Fiyat'), row=1, col=1)

    # Ortalamalar
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'], line=dict(color='orange', width=1), name='SMA 20'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA50'], line=dict(color='cyan', width=1), name='SMA 50'), row=1, col=1)
    
    # Hacim (Renkler: Yükseliş Yeşil, Düşüş Kırmızı)
    colors = ['green' if row['Open'] - row['Close'] >= 0 else 'red' for index, row in df.iterrows()]
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colors, name='Hacim'), row=2, col=1)

    # Hedef ve Stop Çizgileri
    fig.add_hline(y=sinyal['Hedef'], line_dash="dot", annotation_text="HEDEF", annotation_position="top right", line_color="green", row=1, col=1)
    fig.add_hline(y=sinyal['Stop'], line_dash="dot", annotation_text="STOP", annotation_position="bottom right", line_color="red", row=1, col=1)

    # Düzenlemeler
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        height=500,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="#111",
        plot_bgcolor="#111",
        font=dict(color="white"),
        hovermode="x unified"
    )
    fig.update_xaxes(gridcolor='#333')
    fig.update_yaxes(gridcolor='#333')
    
    return fig

# --- 5. ARAYÜZ (ZACHARIA X DASHBOARD) ---
st.title("💎 ZACHARIA X - QUANTUM ENGINE")

with st.sidebar:
    st.header("🎛️ ANALİZ MERKEZİ")
    liste_secimi = st.radio("Tarama Listesi", ["Favorilerim", "BIST 30", "TÜM BIST (Pro)"])
    
    if liste_secimi == "Favorilerim":
        if 'my_favs' not in st.session_state: st.session_state.my_favs = "THYAO, ASELS, GARAN, TCELL, AKBNK"
        txt_hisse = st.text_area("Hisseler:", value=st.session_state.my_favs)
        st.session_state.my_favs = txt_hisse
        hisseler = [x.strip() for x in txt_hisse.split(',')]
    elif liste_secimi == "BIST 30":
        hisseler = BIST_30
    else:
        hisseler = [x.strip() for x in TUM_LISTE_STR.split(',') if len(x)>1]
        
    min_skor = st.slider("Minimum Kalite Skoru", 0, 100, 70, help="Sadece bu puanın üzerindekileri göster")
    bar_sayisi = st.slider("Grafik Derinliği", 50, 300, 100)
    
    btn_baslat = st.button("🚀 X-RAY TARAMASI BAŞLAT", type="primary")

if btn_baslat:
    col_status, col_bar = st.columns([1, 3])
    status_text = col_status.empty()
    progress_bar = col_bar.progress(0)
    
    bulunanlar = []
    
    # --- HIZLI TARAMA DÖNGÜSÜ ---
    for i, hisse in enumerate(hisseler):
        status_text.text(f"Analiz ediliyor: {hisse} (%{int((i+1)/len(hisseler)*100)})")
        progress_bar.progress((i+1)/len(hisseler))
        
        df = veri_getir_ve_hesapla(hisse, bar_sayisi)
        if df is not None:
            skor, nedenler = quant_skorlama(df)
            
            # Filtreleme
            if skor >= min_skor:
                sinyal = formasyon_tespiti(df, skor)
                if sinyal:
                    sinyal['Hisse'] = hisse
                    sinyal['Nedenler'] = ", ".join(nedenler)
                    bulunanlar.append(sinyal)

    progress_bar.empty()
    status_text.empty()
    
    # --- SONUÇLAR ---
    if not bulunanlar:
        st.error("❌ Bu kriterlere uygun 'Süper Hisse' bulunamadı. Kriterleri gevşet.")
    else:
        # Önce En Yüksek Puanlıları Göster
        bulunanlar = sorted(bulunanlar, key=lambda x: x['Skor'], reverse=True)
        
        st.success(f"🔥 {len(bulunanlar)} adet Elit Fırsat Tespit Edildi!")
        
        tab_dashboard, tab_liste = st.tabs(["📊 X-DASHBOARD", "📋 LİSTE"])
        
        with tab_dashboard:
            for veri in bulunanlar:
                with st.expander(f"💎 {veri['Hisse']} | Skor: {veri['Skor']} | {veri['Formasyon']}", expanded=True):
                    
                    # Üst Bilgi Paneli
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Fiyat", f"{veri['Fiyat']:.2f} TL")
                    c2.metric("Hedef", f"{veri['Hedef']:.2f} TL", delta=f"%{veri['Potansiyel']:.1f}")
                    c3.metric("Stop-Loss", f"{veri['Stop']:.2f} TL", delta_color="inverse")
                    c4.metric("Güç Skoru", f"{veri['Skor']}/100")
                    
                    st.caption(f"💡 **Tespit Sebepleri:** {veri['Nedenler']}")
                    
                    # İnteraktif Grafik Çizimi (Anlık)
                    df_chart = veri_getir_ve_hesapla(veri['Hisse'], bar_sayisi)
                    fig = ciz_interaktif_grafik(df_chart, veri['Hisse'], veri)
                    st.plotly_chart(fig, use_container_width=True)
                    
        with tab_liste:
            df_table = pd.DataFrame(bulunanlar)[['Hisse', 'Fiyat', 'Hedef', 'Stop', 'Skor', 'Potansiyel', 'Formasyon']]
            st.dataframe(
                df_table,
                use_container_width=True,
                column_config={
                    "Skor": st.column_config.ProgressColumn("Quant Skoru", min_value=0, max_value=100, format="%d"),
                    "Potansiyel": st.column_config.NumberColumn("Potansiyel %", format="%.1f%%")
                }
            )

else:
    st.info("👈 Soldan ayarlarını yap ve 'X-RAY TARAMASI' butonuna bas.")
    st.markdown("### 🧬 Bu Versiyonda Neler Var?")
    st.markdown("""
    * **Plotly İnteraktif Grafikler:** Zoom yap, kaydır, incele.
    * **Quant Puanlama:** RSI, MACD, Hacim ve Trendi birleştirip 100 üzerinden not verir.
    * **Dinamik Stop-Loss:** Sadece hedefi değil, kaçman gereken yeri de söyler.
    * **Dark Mode UI:** Göz yormayan, profesyonel terminal tasarımı.
    """)
