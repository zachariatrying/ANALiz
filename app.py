import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- 1. SAYFA YAPISI VE TASARIM ---
st.set_page_config(
    page_title="Borsa Sinyal Pro", 
    page_icon="📈", 
    layout="wide", 
    initial_sidebar_state="expanded" # Menü açık başlasın
)

# Koyu Tema CSS Makyajı
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    [data-testid="stSidebar"] { background-color: #262730; }
    [data-testid="stMetric"] { background-color: #1E1E1E; border-radius: 10px; padding: 10px; border: 1px solid #333; }
    h1, h2, h3 { color: #fafafa; }
</style>
""", unsafe_allow_html=True)

# --- 2. AYARLAR MENÜSÜ (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3310/3310624.png", width=80)
    st.title("⚙️ Kontrol Paneli")
    
    st.subheader("📡 Tarama Ayarları")
    hisse_listesi_str = st.text_area(
        "Hisse Listesi (Virgülle Ayır)", 
        "THYAO, ASELS, GARAN, AKBNK, TCELL, EREGL, SASA, HEKTS, FROTO, KCHOL",
        height=100
    )
    
    st.subheader("🎯 Filtreler")
    secilen_formasyonlar = st.multiselect(
        "Hangi Formasyonlar?",
        ["Boğa Bayrak", "Fincan Kulp", "High Tight Flag 🚀", "Düşen Kırılımı"],
        default=["Boğa Bayrak", "High Tight Flag 🚀"]
    )
    
    st.subheader("🎛️ Teknik Hassasiyet")
    bar_sayisi = st.slider("Analiz Periyodu (Mum)", 50, 365, 100)
    tolerans = st.slider("Tolerans (%)", 1, 10, 3)
    
    st.markdown("---")
    btn_baslat = st.button("🚀 TARAMAYI BAŞLAT", use_container_width=True, type="primary")

# --- 3. VERİ MOTORU ---
@st.cache_data(ttl=300)
def veri_getir(hisse, bar):
    try:
        symbol = f"{hisse}.IS" if not hisse.endswith(".IS") else hisse
        # Veriyi yfinance ile çek
        df = yf.download(symbol, period="1y", progress=False)
        
        # Sütun isimlerini ve MultiIndex'i düzelt
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        df = df.rename(columns={'Open':'Open', 'High':'High', 'Low':'Low', 'Close':'Close', 'Volume':'Volume'})
        
        # Son X barı al
        return df.tail(bar)
    except:
        return None

# --- 4. ANALİZ MOTORU (Senin Matematiğin Buraya) ---
def analiz_yap(df, secilenler):
    """
    NOT: Burası örnek analiz motorudur. Kendi özel matematik formüllerini
    buraya entegre edebilirsin. Şu an gerçek grafik noktalarını bulacak
    şekilde 'Trend Takip' mantığıyla çalışıyor.
    """
    son_fiyat = df['Close'].iloc[-1]
    max_fiyat = df['High'].max()
    min_fiyat = df['Low'].min()
    
    # Basit Mantık: Fiyat zirveye yakınsa "Boğa", dipten dönüyorsa "Fincan" diyelim.
    # (Senin karmaşık formüllerin buranın yerini alabilir)
    
    bulunan_formasyon = None
    skor = 0
    
    # Örnek: Zirveye %5 yakınsa -> High Tight Flag
    if son_fiyat >= max_fiyat * 0.95:
        bulunan_formasyon = "High Tight Flag 🚀"
        skor = 95
    # Örnek: Ortalamaların üzerindeyse -> Boğa Bayrak
    elif son_fiyat > df['Close'].mean():
        bulunan_formasyon = "Boğa Bayrak"
        skor = 85
    else:
        bulunan_formasyon = "Düşen Kırılımı"
        skor = 60
        
    # Filtreleme (Kullanıcı seçtiyse göster)
    if bulunan_formasyon in secilenler:
        # GRAFİK İÇİN KRİTİK NOKTALARI BELİRLE
        # Gerçek veriden alıyoruz:
        idx_baslangic = df['Low'].idxmin() # En dip (Başlangıç)
        idx_tepe = df['High'].idxmax()     # En tepe
        idx_son = df.index[-1]             # Bugün
        
        return {
            "Formasyon": bulunan_formasyon,
            "Skor": skor,
            "Hedef": son_fiyat * 1.25, # Örnek hedef
            "Potansiyel": 25.0,
            "Points": {
                "t_start": idx_baslangic, # Tarih objesi olarak gönderiyoruz
                "t_peak": idx_tepe,
                "t_break": idx_son,
                "p_start": df.loc[idx_baslangic]['Low'],
                "p_peak": df.loc[idx_tepe]['High'],
                "p_break": son_fiyat
            }
        }
    return None

# --- 5. ANA EKRAN VE SONUÇLAR ---
st.title("📊 Borsa Sinyal Paneli")

if btn_baslat:
    hisseler = [h.strip() for h in hisse_listesi_str.split(',')]
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.info(f"🔍 {len(hisseler)} Hisse Taranıyor...")
        
    sonuclar = []
    
    # Progress Bar
    bar = st.progress(0)
    
    # Sekmeler
    tab_grafik, tab_tablo = st.tabs(["🖼️ Grafik Galerisi", "📋 Detaylı Liste"])
    
    for i, hisse in enumerate(hisseler):
        bar.progress((i+1) / len(hisseler))
        
        df = veri_getir(hisse, bar_sayisi)
        
        if df is not None and len(df) > 20:
            sinyal = analiz_yap(df, secilen_formasyonlar)
            
            if sinyal:
                sinyal['Hisse'] = hisse
                sinyal['Fiyat'] = df['Close'].iloc[-1]
                sonuclar.append(sinyal)
                
                # --- GRAFİK ÇİZİMİ (TAB 1) ---
                with tab_grafik:
                    # 2 Sütunlu düzen
                    c1, c2 = st.columns([3, 1])
                    
                    with c1: # Grafik Alanı
                        fig, ax = plt.subplots(figsize=(10, 5))
                        
                        # Fiyatı Çiz
                        ax.plot(df.index, df['Close'], color='#2980b9', linewidth=2, label='Fiyat')
                        
                        # Noktaları İşaretle
                        pts = sinyal['Points']
                        
                        # 1. Dip/Başlangıç (Yeşil)
                        ax.scatter(pts['t_start'], pts['p_start'], color='green', s=100, zorder=5, label='Dip')
                        # 2. Tepe (Kırmızı)
                        ax.scatter(pts['t_peak'], pts['p_peak'], color='red', s=100, zorder=5, label='Tepe')
                        # 3. Güncel/Kırılım (Mavi Yıldız)
                        ax.scatter(pts['t_break'], pts['p_break'], color='blue', marker='*', s=200, zorder=5, label='Sinyal')
                        
                        # Süsleme
                        ax.set_title(f"{hisse} - {sinyal['Formasyon']} (Skor: {sinyal['Skor']})")
                        ax.grid(True, alpha=0.3)
                        ax.legend()
                        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
                        plt.xticks(rotation=45)
                        
                        st.pyplot(fig)
                        plt.close(fig)
                    
                    with c2: # Yan Bilgi Kutusu
                        st.success(f"**{hisse}**")
                        st.markdown(f"💰 **Fiyat:** {sinyal['Fiyat']:.2f} TL")
                        st.markdown(f"🎯 **Hedef:** {sinyal['Hedef']:.2f} TL")
                        st.markdown(f"🚀 **Potansiyel:** %{sinyal['Potansiyel']:.1f}")
                        st.caption(f"Tarih: {pts['t_break'].strftime('%d.%m.%Y')}")
                        st.divider()

    bar.empty()
    
    # --- TABLO ÇIKTISI (TAB 2) ---
    with tab_tablo:
        if sonuclar:
            df_sonuc = pd.DataFrame(sonuclar)
            # Okuması kolay sütunlar
            gosterilecek = df_sonuc[['Hisse', 'Fiyat', 'Hedef', 'Potansiyel', 'Formasyon', 'Skor']]
            st.dataframe(
                gosterilecek,
                column_config={
                    "Potansiyel": st.column_config.ProgressColumn("Potansiyel %", format="%.1f%%", min_value=0, max_value=100),
                    "Fiyat": st.column_config.NumberColumn("Fiyat", format="%.2f TL")
                },
                use_container_width=True
            )
        else:
            st.warning("Aradığınız kriterlere uygun hisse bulunamadı. Ayarları gevşetin.")
