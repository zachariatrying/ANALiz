import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- 1. MOBİL AYARLAR ---
st.set_page_config(
    page_title="Mobil Scanner", 
    page_icon="📡", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Mobil için özel CSS (Büyük butonlar, Okunabilir Metinler)
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    /* Metrik kutularını mobilde yan yana sığacak şekilde küçült */
    [data-testid="stMetric"] { background-color: #212529; padding: 10px; border-radius: 10px; }
    div[data-testid="stMetricLabel"] { font-size: 0.8rem; }
    div[data-testid="stMetricValue"] { font-size: 1.1rem; color: #4CAF50; }
    
    /* Butonları büyüt */
    .stButton>button { width: 100%; height: 3.5rem; font-size: 1.2rem; border-radius: 12px; }
    
    /* Expander başlıklarını belirginleştir */
    .streamlit-expanderHeader { font-weight: bold; font-size: 1.1rem; color: #fafafa; background-color: #262730; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ MOTORU ---
@st.cache_data(ttl=300)
def veri_getir(hisse, bar_sayisi=100):
    try:
        symbol = f"{hisse}.IS" if not hisse.endswith(".IS") else hisse
        df = yf.download(symbol, period="6mo", progress=False) # Mobilde hız için 6 ay yeter
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        df = df.rename(columns={'Open':'Open', 'High':'High', 'Low':'Low', 'Close':'Close'})
        
        # Basit Hareketli Ortalamalar (Analiz için)
        df['SMA50'] = df['Close'].rolling(50).mean()
        df['SMA200'] = df['Close'].rolling(200).mean()
        
        return df.tail(bar_sayisi)
    except:
        return None

# --- 3. SCANNER MANTIĞI (Filtre) ---
def scanner_analiz(df):
    """
    PC Scanner mantığının aynısı. Sadece sinyal varsa döndürür.
    """
    if len(df) < 50: return None
    
    son = df.iloc[-1]
    prev = df.iloc[-2]
    
    sinyal = None
    skor = 0
    
    # Kriter 1: Golden Cross (Altın Kesişim)
    if son['SMA50'] > son['SMA200'] and prev['SMA50'] <= prev['SMA200']:
        sinyal = "Golden Cross 🟡"
        skor = 95
        
    # Kriter 2: Fiyat Ortalamaların Üstünde (Güçlü Trend)
    elif son['Close'] > son['SMA50'] > son['SMA200']:
        # Son 3 günde yükseliş varsa
        if df['Close'].iloc[-1] > df['Close'].iloc[-3]:
            sinyal = "Trend Takip (Boğa) 🐂"
            skor = 80

    # Kriter 3: Dipten Dönüş (Basit)
    elif son['Close'] > df['Close'].rolling(20).mean().iloc[-1] and prev['Close'] < df['Close'].rolling(20).mean().iloc[-2]:
         sinyal = "20 Günlük Kırılım 🚀"
         skor = 85

    if sinyal:
        # Noktaları Belirle (Grafik İçin)
        idx_dip = df['Low'].tail(30).idxmin()
        idx_tepe = df['High'].tail(30).idxmax()
        
        return {
            "Formasyon": sinyal,
            "Skor": skor,
            "Fiyat": son['Close'],
            "Hedef": son['Close'] * 1.15,
            "Potansiyel": 15.0,
            "Points": {
                "t_start": idx_dip,
                "t_peak": idx_tepe,
                "t_break": df.index[-1],
                "p_start": df.loc[idx_dip]['Low'],
                "p_peak": df.loc[idx_tepe]['High'],
                "p_break": son['Close']
            }
        }
    return None

# --- 4. ARAYÜZ ---
st.title("📡 Mobil Scanner")

# Üst Panel: Liste Seçimi
col_secim, col_btn = st.columns([2, 1])

with col_secim:
    liste_secimi = st.selectbox(
        "Taranacak Liste", 
        ["Favorilerim", "BIST 30", "BIST Banka", "Teknoloji"]
    )

if liste_secimi == "Favorilerim":
    hisseler_str = "THYAO, ASELS, GARAN, AKBNK, TCELL, EREGL, SASA, HEKTS"
elif liste_secimi == "BIST 30":
    hisseler_str = "AKBNK,ARCLK,ASELS,ASTOR,BIMAS,BRSAN,EKGYO,ENKAI,EREGL,FROTO,GARAN,GUBRF,HEKTS,ISCTR,KCHOL,KONTR,KOZAL,KRDMD,ODAS,OYAKC,PETKM,PGSUS,SAHOL,SASA,SISE,TCELL,THYAO,TOASO,TUPRS,YKBNK"
elif liste_secimi == "BIST Banka":
    hisseler_str = "AKBNK, GARAN, ISCTR, YKBNK, VAKBN, HALKB, SKBNK, TSKB"
else:
    hisseler_str = "ASELS, KFEIN, LOGO, MIATK, KONTR, SDTTR, PATEK"

hisseler = [h.strip() for h in hisseler_str.split(',')]

with col_btn:
    st.write("") # Boşluk
    btn_baslat = st.button("🔍 TARA", type="primary")

# --- 5. SONUÇ EKRANI ---
if btn_baslat:
    st.info(f"⚡ {len(hisseler)} Hisse taranıyor...")
    bar = st.progress(0)
    
    bulunanlar = []
    
    # Tarama Döngüsü
    for i, hisse in enumerate(hisseler):
        bar.progress((i+1)/len(hisseler))
        df = veri_getir(hisse)
        
        if df is not None:
            sonuc = scanner_analiz(df)
            if sonuc:
                sonuc['Hisse'] = hisse
                bulunanlar.append(sonuc)
    
    bar.empty()
    
    if not bulunanlar:
        st.warning("Kriterlere uygun sinyal bulunamadı.")
    else:
        st.success(f"🎉 {len(bulunanlar)} Fırsat Bulundu!")
        
        # 1. ÖZET TABLO (Hemen Sonucu Gör)
        df_ozet = pd.DataFrame(bulunanlar)[['Hisse', 'Fiyat', 'Formasyon', 'Potansiyel']]
        st.dataframe(df_ozet, use_container_width=True)
        
        st.divider()
        st.subheader("📊 Detaylı Analizler")
        
        # 2. DETAYLI KARTLAR (Mobilde Aşağı Kaydırarak Bak)
        for veri in bulunanlar:
            # Her hisseyi açılır kapanır kutuya koy (Yer kaplamasın)
            with st.expander(f"📌 {veri['Hisse']} - {veri['Formasyon']} (Görmek için tıkla)", expanded=True):
                
                # Grafik Alanı
                df_grafik = veri_getir(veri['Hisse']) # Grafiği taze veriyle çiz
                pts = veri['Points']
                
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(df_grafik.index, df_grafik['Close'], color='#2196F3', linewidth=2, label='Fiyat')
                
                # Ortalamalar
                if 'SMA50' in df_grafik.columns:
                    ax.plot(df_grafik.index, df_grafik['SMA50'], color='orange', linestyle='--', alpha=0.7, label='SMA 50')
                
                # Noktalar
                ax.scatter(pts['t_start'], pts['p_start'], color='green', s=100, zorder=5)
                ax.scatter(pts['t_peak'], pts['p_peak'], color='red', s=100, zorder=5)
                ax.scatter(pts['t_break'], pts['p_break'], color='gold', marker='*', s=200, zorder=5)
                
                ax.grid(True, alpha=0.2)
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
                plt.xticks(rotation=45)
                st.pyplot(fig)
                plt.close(fig)
                
                # Bilgi Kutusu (Tarihli & Fiyatlı)
                t_bas = pts['t_start'].strftime('%d.%m')
                t_kir = pts['t_break'].strftime('%d.%m')
                
                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"**AL Sinyali**\n\nFiyat: {veri['Fiyat']:.2f} TL\nHedef: {veri['Hedef']:.2f} TL")
                with col2:
                    st.info(f"**Tarihler**\n\nDip: {t_bas}\nSinyal: {t_kir}")
