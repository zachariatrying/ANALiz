import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="Borsa Mobil", 
    page_icon="📱", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Mobil İçin CSS (Yazıları biraz büyütelim)
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    [data-testid="stMetric"] { background-color: #262730; border-radius: 10px; padding: 10px; }
    div[data-testid="stCaptionContainer"] { font-size: 14px; color: #b0b0b0; }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ MOTORU ---
@st.cache_data(ttl=300)
def veri_getir(hisse):
    try:
        symbol = f"{hisse}.IS" if not hisse.endswith(".IS") else hisse
        df = yf.download(symbol, period="1y", progress=False)
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        df = df.rename(columns={'Open':'Open', 'High':'High', 'Low':'Low', 'Close':'Close'})
        return df
    except:
        return None

# --- 3. ANALİZ MOTORU (Nokta Hesaplayıcı) ---
def analiz_yap(df):
    # --- SENİN MATEMATİKSEL FORMÜLLERİN BURAYA ---
    # Şimdilik noktaları göstermek için simülasyon:
    son_fiyat = df['Close'].iloc[-1]
    
    # Gerçek dip ve tepeleri bulalım ki tarihler doğru olsun
    # Son 3 aydaki en düşük nokta (Başlangıç)
    son_3_ay = df.tail(90)
    idx_dip = son_3_ay['Low'].idxmin()
    
    # Son 1 aydaki en yüksek nokta (Tepe)
    son_1_ay = df.tail(30)
    idx_tepe = son_1_ay['High'].idxmax()
    
    # Bugün (Kırılım)
    idx_son = df.index[-1]
    
    return {
        "Formasyon": "Boğa Bayrak 🐂",
        "Skor": 90,
        "Hedef": son_fiyat * 1.30,
        "Potansiyel": 30.0,
        "Points": {
            "t_start": idx_dip, # Tarih (Timestamp)
            "t_peak": idx_tepe,
            "t_break": idx_son,
            "p_start": df.loc[idx_dip]['Low'], # Fiyat
            "p_peak": df.loc[idx_tepe]['High'],
            "p_break": son_fiyat
        }
    }

# --- 4. ARAYÜZ ---
st.title("📱 Cepten Borsa Takip")

with st.sidebar:
    st.header("Ayarlar")
    hisse_girdisi = st.text_area("Hisseler", "THYAO, ASELS, GARAN, TCELL, EREGL, AKBNK")
    btn_tara = st.button("🚀 TARAMAYI BAŞLAT", type="primary", use_container_width=True)

if btn_tara:
    hisseler = [h.strip() for h in hisse_girdisi.split(',')]
    st.info(f"{len(hisseler)} hisse taranıyor...")
    
    tab_grafik, tab_liste = st.tabs(["📊 Analiz Kartları", "📋 Liste"])
    
    sonuclar = []
    
    with tab_grafik:
        for hisse in hisseler:
            df = veri_getir(hisse)
            
            if df is not None and len(df) > 50:
                sinyal = analiz_yap(df)
                
                if sinyal:
                    sinyal['Hisse'] = hisse
                    sinyal['Fiyat'] = df['Close'].iloc[-1]
                    sonuclar.append(sinyal)
                    
                    # --- KART TASARIMI ---
                    st.markdown(f"### {hisse} - {sinyal['Formasyon']}")
                    
                    # 1. GRAFİK ÇİZİMİ
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.plot(df.index, df['Close'], color='#3498db', linewidth=2, label='Fiyat')
                    
                    pts = sinyal['Points']
                    
                    # Noktaları Çiz
                    ax.scatter(pts['t_start'], pts['p_start'], color='green', s=100, zorder=5)
                    ax.scatter(pts['t_peak'], pts['p_peak'], color='red', s=100, zorder=5)
                    ax.scatter(pts['t_break'], pts['p_break'], color='gold', marker='*', s=200, zorder=5)
                    
                    # Ayarlar
                    ax.grid(True, alpha=0.2)
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    plt.close(fig)
                    
                    # 2. METİNSEL DETAY (İşte İstediğin Kısım)
                    # Mobilde okunabilir olması için renkli kutu içinde veriyoruz
                    
                    t_bas = pts['t_start'].strftime('%d.%m.%Y')
                    t_tep = pts['t_peak'].strftime('%d.%m.%Y')
                    t_kir = pts['t_break'].strftime('%d.%m.%Y')
                    
                    st.info(f"""
                    **🎯 KRİTİK SEVİYELER VE TARİHLER**
                    
                    🟢 **DİP (Başlangıç):** 📅 {t_bas}  | 💰 **{pts['p_start']:.2f} TL**
                    
                    🔴 **TEPE (Direnç):** 📅 {t_tep}  | 💰 **{pts['p_peak']:.2f} TL**
                    
                    🚀 **KIRILIM (Sinyal):** 📅 {t_kir}  | 💰 **{pts['p_break']:.2f} TL**
                    
                    ---
                    🏁 **HEDEF:** {sinyal['Hedef']:.2f} TL (Potansiyel: %{sinyal['Potansiyel']:.1f})
                    """)
                    
                    st.divider() # Çizgi çek

    # Liste Sekmesi
    with tab_liste:
        if sonuclar:
            st.dataframe(pd.DataFrame(sonuclar))
        else:
            st.warning("Sonuç yok.")
