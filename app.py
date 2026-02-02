import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- AYARLAR ---
st.set_page_config(page_title="Debug Modu", layout="wide")
st.title("🛠️ Sistem Test ve Tanı Ekranı")

# --- KONTROL 1: Kütüphaneler ---
st.write("1. Kütüphaneler yüklendi... ✅")

# --- KONTROL 2: Veri İndirme ---
hisse = "THYAO" # Test için sabit hisse
st.write(f"2. {hisse} verisi indiriliyor... ⏳")

try:
    # TCELL.IS formatını zorla
    symbol = f"{hisse}.IS"
    df = yf.download(symbol, period="1mo", progress=False)
    
    # Sütun düzeltme (MultiIndex)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # Veri geldi mi?
    if df is not None and not df.empty:
        st.write(f"3. Veri Başarıyla İndi! ({len(df)} gün) ✅")
        st.dataframe(df.tail(3)) # Son 3 günü göster
        
        # --- KONTROL 3: Grafik Çizme ---
        st.write("4. Grafik çizimi başlatılıyor... 🎨")
        
        try:
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Çizgi
            ax.plot(df.index, df['Close'], color='blue', label='Kapanış')
            
            # NOKTA TESTİ (Son güne kırmızı nokta koy)
            son_tarih = df.index[-1]
            son_fiyat = df['Close'].iloc[-1]
            ax.scatter(son_tarih, son_fiyat, color='red', s=200, label='SON GÜN', zorder=5)
            
            ax.set_title(f"{hisse} Test Grafiği")
            ax.legend()
            ax.grid(True)
            
            # Ekrana bas
            st.pyplot(fig)
            st.success("5. Grafik ekrana basıldı! Görmen lazım. 🚀")
            
        except Exception as e:
            st.error(f"Grafik Çizim Hatası: {e}")
            
    else:
        st.error("Veri indi ama BOŞ geldi! yfinance şu an çalışmıyor olabilir.")

except Exception as e:
    st.error(f"Genel Hata: {e}")
