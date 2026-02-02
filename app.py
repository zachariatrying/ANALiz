import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Borsa Sinyal v4", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

# --- CSS VE MOBİL AYARLARI ---
st.markdown("""
<style>
    [data-testid="stMetric"] { background-color: #1E1E1E; border-radius: 10px; padding: 10px; border: 1px solid #333; }
    .stDataFrame { font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# --- FONKSİYONLAR ---
@st.cache_data(ttl=300)
def veri_getir(hisse, bar_sayisi=100):
    try:
        hisse_kodu = f"{hisse}.IS" if not hisse.endswith(".IS") else hisse
        df = yf.download(hisse_kodu, period="1y", progress=False)
        if df is None or df.empty: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        df.rename(columns={'Open':'Open', 'High':'High', 'Low':'Low', 'Close':'Close', 'Volume':'Volume'}, inplace=True)
        return df
    except: return None

# --- BASIT ANALİZ (Sadece Örnek - Senin Kodların Buraya Gelecek) ---
def analiz_yap(df):
    # BURAYA SENİN ORİJİNAL ANALİZ KODLARINI YAPIŞTIRMAN GEREKEBİLİR
    # Şimdilik örnek sinyal üretiyorum ki sistem çalışsın:
    import random
    if random.random() > 0.7:
        son_fiyat = df['Close'].iloc[-1]
        hedef = son_fiyat * 1.5
        potansiyel = ((hedef - son_fiyat) / son_fiyat) * 100
        
        # Kritik noktaların indekslerini uyduruyorum (Senin kodunda bunlar hesaplanıyor)
        start_idx = len(df) - 50
        end_idx = len(df) - 20
        break_idx = len(df) - 1
        
        return {
            "Formasyon": "Boğa Bayrak", 
            "Skor": 105, 
            "Hedef": hedef,
            "Potansiyel (%)": potansiyel,
            "Points": {"p_start_idx": start_idx, "p_end_idx": end_idx, "f_end_idx": break_idx}
        }
    return None

# --- ARAYÜZ ---
st.title("📱 Zacharia Borsa Takip")

# Sidebar
with st.sidebar:
    hisse_listesi = st.text_area("Hisseler", "THYAO,GARAN,ASELS,TCELL,ASTOR,EUPWR").split(',')
    grafik_ciz = st.toggle("Grafik ve Tarihleri Göster", value=True)
    baslat = st.button("TARAMAYI BAŞLAT", use_container_width=True)

if baslat:
    tab_liste, tab_galeri = st.tabs(["📋 Liste", "🖼️ Galeri"])
    bulunanlar = []
    
    status = st.empty()
    bar = st.progress(0)
    
    for i, hisse in enumerate(hisse_listesi):
        hisse = hisse.strip()
        status.text(f"Analiz: {hisse}...")
        bar.progress((i+1)/len(hisse_listesi))
        
        df = veri_getir(hisse)
        if df is not None:
            sonuc = analiz_yap(df)
            if sonuc:
                sonuc['Hisse'] = hisse
                sonuc['Fiyat'] = df['Close'].iloc[-1]
                bulunanlar.append(sonuc)
                
                # --- GRAFİK ÇİZİMİ (Matplotlib) ---
                if grafik_ciz:
                    with tab_galeri:
                        fig, ax = plt.subplots(figsize=(10, 5))
                        ax.plot(df.index, df['Close'], label='Fiyat', color='#1f77b4')
                        
                        # Noktalar
                        pts = sonuc['Points']
                        t_bas = df.index[pts['p_start_idx']]
                        t_tepe = df.index[pts['p_end_idx']]
                        t_kir = df.index[pts['f_end_idx']]
                        
                        ax.scatter(t_bas, df['Close'].iloc[pts['p_start_idx']], c='green', s=100, zorder=5)
                        ax.scatter(t_tepe, df['Close'].iloc[pts['p_end_idx']], c='red', s=100, zorder=5)
                        ax.scatter(t_kir, df['Close'].iloc[pts['f_end_idx']], c='blue', marker='*', s=150, zorder=5)
                        
                        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
                        ax.grid(True, alpha=0.3)
                        ax.set_title(f"{hisse} - {sonuc['Formasyon']}")
                        
                        st.pyplot(fig)
                        plt.close(fig)
                        
                        # Tarih Bilgisi
                        st.info(f"📅 Başlangıç: {t_bas.strftime('%d.%m')} | Zirve: {t_tepe.strftime('%d.%m')} | Kırılım: {t_kir.strftime('%d.%m')}")

    status.text("✅ Bitti!")
    bar.empty()
    
    with tab_liste:
        if bulunanlar:
            st.dataframe(pd.DataFrame(bulunanlar))
        else:
            st.warning("Formasyon yok.")